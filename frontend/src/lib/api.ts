import { Page, Repository, Run } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    throw new ApiError(response.status, errorData.detail || 'API request failed');
  }

  return response.json();
}

export const api = {
  // Auth
  getGitHubOAuthUrl: (state?: string) =>
    request<{ authorization_url: string }>(`/auth/github/start${state ? `?state=${state}` : ''}`),

  exchangeGitHubCode: (code: string) =>
    request<{ access_token: string }>('/auth/github/callback', {
      method: 'POST',
      body: JSON.stringify({ code }),
    }),

  // Repositories
  listRepositories: (limit = 50, offset = 0) =>
    request<Page<Repository>>(`/repositories?limit=${limit}&offset=${offset}`),

  connectRepository: (data: { owner: string; name: string; clone_url: string; default_branch?: string }) =>
    request<Repository>('/repositories', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Runs
  listRepositoryRuns: (repositoryId: string, limit = 50, offset = 0) =>
    request<Page<Run>>(`/runs/repositories/${repositoryId}?limit=${limit}&offset=${offset}`),

  triggerRun: (repositoryId: string, commitSha: string, branch = 'main') =>
    request<{ run_id: string }>('/runs', {
      method: 'POST',
      body: JSON.stringify({ repository_id: repositoryId, commit_sha: commitSha, branch }),
    }),
};
