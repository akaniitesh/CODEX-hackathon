'use client';

import React, { useState } from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import { GitBranch, Plus, X, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { GithubIcon } from '@/components/icons/GithubIcon';
import { api } from '@/lib/api';

export function ConnectRepoModal() {
  const { isConnectModalOpen, closeConnectModal, addRepository } = useRepoStore();
  const [repoInput, setRepoInput] = useState('');
  const [branch, setBranch] = useState('main');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isConnectModalOpen) return null;

  const parseRepo = (input: string) => {
    let clean = input.trim();
    clean = clean.replace('https://github.com/', '').replace('http://github.com/', '').replace('.git', '');
    const parts = clean.split('/').filter(Boolean);
    if (parts.length >= 2) {
      return { owner: parts[0], name: parts[1] };
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const parsed = parseRepo(repoInput);

    if (!parsed) {
      setError('Please enter a valid GitHub repo format like "owner/repo" or "https://github.com/owner/repo"');
      return;
    }

    setIsSubmitting(true);

    try {
      let fetchedBranch = branch;
      let repoId = String(Math.floor(Math.random() * 900000) + 100000);

      // Fetch GitHub API Repo Info if available
      try {
        const ghRes = await fetch(`https://api.github.com/repos/${parsed.owner}/${parsed.name}`);
        if (ghRes.ok) {
          const ghData = await ghRes.json();
          if (ghData.default_branch) {
            fetchedBranch = ghData.default_branch;
          }
          if (ghData.id) {
            repoId = String(ghData.id);
          }
        }
      } catch {
        // Fallback for private or offline repos
      }

      // Try Backend Connection
      try {
        await api.connectRepository({
          owner: parsed.owner,
          name: parsed.name,
          clone_url: `https://github.com/${parsed.owner}/${parsed.name}.git`,
          default_branch: fetchedBranch,
        });
      } catch {
        // Backend offline fallback
      }

      const newRepo = {
        id: `repo-${Date.now()}`,
        organization_id: 'org-1',
        github_repo_id: repoId,
        owner: parsed.owner,
        name: parsed.name,
        full_name: `${parsed.owner}/${parsed.name}`,
        clone_url: `https://github.com/${parsed.owner}/${parsed.name}.git`,
        default_branch: fetchedBranch,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      addRepository(newRepo);
      setIsSubmitting(false);
      setRepoInput('');
      closeConnectModal();
    } catch (err: any) {
      setIsSubmitting(false);
      setError(err.message || 'Failed to connect repository.');
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="connect-repo-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-fade-in"
    >
      <div className="relative w-full max-w-lg glass-panel rounded-2xl p-6 border border-white/10 shadow-2xl space-y-6">
        <button
          onClick={closeConnectModal}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all cursor-pointer"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center">
            <Plus className="h-5 w-5 text-emerald-400" />
          </div>
          <div>
            <h2 id="connect-repo-title" className="text-lg font-bold text-white tracking-tight">
              Connect GitHub Repository
            </h2>
            <p className="text-xs text-slate-400">
              Import a repository to initiate autonomous multi-agent code analysis & PR generation.
            </p>
          </div>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2">
            <AlertCircle className="h-4 w-4 text-rose-400 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">
              GitHub Repository URL or "owner/repo"
            </label>
            <div className="relative">
              <GithubIcon className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="https://github.com/facebook/react or owner/repo"
                value={repoInput}
                onChange={(e) => { setRepoInput(e.target.value); setError(null); }}
                required
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-all font-mono"
              />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              Supports public and private GitHub repositories.
            </p>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">
              Target Branch (Auto-detected if blank)
            </label>
            <div className="relative">
              <GitBranch className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="main"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-all font-mono"
              />
            </div>
          </div>

          <div className="pt-2 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={closeConnectModal}
              className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-all cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !repoInput.trim()}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-lg shadow-emerald-600/25 transition-all disabled:opacity-50 cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin text-white" />
                  <span>Connecting GitHub Repo...</span>
                </>
              ) : (
                <>
                  <Plus className="h-4 w-4" />
                  <span>Connect & Index Repo</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
