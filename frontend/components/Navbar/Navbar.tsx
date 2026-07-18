'use client';

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="w-full bg-slate-900 border-b border-slate-800 text-white py-4 px-6 md:px-12 flex items-center justify-between">
      <div className="flex items-center space-x-2">
        <Link href="/" className="text-xl font-bold tracking-tight bg-gradient-to-r from-blue-500 to-indigo-500 bg-clip-text text-transparent hover:opacity-90 transition-opacity">
          SingleImage3D
        </Link>
      </div>
      <div className="flex items-center space-x-6">
        <Link href="/" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
          Home
        </Link>
        {user ? (
          <>
            <Link href="/history" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
              History
            </Link>
            <Link href="/profile" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
              Profile
            </Link>
            <button
              onClick={logout}
              className="text-sm font-medium text-red-400 hover:text-red-300 transition-colors cursor-pointer bg-transparent border-none"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link href="/login" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
              Login
            </Link>
            <Link href="/signup" className="text-sm font-medium px-4 py-2 bg-indigo-600 hover:bg-indigo-700 font-bold rounded-xl transition duration-150 text-white">
              Signup
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
