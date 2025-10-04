"""
أدوات مساعدة لنظام الفواتير
"""
import os
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile
from decimal import Decimal
from datetime import datetime

def generate_invoice_pdf(invoice, template=None, context_data=None):
    """
    إنشاء ملف PDF للفاتورة
    
    Args:
        invoice: كائن الفاتورة
        template: قالب الفاتورة (اختياري)
        context_data: بيانات إضافية للقالب (اختياري)
    
    Returns:
        HttpResponse: ملف PDF
    """
    
    # إعداد البيانات للقالب
    context = {
        'invoice': invoice,
        'items': invoice.items.all().order_by('order'),
        'company': {
            'name': 'شركة أيديا للاستشارات والحلول التسويقية',
            'address': 'المملكة العربية السعودية',
            'phone': '+966 XX XXX XXXX',
            'email': 'info@idea-consulting.com',
            'website': 'www.idea-consulting.com',
            'tax_number': 'XXX-XXX-XXX-XXX',
        },
        'generated_at': datetime.now(),
        'currency': 'ريال سعودي',
        'currency_symbol': 'ر.س',
    }
    
    # إضافة البيانات الإضافية
    if context_data:
        context.update(context_data)
    
    # استخدام القالب المحدد أو القالب الافتراضي
    if template and template.html_template:
        html_content = template.html_template
        css_content = template.css_styles or ""
    else:
        # القالب الافتراضي
        html_content = get_default_invoice_template()
        css_content = get_default_invoice_css()
    
    # معالجة القالب
    from django.template import Template, Context
    template_obj = Template(html_content)
    rendered_html = template_obj.render(Context(context))
    
    # إعداد الخطوط العربية
    font_config = FontConfiguration()
    
    # إنشاء PDF
    html_doc = HTML(string=rendered_html, base_url=settings.STATIC_URL)
    css_doc = CSS(string=css_content, font_config=font_config)
    
    # إنشاء ملف مؤقت
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        html_doc.write_pdf(tmp_file.name, stylesheets=[css_doc], font_config=font_config)
        
        # قراءة المحتوى
        with open(tmp_file.name, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # حذف الملف المؤقت
        os.unlink(tmp_file.name)
    
    # إنشاء الاستجابة
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    
    return response

def get_default_invoice_template():
    """الحصول على القالب الافتراضي للفاتورة"""
    return """
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>فاتورة {{ invoice.invoice_number }}</title>
    </head>
    <body>
        <div class="invoice-container">
            <!-- رأس الفاتورة -->
            <header class="invoice-header">
                <div class="company-info">
                    <h1>{{ company.name }}</h1>
                    <p>{{ company.address }}</p>
                    <p>هاتف: {{ company.phone }}</p>
                    <p>بريد إلكتروني: {{ company.email }}</p>
                    <p>الموقع: {{ company.website }}</p>
                    <p>الرقم الضريبي: {{ company.tax_number }}</p>
                </div>
                <div class="invoice-info">
                    <h2>فاتورة</h2>
                    <p><strong>رقم الفاتورة:</strong> {{ invoice.invoice_number }}</p>
                    <p><strong>تاريخ الإصدار:</strong> {{ invoice.issue_date }}</p>
                    <p><strong>تاريخ الاستحقاق:</strong> {{ invoice.due_date }}</p>
                    <p><strong>الحالة:</strong> {{ invoice.get_status_display }}</p>
                </div>
            </header>
            
            <!-- معلومات العميل -->
            <section class="client-info">
                <h3>معلومات العميل</h3>
                <p><strong>اسم العميل:</strong> {{ invoice.client.name }}</p>
                <p><strong>البريد الإلكتروني:</strong> {{ invoice.client.email }}</p>
                <p><strong>الهاتف:</strong> {{ invoice.client.phone }}</p>
                {% if invoice.client.address %}
                <p><strong>العنوان:</strong> {{ invoice.client.address }}</p>
                {% endif %}
            </section>
            
            <!-- تفاصيل الفاتورة -->
            <section class="invoice-details">
                <h3>{{ invoice.title }}</h3>
                {% if invoice.description %}
                <p>{{ invoice.description }}</p>
                {% endif %}
                {% if invoice.project %}
                <p><strong>المشروع:</strong> {{ invoice.project.name }}</p>
                {% endif %}
            </section>
            
            <!-- جدول البنود -->
            <section class="invoice-items">
                <table class="items-table">
                    <thead>
                        <tr>
                            <th>الوصف</th>
                            <th>الوحدة</th>
                            <th>الكمية</th>
                            <th>سعر الوحدة</th>
                            <th>المجموع</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in items %}
                        <tr>
                            <td>
                                {{ item.description }}
                                {% if item.notes %}
                                <br><small>{{ item.notes }}</small>
                                {% endif %}
                            </td>
                            <td>{{ item.unit }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>{{ item.unit_price }} {{ currency_symbol }}</td>
                            <td>{{ item.total_amount }} {{ currency_symbol }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </section>
            
            <!-- المجاميع -->
            <section class="invoice-totals">
                <div class="totals-table">
                    <div class="total-row">
                        <span>المجموع الفرعي:</span>
                        <span>{{ invoice.subtotal }} {{ currency_symbol }}</span>
                    </div>
                    {% if invoice.discount_amount > 0 %}
                    <div class="total-row">
                        <span>الخصم:</span>
                        <span>-{{ invoice.discount_amount }} {{ currency_symbol }}</span>
                    </div>
                    {% endif %}
                    {% if invoice.tax_amount > 0 %}
                    <div class="total-row">
                        <span>{{ invoice.get_tax_type_display }} ({{ invoice.tax_rate }}%):</span>
                        <span>{{ invoice.tax_amount }} {{ currency_symbol }}</span>
                    </div>
                    {% endif %}
                    <div class="total-row final-total">
                        <span><strong>المجموع الإجمالي:</strong></span>
                        <span><strong>{{ invoice.total_amount }} {{ currency_symbol }}</strong></span>
                    </div>
                    {% if invoice.paid_amount > 0 %}
                    <div class="total-row">
                        <span>المبلغ المدفوع:</span>
                        <span>{{ invoice.paid_amount }} {{ currency_symbol }}</span>
                    </div>
                    <div class="total-row">
                        <span><strong>المبلغ المتبقي:</strong></span>
                        <span><strong>{{ invoice.remaining_amount }} {{ currency_symbol }}</strong></span>
                    </div>
                    {% endif %}
                </div>
            </section>
            
            <!-- ملاحظات -->
            {% if invoice.notes %}
            <section class="invoice-notes">
                <h3>ملاحظات</h3>
                <p>{{ invoice.notes }}</p>
            </section>
            {% endif %}
            
            <!-- معلومات الدفع -->
            <section class="payment-info">
                <h3>معلومات الدفع</h3>
                <p>يرجى تحويل المبلغ إلى الحساب البنكي التالي:</p>
                <p><strong>اسم البنك:</strong> البنك الأهلي السعودي</p>
                <p><strong>رقم الحساب:</strong> XXXX-XXXX-XXXX-XXXX</p>
                <p><strong>رقم الآيبان:</strong> SA XX XXXX XXXX XXXX XXXX XXXX</p>
                <p>يرجى إرسال سند التحويل بعد الدفع.</p>
            </section>
            
            <!-- تذييل الفاتورة -->
            <footer class="invoice-footer">
                <p>شكراً لتعاملكم معنا</p>
                <p>تم إنشاء هذه الفاتورة في {{ generated_at|date:"d/m/Y H:i" }}</p>
            </footer>
        </div>
    </body>
    </html>
    """

def get_default_invoice_css():
    """الحصول على CSS الافتراضي للفاتورة"""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Noto Sans Arabic', Arial, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        color: #333;
        direction: rtl;
    }
    
    .invoice-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background: white;
    }
    
    .invoice-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 2px solid #2c5aa0;
    }
    
    .company-info h1 {
        color: #2c5aa0;
        font-size: 24px;
        margin-bottom: 10px;
    }
    
    .company-info p {
        margin-bottom: 5px;
        font-size: 12px;
    }
    
    .invoice-info {
        text-align: left;
        direction: ltr;
    }
    
    .invoice-info h2 {
        color: #2c5aa0;
        font-size: 28px;
        margin-bottom: 15px;
    }
    
    .invoice-info p {
        margin-bottom: 5px;
        font-size: 12px;
    }
    
    .client-info, .invoice-details {
        margin-bottom: 25px;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 5px;
    }
    
    .client-info h3, .invoice-details h3 {
        color: #2c5aa0;
        margin-bottom: 10px;
        font-size: 16px;
    }
    
    .items-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 25px;
    }
    
    .items-table th,
    .items-table td {
        padding: 12px;
        text-align: right;
        border-bottom: 1px solid #ddd;
    }
    
    .items-table th {
        background: #2c5aa0;
        color: white;
        font-weight: 600;
    }
    
    .items-table tbody tr:hover {
        background: #f8f9fa;
    }
    
    .totals-table {
        width: 300px;
        margin-left: auto;
        margin-bottom: 25px;
    }
    
    .total-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #eee;
    }
    
    .final-total {
        border-top: 2px solid #2c5aa0;
        border-bottom: 2px solid #2c5aa0;
        font-size: 16px;
        color: #2c5aa0;
        margin-top: 10px;
        padding-top: 15px;
        padding-bottom: 15px;
    }
    
    .invoice-notes {
        margin-bottom: 25px;
        padding: 15px;
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
    }
    
    .invoice-notes h3 {
        color: #856404;
        margin-bottom: 10px;
    }
    
    .payment-info {
        margin-bottom: 25px;
        padding: 15px;
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
    }
    
    .payment-info h3 {
        color: #0c5460;
        margin-bottom: 10px;
    }
    
    .invoice-footer {
        text-align: center;
        padding-top: 20px;
        border-top: 1px solid #ddd;
        color: #666;
        font-size: 12px;
    }
    
    @media print {
        .invoice-container {
            padding: 0;
        }
        
        .invoice-header {
            page-break-inside: avoid;
        }
        
        .items-table {
            page-break-inside: auto;
        }
        
        .items-table tr {
            page-break-inside: avoid;
        }
    }
    """

def calculate_invoice_totals(invoice):
    """حساب مجاميع الفاتورة"""
    subtotal = sum(item.total_amount for item in invoice.items.all())
    tax_amount = (subtotal * invoice.tax_rate) / 100
    total_amount = subtotal + tax_amount - invoice.discount_amount
    
    invoice.subtotal = subtotal
    invoice.tax_amount = tax_amount
    invoice.total_amount = total_amount
    invoice.save()
    
    return {
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'remaining_amount': total_amount - invoice.paid_amount
    }

def generate_invoice_number():
    """إنشاء رقم فاتورة تلقائي"""
    from .models import Invoice
    from django.utils import timezone
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    
    # البحث عن آخر فاتورة في الشهر الحالي
    last_invoice = Invoice.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month
    ).order_by('-created_at').first()
    
    if last_invoice:
        # استخراج الرقم التسلسلي من آخر فاتورة
        try:
            last_number = int(last_invoice.invoice_number.split('-')[-1])
            next_number = last_number + 1
        except (ValueError, IndexError):
            next_number = 1
    else:
        next_number = 1
    
    # تنسيق رقم الفاتورة: INV-YYYY-MM-XXXX
    invoice_number = f"INV-{current_year}-{current_month:02d}-{next_number:04d}"
    
    return invoice_number

def send_invoice_email(invoice, recipients, subject=None, message=None):
    """إرسال الفاتورة بالبريد الإلكتروني"""
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    
    if not subject:
        subject = f"فاتورة رقم {invoice.invoice_number} - {invoice.client.name}"
    
    if not message:
        message = render_to_string('billing/invoice_email.html', {
            'invoice': invoice,
            'client': invoice.client,
        })
    
    # إنشاء PDF
    pdf_response = generate_invoice_pdf(invoice)
    pdf_content = pdf_response.content
    
    # إنشاء البريد الإلكتروني
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
    )
    
    # إرفاق PDF
    email.attach(
        f"invoice_{invoice.invoice_number}.pdf",
        pdf_content,
        'application/pdf'
    )
    
    # إرسال البريد
    email.send()
    
    return True

