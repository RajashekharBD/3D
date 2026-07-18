'use client';

import React, { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/Auth/ProtectedRoute';
import ProfileCard from '@/components/Profile/ProfileCard';
import StatisticsCard from '@/components/Profile/StatisticsCard';
import { useAuth } from '@/context/AuthContext';

interface ProfileData {
  profile: {
    id: string;
    email: string;
    created_at: string;
    last_login?: string;
  };
  statistics: {
    total_uploads: number;
    completed_jobs: number;
    failed_jobs: number;
    models_generated: number;
    pointclouds_generated: number;
    average_processing_time: number;
    last_upload?: string;
  };
}

export default function ProfilePage() {
  const { session, logout } = useAuth();
  const [data, setData] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

  useEffect(() => {
    if (!session) return;
    setLoading(true);
    fetch(`${backendUrl}/api/v1/profile`, {
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    })
      .then((res) => (res.ok ? res.json() : null))
      .then((resData) => {
        if (resData) setData(resData);
      })
      .catch((err) => console.error('Error fetching profile:', err))
      .finally(() => setLoading(false));
  }, [session, backendUrl]);

  return (
    <ProtectedRoute>
      <div className="flex-grow p-8 max-w-6xl mx-auto w-full space-y-8">
        <div>
          <h2 className="text-3xl font-extrabold text-slate-100 mb-2">My Profile</h2>
          <p className="text-slate-400 text-sm">
            View your account information and reconstruction stats.
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        ) : data ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-1">
              <ProfileCard
                email={data.profile.email}
                createdAt={data.profile.created_at}
                lastLogin={data.profile.last_login}
                logout={logout}
              />
            </div>
            <div className="md:col-span-2">
              <StatisticsCard
                totalUploads={data.statistics.total_uploads}
                completedJobs={data.statistics.completed_jobs}
                failedJobs={data.statistics.failed_jobs}
                modelsGenerated={data.statistics.models_generated}
                pointcloudsGenerated={data.statistics.pointclouds_generated}
                averageTime={data.statistics.average_processing_time}
                lastUpload={data.statistics.last_upload}
              />
            </div>
          </div>
        ) : (
          <div className="p-8 text-center bg-slate-900/20 border border-slate-800 rounded-2xl text-slate-400">
            Failed to load profile. Please refresh the page.
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
