'use client';

import React, { useState } from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import { GitBranch, GitPullRequest, Plus, X } from 'lucide-react';
import { GithubIcon } from '@/components/icons/GithubIcon';

export function ConnectRepoModal() {
  const { isConnectModalOpen, closeConnectModal, setSelectedRepo } = useRepoStore();
  const [repoUrl, setRepoUrl] = useState('');
  const [branch, setBranch] = useState('main');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isConnectModalOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!repoUrl) return;

    setIsSubmitting(true);
    setTimeout(() => {
      const parts = repoUrl.replace('https://github.com/', '').replace('.git', '').split('/');
      const owner = parts[0] || 'enterprise-org';
      const name = parts[1] || 'custom-repo';

      const newRepo = {
        id: `repo-${Date.now()}`,
        organization_id: 'org-1',
        github_repo_id: String(Math.floor(Math.random() * 900000) + 100000),
        owner,
        name,
        full_name: `${owner}/${name}`,
        clone_url: repoUrl,
        default_branch: branch,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      setSelectedRepo(newRepo);
      setIsSubmitting(false);
      closeConnectModal();
    }, 600);
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="connect-repo-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in"
    >
      <div className="relative w-full max-w-lg glass-panel rounded-2xl p-6 border border-white/10 shadow-2xl space-y-6">
        <button
          onClick={closeConnectModal}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center">
            <Plus className="h-5 w-5 text-emerald-400" />
          </div>
          <div>
            <h2 id="connect-repo-title" className="text-lg font-bold text-white tracking-tight">
              Connect Repository
            </h2>
            <p className="text-xs text-slate-400">
              Provide GitHub repository details to initiate autonomous agent orchestration.
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Repository URL or Full Name
            </label>
            <div className="relative">
              <GithubIcon className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="https://github.com/org/repo-name"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                required
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900/90 border border-white/10 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Default Branch
            </label>
            <div className="relative">
              <GitBranch className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="main"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900/90 border border-white/10 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono"
              />
            </div>
          </div>

          <div className="pt-2 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={closeConnectModal}
              className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-all"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex items-center gap-2 px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-lg shadow-emerald-600/20 transition-all disabled:opacity-50 cursor-pointer"
            >
              {isSubmitting ? 'Connecting...' : 'Connect & Index'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
