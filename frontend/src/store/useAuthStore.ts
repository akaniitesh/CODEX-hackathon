import { create } from 'zustand';
import { User } from '@/lib/types';

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoginModalOpen: boolean;
  isLoading: boolean;
  error: string | null;
  setToken: (token: string | null) => void;
  setUser: (user: User | null) => void;
  openLoginModal: () => void;
  closeLoginModal: () => void;
  loginWithGitHubToken: (token: string) => Promise<boolean>;
  loginWithGitHubUser: (profile: {
    id: string;
    login: string;
    display_name: string;
    email?: string;
    avatar_url: string;
  }, token?: string) => void;
  logout: () => void;
  clearError: () => void;
}

const getInitialUser = (): User | null => {
  if (typeof window === 'undefined') return null;
  const storedUser = localStorage.getItem('auth_user');
  if (storedUser) {
    try {
      return JSON.parse(storedUser);
    } catch {
      // Fallback
    }
  }
  return {
    id: 'demo-user-1',
    email: 'engineer@autose.dev',
    display_name: 'Principal AI Engineer',
    role: 'owner',
    github_user_id: 'gh-lead-ai',
    avatar_url: 'https://github.com/github.png',
  };
};

const getInitialToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token') || 'demo-jwt-token-xyz123';
};

export const useAuthStore = create<AuthState>((set) => ({
  token: getInitialToken(),
  user: getInitialUser(),
  isAuthenticated: true,
  isLoginModalOpen: false,
  isLoading: false,
  error: null,
  setToken: (token) => {
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
    set({ token, isAuthenticated: !!token });
  },
  setUser: (user) => {
    if (user) {
      localStorage.setItem('auth_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('auth_user');
    }
    set({ user });
  },
  openLoginModal: () => set({ isLoginModalOpen: true, error: null }),
  closeLoginModal: () => set({ isLoginModalOpen: false, error: null }),
  clearError: () => set({ error: null }),
  loginWithGitHubUser: (profile, token) => {
    const user: User = {
      id: profile.id || `gh-${profile.login}`,
      email: profile.email || `${profile.login}@users.noreply.github.com`,
      display_name: profile.display_name || profile.login,
      role: 'owner',
      github_user_id: profile.login,
      avatar_url: profile.avatar_url || `https://github.com/${profile.login}.png`,
    };
    const jwtToken = token || `gh-token-${Date.now()}`;
    localStorage.setItem('access_token', jwtToken);
    localStorage.setItem('auth_user', JSON.stringify(user));
    set({
      token: jwtToken,
      user,
      isAuthenticated: true,
      isLoginModalOpen: false,
      error: null,
    });
  },
  loginWithGitHubToken: async (githubToken: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('https://api.github.com/user', {
        headers: {
          Authorization: `Bearer ${githubToken.trim()}`,
          Accept: 'application/vnd.github.v3+json',
        },
      });

      if (!response.ok) {
        throw new Error('Invalid GitHub token or authentication failed.');
      }

      const data = await response.json();
      const user: User = {
        id: String(data.id),
        email: data.email || `${data.login}@users.noreply.github.com`,
        display_name: data.name || data.login,
        role: 'owner',
        github_user_id: data.login,
        avatar_url: data.avatar_url,
      };

      localStorage.setItem('access_token', githubToken.trim());
      localStorage.setItem('auth_user', JSON.stringify(user));

      set({
        token: githubToken.trim(),
        user,
        isAuthenticated: true,
        isLoginModalOpen: false,
        isLoading: false,
        error: null,
      });
      return true;
    } catch (err: any) {
      set({
        isLoading: false,
        error: err.message || 'Failed to authenticate with GitHub API.',
      });
      return false;
    }
  },
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('auth_user');
    set({ token: null, user: null, isAuthenticated: false });
  },
}));
