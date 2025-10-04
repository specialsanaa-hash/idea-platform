/**
 * مكون التخطيط الأساسي لبوابة العميل
 */

import { useState } from 'react';
import { 
  Home, 
  FolderOpen, 
  FileText, 
  MessageSquare, 
  LogOut,
  Menu,
  X,
  Bell,
  User
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

const sidebarItems = [
  {
    title: 'الرئيسية',
    icon: Home,
    href: '/',
    badge: null
  },
  {
    title: 'مشاريعي',
    icon: FolderOpen,
    href: '/projects',
    badge: '3'
  },
  {
    title: 'الفواتير',
    icon: FileText,
    href: '/invoices',
    badge: '2'
  },
  {
    title: 'التفاعلات',
    icon: MessageSquare,
    href: '/interactions',
    badge: null
  }
];

export default function ClientLayout({ children, currentPage = 'الرئيسية', clientInfo = null }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    // منطق تسجيل الخروج
    console.log('تسجيل الخروج');
  };

  return (
    <div className="min-h-screen client-portal arabic-text">
      {/* الشريط الجانبي */}
      <div className={`fixed inset-y-0 right-0 z-50 w-64 bg-white border-l border-gray-200 transform transition-transform duration-300 ease-in-out ${
        sidebarOpen ? 'translate-x-0' : 'translate-x-full'
      } lg:translate-x-0 lg:static lg:inset-0`}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
          <div className="flex items-center space-x-3 space-x-reverse">
            <div className="w-8 h-8 bg-idea-blue rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">أ</span>
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900">أيديا</h1>
              <p className="text-xs text-gray-500">بوابة العميل</p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        <nav className="mt-6 px-3">
          <ul className="space-y-2">
            {sidebarItems.map((item) => (
              <li key={item.href}>
                <a
                  href={item.href}
                  className={`flex items-center justify-between px-3 py-3 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50 hover:text-blue-700 ${
                    currentPage === item.title
                      ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-600'
                  }`}
                >
                  <div className="flex items-center space-x-3 space-x-reverse">
                    <item.icon className="h-5 w-5" />
                    <span>{item.title}</span>
                  </div>
                  {item.badge && (
                    <Badge variant="secondary" className="bg-blue-100 text-blue-700 text-xs">
                      {item.badge}
                    </Badge>
                  )}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* معلومات العميل */}
        {clientInfo && (
          <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center space-x-3 space-x-reverse">
              <Avatar className="h-10 w-10">
                <AvatarImage src={clientInfo.avatar} alt={clientInfo.name} />
                <AvatarFallback className="bg-blue-100 text-blue-700">
                  {clientInfo.name?.charAt(0) || 'ع'}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {clientInfo.name || 'عميل أيديا'}
                </p>
                <p className="text-xs text-gray-500 truncate">
                  {clientInfo.email || 'client@idea.com'}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* المحتوى الرئيسي */}
      <div className="lg:mr-64">
        {/* الشريط العلوي */}
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
          <div className="flex items-center space-x-4 space-x-reverse">
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-4 w-4" />
            </Button>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">{currentPage}</h2>
              <p className="text-sm text-gray-500">مرحباً بك في بوابة العميل</p>
            </div>
          </div>

          <div className="flex items-center space-x-4 space-x-reverse">
            {/* الإشعارات */}
            <Button variant="ghost" size="sm" className="relative">
              <Bell className="h-5 w-5 text-gray-600" />
              <Badge className="absolute -top-1 -left-1 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs bg-red-500">
                2
              </Badge>
            </Button>

            {/* ملف المستخدم */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={clientInfo?.avatar} alt="العميل" />
                    <AvatarFallback className="bg-blue-100 text-blue-700">
                      {clientInfo?.name?.charAt(0) || 'ع'}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">
                      {clientInfo?.name || 'عميل أيديا'}
                    </p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {clientInfo?.email || 'client@idea.com'}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <User className="ml-2 h-4 w-4" />
                  الملف الشخصي
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="text-red-600">
                  <LogOut className="ml-2 h-4 w-4" />
                  تسجيل الخروج
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* المحتوى */}
        <main className="p-6">
          {children}
        </main>
      </div>

      {/* خلفية الشريط الجانبي للهواتف */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}

