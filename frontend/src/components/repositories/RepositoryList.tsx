'use client';

import React, { useState } from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import { Repository } from '@/lib/types';
import {
  Activity,
  Bot,
  CheckCircle2,
  Clock,
  GitBranch,
  Play,
  Plus,
  Search,
  ShieldCheck,
  Zap,
} from 'lucide-react';
import { GithubIcon } from '@/components/icons/GithubIcon';

const MOCK_REPOSITORIES: Repository[] = [
  {
    id: 'repo-demo-1',
    organization_id: 'org-1',
    github_repo_id: '992817',
    owner: 'enterprise-org',
    name: 'autonomous-platform',
    full_name: 'enterprise-org/autonomous-platform',
    clone_url: 'https://github.com/enterprise-org/autonomous-platform.git',
    default_branch: 'main',
    is_active: true,
    created_at: new Date(Date.now() - 86400000 * 5).toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 'repo-demo-2',
    organization_id: 'org-1',
    github_repo_id: '883719',
    owner: 'enterprise-org',
    name: 'payments-microservice',
    full_name: 'enterprise-org/payments-microservice',
    clone_url: 'https://github.com/enterprise-org/payments-microservice.git',
    default_branch: 'master',
    is_active: true,
    created_at: new Date(Date.now() - 86400000 * 12).toISOString(),
    updated_at: new Date(Date.now() - 3600000 * 4).toISOString(),
  },
  {
    id: 'repo-demo-3',
    organization_id: 'org-1',
    github_repo_id: '772615',
    owner: 'enterprise-org',
    name: 'auth-rbac-service',
    full_name: 'enterprise-org/auth-rbac-service',
    clone_url: 'https://github.com/enterprise-org/auth-rbac-service.git',
    default_branch: 'main',
    is_active: true,
    created_at: new Date(Date.now() - 86400000 * 30).toISOString(),
    updated_at: new Date(Date.now() - 86400000).toISOString(),
  },
];

export function RepositoryList() {
  const { selectedRepo, setSelectedRepo, openConnectModal, setActiveTab } = useRepoStore();
  const [search, setSearch] = useState('');
  const [repositories] = useState<Repository[]>(MOCK_REPOSITORIES);

  const filtered = repositories.filter(
    (repo) =>
      repo.name.toLowerCase().includes(search.toLowerCase()) ||
      repo.owner.toLowerCase().includes(search.toLowerCase())
  );

  const handleTriggerRun = (repo: Repository) => {
    setSelectedRepo(repo);
    setActiveTab('timeline');
  };

  return (
    <div className="space-y-6">
      {/* Header Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Connected Repositories</h1>
          <p className="text-xs text-slate-400 mt-1">
            Manage repos, launch autonomous execution pipelines, and trace multi-agent reasoning.
          </p>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
            <input
              type="text"
              placeholder="Search repositories..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-900/90 border border-white/10 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <button
            onClick={openConnectModal}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-lg shadow-emerald-600/20 transition-all cursor-pointer whitespace-nowrap"
          >
            <Plus className="h-4 w-4" />
            <span>Connect Repo</span>
          </button>
        </div>
      </div>

      {/* Grid of Repository Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filtered.map((repo) => {
          const isSelected = selectedRepo?.id === repo.id;
          return (
            <div
              key={repo.id}
              onClick={() => setSelectedRepo(repo)}
              className={`group glass-panel rounded-2xl p-5 border transition-all cursor-pointer ${
                isSelected
                  ? 'border-indigo-500/60 bg-slate-900/90 shadow-xl shadow-indigo-500/10'
                  : 'border-white/10 hover:border-white/20 glass-panel-hover'
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-xl bg-slate-800 border border-white/10 flex items-center justify-center group-hover:border-indigo-500/30 transition-colors">
                    <GithubIcon className="h-5 w-5 text-slate-300 group-hover:text-indigo-400 transition-colors" />
                  </div>
                  <div>
                    <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">{repo.owner}</span>
                    <h3 className="text-sm font-bold text-white tracking-tight group-hover:text-indigo-300 transition-colors">
                      {repo.name}
                    </h3>
                  </div>
                </div>

                <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Active
                </span>
              </div>

              {/* Repo Details */}
              <div className="mt-4 pt-4 border-t border-white/5 space-y-2">
                <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
                  <span className="flex items-center gap-1.5">
                    <GitBranch className="h-3.5 w-3.5 text-indigo-400" />
                    {repo.default_branch}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="h-3.5 w-3.5 text-slate-500" />
                    Indexed 2h ago
                  </span>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-400">
                  <span>AST Symbols: 142</span>
                  <span>Safety Scans: Clean</span>
                </div>
              </div>

              {/* Card Actions */}
              <div className="mt-5 flex items-center gap-2">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleTriggerRun(repo);
                  }}
                  className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/20 transition-all cursor-pointer"
                >
                  <Play className="h-3.5 w-3.5 fill-current" />
                  <span>Launch Run</span>
                </button>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedRepo(repo);
                    setActiveTab('graph');
                  }}
                  className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
                  title="View LangGraph Execution Shape"
                >
                  <Bot className="h-4 w-4" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
