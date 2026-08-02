import { create } from 'zustand';
import { Repository } from '@/lib/types';

const INITIAL_USER_REPO: Repository = {
  id: 'repo-1',
  organization_id: 'org-1',
  github_repo_id: '1314878652',
  owner: 'akaniitesh',
  name: 'CODEX-hackathon',
  full_name: 'akaniitesh/CODEX-hackathon',
  clone_url: 'https://github.com/akaniitesh/CODEX-hackathon.git',
  default_branch: 'main',
  is_active: true,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
};

const getInitialRepos = (): Repository[] => {
  if (typeof window === 'undefined') return [INITIAL_USER_REPO];
  const stored = localStorage.getItem('user_repos');
  if (stored) {
    try {
      const parsed = JSON.parse(stored);
      if (Array.isArray(parsed) && parsed.length > 0) {
        return parsed;
      }
    } catch {
      // Fallback
    }
  }
  return [INITIAL_USER_REPO];
};

interface RepoState {
  repositories: Repository[];
  selectedRepo: Repository | null;
  isConnectModalOpen: boolean;
  activeTab: 'repositories' | 'timeline' | 'graph' | 'reviews' | 'architecture' | 'analytics' | 'presentation';
  setSelectedRepo: (repo: Repository | null) => void;
  addRepository: (repo: Repository) => void;
  deleteRepository: (id: string) => void;
  openConnectModal: () => void;
  closeConnectModal: () => void;
  setActiveTab: (tab: RepoState['activeTab']) => void;
}

export const useRepoStore = create<RepoState>((set, get) => ({
  repositories: getInitialRepos(),
  selectedRepo: getInitialRepos()[0] || null,
  isConnectModalOpen: false,
  activeTab: 'repositories',
  setSelectedRepo: (repo) => set({ selectedRepo: repo }),
  addRepository: (repo) => {
    const updated = [repo, ...get().repositories.filter((r) => r.full_name !== repo.full_name)];
    if (typeof window !== 'undefined') {
      localStorage.setItem('user_repos', JSON.stringify(updated));
    }
    set({ repositories: updated, selectedRepo: repo });
  },
  deleteRepository: (id) => {
    const updated = get().repositories.filter((r) => r.id !== id);
    if (typeof window !== 'undefined') {
      localStorage.setItem('user_repos', JSON.stringify(updated));
    }
    const nextSelected = get().selectedRepo?.id === id ? (updated[0] || null) : get().selectedRepo;
    set({ repositories: updated, selectedRepo: nextSelected });
  },
  openConnectModal: () => set({ isConnectModalOpen: true }),
  closeConnectModal: () => set({ isConnectModalOpen: false }),
  setActiveTab: (tab) => set({ activeTab: tab }),
}));
