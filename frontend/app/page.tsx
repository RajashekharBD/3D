import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-6 text-center max-w-4xl mx-auto flex-grow">
      {/* Hero Section */}
      <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-500 bg-clip-text text-transparent mb-6 animate-pulse">
        Single Image to 3D Asset & Point Cloud
      </h1>
      
      <p className="text-lg md:text-xl text-slate-400 max-w-2xl mb-10 leading-relaxed">
        Reconstruct watertight, textured 3D models and semantic point clouds from a single RGB image in under 4 minutes, using GroundingDINO, SAM 2.1, and Hunyuan3D-2.
      </p>

      <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 mb-20">
        <Link href="/upload" className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium rounded-lg shadow-lg hover:shadow-indigo-500/20 transition-all transform hover:-translate-y-0.5">
          Get Started
        </Link>
        <a href="/docs" className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-medium rounded-lg border border-slate-700 transition-all">
          Read Docs
        </a>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full text-left">
        <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl">
          <div className="w-10 h-10 bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center rounded-lg mb-4 font-bold">1</div>
          <h3 className="text-lg font-bold text-white mb-2">Upload Image</h3>
          <p className="text-sm text-slate-400">Drag & drop your single RGB image (PNG, JPG, BMP, etc.). The system automatically enhancements it with OpenCV CLAHE.</p>
        </div>
        <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl">
          <div className="w-10 h-10 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center rounded-lg mb-4 font-bold">2</div>
          <h3 className="text-lg font-bold text-white mb-2">AI Processing</h3>
          <p className="text-sm text-slate-400">Florence-2, GroundingDINO, SAM 2.1, and Hunyuan3D-2 execute sequentially to detect, segment, and reconstruct.</p>
        </div>
        <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl">
          <div className="w-10 h-10 bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center rounded-lg mb-4 font-bold">3</div>
          <h3 className="text-lg font-bold text-white mb-2">3D Output</h3>
          <p className="text-sm text-slate-400">Interact with the textured GLB mesh in the browser, export the 100k Poisson point cloud, and download DBSCAN clusters.</p>
        </div>
      </div>
    </div>
  );
}
