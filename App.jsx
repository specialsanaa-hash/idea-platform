import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import './App.css';

// إنشاء عميل React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={
            <Layout currentPage="لوحة التحكم">
              <Dashboard />
            </Layout>
          } />
          <Route path="/users" element={
            <Layout currentPage="المستخدمين">
              <div className="text-center py-12">
                <h2 className="text-2xl font-bold mb-4">صفحة المستخدمين</h2>
                <p className="text-muted-foreground">قيد التطوير...</p>
              </div>
            </Layout>
          } />
          <Route path="/clients" element={
            <Layout currentPage="العملاء">
              <div className="text-center py-12">
                <h2 className="text-2xl font-bold mb-4">صفحة العملاء</h2>
                <p className="text-muted-foreground">قيد التطوير...</p>
              </div>
            </Layout>
          } />
          <Route path="/projects" element={
            <Layout currentPage="المشاريع">
              <div className="text-center py-12">
                <h2 className="text-2xl font-bold mb-4">صفحة المشاريع</h2>
                <p className="text-muted-foreground">قيد التطوير...</p>
              </div>
            </Layout>
          } />
          <Route path="/tasks" element={
            <Layout currentPage="المهام">
              <div className="text-center py-12">
                <h2 className="text-2xl font-bold mb-4">صفحة المهام</h2>
                <p className="text-muted-foreground">قيد التطوير...</p>
              </div>
            </Layout>
          } />
          <Route path="/invoices" element={
            <Layout currentPage="الفواتير">
              <div className="text-center py-12">
                <h2 className="text-2xl font-bold mb-4">صفحة الفواتير</h2>
                <p className="text-muted-foreground">قيد التطوير...</p>
              </div>
            </Layout>
          } />
          <Route path="/settings" element={
            <Layout currentPage="الإعدادات">
              <div className="text-center py-12">
                <h2 className="text-2xl font-bold mb-4">صفحة الإعدادات</h2>
                <p className="text-muted-foreground">قيد التطوير...</p>
              </div>
            </Layout>
          } />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
