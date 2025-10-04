"""
Serializers لنظام المستخدمين والأدوار
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Role, UserProfile, UserSession


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer للأدوار
    """
    permissions_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = [
            'id', 'name', 'display_name', 'description', 
            'permissions', 'permissions_list', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_permissions_list(self, obj):
        """إرجاع قائمة بأسماء الصلاحيات"""
        return obj.get_permissions_list()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer للملف الشخصي للمستخدم
    """
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'birth_date', 'secondary_email',
            'linkedin_profile', 'language_preference', 'timezone',
            'email_notifications', 'sms_notifications',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer للمستخدمين - للقراءة فقط
    """
    role_details = RoleSerializer(source='role', read_only=True)
    profile = UserProfileSerializer(read_only=True)
    full_name_arabic = serializers.ReadOnlyField()
    full_name_english = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'arabic_first_name', 'arabic_last_name',
            'first_name', 'last_name', 'phone_number', 'role', 'role_details',
            'employee_id', 'department', 'position', 'hire_date',
            'is_active', 'is_verified', 'two_factor_enabled',
            'full_name_arabic', 'full_name_english', 'profile',
            'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'last_login',
            'full_name_arabic', 'full_name_english'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer لإنشاء مستخدم جديد
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'arabic_first_name', 'arabic_last_name',
            'first_name', 'last_name', 'phone_number',
            'role', 'employee_id', 'department', 'position', 'hire_date',
            'profile'
        ]
    
    def validate(self, attrs):
        """التحقق من تطابق كلمات المرور"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(_("كلمات المرور غير متطابقة"))
        return attrs
    
    def create(self, validated_data):
        """إنشاء مستخدم جديد"""
        # إزالة تأكيد كلمة المرور
        validated_data.pop('password_confirm')
        
        # استخراج بيانات الملف الشخصي
        profile_data = validated_data.pop('profile', {})
        
        # إنشاء المستخدم
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        
        # إنشاء الملف الشخصي
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer لتحديث بيانات المستخدم
    """
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'arabic_first_name', 'arabic_last_name',
            'first_name', 'last_name', 'phone_number',
            'role', 'employee_id', 'department', 'position', 'hire_date',
            'is_active', 'is_verified', 'two_factor_enabled',
            'profile'
        ]
    
    def update(self, instance, validated_data):
        """تحديث بيانات المستخدم"""
        # استخراج بيانات الملف الشخصي
        profile_data = validated_data.pop('profile', None)
        
        # تحديث بيانات المستخدم
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # تحديث الملف الشخصي
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer لتغيير كلمة المرور
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """التحقق من صحة البيانات"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(_("كلمات المرور الجديدة غير متطابقة"))
        return attrs
    
    def validate_old_password(self, value):
        """التحقق من كلمة المرور القديمة"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("كلمة المرور القديمة غير صحيحة"))
        return value


class LoginSerializer(serializers.Serializer):
    """
    Serializer لتسجيل الدخول
    """
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """التحقق من بيانات تسجيل الدخول"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(_("اسم المستخدم أو كلمة المرور غير صحيحة"))
            
            if not user.is_active:
                raise serializers.ValidationError(_("هذا الحساب غير نشط"))
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(_("يجب إدخال اسم المستخدم وكلمة المرور"))


class UserSessionSerializer(serializers.ModelSerializer):
    """
    Serializer لجلسات المستخدمين
    """
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'user', 'user_details', 'session_key',
            'ip_address', 'user_agent', 'created_at',
            'last_activity', 'is_active'
        ]
        read_only_fields = [
            'id', 'session_key', 'created_at', 'last_activity'
        ]


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer مبسط لقائمة المستخدمين
    """
    role_name = serializers.CharField(source='role.display_name', read_only=True)
    full_name_arabic = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'full_name_arabic',
            'role_name', 'department', 'is_active',
            'is_verified', 'created_at'
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer لتحديث الملف الشخصي فقط
    """
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'birth_date', 'secondary_email',
            'linkedin_profile', 'language_preference', 'timezone',
            'email_notifications', 'sms_notifications'
        ]
    
    def update(self, instance, validated_data):
        """تحديث الملف الشخصي"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

