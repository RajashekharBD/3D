'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function UploadPage() {
  const router = useRouter();
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
      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
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
    <div className="flex flex-col items-center justify-center py-16 px-6 max-w-xl mx-auto flex-grow w-full">
      <h1 className="text-3xl font-bold mb-2 tracking-tight text-white bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
        Upload Image
      </h1>
      <p className="text-sm text-slate-400 mb-8">Select an image to reconstruct into a 3D model and point cloud.</p>

      {error && (
        <div className="w-full mb-6 p-4 bg-red-950/40 border border-red-900/50 text-red-300 rounded-lg text-sm flex items-center space-x-2">
          <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <span>{error}</span>
        </div>
      )}

      {!previewUrl ? (
        <div 
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          className={`w-full aspect-video border-2 border-dashed rounded-2xl flex flex-col items-center justify-center p-6 text-center cursor-pointer transition-all duration-200 ${
            dragActive ? 'border-blue-500 bg-blue-500/5' : 'border-slate-800 bg-slate-900/20 hover:border-slate-700 hover:bg-slate-900/30'
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
            <div className="w-12 h-12 bg-slate-900/80 border border-slate-800 flex items-center justify-center rounded-xl mb-4 text-slate-400 group-hover:text-white transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <span className="text-sm font-semibold text-slate-200 mb-1">Drag & drop your file here</span>
            <span className="text-xs text-slate-400">or click to browse from files</span>
          </label>
        </div>
      ) : (
        <div className="w-full flex flex-col items-center">
          <div className="w-full border border-slate-800 bg-slate-900/10 rounded-2xl p-4 flex flex-col items-center relative overflow-hidden">
            <button 
              onClick={handleClear}
              className="absolute top-4 right-4 bg-slate-950/80 border border-slate-800 hover:bg-slate-900 text-slate-300 w-8 h-8 flex items-center justify-center rounded-full transition-colors z-10"
              title="Remove image"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img 
              src={previewUrl} 
              alt="Selected Preview" 
              className="max-h-64 object-contain rounded-xl shadow-lg border border-slate-800 bg-slate-950" 
            />
            
            <div className="mt-4 text-center">
              <p className="text-sm font-semibold text-slate-200 truncate max-w-xs">{selectedFile?.name}</p>
              <p className="text-xs text-slate-400 mt-0.5">
                {selectedFile ? (selectedFile.size / (1024 * 1024)).toFixed(2) : 0} MB
              </p>
            </div>
          </div>

          <button
            onClick={handleUpload}
            disabled={loading}
            className="mt-8 w-full py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-indigo-500/20 disabled:opacity-50 transition-all flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
                <span>Uploading and initializing...</span>
              </>
            ) : (
              <span>Start 3D Generation Pipeline</span>
            )}
          </button>
        </div>
      )}
    </div>
  );
}
