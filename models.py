"""
نماذج نظام المستخدمين والأدوار لمنصة أيديا المتكاملة

يتضمن هذا الملف:
- نموذج المستخدم المخصص
- نموذج الأدوار والصلاحيات
- نموذج ملف المستخدم الشخصي
"""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import uuid


class Role(models.Model):
    """
    نموذج الأدوار في النظام
    يحدد الأدوار المختلفة للمستخدمين مثل: مدير عام، مدير مشاريع، مصمم، إلخ
    """
    
    # خيارات الأدوار المتاحة
    ROLE_CHOICES = [
        ('admin', 'مدير عام'),
        ('project_manager', 'مدير مشاريع'),
        ('account_manager', 'مدير حسابات'),
        ('designer', 'مصمم'),
        ('developer', 'مطور'),
        ('content_writer', 'كاتب محتوى'),
        ('social_media_specialist', 'أخصائي وسائل التواصل'),
        ('financial_manager', 'مدير مالي'),
        ('client', 'عميل'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        unique=True,
        verbose_name=_('اسم الدور')
    )
    display_name = models.CharField(
        max_length=100,
        verbose_name=_('الاسم المعروض')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('وصف الدور')
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        verbose_name=_('الصلاحيات')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )
    
    class Meta:
        verbose_name = _('دور')
        verbose_name_plural = _('الأدوار')
        ordering = ['display_name']
    
    def __str__(self):
        return self.display_name
    
    def get_permissions_list(self):
        """إرجاع قائمة بأسماء الصلاحيات"""
        return list(self.permissions.values_list('codename', flat=True))


class CustomUser(AbstractUser):
    """
    نموذج المستخدم المخصص لمنصة أيديا
    يوسع نموذج المستخدم الافتراضي في Django
    """
    
    # معرف فريد للمستخدم
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # معلومات شخصية إضافية
    arabic_first_name = models.CharField(
        max_length=150,
        verbose_name=_('الاسم الأول بالعربية')
    )
    arabic_last_name = models.CharField(
        max_length=150,
        verbose_name=_('اسم العائلة بالعربية')
    )
    
    # معلومات الاتصال
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("رقم الهاتف يجب أن يكون بالصيغة: '+999999999'. حتى 15 رقم مسموح.")
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name=_('رقم الهاتف')
    )
    
    # الدور والصلاحيات
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('الدور')
    )
    
    # معلومات إضافية
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('رقم الموظف')
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('القسم')
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('المنصب')
    )
    hire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ التوظيف')
    )
    
    # إعدادات الحساب
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('تم التحقق')
    )
    two_factor_enabled = models.BooleanField(
        default=False,
        verbose_name=_('المصادقة الثنائية مفعلة')
    )
    
    # تواريخ مهمة
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('آخر عنوان IP للدخول')
    )
    
    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        ordering = ['arabic_first_name', 'arabic_last_name']
    
    def __str__(self):
        if self.arabic_first_name and self.arabic_last_name:
            return f"{self.arabic_first_name} {self.arabic_last_name}"
        return self.username
    
    @property
    def full_name_arabic(self):
        """الاسم الكامل بالعربية"""
        return f"{self.arabic_first_name} {self.arabic_last_name}".strip()
    
    @property
    def full_name_english(self):
        """الاسم الكامل بالإنجليزية"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_role_permissions(self):
        """الحصول على صلاحيات الدور"""
        if self.role:
            return self.role.get_permissions_list()
        return []
    
    def has_role_permission(self, permission_codename):
        """التحقق من وجود صلاحية معينة"""
        return permission_codename in self.get_role_permissions()


class UserProfile(models.Model):
    """
    ملف المستخدم الشخصي - معلومات إضافية
    """
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('المستخدم')
    )
    
    # الصورة الشخصية
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name=_('الصورة الشخصية')
    )
    
    # معلومات شخصية
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_('نبذة شخصية')
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الميلاد')
    )
    
    # معلومات الاتصال الإضافية
    secondary_email = models.EmailField(
        blank=True,
        verbose_name=_('البريد الإلكتروني الثانوي')
    )
    linkedin_profile = models.URLField(
        blank=True,
        verbose_name=_('ملف LinkedIn')
    )
    
    # إعدادات التفضيلات
    language_preference = models.CharField(
        max_length=10,
        choices=[('ar', 'العربية'), ('en', 'English')],
        default='ar',
        verbose_name=_('اللغة المفضلة')
    )
    timezone = models.CharField(
        max_length=50,
        default='Asia/Riyadh',
        verbose_name=_('المنطقة الزمنية')
    )
    
    # إعدادات الإشعارات
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_('إشعارات البريد الإلكتروني')
    )
    sms_notifications = models.BooleanField(
        default=False,
        verbose_name=_('إشعارات الرسائل النصية')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )
    
    class Meta:
        verbose_name = _('ملف شخصي')
        verbose_name_plural = _('الملفات الشخصية')
    
    def __str__(self):
        return f"ملف {self.user.full_name_arabic}"


class UserSession(models.Model):
    """
    نموذج لتتبع جلسات المستخدمين
    """
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_('المستخدم')
    )
    session_key = models.CharField(
        max_length=40,
        unique=True,
        verbose_name=_('مفتاح الجلسة')
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('عنوان IP')
    )
    user_agent = models.TextField(
        verbose_name=_('معلومات المتصفح')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ بداية الجلسة')
    )
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name=_('آخر نشاط')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشطة')
    )
    
    class Meta:
        verbose_name = _('جلسة مستخدم')
        verbose_name_plural = _('جلسات المستخدمين')
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"جلسة {self.user.full_name_arabic} - {self.created_at}"
