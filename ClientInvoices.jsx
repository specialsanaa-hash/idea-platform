/**
 * صفحة فواتير العميل
 */

import { useState, useEffect } from 'react';
import { 
  FileText, 
  Download, 
  Upload, 
  Calendar, 
  DollarSign,
  AlertCircle,
  CheckCircle,
  Clock,
  Eye
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

// بيانات وهمية للفواتير
const mockInvoices = [
  {
    id: 1,
    invoice_number: 'INV-2024-001',
    total_amount: 15000,
    status: 'pending',
    due_date: '2024-01-20',
    created_at: '2024-01-05',
    project_name: 'موقع الشركة الجديد',
    description: 'الدفعة الأولى لتطوير الموقع',
    payment_proof: null
  },
  {
    id: 2,
    invoice_number: 'INV-2024-002',
    total_amount: 8000,
    status: 'paid',
    due_date: '2024-01-15',
    created_at: '2024-01-01',
    project_name: 'حملة التسويق الرقمي',
    description: 'دفعة كاملة للحملة التسويقية',
    payment_proof: 'payment_proof_2.pdf',
    paid_at: '2024-01-12'
  },
  {
    id: 3,
    invoice_number: 'INV-2024-003',
    total_amount: 22000,
    status: 'pending_verification',
    due_date: '2024-01-25',
    created_at: '2024-01-10',
    project_name: 'تطبيق الهاتف المحمول',
    description: 'الدفعة الأولى لتطوير التطبيق',
    payment_proof: 'payment_proof_3.pdf',
    payment_proof_uploaded_at: '2024-01-18'
  },
  {
    id: 4,
    invoice_number: 'INV-2023-045',
    total_amount: 5000,
    status: 'overdue',
    due_date: '2023-12-30',
    created_at: '2023-12-15',
    project_name: 'استشارات تقنية',
    description: 'استشارات تقنية للربع الأخير',
    payment_proof: null
  }
];

const getStatusBadge = (status) => {
  const statusConfig = {
    paid: { 
      label: 'مدفوع', 
      className: 'status-paid',
      icon: CheckCircle
    },
    pending: { 
      label: 'معلق', 
      className: 'status-pending',
      icon: Clock
    },
    pending_verification: { 
      label: 'قيد التحقق', 
      className: 'status-in-progress',
      icon: Clock
    },
    overdue: { 
      label: 'متأخر', 
      className: 'status-unpaid',
      icon: AlertCircle
    }
  };
  
  const config = statusConfig[status] || statusConfig.pending;
  const IconComponent = config.icon;
  
  return (
    <span className={`status-badge ${config.className} flex items-center gap-1`}>
      <IconComponent className="h-3 w-3" />
      {config.label}
    </span>
  );
};

function InvoiceCard({ invoice }) {
  const [uploadDialog, setUploadDialog] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileUpload = () => {
    if (selectedFile) {
      console.log('Uploading payment proof:', selectedFile);
      setUploadDialog(false);
      setSelectedFile(null);
    }
  };

  const isOverdue = invoice.status === 'overdue' || 
    (invoice.status === 'pending' && new Date(invoice.due_date) < new Date());

  return (
    <Card className={`client-card ${isOverdue ? 'border-red-200' : ''}`}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg mb-1">{invoice.invoice_number}</CardTitle>
            <CardDescription className="text-sm text-gray-600 mb-2">
              {invoice.project_name}
            </CardDescription>
            <p className="text-sm text-gray-500 mb-3">{invoice.description}</p>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                تاريخ الإنشاء: {invoice.created_at}
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                تاريخ الاستحقاق: {invoice.due_date}
              </span>
            </div>
          </div>
          <div className="flex flex-col items-end gap-2">
            {getStatusBadge(invoice.status)}
            <div className="text-left">
              <p className="text-2xl font-bold text-gray-900">
                ₪{invoice.total_amount.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between pt-2 border-t">
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Eye className="h-4 w-4 ml-1" />
              عرض التفاصيل
            </Button>
            <Button variant="outline" size="sm">
              <Download className="h-4 w-4 ml-1" />
              تحميل PDF
            </Button>
          </div>

          <div className="flex gap-2">
            {invoice.payment_proof && (
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 ml-1" />
                سند التحويل
              </Button>
            )}
            
            {(invoice.status === 'pending' || invoice.status === 'overdue') && (
              <Dialog open={uploadDialog} onOpenChange={setUploadDialog}>
                <DialogTrigger asChild>
                  <Button 
                    variant="default" 
                    size="sm" 
                    className={isOverdue ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'}
                  >
                    <Upload className="h-4 w-4 ml-1" />
                    رفع سند التحويل
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-md">
                  <DialogHeader>
                    <DialogTitle>رفع سند التحويل</DialogTitle>
                    <DialogDescription>
                      يرجى رفع سند التحويل للفاتورة {invoice.invoice_number}
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="payment-proof">ملف سند التحويل</Label>
                      <Input
                        id="payment-proof"
                        type="file"
                        accept=".pdf,.jpg,.jpeg,.png"
                        onChange={(e) => setSelectedFile(e.target.files[0])}
                        className="mt-1"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        الملفات المدعومة: PDF, JPG, PNG (حد أقصى 5MB)
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        onClick={handleFileUpload}
                        disabled={!selectedFile}
                        className="flex-1"
                      >
                        رفع الملف
                      </Button>
                      <Button 
                        variant="outline"
                        onClick={() => setUploadDialog(false)}
                        className="flex-1"
                      >
                        إلغاء
                      </Button>
                    </div>
                  </div>
                </DialogContent>
              </Dialog>
            )}
          </div>
        </div>

        {invoice.status === 'pending_verification' && (
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center gap-2 text-blue-800">
              <Clock className="h-4 w-4" />
              <span className="text-sm font-medium">قيد المراجعة</span>
            </div>
            <p className="text-xs text-blue-700 mt-1">
              تم رفع سند التحويل في {invoice.payment_proof_uploaded_at} وهو قيد المراجعة من قبل الفريق
            </p>
          </div>
        )}

        {invoice.status === 'paid' && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center gap-2 text-green-800">
              <CheckCircle className="h-4 w-4" />
              <span className="text-sm font-medium">تم الدفع</span>
            </div>
            <p className="text-xs text-green-700 mt-1">
              تم تأكيد الدفع في {invoice.paid_at}
            </p>
          </div>
        )}

        {isOverdue && invoice.status !== 'paid' && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center gap-2 text-red-800">
              <AlertCircle className="h-4 w-4" />
              <span className="text-sm font-medium">فاتورة متأخرة</span>
            </div>
            <p className="text-xs text-red-700 mt-1">
              هذه الفاتورة متأخرة عن تاريخ الاستحقاق. يرجى الدفع في أقرب وقت ممكن.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function ClientInvoices() {
  const [loading, setLoading] = useState(true);
  const [invoices, setInvoices] = useState([]);
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    // محاكاة تحميل البيانات
    const timer = setTimeout(() => {
      setInvoices(mockInvoices);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const filteredInvoices = invoices.filter(invoice => {
    if (activeTab === 'all') return true;
    if (activeTab === 'pending') return ['pending', 'pending_verification', 'overdue'].includes(invoice.status);
    if (activeTab === 'paid') return invoice.status === 'paid';
    return true;
  });

  // حساب الإحصائيات
  const stats = {
    total: invoices.reduce((sum, inv) => sum + inv.total_amount, 0),
    paid: invoices.filter(inv => inv.status === 'paid').reduce((sum, inv) => sum + inv.total_amount, 0),
    pending: invoices.filter(inv => ['pending', 'pending_verification', 'overdue'].includes(inv.status)).reduce((sum, inv) => sum + inv.total_amount, 0),
    overdue: invoices.filter(inv => inv.status === 'overdue').length
  };

  if (loading) {
    return (
      <div className="space-y-6">
        {[...Array(3)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader>
              <div className="h-6 bg-gray-200 rounded w-1/4 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3 mb-4"></div>
              <div className="flex gap-4">
                <div className="h-4 bg-gray-200 rounded w-32"></div>
                <div className="h-4 bg-gray-200 rounded w-32"></div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-8 bg-gray-200 rounded w-full"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* الإحصائيات السريعة */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="client-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">إجمالي الفواتير</p>
                <p className="text-2xl font-bold text-gray-900">₪{stats.total.toLocaleString()}</p>
              </div>
              <FileText className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="client-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">المبلغ المدفوع</p>
                <p className="text-2xl font-bold text-green-600">₪{stats.paid.toLocaleString()}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="client-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">المبلغ المعلق</p>
                <p className="text-2xl font-bold text-orange-600">₪{stats.pending.toLocaleString()}</p>
              </div>
              <Clock className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="client-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">فواتير متأخرة</p>
                <p className="text-2xl font-bold text-red-600">{stats.overdue}</p>
              </div>
              <AlertCircle className="h-8 w-8 text-red-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* تنبيه الفواتير المتأخرة */}
      {stats.overdue > 0 && (
        <Card className="border-red-200 bg-red-50 client-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-800">
              <AlertCircle className="h-5 w-5" />
              تنبيه: فواتير متأخرة
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-700">
              لديك {stats.overdue} فاتورة متأخرة عن تاريخ الاستحقاق. يرجى المراجعة والدفع في أقرب وقت ممكن.
            </p>
          </CardContent>
        </Card>
      )}

      {/* تبويبات الفواتير */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="all">جميع الفواتير</TabsTrigger>
          <TabsTrigger value="pending">الفواتير المعلقة</TabsTrigger>
          <TabsTrigger value="paid">الفواتير المدفوعة</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab} className="mt-6">
          <div className="space-y-4">
            {filteredInvoices.length > 0 ? (
              filteredInvoices.map((invoice) => (
                <InvoiceCard key={invoice.id} invoice={invoice} />
              ))
            ) : (
              <Card className="client-card">
                <CardContent className="p-12 text-center">
                  <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    لا توجد فواتير
                  </h3>
                  <p className="text-gray-600">
                    لا توجد فواتير في هذه الفئة حالياً
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

