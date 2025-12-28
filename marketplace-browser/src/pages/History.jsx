import { Link } from 'react-router-dom'

export function History() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <Link to="/" className="text-blue-400 hover:text-blue-300 text-sm mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-4xl font-bold mb-4">The Context Engineering Journey</h1>
          <p className="text-xl text-gray-400">
            From .context.md to AGENTS.md to Skills — the evolution of AI context standards
          </p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-12">
        {/* Timeline */}
        <div className="space-y-12">

          {/* Codebase Context */}
          <section className="relative pl-8 border-l-2 border-blue-500/30">
            <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-blue-500"></div>
            <div className="mb-2">
              <span className="text-blue-400 text-sm font-mono">2023-2024</span>
            </div>
            <h2 className="text-2xl font-bold text-white mb-4">Codebase Context & .context.md</h2>
            <p className="text-gray-300 mb-6 leading-relaxed">
              It started with a simple observation: AI coding assistants were missing crucial context.
              They could read code, but they couldn't understand <em>why</em> decisions were made,
              what conventions to follow, or how the pieces fit together.
            </p>
            <p className="text-gray-300 mb-6 leading-relaxed">
              The <strong>.context.md</strong> specification was born — a way to embed rich,
              structured context directly in your codebase. Not just for humans, but specifically
              designed for AI consumption.
            </p>

            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-white mb-4">Videos & Talks</h3>
              <ul className="space-y-3">
                <li>
                  <a href="#" className="text-blue-400 hover:text-blue-300 flex items-center gap-2">
                    <svg className="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"/>
                      <path fill="#fff" d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                    </svg>
                    Introduction to Codebase Context (Coming Soon)
                  </a>
                </li>
                <li>
                  <a href="#" className="text-blue-400 hover:text-blue-300 flex items-center gap-2">
                    <svg className="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5814z"/>
                      <path fill="#fff" d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                    </svg>
                    Austin LangChain Meetup: Context Engineering (Coming Soon)
                  </a>
                </li>
              </ul>
            </div>

            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <a href="https://github.com/Agentic-Insights/codebase-context-spec" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                    📄 Original Codebase Context Specification
                  </a>
                </li>
                <li>
                  <a href="https://codebasecontext.org" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                    🌐 codebasecontext.org (legacy docs)
                  </a>
                </li>
              </ul>
            </div>
          </section>

          {/* AGENTS.md */}
          <section className="relative pl-8 border-l-2 border-purple-500/30">
            <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-purple-500"></div>
            <div className="mb-2">
              <span className="text-purple-400 text-sm font-mono">2024</span>
            </div>
            <h2 className="text-2xl font-bold text-white mb-4">AGENTS.md — Industry Adoption</h2>
            <p className="text-gray-300 mb-6 leading-relaxed">
              The ideas from .context.md gained traction. Anthropic, OpenAI, and others began
              adopting similar patterns. The community standardized on <strong>AGENTS.md</strong> —
              a simpler, more focused format for agent instructions.
            </p>
            <p className="text-gray-300 mb-6 leading-relaxed">
              AGENTS.md became the de facto standard for telling AI agents how to work in your
              codebase. Claude Code, Cursor, Windsurf, and others now look for these files automatically.
            </p>

            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <a href="https://agents.md" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                    🤖 agents.md — The Standard
                  </a>
                </li>
                <li>
                  <a href="https://docs.anthropic.com/en/docs/claude-code/memory#agentsmd" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                    📚 Claude Code AGENTS.md Documentation
                  </a>
                </li>
              </ul>
            </div>
          </section>

          {/* Agent Skills */}
          <section className="relative pl-8 border-l-2 border-green-500/30">
            <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-green-500"></div>
            <div className="mb-2">
              <span className="text-green-400 text-sm font-mono">2025</span>
            </div>
            <h2 className="text-2xl font-bold text-white mb-4">Agent Skills — Portable Capabilities</h2>
            <p className="text-gray-300 mb-6 leading-relaxed">
              The next evolution: <strong>Skills</strong>. Not just static context, but portable,
              reusable capabilities that agents can invoke. Skills combine instructions, scripts,
              reference materials, and assets into shareable packages.
            </p>
            <p className="text-gray-300 mb-6 leading-relaxed">
              The <a href="https://agentskills.io" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">Agent Skills specification</a> is
              an open standard — supported by Claude Code, and designed for cross-platform compatibility.
            </p>

            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <a href="https://agentskills.io" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                    ⚡ agentskills.io — The Specification
                  </a>
                </li>
                <li>
                  <a href="https://github.com/agentskills/agentskills" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                    🔧 skills-ref validator tool
                  </a>
                </li>
                <li>
                  <Link to="/" className="text-blue-400 hover:text-blue-300">
                    🏭 Foundry Marketplace — Skills in Action
                  </Link>
                </li>
              </ul>
            </div>
          </section>

          {/* Philosophy */}
          <section className="mt-16 bg-gray-900/30 border border-gray-800 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-white mb-4">The Philosophy</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-blue-400 mb-2">Context over Prompting</h3>
                <p className="text-gray-400 text-sm">
                  Rich, structured context beats clever prompt tricks. Give agents the information
                  they need upfront.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-purple-400 mb-2">Open Standards</h3>
                <p className="text-gray-400 text-sm">
                  Portable formats that work across tools and vendors. No lock-in, no proprietary formats.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-green-400 mb-2">Consulting-Grade</h3>
                <p className="text-gray-400 text-sm">
                  Production patterns from real client engagements. Battle-tested, not theoretical.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-yellow-400 mb-2">Evidence over Claims</h3>
                <p className="text-gray-400 text-sm">
                  Test it, measure it, prove it works. No hype, just results.
                </p>
              </div>
            </div>
          </section>

        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8 mt-12">
        <div className="max-w-4xl mx-auto px-6 text-center text-gray-500 text-sm">
          <p>
            <Link to="/" className="text-blue-400 hover:text-blue-300">
              ← Back to Foundry Marketplace
            </Link>
          </p>
        </div>
      </footer>
    </div>
  )
}
