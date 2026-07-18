import Link from "next/link";
import { Sparkles, Cpu, Layers, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <div className="relative min-h-[85vh] flex flex-col items-center justify-center py-24 px-6 text-center max-w-5xl mx-auto flex-grow overflow-hidden">
      {/* Decorative Glow Elements */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-3xl pointer-events-none animate-pulse-slow" />
      <div className="absolute bottom-10 left-10 w-[250px] h-[250px] bg-blue-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Hero Section */}
      <div className="relative z-10 max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900/80 border border-slate-800 text-xs text-blue-400 font-medium mb-6">
          <Sparkles size={12} className="animate-spin-slow" />
          <span>Next-Gen Single-Image 3D Reconstruction</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white mb-6 leading-tight">
          Turn Any Image into a{" "}
          <span className="bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-500 bg-clip-text text-transparent">
            3D Asset
          </span>
        </h1>
        
        <p className="text-base md:text-lg text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
          Generate watertight, fully textured 3D meshes and clustered point clouds in under 4 minutes. Powered by GroundingDINO, SAM 2.1, and Hunyuan3D-2.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/upload" className="glow-btn flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-indigo-500/20 transition-all">
            <span>Start Reconstructing</span>
            <ArrowRight size={16} />
          </Link>
          <Link href="/history" className="px-8 py-4 bg-slate-900/60 hover:bg-slate-900 text-slate-300 hover:text-white font-medium rounded-xl border border-slate-800 hover:border-slate-700 transition-all backdrop-blur-sm">
            View History
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-6 w-full text-left mt-8">
        <div className="p-6 glass-card rounded-2xl">
          <div className="w-12 h-12 bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center rounded-xl mb-6 shadow-inner">
            <Layers size={20} />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">1. Image Optimization</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Drag and drop your image. The system optimizes the visual qualities automatically using OpenCV CLAHE enhancement.
          </p>
        </div>

        <div className="p-6 glass-card rounded-2xl">
          <div className="w-12 h-12 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center rounded-xl mb-6 shadow-inner">
            <Cpu size={20} />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">2. Multi-Model Pipeline</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Florence-2, GroundingDINO, and SAM 2.1 run sequentially on the backend to segment foreground objects with high precision.
          </p>
        </div>

        <div className="p-6 glass-card rounded-2xl">
          <div className="w-12 h-12 bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center rounded-xl mb-6 shadow-inner">
            <Sparkles size={20} />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">3. Textured 3D Export</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Hunyuan3D-2 generates watertight meshes. Render GLB models, query DBScan point cloud clusters, and download files directly.
          </p>
        </div>
      </div>
    </div>
  );
}
