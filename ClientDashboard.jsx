/**
 * صفحة لوحة تحكم العميل
 */

import { useState, useEffect } from 'react';
import { 
  FolderOpen, 
  CheckSquare, 
  FileText, 
  TrendingUp,
  Calendar,
  Clock,
  AlertCircle,
  Download,
  Upload
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';

// بيانات وهمية للعميل
const mockClientData = {
  client_info: {
    name: 'شركة التقنية المتقدمة',
    email: 'info@techadvanced.com',
    phone: '+970-59-123-4567',
    company: 'شركة التقنية المتقدمة'
  },
  stats: {
    projects: {
      total: 8,
      active: 3,
      completed: 5
    },
    tasks: {
      total: 24,
      completed: 18,
      pending: 6,
      completion_rate: 75
    },
    invoices: {
      total: 12,
      paid: 9,
      pending: 3,
      total_amount: 45000,
      paid_amount: 32000,
      pending_amount: 13000
    }
  },
  recent_data: {
    projects: [
      {
        id: 1,
        name: 'موقع الشركة الجديد',
        status: 'in_progress',
        progress: 75,
        start_date: '2024-01-01',
        end_date: '2024-02-15'
      },
      {
        id: 2,
        name: 'تطبيق الهاتف المحمول',
        status: 'planning',
        progress: 25,
        start_date: '2024-01-15',
        end_date: '2024-03-30'
      },
      {
        id: 3,
        name: 'حملة التسويق الرقمي',
        status: 'completed',
        progress: 100,
        start_date: '2023-12-01',
        end_date: '2024-01-10'
      }
    ],
    invoices: [
      {
        id: 1,
        invoice_number: 'INV-2024-001',
        total_amount: 15000,
        status: 'pending',
        due_date: '2024-01-20',
        created_at: '2024-01-05'
      },
      {
        id: 2,
        invoice_number: 'INV-2024-002',
        total_amount: 8000,
        status: 'paid',
        due_date: '2024-01-15',
        created_at: '2024-01-01'
      }
    ]
  }
};

const getStatusBadge = (status) => {
  const statusConfig = {
    completed: { label: 'مكتمل', className: 'status-completed' },
    in_progress: { label: 'قيد التنفيذ', className: 'status-in-progress' },
    planning: { label: 'التخطيط', className: 'status-pending' },
    paid: { label: 'مدفوع', className: 'status-paid' },
    pending: { label: 'معلق', className: 'status-unpaid' }
  };
  
  const config = statusConfig[status] || statusConfig.pending;
  return (
    <span className={`status-badge ${config.className}`}>
      {config.label}
    </span>
  );
};

export default function ClientDashboard() {
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    // محاكاة تحميل البيانات
    const timer = setTimeout(() => {
      setDashboardData(mockClientData);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(3)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="h-4 bg-gray-200 rounded w-24"></div>
                <div className="h-4 w-4 bg-gray-200 rounded"></div>
              </CardHeader>
              <CardContent>
                <div className="h-8 bg-gray-200 rounded w-16 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-12"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  const { client_info, stats, recent_data } = dashboardData;

  return (
    <div className="space-y-6">
      {/* ترحيب */}
      <div className="client-card p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              مرحباً، {client_info.name}
            </h1>
            <p className="text-gray-600">
              إليك نظرة عامة على مشاريعك وفواتيرك
            </p>
          </div>
          <div className="text-left">
            <p className="text-sm text-gray-500">آخر تحديث</p>
            <p className="text-sm font-medium">اليوم، 2:30 م</p>
          </div>
        </div>
      </div>

      {/* الإحصائيات الرئيسية */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="client-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              المشاريع
            </CardTitle>
            <FolderOpen className="h-5 w-5 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">{stats.projects.total}</div>
            <div className="flex items-center space-x-2 space-x-reverse text-sm text-gray-600 mt-2">
              <span>{stats.projects.active} نشط</span>
              <span>•</span>
              <span>{stats.projects.completed} مكتمل</span>
            </div>
          </CardContent>
        </Card>

        <Card className="client-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              المهام
            </CardTitle>
            <CheckSquare className="h-5 w-5 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">{stats.tasks.total}</div>
            <div className="mt-2">
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>معدل الإنجاز</span>
                <span>{stats.tasks.completion_rate}%</span>
              </div>
              <Progress value={stats.tasks.completion_rate} className="h-2" />
            </div>
          </CardContent>
        </Card>

        <Card className="client-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              الفواتير
            </CardTitle>
            <FileText className="h-5 w-5 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">₪{stats.invoices.total_amount.toLocaleString()}</div>
            <div className="flex items-center space-x-2 space-x-reverse text-sm text-gray-600 mt-2">
              <span className="text-green-600">₪{stats.invoices.paid_amount.toLocaleString()} مدفوع</span>
              <span>•</span>
              <span className="text-red-600">₪{stats.invoices.pending_amount.toLocaleString()} معلق</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* المشاريع الأخيرة */}
        <Card className="client-card">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>مشاريعي</span>
              <Button variant="outline" size="sm">
                عرض الكل
              </Button>
            </CardTitle>
            <CardDescription>
              آخر المشاريع والتقدم المحرز
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recent_data.projects.map((project) => (
                <div key={project.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-900">{project.name}</h4>
                    {getStatusBadge(project.status)}
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>التقدم</span>
                      <span>{project.progress}%</span>
                    </div>
                    <div className="progress-bar" style={{ width: `${project.progress}%` }}></div>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span className="flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {project.start_date}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {project.end_date}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* الفواتير الأخيرة */}
        <Card className="client-card">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>الفواتير</span>
              <Button variant="outline" size="sm">
                عرض الكل
              </Button>
            </CardTitle>
            <CardDescription>
              آخر الفواتير وحالة الدفع
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recent_data.invoices.map((invoice) => (
                <div key={invoice.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <h4 className="font-medium text-gray-900">{invoice.invoice_number}</h4>
                      <p className="text-sm text-gray-600">₪{invoice.total_amount.toLocaleString()}</p>
                    </div>
                    {getStatusBadge(invoice.status)}
                  </div>
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>تاريخ الاستحقاق: {invoice.due_date}</span>
                    <div className="flex gap-2">
                      <Button variant="ghost" size="sm" className="h-6 px-2">
                        <Download className="h-3 w-3" />
                      </Button>
                      {invoice.status === 'pending' && (
                        <Button variant="ghost" size="sm" className="h-6 px-2">
                          <Upload className="h-3 w-3" />
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* التنبيهات */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="border-orange-200 bg-orange-50 client-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-800">
              <AlertCircle className="h-5 w-5" />
              فواتير معلقة
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-orange-700 mb-4">
              لديك {stats.invoices.pending} فواتير معلقة بقيمة ₪{stats.invoices.pending_amount.toLocaleString()}
            </p>
            <Button variant="outline" size="sm" className="border-orange-300 text-orange-800 hover:bg-orange-100">
              عرض الفواتير
            </Button>
          </CardContent>
        </Card>

        <Card className="border-blue-200 bg-blue-50 client-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-blue-800">
              <TrendingUp className="h-5 w-5" />
              تقدم المشاريع
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-blue-700 mb-4">
              {stats.projects.active} مشاريع نشطة بمعدل إنجاز {stats.tasks.completion_rate}%
            </p>
            <Button variant="outline" size="sm" className="border-blue-300 text-blue-800 hover:bg-blue-100">
              عرض المشاريع
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

