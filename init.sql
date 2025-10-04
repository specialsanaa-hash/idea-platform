-- إعداد قاعدة البيانات الأولية لمنصة أيديا
-- تم إنشاؤه تلقائياً بواسطة نظام إعداد المشروع

-- إنشاء قاعدة البيانات الرئيسية
CREATE DATABASE idea_platform;

-- إنشاء مستخدم قاعدة البيانات
CREATE USER idea_user WITH PASSWORD 'idea_password_2024';

-- منح الصلاحيات للمستخدم
GRANT ALL PRIVILEGES ON DATABASE idea_platform TO idea_user;

-- تفعيل الامتدادات المطلوبة
\c idea_platform;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- تعليق توضيحي
COMMENT ON DATABASE idea_platform IS 'قاعدة البيانات الرئيسية لمنصة أيديا المتكاملة';

