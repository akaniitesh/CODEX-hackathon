import { create } from 'zustand';
import { User } from '@/lib/types';

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoginModalOpen: boolean;
  setToken: (token: string | null) => void;
  setUser: (user: User | null) => void;
  openLoginModal: () => void;
  closeLoginModal: () => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: typeof window !== 'undefined' ? localStorage.getItem('access_token') : null,
  user: {
    id: 'demo-user-1',
    email: 'engineer@autose.dev',
    display_name: 'Principal AI Engineer',
    role: 'owner',
    avatar_url: 'https://github.com/github.png',
  },
  isAuthenticated: true,
  isLoginModalOpen: false,
  setToken: (token) => {
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
    set({ token, isAuthenticated: !!token });
  },
  setUser: (user) => set({ user }),
  openLoginModal: () => set({ isLoginModalOpen: true }),
  closeLoginModal: () => set({ isLoginModalOpen: false }),
  logout: () => {
    localStorage.removeItem('access_token');
    set({ token: null, user: null, isAuthenticated: false });
  },
}));
