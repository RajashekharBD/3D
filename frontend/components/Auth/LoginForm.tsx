'use client';

import React, { useState } from 'react';
import { supabase } from '../../utils/supabaseClient';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get('redirectTo') || '/';

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      router.push(redirectTo);
    }
  };

  return (
    <div className="w-full max-w-md p-8 glass-card rounded-2xl shadow-xl">
      <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600 dark:from-indigo-400 dark:to-cyan-400 mb-6 text-center">
        Welcome Back
      </h2>
      <p className="text-slate-600 dark:text-slate-400 text-sm text-center mb-8">
        Log in to your account to generate and view 3D models.
      </p>

      {error && (
        <div className="p-4 mb-6 text-sm text-red-500 dark:text-red-400 bg-red-100 dark:bg-red-950/40 border border-red-200 dark:border-red-900/50 rounded-lg">
          {error}
        </div>
      )}

      <form onSubmit={handleLogin} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Email Address</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 bg-white/90 dark:bg-slate-950/80 border border-slate-300 dark:border-slate-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 text-slate-900 dark:text-slate-200 text-sm placeholder-slate-400"
            placeholder="you@example.com"
            required
          />
        </div>

        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">Password</label>
            <Link href="/forgot-password" className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline">
              Forgot Password?
            </Link>
          </div>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 bg-white/90 dark:bg-slate-950/80 border border-slate-300 dark:border-slate-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 text-slate-900 dark:text-slate-200 text-sm placeholder-slate-400"
            placeholder="••••••••"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="glow-btn w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl transition duration-200 disabled:opacity-50 text-sm shadow-md"
        >
          {loading ? 'Logging in...' : 'Log In'}
        </button>
      </form>

      <div className="mt-8 text-center text-sm text-slate-600 dark:text-slate-400">
        Don&apos;t have an account?{' '}
        <Link href="/signup" className="text-indigo-600 dark:text-indigo-400 hover:underline font-medium">
          Sign Up
        </Link>
      </div>
    </div>
  );
}
