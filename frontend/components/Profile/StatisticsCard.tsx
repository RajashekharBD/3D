'use client';

import React from 'react';

interface StatsProps {
  totalUploads: number;
  completedJobs: number;
  failedJobs: number;
  modelsGenerated: number;
  pointcloudsGenerated: number;
  averageTime: number;
  lastUpload?: string;
}

export default function StatisticsCard({
  totalUploads,
  completedJobs,
  failedJobs,
  modelsGenerated,
  pointcloudsGenerated,
  averageTime,
  lastUpload,
}: StatsProps) {
  const formatTime = (seconds: number) => {
    if (seconds === 0) return '0s';
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}m ${secs}s`;
  };

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return 'Never';
    return new Date(dateStr).toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const statItems = [
    { label: 'Total Uploads', value: totalUploads, color: 'text-indigo-400' },
    { label: 'Completed Jobs', value: completedJobs, color: 'text-emerald-400' },
    { label: 'Failed Jobs', value: failedJobs, color: 'text-rose-400' },
    { label: 'Models Baked', value: modelsGenerated, color: 'text-cyan-400' },
    { label: 'Point Clouds Clustered', value: pointcloudsGenerated, color: 'text-purple-400' },
    { label: 'Avg processing Time', value: formatTime(averageTime), color: 'text-amber-400' },
  ];

  return (
    <div className="p-6 bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-2xl shadow-lg h-full space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-bold text-slate-100">AI Pipeline Statistics</h3>
        <span className="text-xs text-slate-500 font-medium">
          Last Upload: <span className="text-slate-300 font-semibold">{formatDate(lastUpload)}</span>
        </span>
      </div>

      <hr className="border-slate-800" />

      <div className="grid grid-cols-2 gap-4">
        {statItems.map((item, idx) => (
          <div key={idx} className="p-4 bg-slate-950/50 border border-slate-800/80 rounded-xl space-y-1">
            <span className="block text-slate-500 text-xs font-medium">{item.label}</span>
            <span className={`text-2xl font-black ${item.color}`}>{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
