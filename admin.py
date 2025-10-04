"""
إعدادات لوحة الإدارة لنظام المستخدمين
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Role, UserProfile, UserSession


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    إعدادات إدارة الأدوار
    """
    list_display = ['display_name', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['display_name', 'name', 'description']
    filter_horizontal = ['permissions']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('معلومات أساسية'), {
            'fields': ('name', 'display_name', 'description', 'is_active')
        }),
        (_('الصلاحيات'), {
            'fields': ('permissions',)
        }),
        (_('معلومات النظام'), {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class UserProfileInline(admin.StackedInline):
    """
    إدراج ملف المستخدم الشخصي في صفحة المستخدم
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('الملف الشخصي')
    
    fieldsets = (
        (_('الصورة الشخصية'), {
            'fields': ('avatar',)
        }),
        (_('معلومات شخصية'), {
            'fields': ('bio', 'birth_date', 'secondary_email', 'linkedin_profile')
        }),
        (_('التفضيلات'), {
            'fields': ('language_preference', 'timezone')
        }),
        (_('الإشعارات'), {
            'fields': ('email_notifications', 'sms_notifications')
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    إعدادات إدارة المستخدمين المخصصة
    """
    inlines = [UserProfileInline]
    
    list_display = [
        'username', 'full_name_arabic', 'email', 'role', 
        'is_active', 'is_verified', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'is_verified',
        'role', 'department', 'created_at'
    ]
    search_fields = [
        'username', 'email', 'arabic_first_name', 'arabic_last_name',
        'first_name', 'last_name', 'employee_id'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login_ip']
    
    fieldsets = (
        (_('معلومات تسجيل الدخول'), {
            'fields': ('username', 'password')
        }),
        (_('المعلومات الشخصية'), {
            'fields': (
                'arabic_first_name', 'arabic_last_name',
                'first_name', 'last_name', 'email'
            )
        }),
        (_('معلومات الاتصال'), {
            'fields': ('phone_number',)
        }),
        (_('معلومات العمل'), {
            'fields': (
                'role', 'employee_id', 'department', 
                'position', 'hire_date'
            )
        }),
        (_('الصلاحيات'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_verified', 'two_factor_enabled',
                'groups', 'user_permissions'
            ),
        }),
        (_('تواريخ مهمة'), {
            'fields': ('last_login', 'date_joined', 'last_login_ip'),
            'classes': ('collapse',)
        }),
        (_('معلومات النظام'), {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (_('معلومات تسجيل الدخول'), {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('المعلومات الشخصية'), {
            'fields': (
                'arabic_first_name', 'arabic_last_name',
                'first_name', 'last_name', 'email'
            )
        }),
        (_('معلومات العمل'), {
            'fields': ('role', 'employee_id', 'department')
        }),
    )
    
    def full_name_arabic(self, obj):
        """عرض الاسم الكامل بالعربية"""
        return obj.full_name_arabic
    full_name_arabic.short_description = _('الاسم الكامل')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    إعدادات إدارة الملفات الشخصية
    """
    list_display = ['user', 'language_preference', 'timezone', 'created_at']
    list_filter = ['language_preference', 'timezone', 'email_notifications', 'sms_notifications']
    search_fields = ['user__username', 'user__arabic_first_name', 'user__arabic_last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('المستخدم'), {
            'fields': ('user',)
        }),
        (_('الصورة الشخصية'), {
            'fields': ('avatar',)
        }),
        (_('معلومات شخصية'), {
            'fields': ('bio', 'birth_date', 'secondary_email', 'linkedin_profile')
        }),
        (_('التفضيلات'), {
            'fields': ('language_preference', 'timezone')
        }),
        (_('الإشعارات'), {
            'fields': ('email_notifications', 'sms_notifications')
        }),
        (_('معلومات النظام'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """
    إعدادات إدارة جلسات المستخدمين
    """
    list_display = ['user', 'ip_address', 'created_at', 'last_activity', 'is_active']
    list_filter = ['is_active', 'created_at', 'last_activity']
    search_fields = ['user__username', 'user__arabic_first_name', 'ip_address']
    readonly_fields = ['session_key', 'created_at', 'last_activity']
    
    fieldsets = (
        (_('معلومات الجلسة'), {
            'fields': ('user', 'session_key', 'is_active')
        }),
        (_('معلومات الاتصال'), {
            'fields': ('ip_address', 'user_agent')
        }),
        (_('التوقيتات'), {
            'fields': ('created_at', 'last_activity')
        }),
    )
    
    def has_add_permission(self, request):
        """منع إضافة جلسات يدوياً"""
        return False


# تخصيص عنوان لوحة الإدارة
admin.site.site_header = _('لوحة إدارة منصة أيديا')
admin.site.site_title = _('إدارة أيديا')
admin.site.index_title = _('مرحباً بك في لوحة إدارة منصة أيديا المتكاملة')
