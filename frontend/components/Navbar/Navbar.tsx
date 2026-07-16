import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="w-full bg-slate-900 border-b border-slate-800 text-white py-4 px-6 md:px-12 flex items-center justify-between">
      <div className="flex items-center space-x-2">
        <Link href="/" className="text-xl font-bold tracking-tight bg-gradient-to-r from-blue-500 to-indigo-500 bg-clip-text text-transparent hover:opacity-90 transition-opacity">
          SingleImage3D
        </Link>
      </div>
      <div className="flex items-center space-x-6">
        <Link href="/" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
          Home
        </Link>
        <Link href="/upload" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
          Upload
        </Link>
        <Link href="/about" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
          About
        </Link>
      </div>
    </nav>
  );
}
