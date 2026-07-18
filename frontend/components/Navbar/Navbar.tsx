'use client';

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { usePathname } from 'next/navigation';
import { Layers, History, User, LogOut } from 'lucide-react';

export default function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="sticky top-0 z-50 w-full glass-panel border-b border-slate-900/60 text-white py-4 px-6 md:px-12 flex items-center justify-between">
      <div className="flex items-center space-x-2">
        <Link href="/" className="flex items-center space-x-2 text-xl font-bold tracking-tight bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 bg-clip-text text-transparent hover:opacity-90 transition-opacity">
          <Layers className="text-indigo-500" size={20} />
          <span>SingleImage3D</span>
        </Link>
      </div>
      <div className="flex items-center space-x-6">
        <Link 
          href="/" 
          className={`text-sm font-medium transition-colors ${
            isActive('/') ? 'text-blue-400 font-semibold' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Home
        </Link>
        {user ? (
          <>
            <Link 
              href="/history" 
              className={`flex items-center space-x-1 text-sm font-medium transition-colors ${
                isActive('/history') ? 'text-blue-400 font-semibold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <History size={14} />
              <span>History</span>
            </Link>
            <Link 
              href="/profile" 
              className={`flex items-center space-x-1 text-sm font-medium transition-colors ${
                isActive('/profile') ? 'text-blue-400 font-semibold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <User size={14} />
              <span>Profile</span>
            </Link>
            <button
              onClick={logout}
              className="flex items-center space-x-1 text-sm font-medium text-red-400 hover:text-red-300 transition-colors cursor-pointer bg-transparent border-none"
            >
              <LogOut size={14} />
              <span>Logout</span>
            </button>
          </>
        ) : (
          <>
            <Link 
              href="/login" 
              className={`text-sm font-medium transition-colors ${
                isActive('/login') ? 'text-blue-400 font-semibold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Login
            </Link>
            <Link 
              href="/signup" 
              className="glow-btn text-sm font-medium px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 font-bold rounded-xl transition-all text-white shadow-lg shadow-indigo-500/10"
            >
              Signup
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
