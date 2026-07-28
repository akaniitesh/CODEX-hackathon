import { create } from 'zustand';
import { Repository } from '@/lib/types';

interface RepoState {
  selectedRepo: Repository | null;
  isConnectModalOpen: boolean;
  activeTab: 'repositories' | 'timeline' | 'graph' | 'reviews' | 'architecture' | 'analytics';
  setSelectedRepo: (repo: Repository | null) => void;
  openConnectModal: () => void;
  closeConnectModal: () => void;
  setActiveTab: (tab: RepoState['activeTab']) => void;
}

export const useRepoStore = create<RepoState>((set) => ({
  selectedRepo: {
    id: 'repo-demo-1',
    organization_id: 'org-1',
    github_repo_id: '123456',
    owner: 'enterprise-org',
    name: 'autonomous-platform',
    full_name: 'enterprise-org/autonomous-platform',
    clone_url: 'https://github.com/enterprise-org/autonomous-platform.git',
    default_branch: 'main',
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  isConnectModalOpen: false,
  activeTab: 'repositories',
  setSelectedRepo: (repo) => set({ selectedRepo: repo }),
  openConnectModal: () => set({ isConnectModalOpen: true }),
  closeConnectModal: () => set({ isConnectModalOpen: false }),
  setActiveTab: (tab) => set({ activeTab: tab }),
}));
