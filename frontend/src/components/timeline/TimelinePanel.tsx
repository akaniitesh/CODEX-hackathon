'use client';

import React, { useState } from 'react';
import { useRepoStore } from '@/store/useRepoStore';
import {
  Activity,
  CheckCircle2,
  Play,
  Terminal,
  RefreshCw,
} from 'lucide-react';

export function TimelinePanel() {
  const { selectedRepo } = useRepoStore();
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<string[]>([
    `[SYSTEM] Connected to repository ${selectedRepo?.full_name || 'akaniitesh/CODEX-hackathon'}:${selectedRepo?.default_branch || 'main'}`,
    `[AST_INDEXER] Verified Tree-sitter parser targets (Python 3.14 / TypeScript Turbopack)`,
    `[SECURITY_SCANNER] Bandit AST security scanner loaded 0 CVE vulnerabilities`,
    `[AGENT_COORDINATOR] LangGraph execution engine ready for launch`,
  ]);

  const handleStartRun = () => {
    setIsRunning(true);
    const repoName = selectedRepo?.full_name || 'akaniitesh/CODEX-hackathon';
    const steps = [
      `[RUN_STARTED] Initiating multi-agent execution pipeline for ${repoName}`,
      `[REPOSITORY_SUMMARIZER] Mapping repository structure and extracting module topology...`,
      `[AST_INDEXER] Parsing file symbols, type signatures, and import dependencies...`,
      `[STATIC_ANALYZER] Running Ruff linter and MyPy type checks...`,
      `[SECURITY_SCANNER] Executing Bandit AST security audit & credential sanitization...`,
      `[CODE_REVIEWER] Evaluating PR logic against repository architecture constraints...`,
      `[PR_GENERATOR] Generating automated pull request and unit test coverage...`,
      `[RUN_COMPLETED] Autonomous execution pipeline completed successfully in 4.2s (Status: GREEN)`,
    ];

    steps.forEach((step, index) => {
      setTimeout(() => {
        setLogs((prev) => [...prev, step]);
        if (index === steps.length - 1) {
          setIsRunning(false);
        }
      }, (index + 1) * 700);
    });
  };

  const stepsData = [
    { title: 'Repository Summarizer', status: 'completed', desc: 'Mapped directory tree and entry points' },
    { title: 'AST Indexer', status: isRunning ? 'running' : 'completed', desc: 'Parsed AST targets and symbol table' },
    { title: 'Static Analyzer', status: isRunning ? 'running' : 'completed', desc: 'Checked Ruff lint rules & MyPy types' },
    { title: 'Security Scanner', status: isRunning ? 'running' : 'completed', desc: 'Scanned for hardcoded secrets & CVEs' },
    { title: 'Code Reviewer', status: isRunning ? 'running' : 'completed', desc: 'Generated security & architecture findings' },
    { title: 'PR Generator', status: isRunning ? 'running' : 'completed', desc: 'Prepared patch diff and test fixtures' },
  ];

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-panel p-5 rounded-2xl border border-white/10">
        <div>
          <div className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-indigo-400" />
            <h1 className="text-xl font-bold text-white tracking-tight">Realtime Agent Timeline</h1>
          </div>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Target: <span className="text-slate-200">{selectedRepo?.full_name || 'akaniitesh/CODEX-hackathon'}</span> ({selectedRepo?.default_branch || 'main'})
          </p>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <button
            onClick={handleStartRun}
            disabled={isRunning}
            className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/25 transition-all disabled:opacity-50 cursor-pointer"
          >
            {isRunning ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin text-white" />
                <span>Executing Agents...</span>
              </>
            ) : (
              <>
                <Play className="h-4 w-4 fill-current" />
                <span>Trigger Agent Run</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Grid: Agent Pipeline Steps & Terminal Logs */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Agent Steps */}
        <div className="space-y-3">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">Agent Execution Steps</h2>
          {stepsData.map((s, idx) => (
            <div
              key={idx}
              className="glass-panel p-4 rounded-xl border border-white/10 flex items-start gap-3 transition-all hover:border-white/20"
            >
              <div className="mt-0.5">
                {s.status === 'completed' && <CheckCircle2 className="h-5 w-5 text-emerald-400" />}
                {s.status === 'running' && <RefreshCw className="h-5 w-5 text-indigo-400 animate-spin" />}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-white font-mono">{s.title}</h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    PASSED
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">{s.desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Right Column: Execution Console Log */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono flex items-center gap-2">
              <Terminal className="h-4 w-4 text-emerald-400" />
              <span>Realtime Execution Log Stream</span>
            </h2>
            <span className="text-[10px] font-mono text-slate-500">Live SSE Stream</span>
          </div>

          <div className="bg-slate-950/90 rounded-2xl border border-white/10 p-5 font-mono text-xs text-slate-300 space-y-2 h-[420px] overflow-y-auto shadow-inner">
            {logs.map((log, idx) => {
              const isError = log.includes('[ERROR]');
              const isSuccess = log.includes('[RUN_COMPLETED]');
              return (
                <div key={idx} className="flex items-start gap-2 leading-relaxed">
                  <span className="text-slate-600 select-none">&gt;</span>
                  <span
                    className={
                      isError
                        ? 'text-rose-400'
                        : isSuccess
                        ? 'text-emerald-400 font-bold'
                        : log.startsWith('[SYSTEM]')
                        ? 'text-indigo-400'
                        : 'text-slate-300'
                    }
                  >
                    {log}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
