'use client';

import React, { useState } from 'react';
import { Presentation, ExternalLink, User, ChevronLeft, ChevronRight, FileText, Monitor, CheckCircle2, Shield, Cpu, Zap, Activity } from 'lucide-react';

export function PresentationPanel() {
  const [currentSlide, setCurrentSlide] = useState(1);
  const totalSlides = 12;

  const slidesData = [
    {
      id: 1,
      tag: "Title & Introduction",
      title: "Aegis AI",
      subtitle: "State-Orchestrated Multi-Agent Intelligence for Code Reviews, Security Audits, and Repository Automation",
      presenter: "Nitesh Kumar (Lead AI Architect & Systems Engineer)",
      content: (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl bg-gradient-to-br from-indigo-900/40 via-slate-900 to-cyan-950/30 border border-indigo-500/30 shadow-2xl">
            <div className="flex items-center gap-4 mb-4">
              <div className="h-12 w-12 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center font-bold text-lg text-white shadow-lg shadow-indigo-500/30">
                NK
              </div>
              <div>
                <h4 className="text-lg font-bold text-white">Nitesh Kumar</h4>
                <p className="text-xs text-cyan-400 font-mono font-semibold">Lead AI Architect & Systems Engineer</p>
              </div>
            </div>
            <p className="text-slate-300 text-sm leading-relaxed">
              Enterprise-grade platform replacing ad-hoc LLM chatbot prompts with a stateful multi-agent execution pipeline powered by LangGraph, FastAPI, and Next.js 16.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-slate-900/60 border border-white/10 text-center">
              <div className="text-xl font-bold text-indigo-400 font-mono">LangGraph</div>
              <div className="text-xs text-slate-400 mt-1">Multi-Agent Engine</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-white/10 text-center">
              <div className="text-xl font-bold text-cyan-400 font-mono">Gemini 1.5</div>
              <div className="text-xs text-slate-400 mt-1">Primary LLM Provider</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-white/10 text-center">
              <div className="text-xl font-bold text-emerald-400 font-mono">FastAPI</div>
              <div className="text-xs text-slate-400 mt-1">Async Core Backend</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-white/10 text-center">
              <div className="text-xl font-bold text-amber-400 font-mono">Next.js 16</div>
              <div className="text-xs text-slate-400 mt-1">App Router UI</div>
            </div>
          </div>
        </div>
      ),
      notes: "Welcome judges and team. I am Nitesh Kumar, presenting Aegis AI. Today, software development teams spend too much time on manual code reviews, security scanning, and context switching. Our platform introduces a state-orchestrated multi-agent intelligence system built with LangGraph, Next.js 16, and FastAPI."
    },
    {
      id: 2,
      tag: "01 / Industry Bottlenecks",
      title: "The Engineering Efficiency Gap",
      subtitle: "Modern software teams spend 40%+ of engineering cycles on operational friction.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-slate-100 text-base">⏱ PR Review Fatigue</h4>
            <p className="text-xs text-slate-400 leading-relaxed">Engineers spend hours reviewing thousands of lines of PRs manually, catching syntax & style errors that automated systems should prevent.</p>
            <div className="p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-center">
              <span className="text-2xl font-bold text-indigo-400 font-mono">4.8 Hrs</span>
              <p className="text-[10px] text-slate-400 uppercase tracking-wider">Avg PR Cycle Time</p>
            </div>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-slate-100 text-base">🔓 Security Blindspots</h4>
            <p className="text-xs text-slate-400 leading-relaxed">Static analysis alert noise causes vulnerability fatigue. Secret leaks (API keys, JWTs) reach production due to missing pre-commit AST guards.</p>
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-center">
              <span className="text-2xl font-bold text-rose-400 font-mono">34%</span>
              <p className="text-[10px] text-slate-400 uppercase tracking-wider">Leaked Key Risk Rate</p>
            </div>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-slate-100 text-base">🤖 Stateless Chatbot Limits</h4>
            <p className="text-xs text-slate-400 leading-relaxed">Standard AI chatbots lack whole-repository AST graph context, hallucinate imports, cannot execute local CLI scanners, and lack permission guardrails.</p>
            <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-center">
              <span className="text-2xl font-bold text-amber-400 font-mono">0%</span>
              <p className="text-[10px] text-slate-400 uppercase tracking-wider">Repo AST Awareness</p>
            </div>
          </div>
        </div>
      ),
      notes: "Let's start with the problem. Modern engineering teams waste over 40% of their bandwidth on manual PR reviews, static analysis triage, and vulnerability tracking. Traditional chatbots fail here because they are stateless, lack repository AST awareness, and cannot enforce permission safety."
    },
    {
      id: 3,
      tag: "02 / Platform Design",
      title: "High-Level System Architecture",
      subtitle: "Stateful orchestration, asynchronous workers, and resilient multi-provider LLM pipelines.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
              <h4 className="font-bold text-indigo-400 flex items-center gap-2">
                <Cpu className="h-4 w-4" /> Microservice Stack
              </h4>
              <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside">
                <li><strong>Next.js 16 App Router:</strong> Dark glassmorphic dashboard & Zustand stores.</li>
                <li><strong>FastAPI Core:</strong> Async SQLAlchemy, OpenAPI docs, REST routes.</li>
                <li><strong>Celery + Redis:</strong> Async task queue for non-blocking multi-agent execution.</li>
                <li><strong>PostgreSQL + Redis:</strong> Relational storage + SHA summary caching.</li>
              </ul>
            </div>
            <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
              <h4 className="font-bold text-cyan-400 flex items-center gap-2">
                <Shield className="h-4 w-4" /> Security Gateway
              </h4>
              <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside">
                <li><strong>Nginx Proxy:</strong> Unified routing for REST `/api/v1` & WebSockets.</li>
                <li><strong>GitHub Webhook HMAC:</strong> Constant-time SHA256 signature check.</li>
                <li><strong>Sliding Rate Limiter:</strong> Token bucket middleware enforcing IP quotas.</li>
                <li><strong>Secret Sanitizer:</strong> Real-time regex redaction of keys & tokens.</li>
              </ul>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-indigo-500/20 flex flex-wrap items-center justify-between gap-2 text-xs text-center font-mono">
            <span className="p-2 rounded bg-slate-900 text-slate-300 border border-white/10">GitHub Webhook</span>
            <span className="text-indigo-400 font-bold">➔</span>
            <span className="p-2 rounded bg-slate-900 text-cyan-400 border border-white/10">FastAPI API</span>
            <span className="text-indigo-400 font-bold">➔</span>
            <span className="p-2 rounded bg-slate-900 text-amber-400 border border-white/10">Celery Worker</span>
            <span className="text-indigo-400 font-bold">➔</span>
            <span className="p-2 rounded bg-slate-900 text-emerald-400 border border-white/10">LangGraph Agents</span>
          </div>
        </div>
      ),
      notes: "Here is our architecture. We built a production-grade stack with Next.js 16 on the frontend, FastAPI for async API routing, PostgreSQL for persistent storage, and Celery with Redis for background multi-agent execution. GitHub webhooks are secured with constant-time HMAC-SHA256 signatures."
    },
    {
      id: 4,
      tag: "03 / Core Intelligence",
      title: "LangGraph Multi-Agent Orchestration",
      subtitle: "9 Specialized AI Agent Roles operating on a unified StateGraph skeleton.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-indigo-400 text-sm">9 Specialized AI Agent Roles</h4>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <span className="p-2 rounded bg-slate-800 text-slate-200">1. Planner</span>
              <span className="p-2 rounded bg-slate-800 text-slate-200">2. RepoAnalyzer</span>
              <span className="p-2 rounded bg-slate-800 text-slate-200">3. ArchitectureAgent</span>
              <span className="p-2 rounded bg-slate-800 text-slate-200">4. CodeReviewer</span>
              <span className="p-2 rounded bg-slate-800 text-slate-200">5. TestGenerator</span>
              <span className="p-2 rounded bg-slate-800 text-slate-200">6. SecurityAuditor</span>
              <span className="p-2 rounded bg-slate-800 text-slate-200">7. DocumentationAgent</span>
              <span className="p-2 rounded bg-slate-800 text-slate-200">8. PRGenerator</span>
            </div>
            <p className="text-xs text-emerald-400 font-semibold mt-2">+ HumanApproval: Stateful interrupt checkpoint for developer sign-off.</p>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-cyan-400 text-sm">Governance & Safety</h4>
            <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside">
              <li><strong>Versioned Prompt Registry:</strong> Central prompt registry loading versioned text prompts (`planner_v1`, `repo_analyzer_v1`) with variable validation. Zero hardcoded prompt strings.</li>
              <li><strong>Declarative Tool Allow lists:</strong> Central `ToolPermissionManager` enforcing agent-to-tool allowlists. Unauthorized tool calls raise HTTP 403.</li>
            </ul>
          </div>
        </div>
      ),
      notes: "Our core AI engine is built on LangGraph using a unified StateGraph skeleton. We coordinate 9 specialized agent roles—from Planner and RepoAnalyzer to CodeReviewer and SecurityAuditor—with declarative tool permission allowlists and versioned prompt templates."
    },
    {
      id: 5,
      tag: "04 / LLM Reliability",
      title: "Multi-Provider AI Abstraction & Fallbacks",
      subtitle: "Universal AI provider factory with circuit breakers, API key rotation, and cost budgeting.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-indigo-400 text-sm">Universal AI Provider Layer</h4>
            <p className="text-xs text-slate-400">Unified `BaseAIProvider` abstraction supporting Google Gemini 1.5 Flash, OpenAI GPT-4.1, Groq Llama 3.1, and local Ollama without code changes.</p>
            <div className="p-2 rounded bg-slate-950 text-emerald-400 font-mono text-[11px]">
              Gemini ➔ OpenAI ➔ Groq ➔ Ollama
            </div>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-cyan-400 text-sm">3-State Circuit Breaker</h4>
            <p className="text-xs text-slate-400">In-memory 3-state breaker tracking failure thresholds and probe cooldowns per provider.</p>
            <div className="flex gap-1 text-[10px] font-bold">
              <span className="p-1.5 rounded bg-emerald-500/20 text-emerald-400">CLOSED</span>
              <span className="p-1.5 rounded bg-rose-500/20 text-rose-400">OPEN</span>
              <span className="p-1.5 rounded bg-amber-500/20 text-amber-400">HALF_OPEN</span>
            </div>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-amber-400 text-sm">Key Ring & Budgeting</h4>
            <p className="text-xs text-slate-400">Round-robin `ApiKeyRing` cycling credentials + token and USD cost accounting with automatic limit tripping.</p>
          </div>
        </div>
      ),
      notes: "To guarantee zero downtime and manage cost, our AI Provider Abstraction layer supports Google Gemini 1.5 Flash, OpenAI GPT-4.1, Groq, and local Ollama. We feature an automatic fallback chain, a 3-state circuit breaker, and an ApiKeyRing for credential rotation."
    },
    {
      id: 6,
      tag: "05 / Code Intelligence",
      title: "Repository Analysis Engine",
      subtitle: "Deterministic code parsing, static security wrappers, and AST dependency extraction.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-indigo-400 text-sm">AST & Symbol Target Discovery</h4>
            <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside">
              <li><strong>Tree-sitter Service:</strong> Multi-language file parse target identifier.</li>
              <li><strong>Python AST Graph:</strong> Extracts top-level classes, functions, and import graphs.</li>
              <li><strong>Git History Service:</strong> Parses latest commit summaries and author metadata.</li>
              <li><strong>Redis SHA Caching:</strong> SHA-256 keyed cache stores repository summaries.</li>
            </ul>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-cyan-400 text-sm">Subprocess Static Analysis Suite</h4>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="p-2 rounded bg-slate-950 border border-white/10 text-cyan-300"><strong>Ruff:</strong> Linter & style scanner</div>
              <div className="p-2 rounded bg-slate-950 border border-white/10 text-emerald-300"><strong>Bandit:</strong> AST security audit</div>
              <div className="p-2 rounded bg-slate-950 border border-white/10 text-amber-300"><strong>Semgrep:</strong> Multi-language rules</div>
              <div className="p-2 rounded bg-slate-950 border border-white/10 text-indigo-300"><strong>Radon:</strong> Code complexity metrics</div>
            </div>
          </div>
        </div>
      ),
      notes: "For deep repository context, our analysis engine uses Tree-sitter for target discovery and Python AST for symbol extraction. We integrate static security tools like Ruff, Bandit, Semgrep, and Radon safely without shell interpolation, backed by Redis SHA summary caching."
    },
    {
      id: 7,
      tag: "06 / Cyber Defense",
      title: "Enterprise Security & Secret Hardening",
      subtitle: "Multi-layered defense with automatic secret sanitization and RBAC.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-rose-400 text-sm">Secret Sanitizer Engine</h4>
            <p className="text-xs text-slate-300 leading-relaxed">
              Regex filter redacting API keys (`sk-...`, `gsk_...`), GitHub tokens (`ghp_...`), Bearer tokens, and JWTs across logs, exceptions, and outbound AI payloads.
            </p>
            <div className="p-3 rounded-lg bg-slate-950 border border-white/10 text-[11px] font-mono text-slate-300 space-y-1">
              <div><span className="text-slate-500">In:</span> Bearer sk-proj-129837198273</div>
              <div><span className="text-slate-500">Out:</span> Bearer <span className="text-rose-400 font-bold">[REDACTED_API_KEY]</span></div>
            </div>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-indigo-400 text-sm">Access Control & Audit Logging</h4>
            <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside">
              <li><strong>RBAC Scopes:</strong> `OWNER` &gt; `ADMIN` &gt; `MEMBER` &gt; `VIEWER`.</li>
              <li><strong>Webhook Security:</strong> HMAC SHA256 signature verification.</li>
              <li><strong>Audit Logging:</strong> Append-only sanitized audit trail.</li>
            </ul>
          </div>
        </div>
      ),
      notes: "Security is non-negotiable. Our Secret Sanitizer uses real-time regex filters to sanitize API keys, JWTs, and tokens across logs and LLM payloads before transmission. We enforce strict RBAC roles and append-only audit logging."
    },
    {
      id: 8,
      tag: "07 / User Experience",
      title: "Next.js 16 Dashboard & Telemetry",
      subtitle: "Cyberpunk dark aesthetic, real-time WebSockets, and Prometheus metrics exporter.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-indigo-400 text-sm">Next.js 16 App Router Interface</h4>
            <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside">
              <li>Dark mode by default (`#0B0F17`), glassmorphism backdrop blur.</li>
              <li>Zustand state stores (`useAuthStore`, `useRepoStore`).</li>
              <li>React Query integration with optimistic UI updates.</li>
            </ul>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-3">
            <h4 className="font-bold text-cyan-400 text-sm">Observability & Prometheus Metrics</h4>
            <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside">
              <li>Plaintext `/api/v1/metrics/prometheus` exporter for Grafana.</li>
              <li>JSON health telemetry endpoint `/api/v1/telemetry/health`.</li>
              <li>Real-time cost & token accounting panel.</li>
            </ul>
          </div>
        </div>
      ),
      notes: "Our dashboard features Next.js 16 App Router with dark mode and glassmorphic UI. For observability, we export Prometheus metrics at /api/v1/metrics/prometheus and JSON health telemetry to monitor model cost, latency, and circuit breaker states."
    },
    {
      id: 9,
      tag: "08 / Interactive Demo",
      title: "Live Agent Flow Simulation",
      subtitle: "Stateful agent graph execution sequence from plan to PR.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="p-5 rounded-xl bg-slate-950 border border-indigo-500/30 space-y-4">
          <div className="flex flex-wrap gap-2 text-xs">
            <span className="px-3 py-1 rounded bg-indigo-600 text-white font-semibold">1. Planner</span>
            <span className="px-3 py-1 rounded bg-slate-800 text-slate-300">2. RepoAnalyzer</span>
            <span className="px-3 py-1 rounded bg-slate-800 text-slate-300">3. ArchitectureAgent</span>
            <span className="px-3 py-1 rounded bg-slate-800 text-slate-300">4. CodeReviewer</span>
            <span className="px-3 py-1 rounded bg-slate-800 text-slate-300">5. SecurityAuditor</span>
            <span className="px-3 py-1 rounded bg-slate-800 text-slate-300">6. PRGenerator</span>
          </div>
          <div className="p-4 rounded-lg bg-slate-900 border border-white/10 font-mono text-xs text-emerald-400">
            &gt; Planner node initialized. Context ingested for enterprise-org/autonomous-platform.<br/>
            &gt; Scheduled 6 agent nodes on StateGraph skeleton.<br/>
            &gt; Status: In Execution.
          </div>
        </div>
      ),
      notes: "Here on Slide 9, you can see our live agent orchestration simulator. Clicking each node shows how state flows immutably between agents—from execution planning to code review, security auditing, and final pull request generation."
    },
    {
      id: 10,
      tag: "09 / Business Value",
      title: "Quantitative Benchmarks & Impact",
      subtitle: "Measured productivity acceleration and cost savings.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10">
            <div className="text-3xl font-extrabold text-emerald-400 font-mono">85%</div>
            <div className="text-xs font-semibold text-white mt-1">Faster PR Reviews</div>
            <p className="text-[11px] text-slate-400 mt-1">Reduced from 45m to 6.7m</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10">
            <div className="text-3xl font-extrabold text-cyan-400 font-mono">62%</div>
            <div className="text-xs font-semibold text-white mt-1">Cost Reduction</div>
            <p className="text-[11px] text-slate-400 mt-1">Gemini Flash + Groq chain</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10">
            <div className="text-3xl font-extrabold text-indigo-400 font-mono">3.4x</div>
            <div className="text-xs font-semibold text-white mt-1">Defect Coverage</div>
            <p className="text-[11px] text-slate-400 mt-1">Semgrep + Bandit + LLM</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10">
            <div className="text-3xl font-extrabold text-amber-400 font-mono">100%</div>
            <div className="text-xs font-semibold text-white mt-1">Secret Redaction</div>
            <p className="text-[11px] text-slate-400 mt-1">Zero leaks in 5,000+ logs</p>
          </div>
        </div>
      ),
      notes: "Here are our quantitative benchmarks: PR review cycle times are reduced by 85% from 45 minutes to 6.7 minutes. Smart LLM fallbacks cut API costs by 62%, and static scanners combined with LLMs deliver 3.4x higher security defect coverage with 100% secret redaction accuracy."
    },
    {
      id: 11,
      tag: "10 / Future Vision",
      title: "Production Roadmap",
      subtitle: "Strategic roadmap for enterprise scaling.",
      presenter: "Nitesh Kumar",
      content: (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-2">
            <h4 className="font-bold text-indigo-400 text-sm">Phase 1: Persistence</h4>
            <p className="text-xs text-slate-400">Durable LangGraph PostgreSQL checkpointer & execution state snapshots.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-2">
            <h4 className="font-bold text-cyan-400 text-sm">Phase 2: Automation</h4>
            <p className="text-xs text-slate-400">Inline GitHub PR commenting & Slack / Discord bot integrations.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 space-y-2">
            <h4 className="font-bold text-emerald-400 text-sm">Phase 3: Air-Gapped</h4>
            <p className="text-xs text-slate-400">Fine-tuned local Ollama / LLaMA 3.3 model support for 100% offline security.</p>
          </div>
        </div>
      ),
      notes: "Our production roadmap includes three key phases: Phase 1 brings durable LangGraph PostgreSQL checkpointers for long workflows; Phase 2 introduces automatic GitHub PR posting; and Phase 3 enables air-gapped enterprise deployments with local Ollama models."
    },
    {
      id: 12,
      tag: "Conclusion",
      title: "Questions & Discussion",
      subtitle: "Aegis AI",
      presenter: "Nitesh Kumar",
      content: (
        <div className="text-center space-y-6 py-4">
          <div className="inline-flex items-center gap-3 p-4 rounded-2xl bg-indigo-950/60 border border-indigo-500/30">
            <div className="h-10 w-10 rounded-full bg-indigo-500 flex items-center justify-center font-bold text-white">NK</div>
            <div className="text-left">
              <h4 className="font-bold text-white text-base">Nitesh Kumar</h4>
              <p className="text-xs text-cyan-400 font-mono">Autonomous SE Architecture</p>
            </div>
          </div>
          <div className="flex justify-center gap-4 text-xs font-semibold">
            <span className="px-4 py-2 rounded-xl bg-slate-900 border border-white/10 text-slate-200">docs/PRESENTATION.html</span>
            <span className="px-4 py-2 rounded-xl bg-indigo-600 text-white shadow-lg shadow-indigo-600/30">Ready for Q&A</span>
          </div>
        </div>
      ),
      notes: "Thank you! I am Nitesh Kumar, and I am happy to answer any questions about our architecture, multi-agent state graph, security sanitization, or multi-provider fallback engine."
    }
  ];

  const current = slidesData.find((s) => s.id === currentSlide) || slidesData[0];

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-panel border border-white/10">
        <div>
          <div className="flex items-center gap-2">
            <Presentation className="h-6 w-6 text-indigo-400" />
            <h2 className="text-xl font-extrabold text-white tracking-tight">
              Presentation Deck — Nitesh Kumar
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Executive pitch deck and interactive speaker presentation for Aegis AI.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <a
            href="/PRESENTATION.html"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all"
          >
            <Monitor className="h-4 w-4" />
            <span>Launch Fullscreen Deck (HTML)</span>
            <ExternalLink className="h-3.5 w-3.5" />
          </a>
        </div>
      </div>

      {/* Main Slide Viewer Container */}
      <div className="p-8 rounded-2xl bg-[#070a0f] border border-indigo-500/20 shadow-2xl relative min-h-[420px] flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between border-b border-white/10 pb-4 mb-6">
            <div>
              <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded-md border border-cyan-500/20">
                {current.tag}
              </span>
              <h3 className="text-2xl font-bold text-white mt-2">{current.title}</h3>
              <p className="text-xs text-slate-400 mt-1">{current.subtitle}</p>
            </div>
            <div className="hidden sm:flex items-center gap-2 text-xs font-mono text-slate-400 bg-slate-900/80 px-3 py-1.5 rounded-lg border border-white/10">
              <User className="h-3.5 w-3.5 text-indigo-400" />
              <span>{current.presenter}</span>
            </div>
          </div>

          <div className="py-2">{current.content}</div>
        </div>

        {/* Speaker Note Box */}
        <div className="mt-8 p-4 rounded-xl bg-slate-900/90 border border-indigo-500/30 space-y-1">
          <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-wider text-indigo-400 font-mono">
            <FileText className="h-3.5 w-3.5" />
            <span>Speaker Script — Nitesh Kumar</span>
          </div>
          <p className="text-xs text-slate-300 italic leading-relaxed">
            "{current.notes}"
          </p>
        </div>

        {/* Slide Footer Navigation Controls */}
        <div className="flex items-center justify-between border-t border-white/10 pt-4 mt-6">
          <span className="text-xs font-mono text-slate-400">
            Slide <strong className="text-cyan-400">{currentSlide}</strong> of {totalSlides}
          </span>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentSlide((p) => Math.max(p - 1, 1))}
              disabled={currentSlide === 1}
              className="p-2 rounded-lg bg-slate-900 border border-white/10 text-slate-200 hover:bg-indigo-600 hover:border-indigo-600 disabled:opacity-40 transition-all cursor-pointer"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
            <button
              onClick={() => setCurrentSlide((p) => Math.min(p + 1, totalSlides))}
              disabled={currentSlide === totalSlides}
              className="p-2 rounded-lg bg-slate-900 border border-white/10 text-slate-200 hover:bg-indigo-600 hover:border-indigo-600 disabled:opacity-40 transition-all cursor-pointer"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
