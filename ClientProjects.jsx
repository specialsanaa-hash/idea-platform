/**
 * صفحة مشاريع العميل
 */

import { useState, useEffect } from 'react';
import { 
  FolderOpen, 
  Calendar, 
  Clock, 
  Users, 
  CheckSquare,
  Eye,
  MessageSquare,
  ThumbsUp,
  ThumbsDown,
  RotateCcw
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog';
import { Textarea } from '@/components/ui/textarea';

// بيانات وهمية للمشاريع
const mockProjects = [
  {
    id: 1,
    name: 'موقع الشركة الجديد',
    description: 'تطوير موقع إلكتروني متجاوب وحديث للشركة',
    status: 'in_progress',
    progress: 75,
    start_date: '2024-01-01',
    end_date: '2024-02-15',
    budget: 25000,
    project_manager: 'أحمد محمد',
    tasks_count: 12,
    completed_tasks: 9,
    files_pending_approval: true
  },
  {
    id: 2,
    name: 'تطبيق الهاتف المحمول',
    description: 'تطوير تطبيق iOS و Android للشركة',
    status: 'planning',
    progress: 25,
    start_date: '2024-01-15',
    end_date: '2024-03-30',
    budget: 45000,
    project_manager: 'فاطمة أحمد',
    tasks_count: 20,
    completed_tasks: 5,
    files_pending_approval: false
  },
  {
    id: 3,
    name: 'حملة التسويق الرقمي',
    description: 'حملة تسويقية شاملة عبر وسائل التواصل الاجتماعي',
    status: 'completed',
    progress: 100,
    start_date: '2023-12-01',
    end_date: '2024-01-10',
    budget: 15000,
    project_manager: 'محمد علي',
    tasks_count: 8,
    completed_tasks: 8,
    files_pending_approval: false
  }
];

const getStatusBadge = (status) => {
  const statusConfig = {
    completed: { label: 'مكتمل', className: 'status-completed' },
    in_progress: { label: 'قيد التنفيذ', className: 'status-in-progress' },
    planning: { label: 'التخطيط', className: 'status-pending' },
    on_hold: { label: 'معلق', className: 'status-unpaid' }
  };
  
  const config = statusConfig[status] || statusConfig.planning;
  return (
    <span className={`status-badge ${config.className}`}>
      {config.label}
    </span>
  );
};

function ProjectCard({ project }) {
  const [approvalDialog, setApprovalDialog] = useState(false);
  const [approvalComments, setApprovalComments] = useState('');

  const handleFileApproval = (status) => {
    console.log(`File approval: ${status}`, { comments: approvalComments });
    setApprovalDialog(false);
    setApprovalComments('');
  };

  return (
    <Card className="client-card">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg mb-2">{project.name}</CardTitle>
            <CardDescription className="text-sm text-gray-600 mb-3">
              {project.description}
            </CardDescription>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span className="flex items-center gap-1">
                <Users className="h-4 w-4" />
                {project.project_manager}
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                {project.start_date}
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                {project.end_date}
              </span>
            </div>
          </div>
          <div className="flex flex-col items-end gap-2">
            {getStatusBadge(project.status)}
            {project.files_pending_approval && (
              <Badge variant="outline" className="bg-yellow-50 text-yellow-700 border-yellow-200">
                ملفات تحتاج موافقة
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* التقدم */}
          <div>
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>التقدم العام</span>
              <span>{project.progress}%</span>
            </div>
            <Progress value={project.progress} className="h-2" />
          </div>

          {/* المهام */}
          <div className="flex items-center justify-between text-sm">
            <span className="flex items-center gap-1 text-gray-600">
              <CheckSquare className="h-4 w-4" />
              المهام: {project.completed_tasks}/{project.tasks_count}
            </span>
            <span className="text-gray-600">
              الميزانية: ₪{project.budget.toLocaleString()}
            </span>
          </div>

          {/* الإجراءات */}
          <div className="flex items-center justify-between pt-2 border-t">
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Eye className="h-4 w-4 ml-1" />
                عرض التفاصيل
              </Button>
              <Button variant="outline" size="sm">
                <MessageSquare className="h-4 w-4 ml-1" />
                التفاعلات
              </Button>
            </div>

            {project.files_pending_approval && (
              <Dialog open={approvalDialog} onOpenChange={setApprovalDialog}>
                <DialogTrigger asChild>
                  <Button variant="default" size="sm" className="bg-blue-600 hover:bg-blue-700">
                    مراجعة الملفات
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-md">
                  <DialogHeader>
                    <DialogTitle>مراجعة ملفات المشروع</DialogTitle>
                    <DialogDescription>
                      يرجى مراجعة الملفات المرسلة وإبداء رأيك
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm font-medium">التعليقات (اختياري)</label>
                      <Textarea
                        placeholder="أضف تعليقاتك هنا..."
                        value={approvalComments}
                        onChange={(e) => setApprovalComments(e.target.value)}
                        className="mt-1"
                      />
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        onClick={() => handleFileApproval('approved')}
                        className="flex-1 bg-green-600 hover:bg-green-700"
                      >
                        <ThumbsUp className="h-4 w-4 ml-1" />
                        موافق
                      </Button>
                      <Button 
                        onClick={() => handleFileApproval('needs_revision')}
                        variant="outline"
                        className="flex-1"
                      >
                        <RotateCcw className="h-4 w-4 ml-1" />
                        يحتاج تعديل
                      </Button>
                      <Button 
                        onClick={() => handleFileApproval('rejected')}
                        variant="destructive"
                        className="flex-1"
                      >
                        <ThumbsDown className="h-4 w-4 ml-1" />
                        رفض
                      </Button>
                    </div>
                  </div>
                </DialogContent>
              </Dialog>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default function ClientProjects() {
  const [loading, setLoading] = useState(true);
  const [projects, setProjects] = useState([]);
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    // محاكاة تحميل البيانات
    const timer = setTimeout(() => {
      setProjects(mockProjects);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const filteredProjects = projects.filter(project => {
    if (activeTab === 'all') return true;
    if (activeTab === 'active') return ['in_progress', 'planning'].includes(project.status);
    if (activeTab === 'completed') return project.status === 'completed';
    return true;
  });

  if (loading) {
    return (
      <div className="space-y-6">
        {[...Array(3)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader>
              <div className="h-6 bg-gray-200 rounded w-1/3 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3 mb-4"></div>
              <div className="flex gap-4">
                <div className="h-4 bg-gray-200 rounded w-24"></div>
                <div className="h-4 bg-gray-200 rounded w-24"></div>
                <div className="h-4 bg-gray-200 rounded w-24"></div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-2 bg-gray-200 rounded w-full mb-4"></div>
              <div className="flex justify-between">
                <div className="h-4 bg-gray-200 rounded w-32"></div>
                <div className="h-4 bg-gray-200 rounded w-24"></div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* الإحصائيات السريعة */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="client-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">إجمالي المشاريع</p>
                <p className="text-2xl font-bold text-gray-900">{projects.length}</p>
              </div>
              <FolderOpen className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="client-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">المشاريع النشطة</p>
                <p className="text-2xl font-bold text-gray-900">
                  {projects.filter(p => ['in_progress', 'planning'].includes(p.status)).length}
                </p>
              </div>
              <Clock className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="client-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">المشاريع المكتملة</p>
                <p className="text-2xl font-bold text-gray-900">
                  {projects.filter(p => p.status === 'completed').length}
                </p>
              </div>
              <CheckSquare className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* تبويبات المشاريع */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="all">جميع المشاريع</TabsTrigger>
          <TabsTrigger value="active">المشاريع النشطة</TabsTrigger>
          <TabsTrigger value="completed">المشاريع المكتملة</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab} className="mt-6">
          <div className="space-y-4">
            {filteredProjects.length > 0 ? (
              filteredProjects.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))
            ) : (
              <Card className="client-card">
                <CardContent className="p-12 text-center">
                  <FolderOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    لا توجد مشاريع
                  </h3>
                  <p className="text-gray-600">
                    لا توجد مشاريع في هذه الفئة حالياً
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

