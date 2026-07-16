export default function Footer() {
  return (
    <footer className="w-full bg-slate-900 border-t border-slate-800 text-slate-400 py-6 px-6 md:px-12 flex flex-col md:flex-row items-center justify-between text-xs">
      <div>
        <p>&copy; {new Date().getFullYear()} SingleImage3D. All rights reserved. Version 1.0.0</p>
      </div>
      <div className="flex space-x-6 mt-4 md:mt-0">
        <a href="https://github.com/RajashekharBD/3D.git" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
          GitHub
        </a>
        <a href="/docs" className="hover:text-white transition-colors">
          Documentation
        </a>
      </div>
    </footer>
  );
}
