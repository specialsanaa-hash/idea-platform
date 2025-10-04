/**
 * مكون التخطيط الأساسي للوحة التحكم
 */

import { useState } from 'react';
import { 
  LayoutDashboard, 
  Users, 
  Building2, 
  FolderOpen, 
  CheckSquare, 
  FileText, 
  Settings, 
  LogOut,
  Menu,
  X,
  Bell,
  Search
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
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
import './Layout.css';

const sidebarItems = [
  {
    title: 'لوحة التحكم',
    icon: LayoutDashboard,
    href: '/',
    badge: null
  },
  {
    title: 'المستخدمين',
    icon: Users,
    href: '/users',
    badge: null
  },
  {
    title: 'العملاء',
    icon: Building2,
    href: '/clients',
    badge: null
  },
  {
    title: 'المشاريع',
    icon: FolderOpen,
    href: '/projects',
    badge: '12'
  },
  {
    title: 'المهام',
    icon: CheckSquare,
    href: '/tasks',
    badge: '8'
  },
  {
    title: 'الفواتير',
    icon: FileText,
    href: '/invoices',
    badge: null
  },
  {
    title: 'الإعدادات',
    icon: Settings,
    href: '/settings',
    badge: null
  }
];

export default function Layout({ children, currentPage = 'لوحة التحكم' }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    // منطق تسجيل الخروج
    console.log('تسجيل الخروج');
  };

  return (
    <div className="min-h-screen bg-background arabic-text">
      {/* الشريط الجانبي */}
      <div className={`fixed inset-y-0 right-0 z-50 w-64 bg-card border-l border-border transform transition-transform duration-300 ease-in-out ${
        sidebarOpen ? 'translate-x-0' : 'translate-x-full'
      } lg:translate-x-0 lg:static lg:inset-0`}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-border">
          <div className="flex items-center space-x-3 space-x-reverse">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">أ</span>
            </div>
            <div>
              <h1 className="text-lg font-bold text-foreground">أيديا</h1>
              <p className="text-xs text-muted-foreground">لوحة التحكم</p>
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
                  className={`flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground ${
                    currentPage === item.title
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground'
                  }`}
                >
                  <div className="flex items-center space-x-3 space-x-reverse">
                    <item.icon className="h-4 w-4" />
                    <span>{item.title}</span>
                  </div>
                  {item.badge && (
                    <Badge variant="secondary" className="text-xs">
                      {item.badge}
                    </Badge>
                  )}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-3">
          <Button
            variant="ghost"
            className="w-full justify-start text-muted-foreground hover:text-foreground"
            onClick={handleLogout}
          >
            <LogOut className="h-4 w-4 ml-2" />
            تسجيل الخروج
          </Button>
        </div>
      </div>

      {/* المحتوى الرئيسي */}
      <div className="lg:mr-64">
        {/* الشريط العلوي */}
        <header className="h-16 bg-card border-b border-border flex items-center justify-between px-6">
          <div className="flex items-center space-x-4 space-x-reverse">
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-4 w-4" />
            </Button>
            <h2 className="text-xl font-semibold text-foreground">{currentPage}</h2>
          </div>

          <div className="flex items-center space-x-4 space-x-reverse">
            {/* شريط البحث */}
            <div className="relative hidden md:block">
              <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="البحث..."
                className="w-64 pr-10"
              />
            </div>

            {/* الإشعارات */}
            <Button variant="ghost" size="sm" className="relative">
              <Bell className="h-4 w-4" />
              <Badge className="absolute -top-1 -left-1 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs">
                3
              </Badge>
            </Button>

            {/* ملف المستخدم */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src="/avatars/01.png" alt="المستخدم" />
                    <AvatarFallback>أح</AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">أحمد محمد</p>
                    <p className="text-xs leading-none text-muted-foreground">
                      ahmed@idea.com
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  الملف الشخصي
                </DropdownMenuItem>
                <DropdownMenuItem>
                  الإعدادات
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout}>
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

