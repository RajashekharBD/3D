'use client';

import React, { useState } from 'react';
import { supabase } from '../../utils/supabaseClient';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function SignupForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      if (data.session) {
        router.push('/');
      } else {
        setSuccess(true);
        setLoading(false);
      }
    }
  };

  return (
    <div className="w-full max-w-md p-8 bg-slate-900/60 backdrop-blur-md rounded-2xl border border-slate-800 shadow-xl">
      <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400 mb-6 text-center">
        Create Account
      </h2>
      <p className="text-slate-400 text-sm text-center mb-8">
        Sign up to start transforming single images into detailed 3D models.
      </p>

      {error && (
        <div className="p-4 mb-6 text-sm text-red-400 bg-red-950/40 border border-red-900/50 rounded-lg">
          {error}
        </div>
      )}

      {success ? (
        <div className="p-6 text-center bg-emerald-950/30 border border-emerald-800/50 rounded-xl space-y-4">
          <p className="text-emerald-400 font-semibold text-base">Signup Successful!</p>
          <p className="text-slate-300 text-sm leading-relaxed">
            Please check your email inbox to confirm your account and activate your profile.
          </p>
          <Link
            href="/login"
            className="inline-block mt-4 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-slate-100 font-medium rounded-xl transition duration-200 text-sm"
          >
            Go to Login
          </Link>
        </div>
      ) : (
        <form onSubmit={handleSignup} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 text-slate-200 text-sm"
              placeholder="you@example.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 text-slate-200 text-sm"
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 font-bold rounded-xl transition duration-200 disabled:opacity-50 text-sm"
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>
      )}

      {!success && (
        <div className="mt-8 text-center text-sm text-slate-400">
          Already have an account?{' '}
          <Link href="/login" className="text-indigo-400 hover:underline font-medium">
            Log In
          </Link>
        </div>
      )}
    </div>
  );
}
