'use client';

import React, { useState } from 'react';
import { X, Key, ShieldCheck, Check, Eye, EyeOff, Sparkles } from 'lucide-react';

export interface UserProviderKeys {
  activeProvider: 'gemini' | 'openai' | 'anthropic' | 'groq' | 'openrouter' | 'ollama';
  geminiKey: string;
  openaiKey: string;
  anthropicKey: string;
  groqKey: string;
  openrouterKey: string;
  ollamaUrl: string;
}

const DEFAULT_KEYS: UserProviderKeys = {
  activeProvider: 'gemini',
  geminiKey: '',
  openaiKey: '',
  anthropicKey: '',
  groqKey: '',
  openrouterKey: '',
  ollamaUrl: 'http://localhost:11434',
};

export function ProviderKeyModal({
  isOpen,
  onClose,
}: {
  isOpen: boolean;
  onClose: () => void;
}) {
  const [keys, setKeys] = useState<UserProviderKeys>(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('user_provider_keys');
      if (stored) {
        try {
          return JSON.parse(stored);
        } catch {
          // Fallback
        }
      }
    }
    return DEFAULT_KEYS;
  });
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});
  const [savedSuccess, setSavedSuccess] = useState(false);

  if (!isOpen) return null;

  const toggleShowKey = (field: string) => {
    setShowKeys((prev) => ({ ...prev, [field]: !prev[field] }));
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (typeof window !== 'undefined') {
      localStorage.setItem('user_provider_keys', JSON.stringify(keys));
    }
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 800);
  };

  const providerOptions = [
    { id: 'gemini', label: 'Google Gemini', placeholder: 'AIzaSy...' },
    { id: 'openai', label: 'OpenAI', placeholder: 'sk-proj-...' },
    { id: 'anthropic', label: 'Anthropic Claude', placeholder: 'sk-ant-...' },
    { id: 'groq', label: 'Groq', placeholder: 'gsk_...' },
    { id: 'openrouter', label: 'OpenRouter', placeholder: 'sk-or-...' },
    { id: 'ollama', label: 'Local Ollama', placeholder: 'http://localhost:11434' },
  ] as const;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="provider-key-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-fade-in"
    >
      <div className="relative w-full max-w-xl glass-panel rounded-2xl p-6 border border-white/10 shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all cursor-pointer"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center">
            <Key className="h-5 w-5 text-indigo-400" />
          </div>
          <div>
            <h2 id="provider-key-modal-title" className="text-lg font-bold text-white tracking-tight">
              AI Provider Keys &amp; Settings
            </h2>
            <p className="text-xs text-slate-400">
              Bring your own API keys for Gemini, OpenAI, Claude, Groq, OpenRouter, or Ollama.
            </p>
          </div>
        </div>

        <form onSubmit={handleSave} className="space-y-5">
          {/* Active Provider Selector */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-2 flex items-center gap-1.5">
              <Sparkles className="h-3.5 w-3.5 text-amber-400" />
              <span>Active Model Provider</span>
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {providerOptions.map((prov) => {
                const isSelected = keys.activeProvider === prov.id;
                return (
                  <button
                    key={prov.id}
                    type="button"
                    onClick={() => setKeys({ ...keys, activeProvider: prov.id })}
                    className={`py-2 px-3 rounded-xl border text-xs font-medium transition-all text-left flex items-center justify-between cursor-pointer ${
                      isSelected
                        ? 'bg-indigo-600/90 text-white border-indigo-500 shadow-md shadow-indigo-500/20'
                        : 'bg-slate-900/80 text-slate-300 border-white/5 hover:border-white/20'
                    }`}
                  >
                    <span>{prov.label}</span>
                    {isSelected && <Check className="h-3.5 w-3.5 text-white" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Key Inputs */}
          <div className="space-y-3 pt-2">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Google Gemini API Key</label>
              <div className="relative">
                <input
                  type={showKeys.gemini ? 'text' : 'password'}
                  value={keys.geminiKey}
                  onChange={(e) => setKeys({ ...keys, geminiKey: e.target.value })}
                  placeholder="AIzaSy..."
                  className="w-full pr-10 pl-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey('gemini')}
                  className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300"
                >
                  {showKeys.gemini ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">OpenAI API Key</label>
              <div className="relative">
                <input
                  type={showKeys.openai ? 'text' : 'password'}
                  value={keys.openaiKey}
                  onChange={(e) => setKeys({ ...keys, openaiKey: e.target.value })}
                  placeholder="sk-proj-..."
                  className="w-full pr-10 pl-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey('openai')}
                  className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300"
                >
                  {showKeys.openai ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Anthropic Claude API Key</label>
              <div className="relative">
                <input
                  type={showKeys.anthropic ? 'text' : 'password'}
                  value={keys.anthropicKey}
                  onChange={(e) => setKeys({ ...keys, anthropicKey: e.target.value })}
                  placeholder="sk-ant-..."
                  className="w-full pr-10 pl-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey('anthropic')}
                  className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300"
                >
                  {showKeys.anthropic ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Groq API Key</label>
              <div className="relative">
                <input
                  type={showKeys.groq ? 'text' : 'password'}
                  value={keys.groqKey}
                  onChange={(e) => setKeys({ ...keys, groqKey: e.target.value })}
                  placeholder="gsk_..."
                  className="w-full pr-10 pl-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey('groq')}
                  className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300"
                >
                  {showKeys.groq ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">OpenRouter API Key</label>
              <div className="relative">
                <input
                  type={showKeys.openrouter ? 'text' : 'password'}
                  value={keys.openrouterKey}
                  onChange={(e) => setKeys({ ...keys, openrouterKey: e.target.value })}
                  placeholder="sk-or-..."
                  className="w-full pr-10 pl-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey('openrouter')}
                  className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300"
                >
                  {showKeys.openrouter ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Local Ollama Service Endpoint</label>
              <input
                type="text"
                value={keys.ollamaUrl}
                onChange={(e) => setKeys({ ...keys, ollamaUrl: e.target.value })}
                placeholder="http://localhost:11434"
                className="w-full pl-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 font-mono"
              />
            </div>
          </div>

          {/* Security Banner */}
          <div className="flex items-center gap-2 text-slate-400 text-[11px] bg-slate-900/60 p-2.5 rounded-xl border border-white/5">
            <ShieldCheck className="h-4 w-4 text-emerald-400 flex-shrink-0" />
            <span>Keys are stored in local browser session storage and never transmitted to shared servers.</span>
          </div>

          <div className="pt-2 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-all cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex items-center gap-2 px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/25 transition-all cursor-pointer"
            >
              {savedSuccess ? (
                <>
                  <Check className="h-4 w-4 text-emerald-400" />
                  <span>Saved Keys!</span>
                </>
              ) : (
                <span>Save Provider Settings</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
