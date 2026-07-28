'use client';

import { useParams, useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import ThreeViewer from '../../../components/ThreeViewer';
import DownloadPanel from '../../../components/Download/DownloadPanel';
import { ArrowLeft, AlertTriangle, Loader2, Info, CheckCircle } from 'lucide-react';

import ProtectedRoute from '@/components/Auth/ProtectedRoute';
import { useAuth } from '@/context/AuthContext';

export default function ResultsPage() {
  const router = useRouter();
  const { jobId } = useParams() as { jobId: string };
  const { session } = useAuth();
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [resultData, setResultData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
  const token = session?.access_token || '';
  
  const resultUrl = `${apiUrl}/download/${jobId}/result?token=${token}`;
  const glbUrl = `${apiUrl}/download/${jobId}/model?token=${token}`;
  const plyUrl = `${apiUrl}/download/${jobId}/segmented_pointcloud?token=${token}`;

  useEffect(() => {
    if (!jobId || !session) return;
    
    const fetchResults = async () => {
      try {
        setLoading(true);
        const response = await fetch(resultUrl, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        if (!response.ok) {
          throw new Error(`Failed to load reconstruction result metadata (Status: ${response.status}).`);
        }
        const data = await response.json();
        setResultData(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching result.json:', err);
        setError('Reconstruction output is not yet ready or does not exist.');
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [jobId, resultUrl, session, token]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] flex-grow text-slate-400">
        <Loader2 className="animate-spin h-8 w-8 text-blue-500 mb-4" />
        <p className="text-sm font-semibold">Loading reconstruction results...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] flex-grow text-center max-w-md mx-auto px-6">
        <AlertTriangle className="w-12 h-12 text-red-500 mb-4" />
        <h2 className="text-xl font-bold text-white mb-2">Results Unavailable</h2>
        <p className="text-sm text-slate-400 mb-6">{error}</p>
        <button 
          onClick={() => router.push('/upload')} 
          className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-semibold transition-colors cursor-pointer"
        >
          Go to Upload
        </button>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="relative flex flex-col py-12 px-6 md:px-12 max-w-7xl mx-auto w-full flex-grow z-10">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-200 dark:border-slate-900/60 pb-6 mb-8 gap-4">
          <div>
            <div className="inline-flex items-center space-x-1.5 text-xs text-emerald-700 dark:text-green-400 bg-emerald-50 dark:bg-green-500/10 px-2.5 py-0.5 rounded-full mb-2 font-medium border border-emerald-200 dark:border-green-500/10">
              <CheckCircle size={10} />
              <span>Processing Complete</span>
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Reconstruction Results</h1>
            <p className="text-xs text-slate-500 mt-1">Job ID: {jobId}</p>
          </div>
          <div className="flex space-x-3">
            <button 
              onClick={() => router.push('/upload')}
              className="flex items-center space-x-2 px-4 py-2.5 bg-white/80 dark:bg-slate-900/60 hover:bg-white dark:hover:bg-slate-900 text-slate-700 dark:text-slate-200 hover:text-slate-900 dark:hover:text-white border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 rounded-xl text-sm transition-all cursor-pointer backdrop-blur-sm shadow-sm"
            >
              <ArrowLeft size={14} />
              <span>Back to Upload</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 3D Viewer Panel */}
          <div className="lg:col-span-2 flex flex-col space-y-6">
            <div className="shadow-xl rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-900 bg-white/50 dark:bg-slate-950/20">
              <ThreeViewer 
                glbUrl={glbUrl} 
                plyUrl={resultData?.artifacts?.segmented_pointcloud ? plyUrl : ''} 
              />
            </div>
            
            {/* Metadata Metrics Panel */}
            {resultData && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-5 glass-card rounded-2xl">
                <div className="flex flex-col p-3 rounded-xl bg-slate-50/80 dark:bg-slate-950/40 border border-slate-200/80 dark:border-slate-900">
                  <span className="text-[10px] uppercase tracking-wider font-bold text-slate-500">Vertices</span>
                  <span className="text-xl font-extrabold text-slate-800 dark:text-white mt-1">
                    {resultData.mesh_metadata?.vertex_count?.toLocaleString() || 'N/A'}
                  </span>
                </div>
                <div className="flex flex-col p-3 rounded-xl bg-slate-50/80 dark:bg-slate-950/40 border border-slate-200/80 dark:border-slate-900">
                  <span className="text-[10px] uppercase tracking-wider font-bold text-slate-500">Faces</span>
                  <span className="text-xl font-extrabold text-slate-800 dark:text-white mt-1">
                    {resultData.mesh_metadata?.face_count?.toLocaleString() || 'N/A'}
                  </span>
                </div>
                <div className="flex flex-col p-3 rounded-xl bg-slate-50/80 dark:bg-slate-950/40 border border-slate-200/80 dark:border-slate-900">
                  <span className="text-[10px] uppercase tracking-wider font-bold text-slate-500">Points Sampled</span>
                  <span className="text-xl font-extrabold text-slate-800 dark:text-white mt-1">
                    {resultData.pointcloud_metadata?.point_count?.toLocaleString() || '100,000'}
                  </span>
                </div>
                <div className="flex flex-col p-3 rounded-xl bg-slate-50/80 dark:bg-slate-950/40 border border-slate-200/80 dark:border-slate-900">
                  <span className="text-[10px] uppercase tracking-wider font-bold text-slate-500">Semantic Clusters</span>
                  <span className="text-xl font-extrabold text-slate-800 dark:text-white mt-1">
                    {resultData.dbscan_metadata?.total_clusters || '1'}
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Download Panel */}
          <div className="flex flex-col space-y-6">
            <div className="p-6 glass-card rounded-2xl shadow-xl">
              <div className="flex items-center space-x-2 mb-5">
                <Info size={16} className="text-indigo-600 dark:text-blue-400" />
                <h2 className="text-lg font-bold text-slate-900 dark:text-white">Pipeline Deliverables</h2>
              </div>
              <DownloadPanel jobId={jobId} />
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
