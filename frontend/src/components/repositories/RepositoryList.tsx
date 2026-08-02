'use client';

import React, { useState } from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import { Repository } from '@/lib/types';
import {
  Clock,
  GitBranch,
  Play,
  Plus,
  Search,
  Bot,
  ExternalLink,
  Trash2,
} from 'lucide-react';
import { GithubIcon } from '@/components/icons/GithubIcon';

export function RepositoryList() {
  const { repositories, selectedRepo, setSelectedRepo, deleteRepository, openConnectModal, setActiveTab } = useRepoStore();
  const [search, setSearch] = useState('');

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
              className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-mono transition-all"
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
                    <h3 className="text-sm font-bold text-white tracking-tight group-hover:text-indigo-300 transition-colors flex items-center gap-1.5">
                      <span>{repo.name}</span>
                      <a
                        href={`https://github.com/${repo.owner}/${repo.name}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="text-slate-500 hover:text-indigo-400 transition-colors"
                      >
                        <ExternalLink className="h-3 w-3" />
                      </a>
                    </h3>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    Active
                  </span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteRepository(repo.id);
                    }}
                    className="p-1 text-slate-500 hover:text-rose-400 transition-colors cursor-pointer"
                    title="Disconnect Repository"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </button>
                </div>
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
                    Indexed
                  </span>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
                  <span>ID: #{repo.github_repo_id}</span>
                  <span className="text-emerald-400">AST Verified</span>
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
                  <span>Launch Agent Run</span>
                </button>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedRepo(repo);
                    setActiveTab('graph');
                  }}
                  className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors cursor-pointer"
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
