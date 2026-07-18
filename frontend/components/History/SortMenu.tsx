'use client';

import React from 'react';
import { ListFilter } from 'lucide-react';

interface SortMenuProps {
  sortBy: string;
  onChange: (val: string) => void;
  statusFilter: string;
  onStatusChange: (val: string) => void;
}

export default function SortMenu({ sortBy, onChange, statusFilter, onStatusChange }: SortMenuProps) {
  return (
    <div className="flex flex-wrap gap-3 items-center">
      {/* Status Filter */}
      <div className="flex items-center space-x-2 bg-slate-900/40 backdrop-blur-sm border border-slate-800 rounded-xl px-3 py-1.5 text-sm text-slate-300">
        <ListFilter className="h-4 w-4 text-indigo-400" />
        <span className="text-xs text-slate-500 font-medium">Status:</span>
        <select
          value={statusFilter}
          onChange={(e) => onStatusChange(e.target.value)}
          className="bg-transparent border-none outline-none focus:ring-0 text-xs font-semibold cursor-pointer text-slate-200"
        >
          <option value="" className="bg-slate-900 text-slate-200">All</option>
          <option value="completed" className="bg-slate-900 text-slate-200">Completed</option>
          <option value="failed" className="bg-slate-900 text-slate-200">Failed</option>
          <option value="processing" className="bg-slate-900 text-slate-200">Processing</option>
        </select>
      </div>

      {/* Sort By Dropdown */}
      <div className="flex items-center space-x-2 bg-slate-900/40 backdrop-blur-sm border border-slate-800 rounded-xl px-3 py-1.5 text-sm text-slate-300">
        <span className="text-xs text-slate-500 font-medium">Sort:</span>
        <select
          value={sortBy}
          onChange={(e) => onChange(e.target.value)}
          className="bg-transparent border-none outline-none focus:ring-0 text-xs font-semibold cursor-pointer text-slate-200"
        >
          <option value="newest" className="bg-slate-900 text-slate-200">Newest First</option>
          <option value="oldest" className="bg-slate-900 text-slate-200">Oldest First</option>
        </select>
      </div>
    </div>
  );
}
