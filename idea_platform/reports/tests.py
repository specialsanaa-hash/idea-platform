
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.utils import timezone
import uuid

from .models import Report, ReportTemplate, ScheduledReport, ReportType, ReportStatus, ReportFrequency, DataSource

User = get_user_model()

class ReportModelsTestCase(TestCase):
    """مجموعة اختبارات لنماذج التقارير"""

    def setUp(self):
        """إعداد بيانات الاختبار"""
        self.user = User.objects.create_user(username=\'testuser\', password=\'password\')
        self.template = ReportTemplate.objects.create(
            name=\'Project Performance Template\',
            report_type=ReportType.PROJECT_PERFORMANCE,
            html_template=\'<h1>Project Report</h1>\',
            created_by=self.user
        )

    def test_create_report(self):
        """اختبار إنشاء تقرير جديد"""
        report = Report.objects.create(
            title=\'Monthly Project Summary\',
            template=self.template,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today(),
            generated_by=self.user,
            raw_data={\'projects_count\': 10, \'completed_projects\': 8},
            summary_stats={\'avg_completion_rate\': 0.8}
        )
        self.assertEqual(report.title, \'Monthly Project Summary\')
        self.assertEqual(report.status, ReportStatus.PENDING)
        self.assertTrue(report.raw_data)
        self.assertTrue(report.summary_stats)

    def test_report_properties(self):
        """اختبار خصائص التقرير"""
        report = Report.objects.create(
            title=\'Test Report\',
            template=self.template,
            start_date=date.today() - timedelta(days=7),
            end_date=date.today(),
            generated_by=self.user,
            status=ReportStatus.COMPLETED,
            generation_started_at=timezone.now() - timedelta(minutes=5),
            generation_completed_at=timezone.now()
        )
        self.assertTrue(report.is_completed)
        self.assertIsNotNone(report.generation_duration)
        self.assertFalse(report.has_files) # No files uploaded yet

        report.pdf_file = \'reports/pdf/test_report.pdf\'
        report.save()
        self.assertTrue(report.has_files)

    def test_create_scheduled_report(self):
        """اختبار إنشاء تقرير مجدول"""
        scheduled_report = ScheduledReport.objects.create(
            name=\'Weekly Client Report\',
            template=self.template,
            schedule_type=ReportFrequency.WEEKLY,
            created_by=self.user
        )
        self.assertEqual(scheduled_report.name, \'Weekly Client Report\')
        self.assertEqual(scheduled_report.schedule_type, ReportFrequency.WEEKLY)
        self.assertTrue(scheduled_report.is_active)

    def test_scheduled_report_next_run_calculation(self):
        """اختبار حساب وقت التشغيل التالي للتقرير المجدول"""
        scheduled_report = ScheduledReport.objects.create(
            name=\'Daily Report\',
            template=self.template,
            schedule_type=ReportFrequency.DAILY,
            created_by=self.user
        )
        # Initial next_run_at should be None
        self.assertIsNone(scheduled_report.next_run_at)

        scheduled_report.calculate_next_run()
        self.assertIsNotNone(scheduled_report.next_run_at)
        # Check if it\'s approximately one day from now (allowing for slight time differences)
        self.assertLessEqual(scheduled_report.next_run_at - timezone.now(), timedelta(days=1, seconds=1))
        self.assertGreaterEqual(scheduled_report.next_run_at - timezone.now(), timedelta(days=1, seconds=-1))

        scheduled_report.schedule_type = ReportFrequency.MONTHLY
        scheduled_report.save()
        scheduled_report.calculate_next_run()
        self.assertIsNotNone(scheduled_report.next_run_at)
        self.assertLessEqual(scheduled_report.next_run_at - timezone.now(), timedelta(days=30, seconds=1))
        self.assertGreaterEqual(scheduled_report.next_run_at - timezone.now(), timedelta(days=30, seconds=-1))

    def test_report_template_str(self):
        """اختبار دالة __str__ لقالب التقرير"""
        self.assertEqual(str(self.template), \'Project Performance Template\')

    def test_report_str(self):
        """اختبار دالة __str__ للتقرير"""
        report = Report.objects.create(
            title=\'Daily Summary\',
            template=self.template,
            start_date=date(2025, 10, 1),
            end_date=date(2025, 10, 1),
            generated_by=self.user
        )
        self.assertEqual(str(report), \'Daily Summary - 2025-10-01 إلى 2025-10-01\')

    def test_scheduled_report_str(self):
        """اختبار دالة __str__ للتقرير المجدول"""
        scheduled_report = ScheduledReport.objects.create(
            name=\'Quarterly Review\',
            template=self.template,
            schedule_type=ReportFrequency.QUARTERLY,
            created_by=self.user
        )
        self.assertEqual(str(scheduled_report), \'Quarterly Review\')




from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch

class ReportAPITestCase(APITestCase):
    """مجموعة اختبارات لواجهات برمجة تطبيقات التقارير"""

    def setUp(self):
        self.user = User.objects.create_user(username=\'testuser\', password=\'password\')
        self.client.force_authenticate(user=self.user)

        self.template = ReportTemplate.objects.create(
            name=\'API Test Template\',
            report_type=ReportType.CUSTOM,
            html_template=\'<div>Report Content</div>\',
            created_by=self.user
        )
        self.report = Report.objects.create(
            title=\'API Test Report\',
            template=self.template,
            start_date=date.today() - timedelta(days=7),
            end_date=date.today(),
            generated_by=self.user,
            status=ReportStatus.COMPLETED
        )
        self.scheduled_report = ScheduledReport.objects.create(
            name=\'API Scheduled Report\',
            template=self.template,
            schedule_type=ReportFrequency.MONTHLY,
            created_by=self.user
        )

    def test_report_template_list_create_api_view(self):
        url = reverse(\'reporttemplate-list\')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        new_template_data = {
            \"name\": \"New Template\",
            \"report_type\": \"financial\",
            \"html_template\": \"<h1>Financial Report</h1>\",
            \"created_by\": self.user.id
        }
        response = self.client.post(url, new_template_data, format=\'json\')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReportTemplate.objects.count(), 2)

    def test_report_list_create_api_view(self):
        url = reverse(\'report-list\')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        new_report_data = {
            \"title\": \"New Report\",
            \"template\": self.template.id,
            \"start_date\": date.today().isoformat(),
            \"end_date\": date.today().isoformat(),
            \"generated_by\": self.user.id
        }
        response = self.client.post(url, new_report_data, format=\'json\')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 2)

    @patch(\'idea_platform.reports.views.initialize_analytics_reporting\')
    @patch(\'idea_platform.reports.views.get_analytics_data\')
    def test_analytics_dashboard_api_view(self, mock_get_analytics_data, mock_initialize_analytics_reporting):
        mock_initialize_analytics_reporting.return_value = True
        mock_get_analytics_data.return_value = {
            \'reports\': [{
                \'data\': {
                    \'rows\': [{
                        \'dimensions\': [\'20251001\'],
                        \'metrics\': [{\'values\': [\'100\', \'200\', \'300\]}]}
                    }]
                }
            }]
        }
        
        url = reverse(\'analytics-dashboard\')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(\'overview\', response.data)
        self.assertIn(\'monthly_performance\', response.data)
        self.assertIn(\'google_analytics\', response.data)
        self.assertEqual(response.data[\"google_analytics\"][\'20251001\"][\'users\'], \"100\")

    def test_generate_report_pdf_view(self):
        url = reverse(\'generatereportpdf-detail\', kwargs={\'pk\': self.report.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response[\'Content-Type\'], \'application/pdf\')
        self.assertTrue(f\'attachment; filename=\"Report_{self.report.title.replace(\' \', \'_\')}.pdf\"\' in response[\'Content-Disposition\'])


class ReportIntegrationTestCase(APITestCase):
    """مجموعة اختبارات التكامل لنظام التقارير"""

    def setUp(self):
        self.user = User.objects.create_user(username=\'testuser\', password=\'password\')
        self.client.force_authenticate(user=self.user)

        self.template = ReportTemplate.objects.create(
            name=\'Integration Test Template\',
            report_type=ReportType.PROJECT_PERFORMANCE,
            html_template=\'<div>Integration Report Content</div>\',
            created_by=self.user
        )

    def test_report_creation_with_template_details(self):
        url = reverse(\'report-list\')
        new_report_data = {
            \"title\": \"Integration Report\",
            \"template\": self.template.id,
            \"start_date\": date.today().isoformat(),
            \"end_date\": date.today().isoformat(),
            \"generated_by\": self.user.id,
            \"status\": ReportStatus.COMPLETED
        }
        response = self.client.post(url, new_report_data, format=\'json\')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        report_id = response.data[\"id\"]

        retrieve_url = reverse(\'report-detail\', kwargs={\'pk\': report_id})
        retrieve_response = self.client.get(retrieve_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertIn(\'template_details\', retrieve_response.data)
        self.assertEqual(retrieve_response.data[\"template_details\"][\'name\'], \"Integration Test Template\")

    def test_scheduled_report_next_run_logic(self):
        scheduled_report = ScheduledReport.objects.create(
            name=\'Daily Scheduled Integration Report\',
            template=self.template,
            schedule_type=ReportFrequency.DAILY,
            created_by=self.user
        )
        self.assertIsNone(scheduled_report.next_run_at)

        scheduled_report.calculate_next_run()
        self.assertIsNotNone(scheduled_report.next_run_at)
        # Check if it\'s approximately one day from now (allowing for slight time differences)
        self.assertLessEqual(scheduled_report.next_run_at - timezone.now(), timedelta(days=1, seconds=1))
        self.assertGreaterEqual(scheduled_report.next_run_at - timezone.now(), timedelta(days=1, seconds=-1))




