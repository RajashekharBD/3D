'use client';

import React from 'react';

interface ProfileCardProps {
  email: string;
  createdAt: string;
  lastLogin?: string;
  logout: () => void;
}

export default function ProfileCard({ email, createdAt, lastLogin, logout }: ProfileCardProps) {
  const formatDate = (dateStr?: string) => {
    if (!dateStr || dateStr === 'now()') return 'N/A';
    return new Date(dateStr).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="flex flex-col p-6 bg-white/80 dark:bg-slate-900/40 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-2xl shadow-lg h-full justify-between space-y-6">
      <div className="space-y-4">
        <div className="flex items-center space-x-4">
          <div className="h-14 w-14 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-500 flex items-center justify-center font-black text-xl text-slate-950 shadow-md">
            {email.slice(0, 2).toUpperCase()}
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100 truncate max-w-[200px]" title={email}>
              {email}
            </h3>
            <p className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">User Profile</p>
          </div>
        </div>

        <hr className="border-slate-200 dark:border-slate-800" />

        <div className="space-y-3 text-sm">
          <div>
            <span className="block text-slate-500 text-xs">Account Created</span>
            <span className="font-semibold text-slate-700 dark:text-slate-300">{formatDate(createdAt)}</span>
          </div>

          {lastLogin && (
            <div>
              <span className="block text-slate-500 text-xs">Last Login</span>
              <span className="font-semibold text-slate-700 dark:text-slate-300">{formatDate(lastLogin)}</span>
            </div>
          )}
        </div>
      </div>

      <button
        onClick={logout}
        className="w-full py-3 bg-rose-50 dark:bg-red-950/20 hover:bg-rose-100 dark:hover:bg-red-900/30 border border-rose-200 dark:border-red-900/40 hover:border-rose-300 dark:hover:border-red-900/70 text-rose-600 dark:text-red-400 font-bold rounded-xl transition duration-200 text-sm shadow-xs cursor-pointer"
      >
        Log Out
      </button>
    </div>
  );
}
