'use client';

import React from 'react';
import Link from 'next/link';
import { Play, Download, Trash2, CheckCircle, AlertTriangle, RefreshCw } from 'lucide-react';

export interface JobRecord {
  job_id: string;
  original_filename: string;
  status: 'uploaded' | 'processing' | 'completed' | 'failed';
  started_at: string;
  completed_at?: string;
  processing_duration_seconds?: number;
  model_generated: boolean;
  pointcloud_generated: boolean;
  error_message?: string;
}

interface HistoryCardProps {
  job: JobRecord;
  onDelete: (jobId: string) => void;
  token?: string;
}

export default function HistoryCard({ job, onDelete, token }: HistoryCardProps) {
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-emerald-400" />;
      case 'failed':
        return <AlertTriangle className="h-4 w-4 text-rose-400" />;
      default:
        return <RefreshCw className="h-4 w-4 text-indigo-400 animate-spin" />;
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-emerald-950/40 text-emerald-400 border-emerald-900/50';
      case 'failed':
        return 'bg-rose-950/40 text-rose-400 border-rose-900/50';
      default:
        return 'bg-indigo-950/40 text-indigo-400 border-indigo-900/50';
    }
  };

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${seconds.toFixed(0)}s`;
    return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  };

  // Construct absolute thumbnail URL pointing to backend local output static files if storage is disabled
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
  const thumbnailUrl = `${backendUrl}/outputs/${job.job_id}/original.png`;

  return (
    <div className="flex flex-col bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-2xl overflow-hidden hover:border-slate-700/80 transition duration-200 shadow-md">
      {/* Thumbnail */}
      <div className="relative h-44 bg-slate-950 flex items-center justify-center border-b border-slate-800">
        <img
          src={thumbnailUrl}
          alt={job.original_filename}
          className="w-full h-full object-cover opacity-80"
          onError={(e) => {
            // Placeholder fallback if image is missing or loading fails
            (e.target as HTMLImageElement).src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="%23334155" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>';
          }}
        />
        <div className="absolute top-3 right-3 flex items-center space-x-2">
          <span className={`flex items-center space-x-1.5 px-2.5 py-1 text-xs font-semibold rounded-full border ${getStatusBadgeClass(job.status)}`}>
            {getStatusIcon(job.status)}
            <span className="capitalize">{job.status}</span>
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-5 flex-grow flex flex-col justify-between space-y-4">
        <div>
          <h4 className="font-bold text-slate-100 truncate mb-1" title={job.original_filename}>
            {job.original_filename}
          </h4>
          <p className="text-xs text-slate-500">{formatDate(job.started_at)}</p>
        </div>

        <div className="grid grid-cols-2 gap-3 text-xs border-y border-slate-800/80 py-3 my-2">
          <div>
            <span className="block text-slate-500 mb-0.5">Duration</span>
            <span className="font-semibold text-slate-300">{formatDuration(job.processing_duration_seconds)}</span>
          </div>
          <div>
            <span className="block text-slate-500 mb-0.5">Outputs</span>
            <span className="font-semibold text-indigo-400">
              {job.model_generated ? 'Mesh' : ''}
              {job.model_generated && job.pointcloud_generated ? ' + ' : ''}
              {job.pointcloud_generated ? 'PC' : ''}
              {!job.model_generated && !job.pointcloud_generated ? 'None' : ''}
            </span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between space-x-2">
          {job.status === 'completed' ? (
            <Link
              href={`/results/${job.job_id}`}
              className="flex-grow flex items-center justify-center space-x-1.5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-slate-100 font-bold rounded-xl transition duration-150 text-xs"
            >
              <Play className="h-3.5 w-3.5 fill-current" />
              <span>View Results</span>
            </Link>
          ) : (
            <div className="flex-grow flex items-center justify-center py-2.5 bg-slate-800/40 text-slate-500 font-semibold rounded-xl text-xs border border-slate-800">
              {job.status === 'failed' ? 'Failed' : 'Processing...'}
            </div>
          )}

          {job.status === 'completed' && job.model_generated && (
            <a
              href={`${backendUrl}/api/v1/download/${job.job_id}/model`}
              headers={{ Authorization: `Bearer ${token}` }}
              onClick={async (e) => {
                e.preventDefault();
                // Custom fetch trigger to download with Authorization bearer token header
                try {
                  const res = await fetch(`${backendUrl}/api/v1/download/${job.job_id}/model`, {
                    headers: { Authorization: `Bearer ${token}` }
                  });
                  if (res.ok) {
                    const blob = await res.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${job.job_id}_model.glb`;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                  }
                } catch (err) {
                  console.error('Failed to download artifact:', err);
                }
              }}
              className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-slate-100 rounded-xl transition duration-150 border border-slate-700/50"
              title="Download GLB Model"
            >
              <Download className="h-4 w-4" />
            </a>
          )}

          <button
            onClick={() => onDelete(job.job_id)}
            className="p-2.5 bg-rose-950/20 hover:bg-rose-900/30 text-rose-400 hover:text-rose-300 rounded-xl transition duration-150 border border-rose-900/30 hover:border-rose-900/60"
            title="Delete History"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
