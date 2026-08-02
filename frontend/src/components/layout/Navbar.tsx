'use client';

import React, { useState } from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import { useRepoStore } from '@/store/useRepoStore';
import {
  Activity,
  Bot,
  Cpu,
  GitBranch,
  Layers,
  LogOut,
  Plus,
  ShieldAlert,
  Zap,
  Presentation,
  ShieldCheck,
  Key,
} from 'lucide-react';
import { GithubIcon } from '@/components/icons/GithubIcon';
import { ProviderKeyModal } from '@/components/settings/ProviderKeyModal';

export function Navbar() {
  const { user, logout, openLoginModal } = useAuthStore();
  const { selectedRepo, openConnectModal, activeTab, setActiveTab } = useRepoStore();
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);

  const navItems = [
    { id: 'repositories', label: 'Repositories', icon: Layers },
    { id: 'timeline', label: 'Realtime Timeline', icon: Activity },
    { id: 'graph', label: 'Graph Trace', icon: Bot },
    { id: 'reviews', label: 'Reviews & Findings', icon: ShieldAlert },
    { id: 'architecture', label: 'Architecture', icon: Cpu },
    { id: 'analytics', label: 'Cost & Health', icon: Zap },
    { id: 'presentation', label: 'Presentation Deck', icon: Presentation },
  ] as const;

  return (
    <>
      <header className="sticky top-0 z-40 w-full glass-panel border-b border-white/10 px-4 lg:px-8 py-3 backdrop-blur-xl">
        <div className="flex items-center justify-between gap-4">
          {/* Brand & Repository Selector */}
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('repositories')}>
              <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-emerald-500 to-cyan-400 p-[1px] shadow-lg shadow-indigo-500/20">
                <div className="flex h-full w-full items-center justify-center rounded-[11px] bg-slate-950">
                  <ShieldCheck className="h-5 w-5 text-cyan-400" />
                </div>
              </div>
              <div>
                <span className="font-extrabold tracking-tight text-white text-lg bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-slate-300">
                  Aegis AI
                </span>
                <span className="ml-2.5 text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  v0.2.0 Engine
                </span>
              </div>
            </div>

            {/* Selected Repo Badge */}
            {selectedRepo && (
              <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-white/10 text-xs text-slate-300 shadow-inner">
                <GitBranch className="h-3.5 w-3.5 text-indigo-400" />
                <span className="font-mono font-medium text-slate-200">{selectedRepo.owner}/{selectedRepo.name}</span>
                <span className="text-slate-500">•</span>
                <span className="font-mono text-emerald-400">{selectedRepo.default_branch}</span>
              </div>
            )}
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden xl:flex items-center gap-1 bg-slate-900/80 p-1 rounded-xl border border-white/5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer ${
                    isActive
                      ? 'bg-indigo-600/90 text-white shadow-md shadow-indigo-500/20'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className={`h-3.5 w-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Right Actions & Profile */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* AI Provider Keys Button */}
            <button
              onClick={() => setIsKeyModalOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-indigo-500/30 text-indigo-300 hover:text-white text-xs font-medium transition-all cursor-pointer"
              title="Configure User AI Provider Keys (Gemini, OpenAI, Claude, Groq, OpenRouter, Ollama)"
            >
              <Key className="h-3.5 w-3.5 text-indigo-400" />
              <span className="hidden sm:inline">AI Keys</span>
            </button>

            <button
              onClick={openConnectModal}
              className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-lg shadow-emerald-600/20 transition-all cursor-pointer"
            >
              <Plus className="h-4 w-4" />
              <span className="hidden sm:inline">Connect Repo</span>
            </button>

            {user ? (
              <div className="flex items-center gap-3 pl-2 border-l border-white/10">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={user.avatar_url || 'https://github.com/github.png'}
                  alt={user.display_name}
                  className="h-8 w-8 rounded-full border border-indigo-500/30 object-cover shadow-sm"
                />
                <div className="hidden sm:block text-left">
                  <p className="text-xs font-semibold text-slate-200 leading-none">{user.display_name}</p>
                  <span className="text-[10px] font-mono text-indigo-400 capitalize">@{user.github_user_id || 'github'}</span>
                </div>
                <button
                  onClick={logout}
                  title="Sign Out"
                  className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors cursor-pointer"
                >
                  <LogOut className="h-4 w-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={openLoginModal}
                className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-all cursor-pointer border border-white/10"
              >
                <GithubIcon className="h-4 w-4 text-white" />
                <span>Sign In with GitHub</span>
              </button>
            )}
          </div>
        </div>
      </header>

      <ProviderKeyModal isOpen={isKeyModalOpen} onClose={() => setIsKeyModalOpen(false)} />
    </>
  );
}
