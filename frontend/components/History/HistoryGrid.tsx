'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@/context/AuthContext';
import HistoryCard, { JobRecord } from './HistoryCard';
import SearchBar from './SearchBar';
import SortMenu from './SortMenu';
import { ArrowLeft, ArrowRight, Database } from 'lucide-react';

export default function HistoryGrid() {
  const { session } = useAuth();
  const [jobs, setJobs] = useState<JobRecord[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [sortBy, setSortBy] = useState('newest');

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

  const fetchHistory = useCallback(async () => {
    if (!session) return;
    setLoading(true);
    try {
      const queryParams = new URLSearchParams({
        page: page.toString(),
        sort_by: sortBy,
      });
      if (search) queryParams.append('filename', search);
      if (statusFilter) queryParams.append('status', statusFilter);

      const res = await fetch(`${backendUrl}/api/v1/history?${queryParams.toString()}`, {
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      });

      if (res.ok) {
        const data = await res.json();
        setJobs(data.jobs || []);
        setTotal(data.total || 0);
        setPages(data.pages || 1);
      }
    } catch (err) {
      console.error('Error fetching job history:', err);
    } finally {
      setLoading(false);
    }
  }, [session, page, sortBy, search, statusFilter, backendUrl]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleDelete = async (jobId: string) => {
    if (!session || !window.confirm('Are you sure you want to delete this job and all associated files?')) return;
    try {
      const res = await fetch(`${backendUrl}/api/v1/history/${jobId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      });
      if (res.ok) {
        // Refresh page or list
        fetchHistory();
      }
    } catch (err) {
      console.error('Error deleting job:', err);
    }
  };

  return (
    <div className="space-y-8">
      {/* Search and Sort Toolbar */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <SearchBar value={search} onChange={(val) => { setSearch(val); setPage(1); }} />
        <SortMenu
          sortBy={sortBy}
          onChange={(val) => { setSortBy(val); setPage(1); }}
          statusFilter={statusFilter}
          onStatusChange={(val) => { setStatusFilter(val); setPage(1); }}
        />
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : jobs.length === 0 ? (
        <div className="flex flex-col items-center justify-center p-12 bg-white/80 dark:bg-slate-900/20 border border-slate-200 dark:border-slate-800 rounded-2xl text-center space-y-4 shadow-sm">
          <Database className="h-12 w-12 text-slate-400 dark:text-slate-700" />
          <h3 className="text-lg font-bold text-slate-800 dark:text-slate-300">No History Records</h3>
          <p className="text-slate-500 text-sm max-w-sm">
            You haven&apos;t uploaded any images yet. Start by generating a 3D reconstruction from the home page.
          </p>
        </div>
      ) : (
        <>
          {/* Grid Layout */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {jobs.map((job) => (
              <HistoryCard
                key={job.job_id}
                job={job}
                onDelete={handleDelete}
                token={session?.access_token}
              />
            ))}
          </div>

          {/* Pagination Controls */}
          {pages > 1 && (
            <div className="flex items-center justify-center space-x-4 pt-6">
              <button
                onClick={() => setPage((p) => Math.max(p - 1, 1))}
                disabled={page === 1}
                className="flex items-center space-x-1 px-4 py-2 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 rounded-xl transition duration-150 text-xs font-semibold text-slate-700 dark:text-slate-300 shadow-sm disabled:opacity-50"
              >
                <ArrowLeft className="h-3.5 w-3.5" />
                <span>Prev</span>
              </button>
              <span className="text-xs text-slate-500 font-medium">
                Page <span className="text-slate-800 dark:text-slate-300 font-bold">{page}</span> of{' '}
                <span className="text-slate-800 dark:text-slate-300 font-bold">{pages}</span>
              </span>
              <button
                onClick={() => setPage((p) => Math.min(p + 1, pages))}
                disabled={page === pages}
                className="flex items-center space-x-1 px-4 py-2 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 rounded-xl transition duration-150 text-xs font-semibold text-slate-700 dark:text-slate-300 shadow-sm disabled:opacity-50"
              >
                <span>Next</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
