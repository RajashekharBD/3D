'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ListFilter, ChevronDown, Check } from 'lucide-react';

interface SortMenuProps {
  sortBy: string;
  onChange: (val: string) => void;
  statusFilter: string;
  onStatusChange: (val: string) => void;
}

export default function SortMenu({ sortBy, onChange, statusFilter, onStatusChange }: SortMenuProps) {
  const [statusOpen, setStatusOpen] = useState(false);
  const [sortOpen, setSortOpen] = useState(false);

  const statusRef = useRef<HTMLDivElement>(null);
  const sortRef = useRef<HTMLDivElement>(null);

  const statusOptions = [
    { value: '', label: 'All Statuses' },
    { value: 'completed', label: 'Completed' },
    { value: 'failed', label: 'Failed' },
    { value: 'processing', label: 'Processing' },
  ];

  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'oldest', label: 'Oldest First' },
  ];

  // Close dropdowns on click outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (statusRef.current && !statusRef.current.contains(event.target as Node)) {
        setStatusOpen(false);
      }
      if (sortRef.current && !sortRef.current.contains(event.target as Node)) {
        setSortOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const currentStatusLabel = statusOptions.find((o) => o.value === statusFilter)?.label || 'All Statuses';
  const currentSortLabel = sortOptions.find((o) => o.value === sortBy)?.label || 'Newest First';

  return (
    <div className="flex flex-wrap gap-3 items-center">
      {/* Status Filter Custom Dropdown */}
      <div className="relative" ref={statusRef}>
        <button
          type="button"
          onClick={() => {
            setStatusOpen(!statusOpen);
            setSortOpen(false);
          }}
          className="flex items-center space-x-2 bg-white/90 dark:bg-slate-900/60 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-xl px-3.5 py-2 text-xs font-medium text-slate-700 dark:text-slate-300 shadow-sm hover:border-indigo-300 dark:hover:border-slate-700 transition-all cursor-pointer"
        >
          <ListFilter className="h-4 w-4 text-indigo-500 dark:text-indigo-400 flex-shrink-0" />
          <span className="text-slate-400 dark:text-slate-500">Status:</span>
          <span className="font-semibold text-slate-800 dark:text-slate-200">{currentStatusLabel}</span>
          <ChevronDown className={`h-3.5 w-3.5 text-slate-400 transition-transform duration-200 ${statusOpen ? 'rotate-180' : ''}`} />
        </button>

        {statusOpen && (
          <div className="absolute left-0 mt-2 w-44 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl py-1.5 z-50 animate-in fade-in zoom-in-95 duration-100">
            {statusOptions.map((option) => {
              const isSelected = statusFilter === option.value;
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => {
                    onStatusChange(option.value);
                    setStatusOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-3.5 py-2 text-xs transition-colors text-left cursor-pointer ${
                    isSelected
                      ? 'bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 font-semibold'
                      : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/70'
                  }`}
                >
                  <span>{option.label}</span>
                  {isSelected && <Check className="h-3.5 w-3.5 text-indigo-600 dark:text-indigo-400" />}
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* Sort By Custom Dropdown */}
      <div className="relative" ref={sortRef}>
        <button
          type="button"
          onClick={() => {
            setSortOpen(!sortOpen);
            setStatusOpen(false);
          }}
          className="flex items-center space-x-2 bg-white/90 dark:bg-slate-900/60 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-xl px-3.5 py-2 text-xs font-medium text-slate-700 dark:text-slate-300 shadow-sm hover:border-indigo-300 dark:hover:border-slate-700 transition-all cursor-pointer"
        >
          <span className="text-slate-400 dark:text-slate-500">Sort:</span>
          <span className="font-semibold text-slate-800 dark:text-slate-200">{currentSortLabel}</span>
          <ChevronDown className={`h-3.5 w-3.5 text-slate-400 transition-transform duration-200 ${sortOpen ? 'rotate-180' : ''}`} />
        </button>

        {sortOpen && (
          <div className="absolute left-0 mt-2 w-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl py-1.5 z-50 animate-in fade-in zoom-in-95 duration-100">
            {sortOptions.map((option) => {
              const isSelected = sortBy === option.value;
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => {
                    onChange(option.value);
                    setSortOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-3.5 py-2 text-xs transition-colors text-left cursor-pointer ${
                    isSelected
                      ? 'bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 font-semibold'
                      : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/70'
                  }`}
                >
                  <span>{option.label}</span>
                  {isSelected && <Check className="h-3.5 w-3.5 text-indigo-600 dark:text-indigo-400" />}
                </button>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
