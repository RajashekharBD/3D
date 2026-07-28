import React from 'react';
import ProtectedRoute from '@/components/Auth/ProtectedRoute';
import HistoryGrid from '@/components/History/HistoryGrid';

export default function HistoryPage() {
  return (
    <ProtectedRoute>
      <div className="flex-grow p-8 max-w-7xl mx-auto w-full space-y-8">
        <div>
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-slate-100 mb-2">Processing History</h2>
          <p className="text-slate-600 dark:text-slate-400 text-sm">
            Manage your uploads and browse previously generated 3D models and point clouds.
          </p>
        </div>

        <HistoryGrid />
      </div>
    </ProtectedRoute>
  );
}
