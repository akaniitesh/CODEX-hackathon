import { create } from 'zustand';
import { Repository } from '@/lib/types';

const DEFAULT_REPOS: Repository[] = [
  {
    id: 'repo-1',
    organization_id: 'org-1',
    github_repo_id: '992817',
    owner: 'akaniitesh',
    name: 'CODEX-hackathon',
    full_name: 'akaniitesh/CODEX-hackathon',
    clone_url: 'https://github.com/akaniitesh/CODEX-hackathon.git',
    default_branch: 'main',
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 'repo-2',
    organization_id: 'org-1',
    github_repo_id: '883719',
    owner: 'enterprise-org',
    name: 'aegis-ai-engine',
    full_name: 'enterprise-org/aegis-ai-engine',
    clone_url: 'https://github.com/enterprise-org/aegis-ai-engine.git',
    default_branch: 'main',
    is_active: true,
    created_at: new Date(Date.now() - 86400000 * 5).toISOString(),
    updated_at: new Date().toISOString(),
  },
];

const getInitialRepos = (): Repository[] => {
  if (typeof window === 'undefined') return DEFAULT_REPOS;
  const stored = localStorage.getItem('user_repos');
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      // Fallback
    }
  }
  return DEFAULT_REPOS;
};

interface RepoState {
  repositories: Repository[];
  selectedRepo: Repository | null;
  isConnectModalOpen: boolean;
  activeTab: 'repositories' | 'timeline' | 'graph' | 'reviews' | 'architecture' | 'analytics' | 'presentation';
  setSelectedRepo: (repo: Repository | null) => void;
  addRepository: (repo: Repository) => void;
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
  openConnectModal: () => set({ isConnectModalOpen: true }),
  closeConnectModal: () => set({ isConnectModalOpen: false }),
  setActiveTab: (tab) => set({ activeTab: tab }),
}));
