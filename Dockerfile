# استخدام Python 3.11 كصورة أساسية
FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعيين مجلد العمل
WORKDIR /app

# تثبيت متطلبات النظام
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كود المشروع
COPY . /app/

# إنشاء مجلدات مطلوبة
RUN mkdir -p /app/static /app/media /app/logs

# تعيين الصلاحيات
RUN chmod +x /app/manage.py

# فتح المنفذ
EXPOSE 8000

# الأمر الافتراضي
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

