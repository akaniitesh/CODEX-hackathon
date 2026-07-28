'use client';

import React from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import { Navbar } from './Navbar';
import { LoginModal } from '../auth/LoginModal';
import { ConnectRepoModal } from '../auth/ConnectRepoModal';
import { RepositoryList } from '../repositories/RepositoryList';
import { AnalyticsPanel } from '../analytics/AnalyticsPanel';

export function AppShell({ children }: { children?: React.ReactNode }) {
  const { activeTab } = useRepoStore();

  return (
    <div className="min-h-screen bg-[#0B0F17] text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-8 space-y-8">
        {activeTab === 'repositories' ? (
          <RepositoryList />
        ) : activeTab === 'analytics' ? (
          <AnalyticsPanel />
        ) : (
          children
        )}
      </main>

      <LoginModal />
      <ConnectRepoModal />
    </div>
  );
}
