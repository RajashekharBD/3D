'use client';

import { useState, useEffect } from 'react';
import { Download, FileBox, Image as ImageIcon, FileText, Scan, Layers, Package, CheckCircle2 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

interface DownloadPanelProps {
  jobId: string;
}

interface ArtifactCard {
  key: string;
  label: string;
  description: string;
  icon: React.ReactNode;
  category: 'model' | 'image' | 'data';
}

const ARTIFACT_CARDS: ArtifactCard[] = [
  {
    key: 'model',
    label: 'Textured Mesh',
    description: 'GLB format, textured',
    icon: <Package size={18} />,
    category: 'model',
  },
  {
    key: 'pointcloud',
    label: 'Raw Point Cloud',
    description: 'PLY, 100K points',
    icon: <Layers size={18} />,
    category: 'model',
  },
  {
    key: 'segmented_pointcloud',
    label: 'Segmented Point Cloud',
    description: 'PLY, DBSCAN clustered',
    icon: <Layers size={18} />,
    category: 'model',
  },
  {
    key: 'rgba',
    label: 'Transparent Image',
    description: 'RGBA PNG, no background',
    icon: <ImageIcon size={18} />,
    category: 'image',
  },
  {
    key: 'detection',
    label: 'Detection Overlay',
    description: 'Bounding box visualization',
    icon: <Scan size={18} />,
    category: 'image',
  },
  {
    key: 'segmentation',
    label: 'Segmentation Map',
    description: 'SAM2.1 mask overlay',
    icon: <Scan size={18} />,
    category: 'image',
  },
  {
    key: 'mask_overlay',
    label: 'Mask Overlay',
    description: 'Binary segmentation mask',
    icon: <Scan size={18} />,
    category: 'image',
  },
  {
    key: 'part_detection',
    label: 'Part Detection',
    description: 'Florence-2 part boxes',
    icon: <Scan size={18} />,
    category: 'image',
  },
  {
    key: 'original',
    label: 'Original Image',
    description: 'Uploaded source image',
    icon: <ImageIcon size={18} />,
    category: 'image',
  },
  {
    key: 'enhanced',
    label: 'Enhanced Image',
    description: 'CLAHE processed',
    icon: <ImageIcon size={18} />,
    category: 'image',
  },
  {
    key: 'result',
    label: 'Job Metadata',
    description: 'Full pipeline result.json',
    icon: <FileText size={18} />,
    category: 'data',
  },
  {
    key: 'caption',
    label: 'Caption',
    description: 'Florence-2 text caption',
    icon: <FileText size={18} />,
    category: 'data',
  },
];

const CATEGORY_LABELS: Record<string, string> = {
  model: '3D Assets',
  image: 'Image Artifacts',
  data: 'Metadata',
};

const CATEGORY_ORDER = ['model', 'image', 'data'];

export default function DownloadPanel({ jobId }: DownloadPanelProps) {
  const { session } = useAuth();
  const [availability, setAvailability] = useState<Record<string, boolean>>({});
  const [loadingKey, setLoadingKey] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

  useEffect(() => {
    if (!session) return;
    const fetchAvailability = async () => {
      try {
        const response = await fetch(`${apiUrl}/download/${jobId}`, {
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          setAvailability(data.artifacts || {});
        }
      } catch (err) {
        console.error('Failed to fetch artifact availability:', err);
      }
    };
    fetchAvailability();
  }, [apiUrl, jobId, session]);

  const handleDownload = (artifactKey: string) => {
    setLoadingKey(artifactKey);
    const token = session?.access_token || '';
    const downloadUrl = `${apiUrl}/download/${jobId}/${artifactKey}?token=${token}`;
    
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    setTimeout(() => setLoadingKey(null), 1500);
  };

  return (
    <div className="space-y-6">
      {CATEGORY_ORDER.map((category) => {
        const cards = ARTIFACT_CARDS.filter(
          (c) => c.category === category && availability[c.key]
        );
        if (cards.length === 0) return null;

        return (
          <div key={category}>
            <h3 className="text-[10px] uppercase tracking-wider font-bold text-slate-500 mb-3">
              {CATEGORY_LABELS[category]}
            </h3>
            <div className="space-y-2">
              {cards.map((card) => (
                <button
                  key={card.key}
                  onClick={() => handleDownload(card.key)}
                  disabled={loadingKey === card.key}
                  className="w-full flex items-center justify-between p-3.5 bg-slate-950 hover:bg-slate-900 rounded-xl border border-slate-900 hover:border-slate-800 transition-all group cursor-pointer disabled:opacity-60"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-9 h-9 rounded-lg bg-slate-900 group-hover:bg-slate-800 border border-slate-800 flex items-center justify-center text-slate-400 group-hover:text-blue-400 transition-colors">
                      {card.icon}
                    </div>
                    <div className="text-left">
                      <p className="text-sm font-semibold text-slate-200 group-hover:text-white transition-colors">
                        {card.label}
                      </p>
                      <p className="text-[10px] text-slate-500">{card.description}</p>
                    </div>
                  </div>
                  <div className="flex-shrink-0 text-slate-600 group-hover:text-blue-400 transition-colors">
                    {loadingKey === card.key ? (
                      <CheckCircle2 size={16} className="text-emerald-400" />
                    ) : (
                      <Download size={16} />
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        );
      })}

      {Object.keys(availability).length === 0 && (
        <div className="flex items-center justify-center p-6 text-center">
          <div className="flex flex-col items-center">
            <FileBox size={28} className="text-slate-700 mb-2" />
            <p className="text-xs text-slate-500">No artifacts available yet.</p>
          </div>
        </div>
      )}
    </div>
  );
}
