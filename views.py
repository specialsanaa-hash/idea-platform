"""
Views لنظام المستخدمين والأدوار
"""

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import CustomUser, Role, UserProfile, UserSession
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    UserListSerializer, ChangePasswordSerializer, LoginSerializer,
    RoleSerializer, UserProfileSerializer, UserProfileUpdateSerializer,
    UserSessionSerializer
)


class RoleListCreateView(generics.ListCreateAPIView):
    """
    عرض وإنشاء الأدوار
    """
    queryset = Role.objects.filter(is_active=True)
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """تصفية الأدوار حسب الصلاحيات"""
        queryset = super().get_queryset()
        
        # البحث
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(display_name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('display_name')


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    عرض وتحديث وحذف دور محدد
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """حذف منطقي للدور"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListCreateView(generics.ListCreateAPIView):
    """
    عرض وإنشاء المستخدمين
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """اختيار Serializer حسب العملية"""
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer
    
    def get_queryset(self):
        """تصفية المستخدمين"""
        queryset = super().get_queryset()
        
        # البحث
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(arabic_first_name__icontains=search) |
                Q(arabic_last_name__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        # تصفية حسب الدور
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role__name=role)
        
        # تصفية حسب القسم
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        # تصفية حسب الحالة
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset.order_by('-created_at')


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    عرض وتحديث وحذف مستخدم محدد
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """اختيار Serializer حسب العملية"""
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    def destroy(self, request, *args, **kwargs):
        """إلغاء تفعيل المستخدم بدلاً من الحذف"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {'message': _('تم إلغاء تفعيل المستخدم بنجاح')},
            status=status.HTTP_200_OK
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    عرض وتحديث الملف الشخصي للمستخدم
    """
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """الحصول على الملف الشخصي للمستخدم الحالي"""
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ChangePasswordView(APIView):
    """
    تغيير كلمة المرور
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response(
                {'message': _('تم تغيير كلمة المرور بنجاح')},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    تسجيل الدخول
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # تسجيل الدخول
            login(request, user)
            
            # إنشاء JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # تسجيل الجلسة
            self._create_user_session(request, user)
            
            # إرجاع البيانات
            user_serializer = UserSerializer(user)
            return Response({
                'message': _('تم تسجيل الدخول بنجاح'),
                'user': user_serializer.data,
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _create_user_session(self, request, user):
        """إنشاء جلسة مستخدم"""
        try:
            # الحصول على معلومات الطلب
            ip_address = self._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            session_key = request.session.session_key
            
            # إنشاء أو تحديث الجلسة
            session, created = UserSession.objects.get_or_create(
                user=user,
                session_key=session_key,
                defaults={
                    'ip_address': ip_address,
                    'user_agent': user_agent,
                    'is_active': True
                }
            )
            
            if not created:
                session.ip_address = ip_address
                session.user_agent = user_agent
                session.is_active = True
                session.save()
                
        except Exception as e:
            # تسجيل الخطأ ولكن لا نوقف عملية تسجيل الدخول
            pass
    
    def _get_client_ip(self, request):
        """الحصول على عنوان IP للعميل"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(APIView):
    """
    تسجيل الخروج
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # إلغاء تفعيل الجلسة
            session_key = request.session.session_key
            if session_key:
                UserSession.objects.filter(
                    user=request.user,
                    session_key=session_key
                ).update(is_active=False)
            
            # تسجيل الخروج
            logout(request)
            
            return Response(
                {'message': _('تم تسجيل الخروج بنجاح')},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': _('حدث خطأ أثناء تسجيل الخروج')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CurrentUserView(APIView):
    """
    عرض بيانات المستخدم الحالي
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserSessionsView(generics.ListAPIView):
    """
    عرض جلسات المستخدم الحالي
    """
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user
        ).order_by('-last_activity')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def terminate_session(request, session_id):
    """
    إنهاء جلسة محددة
    """
    try:
        session = UserSession.objects.get(
            id=session_id,
            user=request.user
        )
        session.is_active = False
        session.save()
        
        return Response(
            {'message': _('تم إنهاء الجلسة بنجاح')},
            status=status.HTTP_200_OK
        )
    except UserSession.DoesNotExist:
        return Response(
            {'error': _('الجلسة غير موجودة')},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    إحصائيات المستخدمين
    """
    stats = {
        'total_users': CustomUser.objects.count(),
        'active_users': CustomUser.objects.filter(is_active=True).count(),
        'verified_users': CustomUser.objects.filter(is_verified=True).count(),
        'users_by_role': {},
        'users_by_department': {},
    }
    
    # إحصائيات حسب الدور
    roles = Role.objects.filter(is_active=True)
    for role in roles:
        count = CustomUser.objects.filter(role=role).count()
        stats['users_by_role'][role.display_name] = count
    
    # إحصائيات حسب القسم
    departments = CustomUser.objects.values_list('department', flat=True).distinct()
    for dept in departments:
        if dept:
            count = CustomUser.objects.filter(department=dept).count()
            stats['users_by_department'][dept] = count
    
    return Response(stats)
