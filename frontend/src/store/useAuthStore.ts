import { create } from 'zustand';

export interface AuthUser {
  id: string;
  login: string;
  display_name: string;
  avatar_url: string;
  github_user_id?: string;
  email?: string;
}

interface AuthState {
  user: AuthUser | null;
  token: string | null;
  isLoginModalOpen: boolean;
  isLoading: boolean;
  error: string | null;
  openLoginModal: () => void;
  closeLoginModal: () => void;
  logout: () => void;
  clearError: () => void;
  loginWithGitHubUser: (user: AuthUser, token?: string) => void;
  loginWithGitHubToken: (patToken: string) => Promise<boolean>;
}

const getInitialUser = (): AuthUser | null => {
  if (typeof window === 'undefined') return null;
  const stored = localStorage.getItem('auth_user');
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      // Fallback
    }
  }
  return {
    id: 'gh-lead-ai',
    login: 'nitesh_kumar',
    display_name: 'Nitesh Kumar',
    avatar_url: 'https://github.com/akaniitesh.png',
    github_user_id: 'akaniitesh',
  };
};

const getInitialToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
};

export const useAuthStore = create<AuthState>((set) => ({
  user: getInitialUser(),
  token: getInitialToken(),
  isLoginModalOpen: false,
  isLoading: false,
  error: null,
  openLoginModal: () => set({ isLoginModalOpen: true, error: null }),
  closeLoginModal: () => set({ isLoginModalOpen: false, error: null }),
  clearError: () => set({ error: null }),
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_user');
      localStorage.removeItem('auth_token');
    }
    set({ user: null, token: null });
  },
  loginWithGitHubUser: (user, token) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_user', JSON.stringify(user));
      if (token) {
        localStorage.setItem('auth_token', token);
      }
    }
    set({ user, token: token || null, isLoginModalOpen: false, error: null });
  },
  loginWithGitHubToken: async (patToken: string): Promise<boolean> => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('https://api.github.com/user', {
        headers: {
          Authorization: `token ${patToken}`,
          Accept: 'application/vnd.github.v3+json',
        },
      });

      if (!response.ok) {
        throw new Error('Invalid Personal Access Token or network error.');
      }

      const data = await response.json();
      const userObj: AuthUser = {
        id: String(data.id || `gh-${Date.now()}`),
        login: data.login,
        display_name: data.name || data.login,
        avatar_url: data.avatar_url || 'https://github.com/github.png',
        github_user_id: data.login,
        email: data.email || undefined,
      };

      if (typeof window !== 'undefined') {
        localStorage.setItem('auth_user', JSON.stringify(userObj));
        localStorage.setItem('auth_token', patToken);
      }

      set({
        user: userObj,
        token: patToken,
        isLoading: false,
        isLoginModalOpen: false,
        error: null,
      });
      return true;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to authenticate with GitHub API.';
      set({
        isLoading: false,
        error: msg,
      });
      return false;
    }
  },
}));
