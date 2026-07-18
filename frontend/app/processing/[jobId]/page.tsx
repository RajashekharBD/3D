'use client';

import { useParams } from 'next/navigation';
import ProgressTracker from '../../../components/Progress/ProgressTracker';

import ProtectedRoute from '@/components/Auth/ProtectedRoute';

export default function ProcessingPage() {
  const { jobId } = useParams() as { jobId: string };

  return (
    <ProtectedRoute>
      <div className="flex flex-col items-center justify-center py-16 px-6 flex-grow w-full">
        <h1 className="text-3xl font-bold mb-2 tracking-tight text-white">Processing Asset</h1>
        <p className="text-sm text-slate-400 mb-10">Job ID: {jobId}</p>

        <ProgressTracker jobId={jobId} pollingIntervalMs={3000} />
      </div>
    </ProtectedRoute>
  );
}
