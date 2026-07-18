'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import ProtectedRoute from '@/components/Auth/ProtectedRoute';
import { Upload, X, Image as ImageIcon, Sparkles, AlertCircle } from 'lucide-react';

export default function UploadPage() {
  const router = useRouter();
  const { session } = useAuth();
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Constants matching backend constraints
  const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp', 'bmp'];
  const MAX_SIZE_MB = 25;

  const validateFile = (file: File): boolean => {
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (!ext || !ALLOWED_EXTENSIONS.includes(ext)) {
      setError(`Unsupported file type. Please upload: ${ALLOWED_EXTENSIONS.join(', ').toUpperCase()}`);
      return false;
    }
    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > MAX_SIZE_MB) {
      setError(`File is too large (${sizeMB.toFixed(1)}MB). Max size allowed is ${MAX_SIZE_MB}MB.`);
      return false;
    }
    setError(null);
    return true;
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
      }
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const headers: Record<string, string> = {};
      if (session?.access_token) {
        headers['Authorization'] = `Bearer ${session.access_token}`;
      }
      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.message || 'Upload failed');
      }

      const data = await response.json();
      if (data && data.job_id) {
        router.push(`/processing/${data.job_id}`);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to connect to the backend server.';
      setError(errorMessage);
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="relative flex flex-col items-center justify-center py-20 px-6 max-w-xl mx-auto flex-grow w-full z-10">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold mb-2 tracking-tight text-white bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
            Upload Image
          </h1>
          <p className="text-sm text-slate-400">Reconstruct single RGB images into textured 3D models and point clouds.</p>
        </div>

        {error && (
          <div className="w-full mb-6 p-4 bg-red-950/20 border border-red-900/40 text-red-300 rounded-xl text-sm flex items-start space-x-3 backdrop-blur-sm">
            <AlertCircle className="w-5 h-5 flex-shrink-0 text-red-400 mt-0.5" />
            <span className="leading-relaxed">{error}</span>
          </div>
        )}

        {!previewUrl ? (
          <div 
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
            className={`w-full aspect-video border-2 border-dashed rounded-2xl flex flex-col items-center justify-center p-6 text-center cursor-pointer transition-all duration-300 relative group overflow-hidden ${
              dragActive 
                ? 'border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/5' 
                : 'border-slate-800 bg-slate-900/30 hover:border-slate-700 hover:bg-slate-900/50'
            }`}
          >
            <input 
              type="file" 
              id="file-upload" 
              className="hidden" 
              accept="image/jpeg,image/jpg,image/png,image/webp,image/bmp"
              onChange={handleFileChange}
            />
            <label htmlFor="file-upload" className="cursor-pointer w-full h-full flex flex-col items-center justify-center">
              <div className="w-14 h-14 bg-slate-950/80 border border-slate-800 flex items-center justify-center rounded-2xl mb-4 text-slate-400 group-hover:text-blue-400 group-hover:border-blue-500/30 transition-all shadow-inner">
                <Upload size={22} className="group-hover:-translate-y-0.5 transition-transform" />
              </div>
              <span className="text-sm font-semibold text-slate-200 mb-1 group-hover:text-white transition-colors">
                Drag & drop your file here
              </span>
              <span className="text-xs text-slate-400 group-hover:text-slate-300 transition-colors">
                or click to browse files
              </span>
              <span className="text-[10px] text-slate-500 mt-4">
                Supported formats: {ALLOWED_EXTENSIONS.join(', ').toUpperCase()} (Max {MAX_SIZE_MB}MB)
              </span>
            </label>
          </div>
        ) : (
          <div className="w-full flex flex-col items-center">
            <div className="w-full glass-card rounded-2xl p-5 flex flex-col items-center relative overflow-hidden shadow-xl">
              <button 
                onClick={handleClear}
                className="absolute top-4 right-4 bg-slate-950/85 border border-slate-850 hover:bg-slate-900 hover:border-slate-700 text-slate-400 hover:text-slate-200 w-8 h-8 flex items-center justify-center rounded-full transition-all z-10 shadow-lg"
                title="Remove image"
              >
                <X size={15} />
              </button>
              
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img 
                src={previewUrl} 
                alt="Selected Preview" 
                className="max-h-64 object-contain rounded-xl shadow-lg border border-slate-850 bg-slate-950/60" 
              />
              
              <div className="mt-4 text-center w-full px-4">
                <p className="text-sm font-semibold text-slate-200 truncate max-w-xs mx-auto">{selectedFile?.name}</p>
                <div className="inline-flex items-center space-x-1.5 mt-1 bg-slate-950/50 border border-slate-900 px-2.5 py-0.5 rounded-full">
                  <ImageIcon size={10} className="text-slate-400" />
                  <span className="text-[11px] font-medium text-slate-400">
                    {selectedFile ? (selectedFile.size / (1024 * 1024)).toFixed(2) : 0} MB
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={handleUpload}
              disabled={loading}
              className="glow-btn mt-8 w-full py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold rounded-xl shadow-xl hover:shadow-indigo-500/20 disabled:opacity-50 transition-all flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
                  <span>Uploading and initializing...</span>
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  <span>Start 3D Generation Pipeline</span>
                </>
              )}
            </button>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
