export interface User {
  id: string;
  email: string;
  display_name: string;
  github_user_id?: string;
  avatar_url?: string;
  role: 'owner' | 'admin' | 'member' | 'viewer';
}

export interface Repository {
  id: string;
  organization_id: string;
  github_repo_id: string;
  owner: string;
  name: string;
  full_name?: string;
  clone_url: string;
  default_branch: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Run {
  id: string;
  repository_id: string;
  event_type: string;
  status: 'queued' | 'running' | 'completed' | 'failed' | 'interrupted';
  commit_sha: string;
  branch?: string;
  webhook_delivery_id?: string;
  plan_summary?: string;
  created_at: string;
  updated_at: string;
}

export interface Page<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface WebhookAcceptedResponse {
  accepted: boolean;
  duplicate: boolean;
  run_id?: string;
}
