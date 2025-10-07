
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from idea_platform.crm.models import Client
from idea_platform.projects.models import Project
from .models import Invoice, InvoiceItem, Payment, InvoiceStatus

User = get_user_model()

class BillingModelsTestCase(TestCase):
    """مجموعة اختبارات لنماذج الفواتير"""

    def setUp(self):
        """إعداد بيانات الاختبار"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client.objects.create(name='Test Client', email='client@example.com', created_by=self.user)
        self.project = Project.objects.create(name='Test Project', client=self.client, created_by=self.user)

    def test_create_invoice(self):
        """اختبار إنشاء فاتورة جديدة"""
        invoice = Invoice.objects.create(
            invoice_number='INV-001',
            client=self.client,
            project=self.project,
            created_by=self.user,
            title='Test Invoice',
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            tax_rate=Decimal('15.00')
        )
        self.assertEqual(invoice.invoice_number, 'INV-001')
        self.assertEqual(invoice.status, InvoiceStatus.DRAFT)
        self.assertEqual(invoice.total_amount, Decimal('0.00'))

    def test_create_invoice_item(self):
        """اختبار إنشاء بند فاتورة"""
        invoice = Invoice.objects.create(
            invoice_number='INV-002',
            client=self.client,
            created_by=self.user,
            title='Invoice with Items',
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            tax_rate=Decimal('10.00')
        )
        item1 = InvoiceItem.objects.create(
            invoice=invoice,
            description='Service 1',
            quantity=Decimal('2.00'),
            unit_price=Decimal('100.00')
        )
        item2 = InvoiceItem.objects.create(
            invoice=invoice,
            description='Service 2',
            quantity=Decimal('1.00'),
            unit_price=Decimal('50.00')
        )

        # Refresh invoice from DB to get updated totals
        invoice.refresh_from_db()

        self.assertEqual(item1.total_price, Decimal('200.00'))
        self.assertEqual(item2.total_price, Decimal('50.00'))
        self.assertEqual(invoice.subtotal, Decimal('250.00'))
        self.assertEqual(invoice.tax_amount, Decimal('25.00'))
        self.assertEqual(invoice.total_amount, Decimal('275.00'))

    def test_create_payment(self):
        """اختبار إنشاء دفعة"""
        invoice = Invoice.objects.create(
            invoice_number='INV-003',
            client=self.client,
            created_by=self.user,
            title='Invoice for Payment',
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            tax_rate=Decimal('10.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice,
            description='Product A',
            quantity=Decimal('1.00'),
            unit_price=Decimal('1000.00')
        )
        invoice.refresh_from_db()

        self.assertEqual(invoice.total_amount, Decimal('1100.00'))
        self.assertEqual(invoice.status, InvoiceStatus.DRAFT)

        # Make a partial payment
        payment1 = Payment.objects.create(
            invoice=invoice,
            amount=Decimal('500.00'),
            created_by=self.user
        )
        invoice.refresh_from_db()

        self.assertEqual(invoice.paid_amount, Decimal('500.00'))
        self.assertEqual(invoice.remaining_amount, Decimal('600.00'))
        self.assertEqual(invoice.status, InvoiceStatus.SENT) # Status should change after payment

        # Make the final payment
        payment2 = Payment.objects.create(
            invoice=invoice,
            amount=Decimal('600.00'),
            created_by=self.user
        )
        invoice.refresh_from_db()

        self.assertEqual(invoice.paid_amount, Decimal('1100.00'))
        self.assertEqual(invoice.remaining_amount, Decimal('0.00'))
        self.assertTrue(invoice.is_fully_paid)
        self.assertEqual(invoice.status, InvoiceStatus.PAID)

    def test_invoice_overdue_status(self):
        """اختبار حالة الفاتورة المتأخرة"""
        invoice = Invoice.objects.create(
            invoice_number='INV-004',
            client=self.client,
            created_by=self.user,
            title='Overdue Invoice',
            issue_date=date.today() - timedelta(days=40),
            due_date=date.today() - timedelta(days=10),
            status=InvoiceStatus.SENT # Manually set to SENT to test overdue logic
        )
        self.assertTrue(invoice.is_overdue)


class BillingViewsTestCase(TestCase):
    """مجموعة اختبارات لواجهات برمجة تطبيقات الفواتير"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client_obj = Client.objects.create(name='Test Client', email='client@example.com', created_by=self.user)
        self.invoice = Invoice.objects.create(
            invoice_number='INV-API-001',
            client=self.client_obj,
            created_by=self.user,
            title='API Test Invoice',
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            tax_rate=Decimal('10.00')
        )
        self.invoice_item = InvoiceItem.objects.create(
            invoice=self.invoice,
            description='API Service',
            quantity=Decimal('1'),
            unit_price=Decimal('100')
        )
        self.invoice.refresh_from_db()
        self.client.force_login(self.user)

    def test_invoice_list_create_api_view(self):
        response = self.client.get('/api/billing/invoices/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        new_invoice_data = {
            'invoice_number': 'INV-API-002',
            'client': self.client_obj.id,
            'title': 'New API Invoice',
            'issue_date': date.today().isoformat(),
            'due_date': (date.today() + timedelta(days=60)).isoformat(),
            'tax_rate': '15.00',
            'items': [
                {'description': 'Item 1', 'quantity': '2', 'unit_price': '50.00'}, 
                {'description': 'Item 2', 'quantity': '1', 'unit_price': '75.00'}
            ]
        }
        response = self.client.post('/api/billing/invoices/', new_invoice_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Invoice.objects.count(), 2)
        new_invoice = Invoice.objects.get(invoice_number='INV-API-002')
        self.assertEqual(new_invoice.total_amount, Decimal('195.50')) # (2*50 + 1*75) * 1.15

    def test_generate_invoice_pdf_view(self):
        response = self.client.get(f'/api/billing/invoices/{self.invoice.id}/generate_pdf/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(f'attachment; filename="Invoice_{self.invoice.invoice_number}.pdf"' in response['Content-Disposition'])


class BillingIntegrationTestCase(TestCase):
    """مجموعة اختبارات التكامل لنظام الفواتير"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client_obj = Client.objects.create(name='Integration Client', email='integration@example.com', created_by=self.user)
        self.invoice = Invoice.objects.create(
            invoice_number='INV-INT-001',
            client=self.client_obj,
            created_by=self.user,
            title='Integration Invoice',
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            tax_rate=Decimal('5.00')
        )
        self.client.force_login(self.user)

    def test_invoice_item_creation_updates_invoice_totals(self):
        self.assertEqual(self.invoice.subtotal, Decimal('0.00'))
        self.assertEqual(self.invoice.total_amount, Decimal('0.00'))

        InvoiceItem.objects.create(
            invoice=self.invoice,
            description='Item A',
            quantity=Decimal('3'),
            unit_price=Decimal('10.00')
        )
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.subtotal, Decimal('30.00'))
        self.assertEqual(self.invoice.tax_amount, Decimal('1.50')) # 5% of 30
        self.assertEqual(self.invoice.total_amount, Decimal('31.50'))

        InvoiceItem.objects.create(
            invoice=self.invoice,
            description='Item B',
            quantity=Decimal('2'),
            unit_price=Decimal('20.00')
        )
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.subtotal, Decimal('70.00')) # 30 + (2*20)
        self.assertEqual(self.invoice.tax_amount, Decimal('3.50')) # 5% of 70
        self.assertEqual(self.invoice.total_amount, Decimal('73.50'))

    def test_payment_updates_invoice_status_and_paid_amount(self):
        InvoiceItem.objects.create(
            invoice=self.invoice,
            description='Full Payment Item',
            quantity=Decimal('1'),
            unit_price=Decimal('100.00')
        )
        self.invoice.refresh_from_db()
        self.invoice.status = InvoiceStatus.SENT # Set to sent for payment logic
        self.invoice.save()
        self.assertEqual(self.invoice.total_amount, Decimal('105.00')) # 100 * 1.05
        self.assertEqual(self.invoice.paid_amount, Decimal('0.00'))
        self.assertEqual(self.invoice.status, InvoiceStatus.SENT)

        Payment.objects.create(
            invoice=self.invoice,
            amount=Decimal('50.00'),
            created_by=self.user
        )
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.paid_amount, Decimal('50.00'))
        self.assertEqual(self.invoice.status, InvoiceStatus.SENT) # Still sent, not fully paid

        Payment.objects.create(
            invoice=self.invoice,
            amount=Decimal('55.00'),
            created_by=self.user
        )
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.paid_amount, Decimal('105.00'))
        self.assertEqual(self.invoice.status, InvoiceStatus.PAID)
        self.assertTrue(self.invoice.is_fully_paid)
        self.assertIsNotNone(self.invoice.paid_date)

