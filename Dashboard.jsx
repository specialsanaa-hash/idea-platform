/**
 * صفحة لوحة التحكم الرئيسية
 */

import { useState, useEffect } from 'react';
import { 
  Users, 
  Building2, 
  FolderOpen, 
  CheckSquare, 
  TrendingUp, 
  Calendar,
  Clock,
  AlertCircle
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

// بيانات وهمية للإحصائيات
const statsData = [
  {
    title: 'إجمالي العملاء',
    value: '156',
    change: '+12%',
    changeType: 'positive',
    icon: Building2,
    color: 'bg-blue-500'
  },
  {
    title: 'المشاريع النشطة',
    value: '23',
    change: '+5%',
    changeType: 'positive',
    icon: FolderOpen,
    color: 'bg-green-500'
  },
  {
    title: 'المهام المعلقة',
    value: '47',
    change: '-8%',
    changeType: 'negative',
    icon: CheckSquare,
    color: 'bg-orange-500'
  },
  {
    title: 'الإيرادات الشهرية',
    value: '₪45,230',
    change: '+18%',
    changeType: 'positive',
    icon: TrendingUp,
    color: 'bg-purple-500'
  }
];

// بيانات المشاريع الشهرية
const monthlyProjectsData = [
  { month: 'يناير', projects: 12, completed: 8 },
  { month: 'فبراير', projects: 15, completed: 12 },
  { month: 'مارس', projects: 18, completed: 14 },
  { month: 'أبريل', projects: 22, completed: 18 },
  { month: 'مايو', projects: 25, completed: 20 },
  { month: 'يونيو', projects: 28, completed: 23 }
];

// بيانات حالة المشاريع
const projectStatusData = [
  { name: 'مكتملة', value: 45, color: '#10b981' },
  { name: 'قيد التنفيذ', value: 30, color: '#3b82f6' },
  { name: 'معلقة', value: 15, color: '#f59e0b' },
  { name: 'ملغاة', value: 10, color: '#ef4444' }
];

// المهام الأخيرة
const recentTasks = [
  {
    id: 1,
    title: 'تصميم واجهة المستخدم',
    project: 'موقع شركة التقنية',
    assignee: 'أحمد محمد',
    dueDate: '2024-01-15',
    status: 'in_progress',
    priority: 'high'
  },
  {
    id: 2,
    title: 'مراجعة المحتوى',
    project: 'حملة التسويق الرقمي',
    assignee: 'فاطمة أحمد',
    dueDate: '2024-01-12',
    status: 'pending',
    priority: 'medium'
  },
  {
    id: 3,
    title: 'اختبار الأداء',
    project: 'تطبيق الهاتف المحمول',
    assignee: 'محمد علي',
    dueDate: '2024-01-10',
    status: 'completed',
    priority: 'low'
  }
];

const getStatusBadge = (status) => {
  const statusConfig = {
    completed: { label: 'مكتملة', variant: 'default', className: 'bg-green-100 text-green-800' },
    in_progress: { label: 'قيد التنفيذ', variant: 'secondary', className: 'bg-blue-100 text-blue-800' },
    pending: { label: 'معلقة', variant: 'outline', className: 'bg-yellow-100 text-yellow-800' }
  };
  
  const config = statusConfig[status] || statusConfig.pending;
  return (
    <Badge variant={config.variant} className={config.className}>
      {config.label}
    </Badge>
  );
};

const getPriorityBadge = (priority) => {
  const priorityConfig = {
    high: { label: 'عالية', className: 'bg-red-100 text-red-800' },
    medium: { label: 'متوسطة', className: 'bg-yellow-100 text-yellow-800' },
    low: { label: 'منخفضة', className: 'bg-green-100 text-green-800' }
  };
  
  const config = priorityConfig[priority] || priorityConfig.medium;
  return (
    <Badge variant="outline" className={config.className}>
      {config.label}
    </Badge>
  );
};

export default function Dashboard() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // محاكاة تحميل البيانات
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="h-4 bg-muted rounded w-24"></div>
                <div className="h-4 w-4 bg-muted rounded"></div>
              </CardHeader>
              <CardContent>
                <div className="h-8 bg-muted rounded w-16 mb-2"></div>
                <div className="h-3 bg-muted rounded w-12"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* الإحصائيات الرئيسية */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statsData.map((stat, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${stat.color}`}>
                <stat.icon className="h-4 w-4 text-white" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className={`text-xs ${
                stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
              }`}>
                {stat.change} من الشهر الماضي
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* رسم بياني للمشاريع الشهرية */}
        <Card>
          <CardHeader>
            <CardTitle>المشاريع الشهرية</CardTitle>
            <CardDescription>
              مقارنة بين المشاريع الجديدة والمكتملة
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={monthlyProjectsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="projects" fill="var(--primary)" name="مشاريع جديدة" />
                <Bar dataKey="completed" fill="var(--accent)" name="مشاريع مكتملة" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* رسم دائري لحالة المشاريع */}
        <Card>
          <CardHeader>
            <CardTitle>حالة المشاريع</CardTitle>
            <CardDescription>
              توزيع المشاريع حسب الحالة
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={projectStatusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {projectStatusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* المهام الأخيرة */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>المهام الأخيرة</span>
            <Button variant="outline" size="sm">
              عرض الكل
            </Button>
          </CardTitle>
          <CardDescription>
            آخر المهام المضافة والمحدثة
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentTasks.map((task) => (
              <div key={task.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-medium">{task.title}</h4>
                    {getPriorityBadge(task.priority)}
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">{task.project}</p>
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Users className="h-3 w-3" />
                      {task.assignee}
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {task.dueDate}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {getStatusBadge(task.status)}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* التنبيهات والإشعارات */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="border-orange-200 bg-orange-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-800">
              <AlertCircle className="h-5 w-5" />
              مهام متأخرة
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-orange-700 mb-4">
              لديك 3 مهام متأخرة عن الموعد المحدد
            </p>
            <Button variant="outline" size="sm" className="border-orange-300 text-orange-800 hover:bg-orange-100">
              عرض المهام
            </Button>
          </CardContent>
        </Card>

        <Card className="border-blue-200 bg-blue-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-blue-800">
              <Clock className="h-5 w-5" />
              اجتماعات اليوم
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-blue-700 mb-4">
              لديك اجتماعان مجدولان لليوم
            </p>
            <Button variant="outline" size="sm" className="border-blue-300 text-blue-800 hover:bg-blue-100">
              عرض التقويم
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

