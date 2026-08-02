'use client';

import React from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import { Cpu, Layers, FileCode2 } from 'lucide-react';

export function ArchitecturePanel() {
  const { selectedRepo } = useRepoStore();

  const components = [
    { name: 'FastAPI Backend API', path: 'backend/app/main.py', type: 'REST & WebSocket', status: 'Active' },
    { name: 'Next.js 16 App Router', path: 'frontend/src/app', type: 'Turbopack Web UI', status: 'Active' },
    { name: 'LangGraph Execution Engine', path: 'backend/app/agents', type: 'State Graph', status: 'Active' },
    { name: 'AI Provider Abstraction', path: 'backend/app/ai', type: 'Multi-Provider Ring', status: 'Active' },
    { name: 'AST & Static Analyzer', path: 'backend/app/analysis', type: 'Tree-sitter Parser', status: 'Active' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel p-5 rounded-2xl border border-white/10 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Cpu className="h-5 w-5 text-indigo-400" />
            <h1 className="text-xl font-bold text-white tracking-tight">Repository Architecture Map</h1>
          </div>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Deterministic AST topology for <span className="text-indigo-300">{selectedRepo?.full_name || 'akaniitesh/CODEX-hackathon'}</span>
          </p>
        </div>
        <span className="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-mono">
          AST Symbols: 142
        </span>
      </div>

      {/* Component Topology */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {components.map((c, idx) => (
          <div key={idx} className="glass-panel p-5 rounded-2xl border border-white/10 space-y-3">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-xl bg-slate-800 border border-white/10 flex items-center justify-center text-indigo-400">
                  <Layers className="h-4 w-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white font-mono">{c.name}</h3>
                  <span className="text-[11px] text-slate-400">{c.type}</span>
                </div>
              </div>
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-mono border border-emerald-500/20">
                {c.status}
              </span>
            </div>
            <div className="pt-2 border-t border-white/5 flex items-center gap-2 text-xs text-slate-400 font-mono">
              <FileCode2 className="h-3.5 w-3.5 text-indigo-400" />
              <span>{c.path}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
