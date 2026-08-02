import { Page, Repository, Run } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
  const headers = new Headers(options.headers || {});
  headers.set('Content-Type', 'application/json');
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorText = await response.text();
    let errorMessage = `HTTP error! status: ${response.status}`;
    try {
      const errorJson = JSON.parse(errorText);
      errorMessage = errorJson.detail || errorJson.message || errorMessage;
    } catch {
      // Use fallback error message
    }
    throw new ApiError(response.status, errorMessage);
  }

  return response.json();
}

export const api = {
  getGitHubOAuthUrl: async (): Promise<{ authorization_url: string; state: string }> => {
    return fetchApi<{ authorization_url: string; state: string }>('/auth/github/start');
  },
  exchangeGitHubCode: async (code: string): Promise<{ access_token: string; token_type: string }> => {
    return fetchApi<{ access_token: string; token_type: string }>('/auth/github/callback', {
      method: 'POST',
      body: JSON.stringify({ code }),
    });
  },
  connectRepository: async (repo: { owner: string; name: string; clone_url: string; default_branch: string }): Promise<Repository> => {
    return fetchApi<Repository>('/repositories', {
      method: 'POST',
      body: JSON.stringify(repo),
    });
  },
  getRepositories: async (): Promise<Page<Repository>> => {
    return fetchApi<Page<Repository>>('/repositories');
  },
  triggerRun: async (repoId: string, options?: { prompt?: string }): Promise<Run> => {
    return fetchApi<Run>(`/repositories/${repoId}/runs`, {
      method: 'POST',
      body: JSON.stringify(options || {}),
    });
  },
};
