'use client';

import { useEffect, useState, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Loader2, CheckCircle2, XCircle, Zap } from 'lucide-react';

import { useAuth } from '@/context/AuthContext';

interface PipelineStatus {
  job_id: string;
  status: string;
  current_stage: string;
  progress: number;
  completed_phases: string[];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  artifacts: Record<string, any>;
  message?: string;
}

interface ProgressTrackerProps {
  jobId: string;
  pollingIntervalMs?: number;
}

const PHASE_LABELS: Record<string, string> = {
  upload: 'Upload',
  validation: 'Image Validation',
  analysis: 'Image Analysis',
  clahe: 'CLAHE Enhancement',
  caption_generation: 'Florence-2 Captioning',
  groundingdino_detection: 'GroundingDINO Detection',
  part_detection: 'Florence-2 Part Detection',
  segmentation: 'SAM2.1 Segmentation',
  background_removal: 'Background Removal',
  shape_generation: 'Hunyuan3D-2 Shape Generation',
  texture_generation: 'Hunyuan3D-2 Texture Generation',
  mesh_validation: 'Mesh Validation',
  pointcloud_generation: 'Point Cloud Generation',
  dbscan_segmentation: 'DBSCAN Segmentation',
};

const PHASE_ORDER = Object.keys(PHASE_LABELS);

export default function ProgressTracker({ jobId, pollingIntervalMs = 3000 }: ProgressTrackerProps) {
  const router = useRouter();
  const { session } = useAuth();
  const [status, setStatus] = useState<PipelineStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const hasRedirected = useRef(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

  const fetchStatus = useCallback(async () => {
    try {
      const headers: Record<string, string> = {};
      if (session?.access_token) {
        headers['Authorization'] = `Bearer ${session.access_token}`;
      }
      const response = await fetch(`${apiUrl}/pipeline/status/${jobId}`, { headers });
      if (!response.ok) {
        throw new Error('Failed to fetch pipeline status.');
      }
      const data: PipelineStatus = await response.json();
      setStatus(data);
      setError(null);

      // If completed, stop polling and redirect
      if ((data.status === 'completed' || data.progress >= 100) && !hasRedirected.current) {
        hasRedirected.current = true;
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
        setTimeout(() => {
          router.push(`/results/${jobId}`);
        }, 1200);
      }

      // If failed, stop polling
      if (data.status === 'failed') {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      }
    } catch (err) {
      console.error('Polling error:', err);
      setError('Unable to reach the backend. Retrying...');
    }
  }, [apiUrl, jobId, router]);

  useEffect(() => {
    // Initial fetch
    fetchStatus();

    // Start polling
    intervalRef.current = setInterval(fetchStatus, pollingIntervalMs);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [fetchStatus, pollingIntervalMs]);

  const progress = status?.progress ?? 0;
  const currentStage = status?.current_stage ?? 'Initializing Pipeline';
  const pipelineStatus = status?.status ?? 'running';
  const completedPhases = status?.completed_phases ?? [];

  const isFailed = pipelineStatus === 'failed';
  const isComplete = pipelineStatus === 'completed' || progress >= 100;

  return (
    <div className="w-full max-w-lg mx-auto z-10">
      {/* Main Progress Card */}
      <div className="glass-card rounded-2xl p-8 mb-6 shadow-2xl">
        {/* Status Icon */}
        <div className="flex justify-center mb-6">
          {isFailed ? (
            <div className="w-16 h-16 rounded-full bg-rose-50 dark:bg-red-950/30 border border-rose-200 dark:border-red-900/40 flex items-center justify-center shadow-lg">
              <XCircle className="w-8 h-8 text-rose-600 dark:text-red-500" />
            </div>
          ) : isComplete ? (
            <div className="w-16 h-16 rounded-full bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900/40 flex items-center justify-center shadow-lg animate-pulse">
              <CheckCircle2 className="w-8 h-8 text-emerald-600 dark:text-emerald-400" />
            </div>
          ) : (
            <div className="w-16 h-16 rounded-full bg-indigo-50 dark:bg-blue-950/30 border border-indigo-200 dark:border-blue-900/40 flex items-center justify-center shadow-lg">
              <Loader2 className="w-8 h-8 text-indigo-600 dark:text-blue-400 animate-spin" />
            </div>
          )}
        </div>

        {/* Current Stage Label */}
        <div className="text-center mb-6">
          <p className="text-lg font-bold text-slate-900 dark:text-white mb-1">
            {isComplete ? 'Processing Complete' : isFailed ? 'Processing Failed' : currentStage}
          </p>
          <p className="text-xs text-slate-500">
            {isComplete
              ? 'Redirecting to results...'
              : isFailed
                ? (status?.message || 'An error occurred during processing.')
                : 'Do not close this tab.'}
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Progress</span>
            <span className={`text-sm font-extrabold ${
              isFailed ? 'text-rose-600 dark:text-red-400' : isComplete ? 'text-emerald-600 dark:text-emerald-400' : 'text-indigo-600 dark:text-blue-400'
            }`}>
              {progress}%
            </span>
          </div>
          <div className="w-full bg-slate-200 dark:bg-slate-950/60 h-2.5 rounded-full overflow-hidden border border-slate-300 dark:border-slate-900">
            <div
              className={`h-full transition-all duration-700 ease-out rounded-full ${
                isFailed
                  ? 'bg-rose-500'
                  : isComplete
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-400'
                    : 'bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500'
              }`}
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {error && (
          <p className="text-xs text-amber-600 dark:text-amber-400/80 text-center mt-3">{error}</p>
        )}
      </div>

      {/* Phase List */}
      <div className="glass-card rounded-2xl p-6 shadow-xl">
        <h3 className="text-xs uppercase tracking-wider font-bold text-slate-500 mb-4 flex items-center space-x-1.5 border-b border-slate-200 dark:border-slate-900/60 pb-3">
          <Zap size={12} className="text-indigo-600 dark:text-indigo-400 animate-pulse" />
          <span>Pipeline Stages</span>
        </h3>
        <div className="space-y-2">
          {PHASE_ORDER.map((phaseKey) => {
            const label = PHASE_LABELS[phaseKey];
            const isDone = completedPhases.includes(phaseKey);
            const isActive = !isDone && currentStage === label;

            return (
              <div
                key={phaseKey}
                className={`flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs transition-all ${
                  isDone
                    ? 'bg-emerald-50 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-400 border border-emerald-200/60 dark:border-emerald-900/30 font-medium'
                    : isActive
                      ? 'bg-indigo-50 dark:bg-blue-950/30 text-indigo-700 dark:text-blue-300 border border-indigo-200 dark:border-blue-900/30 font-semibold shadow-xs'
                      : 'text-slate-500 dark:text-slate-500'
                }`}
              >
                {isDone ? (
                  <CheckCircle2 size={14} className="flex-shrink-0 text-emerald-600 dark:text-emerald-400" />
                ) : isActive ? (
                  <Loader2 size={14} className="flex-shrink-0 animate-spin text-indigo-600 dark:text-blue-400" />
                ) : (
                  <div className="w-3.5 h-3.5 rounded-full border border-slate-300 dark:border-slate-700 flex-shrink-0" />
                )}
                <span>{label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
