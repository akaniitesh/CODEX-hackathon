'use client';

import React from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import { Navbar } from '@/components/layout/Navbar';
import { LoginModal } from '@/components/auth/LoginModal';
import { ConnectRepoModal } from '@/components/auth/ConnectRepoModal';
import { RepositoryList } from '@/components/repositories/RepositoryList';
import { TimelinePanel } from '@/components/timeline/TimelinePanel';
import { GraphTracePanel } from '@/components/graph/GraphTracePanel';
import { ReviewsPanel } from '@/components/reviews/ReviewsPanel';
import { ArchitecturePanel } from '@/components/architecture/ArchitecturePanel';
import { AnalyticsPanel } from '@/components/analytics/AnalyticsPanel';
import { PresentationPanel } from '@/components/presentation/PresentationPanel';

export function AppShell({ children }: { children?: React.ReactNode }) {
  const { activeTab } = useRepoStore();

  return (
    <div className="min-h-screen bg-[#0B0F17] text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-8 space-y-8">
        {activeTab === 'repositories' && <RepositoryList />}
        {activeTab === 'timeline' && <TimelinePanel />}
        {activeTab === 'graph' && <GraphTracePanel />}
        {activeTab === 'reviews' && <ReviewsPanel />}
        {activeTab === 'architecture' && <ArchitecturePanel />}
        {activeTab === 'analytics' && <AnalyticsPanel />}
        {activeTab === 'presentation' && <PresentationPanel />}
        {children}
      </main>

      <LoginModal />
      <ConnectRepoModal />
    </div>
  );
}
