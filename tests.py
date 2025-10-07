
'''
اختبارات شاملة لمنصة أيديا المتكاملة - Sprint 8
تتضمن اختبارات الوحدات والتكامل للوظائف الحيوية
'''

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from datetime import datetime, timedelta
import json
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

# استيراد النماذج
from idea_platform.accounts.models import CustomUser, Role, UserProfile
from idea_platform.crm.models import Client as ClientModel
from idea_platform.projects.models import Project
from idea_platform.billing.models import Invoice, InvoiceItem
from idea_platform.reports.models import ReportTemplate, Report

User = get_user_model()


class UserModelTests(TestCase):
    '''اختبارات نموذج المستخدم'''
    def setUp(self):
        '''إعداد البيانات للاختبارات'''
        self.role = Role.objects.create(
            name='admin',
            display_name='مدير عام',
            description='مدير عام للنظام'
        )
    
    def test_create_user(self):
        '''اختبار إنشاء مستخدم جديد'''
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            arabic_first_name='أحمد',
            arabic_last_name='محمد',
            role=self.role
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.arabic_first_name, 'أحمد')
        self.assertEqual(user.role, self.role)
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_full_name_arabic(self):
        '''اختبار خاصية الاسم الكامل بالعربية'''
        user = CustomUser.objects.create_user(
            username='testuser',
            arabic_first_name='أحمد',
            arabic_last_name='محمد'
        )
        
        self.assertEqual(user.full_name_arabic, 'أحمد محمد')
    
    def test_user_profile_creation(self):
        '''اختبار إنشاء ملف المستخدم الشخصي'''
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        
        profile = UserProfile.objects.create(
            user=user,
            bio='نبذة تجريبية',
            language_preference='ar'
        )
        
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.language_preference, 'ar')


class BillingModelTests(TestCase):
    '''اختبارات نماذج الفواتير'''
    def setUp(self):
        '''إعداد البيانات للاختبارات'''
        self.user = CustomUser.objects.create_user(
            username='billingtestuser',
            email='billing@example.com',
            password='billingpass123'
        )
        self.client_model = ClientModel.objects.create(
            name='شركة الاختبار',
            email='test@company.com',
            phone_number='0501234567',
            address='الرياض، السعودية',
            city='الرياض',
            client_type='company'
        )
        
        self.project = Project.objects.create(
            name='مشروع تجريبي',
            description='وصف المشروع التجريبي',
            client=self.client_model,
            project_type='consulting',
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=30),
            budget=Decimal('10000.00')
        )

    
    def test_create_client(self):
        '''اختبار إنشاء عميل جديد'''
        self.assertEqual(self.client_model.name, 'شركة الاختبار')
        self.assertEqual(self.client_model.client_type, 'company')
        self.assertEqual(self.client_model.total_projects, 1)
    
    def test_create_project(self):
        '''اختبار إنشاء مشروع جديد'''
        self.assertEqual(self.project.name, 'مشروع تجريبي')
        self.assertEqual(self.project.client, self.client_model)
        self.assertEqual(self.project.budget, Decimal('10000.00'))
        self.assertFalse(self.project.is_overdue)

    def test_create_invoice(self):
        '''اختبار إنشاء فاتورة جديدة'''
        invoice = Invoice.objects.create(
            invoice_number='INV-TEST-001',
            client=self.client_model,
            project=self.project,
            issue_date=datetime.now().date(),
            due_date=datetime.now().date() + timedelta(days=30),
            created_by=self.user,
            tax_rate=Decimal('15.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice,
            description='خدمة استشارية',
            quantity=Decimal('10.00'),
            unit_price=Decimal('100.00')
        )
        invoice.refresh_from_db()
        self.assertEqual(invoice.client, self.client_model)
        self.assertEqual(invoice.subtotal, Decimal('1000.00'))
        self.assertEqual(invoice.tax_amount, Decimal('150.00'))
        self.assertEqual(invoice.total_amount, Decimal('1150.00'))

    def test_invoice_items(self):
        '''اختبار عناصر الفاتورة'''
        invoice = Invoice.objects.create(
            invoice_number='INV-TEST-002',
            client=self.client_model,
            issue_date=datetime.now().date(),
            due_date=datetime.now().date() + timedelta(days=30),
            created_by=self.user
        )
        
        item1 = InvoiceItem.objects.create(
            invoice=invoice,
            description='خدمة استشارية',
            quantity=Decimal('10.00'),
            unit_price=Decimal('100.00')
        )
        
        item2 = InvoiceItem.objects.create(
            invoice=invoice,
            description='تصميم شعار',
            quantity=Decimal('1.00'),
            unit_price=Decimal('500.00')
        )
        
        self.assertEqual(item1.total_price, Decimal('1000.00'))
        self.assertEqual(item2.total_price, Decimal('500.00'))
        
        # تحديث الفاتورة
        invoice.refresh_from_db()
        self.assertEqual(invoice.subtotal, Decimal('1500.00'))


class BillingAPITests(APITestCase):
    '''اختبارات API للفواتير والتقارير'''
    def setUp(self):
        '''إعداد البيانات للاختبارات'''
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.user)
        # Grant permission to add client for the test user
        client_content_type = ContentType.objects.get_for_model(ClientModel)
        add_client_permission = Permission.objects.get(content_type=client_content_type, codename='add_client')
        self.user.user_permissions.add(add_client_permission)
        self.user.save()
        
        self.client_model = ClientModel.objects.create(
            name='شركة الاختبار API',
            email='api@company.com',
            phone_number='0501234567',
            address='الرياض، السعودية',
            city='الرياض'
        )
    
    def test_client_list_api(self):
        '''اختبار API قائمة العملاء'''
        url = '/api/crm/clients/'
        response = self.client_api.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'شركة الاختبار API')
    
    def test_create_client_api(self):
        '''اختبار API إنشاء عميل جديد'''
        url = '/api/crm/clients/'
        data = {
            'name': 'عميل جديد',
            'email': 'new@client.com',
            'phone_number': '0509876543',
            'address': 'جدة، السعودية',
            'city': 'جدة',
            'client_type': 'company'
        }
        
        response = self.client_api.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClientModel.objects.count(), 2)
    
    def test_create_invoice_api(self):
        '''اختبار API إنشاء فاتورة جديدة'''
        url = '/api/billing/invoices/'
        data = {
            'invoice_number': 'INV-API-001',
            'title': 'فاتورة اختبار API',
            'client': str(self.client_model.id),
            'issue_date': datetime.now().date().isoformat(),
            'due_date': (datetime.now().date() + timedelta(days=30)).isoformat(),
            'payment_terms': 'net_30',
            'created_by': self.user.id,
            'items': [
                {
                    'description': 'خدمة استشارية',
                    'quantity': '10.00',
                    'unit_price': '100.00'
                }
            ]
        }
        
        response = self.client_api.post(url, data, format='json')
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Data: {response.data}")
        print(f"Response JSON: {response.json()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("invoice_number" in response.data)





    def test_analytics_dashboard_api(self):
        """اختبار API لوحة التحكم التحليلية"""
        url = '/api/reports/analytics_dashboard/'
        response = self.client_api.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('overview' in response.data)
        self.assertTrue('monthly_performance' in response.data)


class ReportTemplateTests(TestCase):
    '''اختبارات قوالب التقارير'''
    def setUp(self):
        '''إعداد البيانات للاختبارات'''
        self.user = CustomUser.objects.create_user(
            username='reportuser',
            email='report@example.com',
            password='reportpass123'
        )
        self.template = ReportTemplate.objects.create(
            name='قالب تجريبي',
            description='قالب تجريبي للاختبار',
            report_type='project_summary',
            html_template='<html><body>{{ data.title }}</body></html>',
            data_sources=['projects'],
            template_config={'filters': {'date_range': True}},
            created_by=self.user
        )



    def test_create_report_template(self):
        '''اختبار إنشاء قالب تقرير'''
        self.assertEqual(self.template.name, 'قالب تجريبي')
        self.assertEqual(self.template.report_type, 'project_summary')
        self.assertTrue(self.template.is_active)

    def test_generate_report(self):
        '''اختبار إنشاء تقرير من القالب'''
        report = Report.objects.create(
            title='تقرير تجريبي',
            template=self.template,
            start_date=datetime.now().date() - timedelta(days=30),
            end_date=datetime.now().date(),
            generated_by=self.user,
            status='completed',
            raw_data={'title': 'تقرير تجريبي'}
        )
        
        self.assertEqual(report.template, self.template)
        self.assertEqual(report.status, 'completed')

class IntegrationTests(TestCase):
    '''اختبارات التكامل'''
    def setUp(self):
        '''إعداد البيانات للاختبارات'''
        self.user = CustomUser.objects.create_user(
            username='integrationuser',
            email='integration@test.com',
            password='testpass123'
        )
        
        self.client = Client()
        self.client.login(username='integrationuser', password='testpass123')
        
        self.client_model = ClientModel.objects.create(
            name='عميل التكامل',
            email='integration@client.com',
            phone_number='0501234567',
            address='الرياض، السعودية',
            city='الرياض'
        )
    
    def test_full_invoice_workflow(self):
        '''اختبار سير العمل الكامل للفاتورة'''
        # إنشاء مشروع
        project = Project.objects.create(
            name='مشروع التكامل',
            description='مشروع لاختبار التكامل',
            client=self.client_model,
            project_type='consulting',
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=30),
            budget=Decimal('5000.00')
        )
        
        # إنشاء فاتورة
        invoice = Invoice.objects.create(
            invoice_number='INT-001',
            client=self.client_model,
            project=project,
            issue_date=datetime.now().date(),
            due_date=datetime.now().date() + timedelta(days=30),
            status='draft',
            created_by=self.user,
            tax_rate=Decimal('15.00')
        )
        
        # إضافة عناصر للفاتورة
        InvoiceItem.objects.create(
            invoice=invoice,
            description='استشارة تقنية',
            quantity=Decimal('20.00'),
            unit_price=Decimal('150.00')
        )
        
        # التحقق من حساب المبالغ
        invoice.refresh_from_db()
        self.assertEqual(invoice.subtotal, Decimal('3000.00'))
        self.assertEqual(invoice.tax_amount, Decimal('450.00'))
        self.assertEqual(invoice.total_amount, Decimal('3450.00'))
        
        # تحديث حالة الفاتورة
        invoice.status = 'sent'
        invoice.save()
        
        self.assertEqual(invoice.status, 'sent')
    
    def test_client_analytics_integration(self):
        '''اختبار تكامل تحليلات العميل'''
        # إنشاء مشاريع متعددة
        for i in range(3):
            Project.objects.create(
                name=f'مشروع {i+1}',
                description=f'وصف المشروع {i+1}',
                client=self.client_model,
                project_type='consulting',
                start_date=datetime.now().date(),
                end_date=datetime.now().date() + timedelta(days=30),
                budget=Decimal('1000.00'),
                status='completed' if i < 2 else 'in_progress'
            )
        
        # إنشاء فواتير
        for i in range(2):
            invoice = Invoice.objects.create(
                invoice_number=f'ANA-{i+1:03d}',
                client=self.client_model,
                issue_date=datetime.now().date(),
                due_date=datetime.now().date() + timedelta(days=30),
                created_by=self.user,
                tax_rate=Decimal('15.00'),
                status='paid' if i == 0 else 'sent'
            )
            InvoiceItem.objects.create(
                invoice=invoice,
                description='بند فاتورة',
                quantity=Decimal('1.00'),
                unit_price=Decimal('1000.00')
            )
        
        # التحقق من الإحصائيات
        self.assertEqual(self.client_model.total_projects, 3)
        total_invoiced = self.client_model.total_invoiced_amount
        self.assertEqual(total_invoiced, Decimal('2300.00'))  # 2 * (1000 + 150 tax)


class PerformanceTests(TestCase):
    '''اختبارات الأداء'''
    def setUp(self):
        '''إعداد بيانات كبيرة للاختبار'''
        self.clients = []
        for i in range(10):
            client = ClientModel.objects.create(
                name=f'عميل {i+1}',
                email=f'client{i+1}@test.com',
                phone_number=f'05012345{i:02d}',
                address='الرياض، السعودية',
                city='الرياض'
            )
            self.clients.append(client)
 
    def test_bulk_operations_performance(self):
        '''اختبار أداء العمليات المجمعة'''
        import time
        
        # قياس وقت إنشاء مشاريع متعددة
        start_time = time.time()
        
        projects = []
        for i, client in enumerate(self.clients):
            for j in range(5):
                project = Project(
                    name=f'مشروع {i+1}-{j+1}',
                    description=f'وصف المشروع {i+1}-{j+1}',
                    client=client,
                    project_type='consulting',
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=30),
                    budget=Decimal('1000.00')
                )
                projects.append(project)
        
        Project.objects.bulk_create(projects)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # يجب أن يكون الوقت أقل من ثانية واحدة لإنشاء 50 مشروع
        self.assertLess(execution_time, 1.0)
        self.assertEqual(Project.objects.count(), 50)


class SecurityTests(TestCase):
    '''اختبارات الأمان'''
    def setUp(self):
        '''إعداد المستخدمين والأدوار'''
        self.admin_role = Role.objects.create(
            name='admin',
            display_name='مدير عام'
        )
        # Add a dummy permission for testing role-based access
        view_client_permission = Permission.objects.create(
            codename='view_all_clients',
            name='Can view all clients',
            content_type=ContentType.objects.get_for_model(ClientModel)
        )
        self.admin_role.permissions.add(view_client_permission)

        
        self.client_role = Role.objects.create(
            name='client',
            display_name='عميل'
        )
        
        self.admin_user = CustomUser.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            role=self.admin_role
        )
        
        self.client_user = CustomUser.objects.create_user(
            username='client',
            email='client@test.com',
            password='clientpass123',
            role=self.client_role
        )
        
        self.client_model = ClientModel.objects.create(
            name='عميل الأمان',
            email='security@client.com',
            phone_number='0501234567'
        )

    def test_user_authentication_required(self):
        """اختبار وجوب المصادقة للوصول للAPI"""
        client = APIClient()
        url = '/api/crm/clients/'
        response = client.get(url)
        self.assertIn(response.status_code, [401, 403])

    def test_role_based_access(self):
        """اختبار التحكم في الوصول حسب الأدوار"""
        # يجب أن يكون لدى المستخدم المسؤول إذن لعرض جميع العملاء
        self.assertTrue(self.admin_user.has_role_permission('view_all_clients'))
        
        # لا ينبغي أن يكون لدى المستخدم العميل إذن لعرض جميع العملاء
        self.assertFalse(self.client_user.has_role_permission('view_all_clients'))

