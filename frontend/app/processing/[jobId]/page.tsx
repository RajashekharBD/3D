'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';

export default function ProcessingPage() {
  const router = useRouter();
  const { jobId } = useParams();
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState("Initializing Pipeline");

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        const next = prev + 10;
        if (next >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            router.push(`/results/${jobId}`);
          }, 1000);
          return 100;
        }
        
        // Update stage based on progress
        if (next < 15) setStage("Image Analysis");
        else if (next < 25) setStage("CLAHE Enhancement");
        else if (next < 40) setStage("Florence-2 Captioning");
        else if (next < 50) setStage("GroundingDINO Detection");
        else if (next < 60) setStage("Florence-2 Parts Detection");
        else if (next < 70) setStage("SAM2.1 Instance Segmentation");
        else if (next < 80) setStage("rembg Background Removal");
        else if (next < 90) setStage("Hunyuan3D-2 Shape Generation");
        else setStage("Open3D Point Cloud Generation");
        
        return next;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [jobId, router]);

  return (
    <div className="flex flex-col items-center justify-center py-20 px-6 max-w-md mx-auto flex-grow w-full text-center">
      <h1 className="text-3xl font-bold mb-2">Processing Asset</h1>
      <p className="text-sm text-slate-400 mb-10">Job ID: {jobId}</p>

      {/* Progress Circle or Bar */}
      <div className="w-full bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <span className="text-sm font-semibold text-slate-300">{stage}</span>
          <span className="text-sm font-bold text-blue-400">{progress}%</span>
        </div>
        <div className="w-full bg-slate-850 h-3 rounded-full overflow-hidden">
          <div 
            className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full transition-all duration-500 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <p className="text-xs text-slate-500">Estimated remaining time: ~3 minutes. Do not close this tab.</p>
    </div>
  );
}
