import React, { Suspense } from 'react';
import LoginForm from '@/components/Auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="flex-grow flex items-center justify-center p-6 bg-slate-950">
      <Suspense fallback={
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      }>
        <LoginForm />
      </Suspense>
    </div>
  );
}
