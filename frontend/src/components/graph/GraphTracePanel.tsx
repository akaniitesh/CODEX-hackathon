'use client';

import React from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import { Bot, ArrowRight, CheckCircle2, GitBranch, Cpu } from 'lucide-react';

export function GraphTracePanel() {
  const { selectedRepo } = useRepoStore();

  const nodes = [
    { id: 'start', name: 'Start Trigger', type: 'entry', desc: 'Webhook / Manual Launch' },
    { id: 'summarizer', name: 'Repo Summarizer', type: 'agent', desc: 'Tree topology & AST routes' },
    { id: 'ast_indexer', name: 'AST Indexer', type: 'tool', desc: 'Symbol table & import graph' },
    { id: 'static_analyzer', name: 'Static Analyzer', type: 'tool', desc: 'Ruff & MyPy static checks' },
    { id: 'security_scanner', name: 'Security Scanner', type: 'tool', desc: 'Bandit AST & secret audit' },
    { id: 'code_reviewer', name: 'Code Reviewer', type: 'agent', desc: 'LLM reasoning & findings' },
    { id: 'pr_generator', name: 'PR Generator', type: 'agent', desc: 'Git commit & PR creation' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel p-5 rounded-2xl border border-white/10 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Bot className="h-5 w-5 text-indigo-400" />
            <h1 className="text-xl font-bold text-white tracking-tight">LangGraph Execution Shape</h1>
          </div>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            State Graph topology for repository <span className="text-indigo-300">{selectedRepo?.full_name || 'akaniitesh/CODEX-hackathon'}</span>
          </p>
        </div>
        <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono">
          Stateful Reduction Ready
        </span>
      </div>

      {/* Graph Visualizer Canvas */}
      <div className="glass-panel p-8 rounded-2xl border border-white/10 space-y-6">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">Multi-Agent State Machine Topology</h2>
        
        <div className="flex flex-wrap items-center justify-center gap-4 py-8">
          {nodes.map((node, idx) => (
            <React.Fragment key={node.id}>
              <div className="flex flex-col items-center p-4 rounded-2xl bg-slate-900/90 border border-indigo-500/30 w-48 shadow-xl shadow-indigo-500/5 group hover:border-indigo-500 transition-all cursor-pointer">
                <div className="h-10 w-10 rounded-xl bg-slate-800 border border-white/10 flex items-center justify-center text-indigo-400 mb-2 group-hover:bg-indigo-600 group-hover:text-white transition-all">
                  {node.type === 'entry' ? <GitBranch className="h-5 w-5" /> : node.type === 'agent' ? <Bot className="h-5 w-5" /> : <Cpu className="h-5 w-5" />}
                </div>
                <h3 className="text-xs font-bold text-white font-mono text-center">{node.name}</h3>
                <span className="text-[10px] text-slate-400 text-center mt-1">{node.desc}</span>
                <span className="mt-3 px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[9px] font-mono border border-emerald-500/20 flex items-center gap-1">
                  <CheckCircle2 className="h-3 w-3" /> State Reduced
                </span>
              </div>

              {idx < nodes.length - 1 && (
                <div className="text-slate-600 flex items-center">
                  <ArrowRight className="h-5 w-5 text-indigo-400/60" />
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
}
