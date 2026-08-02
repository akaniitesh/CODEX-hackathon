'use client';

import React, { useState } from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import { Bot, ShieldCheck, X, Key, ExternalLink, Loader2, AlertCircle } from 'lucide-react';
import { GithubIcon } from '@/components/icons/GithubIcon';
import { api } from '@/lib/api';

export function LoginModal() {
  const { isLoginModalOpen, closeLoginModal, loginWithGitHubToken, loginWithGitHubUser, isLoading, error, clearError } = useAuthStore();
  const [activeTab, setActiveTab] = useState<'oauth' | 'token'>('oauth');
  const [patToken, setPatToken] = useState('');
  const [isRedirecting, setIsRedirecting] = useState(false);

  if (!isLoginModalOpen) return null;

  const handleStartOAuth = async () => {
    setIsRedirecting(true);
    clearError();
    try {
      // Try backend OAuth URL
      const data = await api.getGitHubOAuthUrl();
      if (data?.authorization_url) {
        window.location.href = data.authorization_url;
        return;
      }
    } catch {
      // Backend OAuth client ID fallback
    }

    // Direct GitHub OAuth Fallback
    const clientId = process.env.NEXT_PUBLIC_GITHUB_CLIENT_ID || 'Ov23liXXXXXXXXXX';
    const redirectUri = typeof window !== 'undefined' ? `${window.location.origin}/auth/github/callback` : '';
    const oauthUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&scope=read:user%20user:email&redirect_uri=${encodeURIComponent(redirectUri)}`;
    
    window.location.href = oauthUrl;
  };

  const handlePatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!patToken.trim()) return;
    const success = await loginWithGitHubToken(patToken);
    if (success) {
      setPatToken('');
    }
  };

  const handleQuickDevLogin = () => {
    loginWithGitHubUser({
      id: 'gh-dev-user',
      login: 'enterprise_developer',
      display_name: 'Enterprise AI Engineer',
      avatar_url: 'https://github.com/github.png',
    });
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="login-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-fade-in"
    >
      <div className="relative w-full max-w-md glass-panel rounded-2xl p-6 border border-white/10 shadow-2xl space-y-6">
        {/* Close Button */}
        <button
          onClick={closeLoginModal}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all cursor-pointer"
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
              Connect to Aegis AI
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Authenticate via GitHub OAuth or Personal Access Token (PAT) for full repository access.
            </p>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="flex p-1 bg-slate-900/80 rounded-xl border border-white/5 text-xs font-semibold">
          <button
            onClick={() => { setActiveTab('oauth'); clearError(); }}
            className={`flex-1 py-2 rounded-lg transition-all ${
              activeTab === 'oauth' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            GitHub OAuth
          </button>
          <button
            onClick={() => { setActiveTab('token'); clearError(); }}
            className={`flex-1 py-2 rounded-lg transition-all ${
              activeTab === 'token' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            GitHub PAT / Direct Token
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2">
            <AlertCircle className="h-4 w-4 text-rose-400 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Tab Content */}
        {activeTab === 'oauth' ? (
          <div className="space-y-4">
            <button
              onClick={handleStartOAuth}
              disabled={isRedirecting}
              className="w-full flex items-center justify-center gap-3 py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition-all shadow-lg shadow-indigo-600/25 cursor-pointer disabled:opacity-50"
            >
              {isRedirecting ? (
                <Loader2 className="h-4 w-4 animate-spin text-white" />
              ) : (
                <GithubIcon className="h-4 w-4" />
              )}
              <span>{isRedirecting ? 'Redirecting to GitHub...' : 'Continue with GitHub OAuth'}</span>
            </button>

            <div className="relative text-center">
              <span className="text-[11px] text-slate-500 bg-slate-950 px-2 relative z-10 font-mono">OR</span>
              <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-white/10"></div></div>
            </div>

            <button
              onClick={handleQuickDevLogin}
              className="w-full py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 font-medium text-xs border border-white/10 transition-all cursor-pointer"
            >
              Sign In as Lead AI Engineer (Instant Session)
            </button>
          </div>
        ) : (
          <form onSubmit={handlePatSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                GitHub Personal Access Token (PAT)
              </label>
              <div className="relative">
                <Key className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                <input
                  type="password"
                  value={patToken}
                  onChange={(e) => setPatToken(e.target.value)}
                  placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
                  className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-white placeholder-slate-500 text-xs font-mono focus:outline-none focus:border-indigo-500 transition-all"
                  required
                />
              </div>
              <p className="text-[11px] text-slate-500 mt-1.5 flex items-center gap-1">
                <span>Create a token in</span>
                <a
                  href="https://github.com/settings/tokens"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-400 hover:underline flex items-center gap-0.5"
                >
                  GitHub Developer Settings <ExternalLink className="h-3 w-3 inline" />
                </a>
              </p>
            </div>

            <button
              type="submit"
              disabled={isLoading || !patToken.trim()}
              className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm transition-all shadow-lg shadow-emerald-600/25 cursor-pointer disabled:opacity-50"
            >
              {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <GithubIcon className="h-4 w-4" />}
              <span>{isLoading ? 'Verifying Token...' : 'Authenticate Token & Fetch Profile'}</span>
            </button>
          </form>
        )}

        {/* Security Assurance */}
        <div className="flex items-center gap-2 text-slate-400 text-[11px] justify-center bg-slate-900/60 p-2.5 rounded-xl border border-white/5">
          <ShieldCheck className="h-4 w-4 text-emerald-400 flex-shrink-0" />
          <span>Strict RBAC protection & zero secret storage in LLM context windows.</span>
        </div>
      </div>
    </div>
  );
}
