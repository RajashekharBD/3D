import Link from 'next/link';

export default function ViewerRedirectPage() {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-6 max-w-md mx-auto flex-grow w-full text-center">
      <h1 className="text-2xl font-bold mb-4">3D Viewer</h1>
      <p className="text-sm text-slate-400 mb-6">Please upload an image first to visualize a 3D model.</p>
      <Link href="/upload" className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-semibold transition-colors">
        Go to Upload
      </Link>
    </div>
  );
}
