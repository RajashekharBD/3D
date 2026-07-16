'use client';

import { useParams } from 'next/navigation';

export default function ResultsPage() {
  const { jobId } = useParams();

  return (
    <div className="flex flex-col py-12 px-6 md:px-12 max-w-7xl mx-auto w-full flex-grow">
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-6 mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold">Reconstruction Results</h1>
          <p className="text-sm text-slate-400">Job ID: {jobId}</p>
        </div>
        <div className="flex space-x-3">
          <button className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-sm transition-colors">
            Back to Upload
          </button>
          <button className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-semibold transition-colors">
            Download All (.zip)
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* 3D Viewer Panel */}
        <div className="lg:col-span-2 aspect-video bg-slate-900 border border-slate-800 rounded-2xl flex flex-col items-center justify-center p-6 text-slate-400 relative">
          <div className="absolute top-4 left-4 bg-slate-950/80 border border-slate-850 px-3 py-1 rounded-full text-xs font-semibold text-slate-300">
            3D Viewer
          </div>
          <svg className="w-16 h-16 text-slate-700 mb-4 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
          </svg>
          <p className="text-sm font-medium">3D Viewer Sandbox (Three.js)</p>
          <p className="text-xs text-slate-500 mt-1">GLB models rendering will be loaded here in Phase 19</p>
        </div>

        {/* Outputs and Downloads Panel */}
        <div className="flex flex-col space-y-6">
          <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-2xl">
            <h2 className="text-lg font-bold mb-4">Pipeline Deliverables</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-sm font-medium text-slate-300">Textured Mesh (.GLB)</span>
                <button className="text-xs font-bold text-blue-400 hover:text-blue-300">Download</button>
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-sm font-medium text-slate-300">Raw Point Cloud (.PLY)</span>
                <button className="text-xs font-bold text-blue-400 hover:text-blue-300">Download</button>
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-sm font-medium text-slate-300">Clustered Point Cloud (.PLY)</span>
                <button className="text-xs font-bold text-blue-400 hover:text-blue-300">Download</button>
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-sm font-medium text-slate-300">Transparent Image (.PNG)</span>
                <button className="text-xs font-bold text-blue-400 hover:text-blue-300">Download</button>
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-sm font-medium text-slate-300">Job Metadata (.JSON)</span>
                <button className="text-xs font-bold text-blue-400 hover:text-blue-300">Download</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
