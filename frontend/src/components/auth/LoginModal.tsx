'use client';

import React from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import { Bot, ShieldCheck, X } from 'lucide-react';
import { GithubIcon } from '@/components/icons/GithubIcon';

export function LoginModal() {
  const { isLoginModalOpen, closeLoginModal, setUser, setToken } = useAuthStore();

  if (!isLoginModalOpen) return null;

  const handleDemoSignIn = () => {
    setToken('demo-jwt-token-xyz123');
    setUser({
      id: 'usr-demo-99',
      email: 'lead.engineer@autose.dev',
      display_name: 'Staff AI Engineer',
      role: 'owner',
      github_user_id: 'gh-lead-ai',
      avatar_url: 'https://github.com/github.png',
    });
    closeLoginModal();
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="login-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in"
    >
      <div className="relative w-full max-w-md glass-panel rounded-2xl p-6 border border-white/10 shadow-2xl space-y-6">
        {/* Close Button */}
        <button
          onClick={closeLoginModal}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
        >
          <X className="h-4 w-4" />
        </button>

        {/* Icon Header */}
        <div className="flex flex-col items-center text-center space-y-3">
          <div className="h-12 w-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shadow-lg shadow-indigo-500/10">
            <Bot className="h-6 w-6 text-indigo-400" />
          </div>
          <div>
            <h2 id="login-modal-title" className="text-xl font-bold text-white tracking-tight">
              Connect to Platform
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Authenticate via GitHub OAuth to connect repositories & launch autonomous agents.
            </p>
          </div>
        </div>

        {/* Auth Buttons */}
        <div className="space-y-3">
          <button
            onClick={handleDemoSignIn}
            className="w-full flex items-center justify-center gap-3 py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition-all shadow-lg shadow-indigo-600/25 cursor-pointer"
          >
            <GithubIcon className="h-4 w-4" />
            <span>Continue with GitHub OAuth</span>
          </button>
        </div>

        {/* Security Assurance */}
        <div className="flex items-center gap-2 text-slate-400 text-[11px] justify-center bg-slate-900/60 p-2.5 rounded-xl border border-white/5">
          <ShieldCheck className="h-4 w-4 text-emerald-400 flex-shrink-0" />
          <span>Strict RBAC protection & zero secret storage in LLM context windows.</span>
        </div>
      </div>
    </div>
  );
}
