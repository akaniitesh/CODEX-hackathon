'use client';

import React, { useState } from 'react';
import { Presentation, ChevronLeft, ChevronRight } from 'lucide-react';

export function PresentationPanel() {
  const [currentSlide, setCurrentSlide] = useState(1);

  const slidesData = [
    {
      id: 1,
      title: 'Aegis AI',
      subtitle: 'Autonomous Software Engineering & Agentic Safety Platform',
      tagline: 'Deterministic AST analysis + LangGraph Multi-Agent Collaboration',
      bullets: [
        'Deterministic repository indexing & static security analysis',
        'State-reduced multi-agent reasoning graph (LangGraph)',
        'Resilient multi-provider AI fallback ring (Gemini, OpenAI, Anthropic, Groq, OpenRouter, Ollama)',
        'Full RBAC security, zero secret leakage, and instant PR generation',
      ],
      notes: 'Welcome everyone! Aegis AI transforms manual code reviews and architecture analysis into an autonomous, state-driven multi-agent execution pipeline.',
    },
    {
      id: 2,
      title: 'Problem Statement & Opportunity',
      subtitle: 'The Bottleneck in Modern SE Workflows',
      tagline: 'Ad-hoc LLM chatbots lack repository context, AST determinism, and execution safety',
      bullets: [
        'SE teams spend 35%+ of sprint bandwidth manually reviewing pull requests',
        'Traditional LLM prompts suffer from context truncation and hallucinations',
        'Hardcoded API credentials and unvetted code generation pose critical security risks',
        'Aegis AI provides deterministic Tree-sitter AST parsing and stateful multi-agent orchestration',
      ],
      notes: 'Engineering teams lose hundreds of hours every month. Aegis AI solves this by introducing a deterministic, state-driven multi-agent platform.',
    },
  ];

  const current = slidesData.find((s) => s.id === currentSlide) || slidesData[0];

  return (
    <div className="space-y-6">
      {/* Slide Header */}
      <div className="glass-panel p-5 rounded-2xl border border-white/10 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-emerald-500 to-cyan-400 p-[1px] shadow-lg shadow-indigo-500/20">
            <div className="flex h-full w-full items-center justify-center rounded-[11px] bg-slate-950">
              <Presentation className="h-5 w-5 text-indigo-400" />
            </div>
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">Interactive Presentation Deck</h1>
            <p className="text-xs text-slate-400">Executive walkthrough &amp; architecture overview for Aegis AI</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentSlide((prev) => Math.max(1, prev - 1))}
            disabled={currentSlide === 1}
            className="p-2 rounded-xl bg-slate-900 border border-white/10 text-slate-300 hover:text-white disabled:opacity-40 cursor-pointer"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <span className="text-xs font-mono px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-slate-300">
            {currentSlide} / {slidesData.length}
          </span>
          <button
            onClick={() => setCurrentSlide((prev) => Math.min(slidesData.length, prev + 1))}
            disabled={currentSlide === slidesData.length}
            className="p-2 rounded-xl bg-slate-900 border border-white/10 text-slate-300 hover:text-white disabled:opacity-40 cursor-pointer"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Main Slide Card */}
      <div className="glass-panel p-8 rounded-2xl border border-white/10 space-y-6 min-h-[420px] flex flex-col justify-between">
        <div className="space-y-4">
          <span className="text-xs font-mono font-semibold text-indigo-400 uppercase tracking-widest">
            {current.tagline}
          </span>
          <h2 className="text-3xl font-extrabold text-white tracking-tight">{current.title}</h2>
          <p className="text-base text-slate-300 font-medium">{current.subtitle}</p>

          <ul className="mt-6 space-y-3">
            {current.bullets.map((bullet, idx) => (
              <li key={idx} className="flex items-start gap-3 text-xs text-slate-300">
                <span className="h-1.5 w-1.5 rounded-full bg-indigo-400 mt-1.5 flex-shrink-0" />
                <span>{bullet}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Speaker Notes */}
        <div className="pt-4 border-t border-white/10 text-xs text-slate-400 italic">
          <p>&quot;{current.notes}&quot;</p>
        </div>
      </div>
    </div>
  );
}
