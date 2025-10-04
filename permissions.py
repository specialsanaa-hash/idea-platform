"""
صلاحيات مخصصة لنظام المستخدمين
"""

from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    """
    صلاحية مخصصة للتحقق من وجود صلاحية محددة للمستخدم
    """
    
    def has_permission(self, request, view):
        """
        التحقق من الصلاحية على مستوى العرض
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # إذا كان المستخدم superuser، فلديه جميع الصلاحيات
        if request.user.is_superuser:
            return True
        
        # الحصول على الصلاحية المطلوبة من العرض
        required_permission = getattr(view, 'required_permission', None)
        
        # إذا لم تكن هناك صلاحية محددة، السماح بالوصول
        if not required_permission:
            return True
        
        # إذا كان العرض يحتوي على دالة للحصول على الصلاحية المطلوبة
        if hasattr(view, 'get_required_permission'):
            required_permission = view.get_required_permission()
        
        # التحقق من وجود الصلاحية
        return request.user.has_perm(required_permission)
    
    def has_object_permission(self, request, view, obj):
        """
        التحقق من الصلاحية على مستوى الكائن
        """
        # التحقق من الصلاحية العامة أولاً
        if not self.has_permission(request, view):
            return False
        
        # إذا كان المستخدم superuser، فلديه جميع الصلاحيات
        if request.user.is_superuser:
            return True
        
        # يمكن إضافة منطق إضافي للتحقق من الصلاحيات على مستوى الكائن
        return True


class IsOwnerOrReadOnly(BasePermission):
    """
    صلاحية مخصصة للسماح للمالك فقط بالتعديل
    """
    
    def has_object_permission(self, request, view, obj):
        """
        صلاحيات القراءة متاحة لأي طلب،
        لكن صلاحيات الكتابة متاحة فقط لمالك الكائن
        """
        # صلاحيات القراءة متاحة لأي طلب مصادق عليه
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # صلاحيات الكتابة متاحة فقط لمالك الكائن
        return obj.created_by == request.user


class IsClientOrStaff(BasePermission):
    """
    صلاحية مخصصة للعملاء أو الموظفين
    """
    
    def has_permission(self, request, view):
        """
        السماح للموظفين أو العملاء المصادق عليهم
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # السماح للموظفين
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # السماح للعملاء
        return hasattr(request.user, 'client_profile')
    
    def has_object_permission(self, request, view, obj):
        """
        التحقق من الصلاحية على مستوى الكائن
        """
        if not self.has_permission(request, view):
            return False
        
        # السماح للموظفين بالوصول لجميع الكائنات
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # السماح للعملاء بالوصول لكائناتهم فقط
        if hasattr(obj, 'client'):
            return obj.client.user == request.user
        
        return False




class IsStaffOrReadOnly(BasePermission):
    """
    صلاحية للموظفين للكتابة والقراءة للجميع
    """
    
    def has_permission(self, request, view):
        """
        السماح بالقراءة للجميع والكتابة للموظفين فقط
        """
        # السماح بالقراءة للجميع
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # السماح بالكتابة للمستخدمين المصادق عليهم والموظفين
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    صلاحية للمالك أو الموظفين للكتابة والقراءة للجميع
    """
    
    def has_permission(self, request, view):
        """
        السماح بالقراءة للجميع والكتابة للمستخدمين المصادق عليهم
        """
        # السماح بالقراءة للجميع
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # السماح بالكتابة للمستخدمين المصادق عليهم
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        التحقق من الصلاحية على مستوى الكائن
        """
        # السماح بالقراءة للجميع
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # السماح للموظفين بالتعديل على جميع الكائنات
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # السماح للمالك بالتعديل على كائناته
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        elif hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user
        
        return False

