'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Play, Download, Trash2, CheckCircle, AlertTriangle, RefreshCw, Eye, X } from 'lucide-react';
import ThreeViewer from '../ThreeViewer';

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
  const [showPreview, setShowPreview] = useState(false);

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
        return <CheckCircle className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />;
      case 'failed':
        return <AlertTriangle className="h-4 w-4 text-rose-600 dark:text-rose-400" />;
      default:
        return <RefreshCw className="h-4 w-4 text-indigo-600 dark:text-indigo-400 animate-spin" />;
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-900/50';
      case 'failed':
        return 'bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-900/50';
      default:
        return 'bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-400 border-indigo-200 dark:border-indigo-900/50';
    }
  };

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${seconds.toFixed(0)}s`;
    return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  };

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
  const thumbnailUrl = `${backendUrl}/outputs/${job.job_id}/original.png`;

  const getDisplayName = (filename: string, jobId: string) => {
    if (!filename) return `Asset_${jobId.slice(0, 8)}`;
    if (filename.includes('_original.')) {
      const ext = filename.split('.').pop() || 'png';
      return `Uploaded Image (${jobId.slice(0, 8)}.${ext})`;
    }
    if (/^[0-9a-fA-F-]{36}$/.test(filename)) {
      return `Asset_${filename.slice(0, 8)}`;
    }
    return filename;
  };

  const displayName = getDisplayName(job.original_filename, job.job_id);

  return (
    <>
      <div className="flex flex-col bg-white/80 dark:bg-slate-900/40 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden hover:border-indigo-300 dark:hover:border-slate-700/80 transition duration-200 shadow-md hover:shadow-lg group">
        {/* Thumbnail */}
        <div className="relative h-44 bg-slate-100 dark:bg-slate-950 flex items-center justify-center border-b border-slate-200 dark:border-slate-800 overflow-hidden">
          <img
            src={thumbnailUrl}
            alt={displayName}
            className="w-full h-full object-cover opacity-90 dark:opacity-80 group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              (e.target as HTMLImageElement).src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>';
            }}
          />
          <div className="absolute top-3 right-3 flex items-center space-x-2 z-10">
            <span className={`flex items-center space-x-1.5 px-2.5 py-1 text-xs font-semibold rounded-full border ${getStatusBadgeClass(job.status)}`}>
              {getStatusIcon(job.status)}
              <span className="capitalize">{job.status}</span>
            </span>
          </div>

          {/* Quick Preview Hover Overlay */}
          {job.status === 'completed' && (
            <div className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center z-10">
              <button
                onClick={() => setShowPreview(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-white/90 dark:bg-slate-900/90 text-slate-800 dark:text-slate-100 font-bold rounded-xl text-xs backdrop-blur-md shadow-lg hover:scale-105 transition-all cursor-pointer border border-slate-200 dark:border-slate-700"
              >
                <Eye className="h-4 w-4 text-indigo-600 dark:text-indigo-400" />
                <span>Quick Preview</span>
              </button>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-5 flex-grow flex flex-col justify-between space-y-4">
          <div>
            <h4 className="font-bold text-slate-800 dark:text-slate-100 truncate mb-1" title={displayName}>
              {displayName}
            </h4>
            <p className="text-xs text-slate-500">{formatDate(job.started_at)}</p>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs border-y border-slate-200/80 dark:border-slate-800/80 py-3 my-2">
            <div>
              <span className="block text-slate-500 mb-0.5">Duration</span>
              <span className="font-semibold text-slate-700 dark:text-slate-300">{formatDuration(job.processing_duration_seconds)}</span>
            </div>
            <div>
              <span className="block text-slate-500 mb-0.5">Outputs</span>
              <span className="font-semibold text-indigo-600 dark:text-indigo-400">
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
              <>
                <Link
                  href={`/results/${job.job_id}`}
                  className="flex-grow flex items-center justify-center space-x-1.5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition duration-150 text-xs shadow-sm"
                >
                  <Play className="h-3.5 w-3.5 fill-current" />
                  <span>View Results</span>
                </Link>

                <button
                  onClick={() => setShowPreview(true)}
                  className="p-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-slate-100 rounded-xl transition duration-150 border border-slate-200 dark:border-slate-700/50 shadow-sm cursor-pointer"
                  title="Quick 3D Preview"
                >
                  <Eye className="h-4 w-4" />
                </button>
              </>
            ) : (
              <div className="flex-grow flex items-center justify-center py-2.5 bg-slate-100 dark:bg-slate-800/40 text-slate-400 dark:text-slate-500 font-semibold rounded-xl text-xs border border-slate-200 dark:border-slate-800">
                {job.status === 'failed' ? 'Failed' : 'Processing...'}
              </div>
            )}

            {job.status === 'completed' && job.model_generated && (
              <a
                href={`${backendUrl}/api/v1/download/${job.job_id}/model`}
                onClick={async (e) => {
                  e.preventDefault();
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
                className="p-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-slate-100 rounded-xl transition duration-150 border border-slate-200 dark:border-slate-700/50 shadow-sm cursor-pointer"
                title="Download GLB Model"
              >
                <Download className="h-4 w-4" />
              </a>
            )}

            <button
              onClick={() => onDelete(job.job_id)}
              className="p-2.5 bg-rose-50 dark:bg-rose-950/20 hover:bg-rose-100 dark:hover:bg-rose-900/30 text-rose-600 dark:text-rose-400 rounded-xl transition duration-150 border border-rose-200 dark:border-rose-900/30 hover:border-rose-300 dark:hover:border-rose-900/60 shadow-sm cursor-pointer"
              title="Delete History"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Quick 3D Preview Modal */}
      {showPreview && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/75 backdrop-blur-md p-4 animate-in fade-in duration-200">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden max-w-4xl w-full shadow-2xl flex flex-col max-h-[90vh]">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-4 px-6 border-b border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/50">
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white text-lg">{displayName}</h3>
                <p className="text-xs text-slate-500 font-mono">Job ID: {job.job_id}</p>
              </div>
              <button
                onClick={() => setShowPreview(false)}
                className="p-2 rounded-xl text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-200/50 dark:hover:bg-slate-800 transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* 3D Viewer Container */}
            <div className="p-4 flex-grow overflow-hidden">
              <ThreeViewer
                glbUrl={`${apiUrl}/download/${job.job_id}/model?token=${token}`}
                plyUrl={`${apiUrl}/download/${job.job_id}/segmented_pointcloud?token=${token}`}
              />
            </div>

            {/* Modal Footer */}
            <div className="p-4 px-6 border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/50 flex justify-end space-x-3">
              <button
                onClick={() => setShowPreview(false)}
                className="px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-200/50 dark:hover:bg-slate-800 rounded-xl transition cursor-pointer"
              >
                Close
              </button>
              <Link
                href={`/results/${job.job_id}`}
                className="px-5 py-2 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition shadow-sm flex items-center space-x-1.5 cursor-pointer"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Full Results Page</span>
              </Link>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
