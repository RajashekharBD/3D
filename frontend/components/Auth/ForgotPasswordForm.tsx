'use client';

import React, { useState } from 'react';
import { supabase } from '../utils/supabaseClient';
import Link from 'next/link';

export default function ForgotPasswordForm() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleResetRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/login`,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      setMessage('Password reset link has been sent to your email inbox.');
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md p-8 bg-slate-900/60 backdrop-blur-md rounded-2xl border border-slate-800 shadow-xl">
      <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400 mb-6 text-center">
        Reset Password
      </h2>
      <p className="text-slate-400 text-sm text-center mb-8">
        Enter your email address and we'll send you a link to reset your password.
      </p>

      {error && (
        <div className="p-4 mb-6 text-sm text-red-400 bg-red-950/40 border border-red-900/50 rounded-lg">
          {error}
        </div>
      )}

      {message && (
        <div className="p-4 mb-6 text-sm text-emerald-400 bg-emerald-950/40 border border-emerald-900/50 rounded-lg">
          {message}
        </div>
      )}

      <form onSubmit={handleResetRequest} className="space-y-6">
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

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 font-bold rounded-xl transition duration-200 disabled:opacity-50 text-sm"
        >
          {loading ? 'Sending link...' : 'Send Reset Link'}
        </button>
      </form>

      <div className="mt-8 text-center text-sm text-slate-400">
        Back to{' '}
        <Link href="/login" className="text-indigo-400 hover:underline font-medium">
          Log In
        </Link>
      </div>
    </div>
  );
}
