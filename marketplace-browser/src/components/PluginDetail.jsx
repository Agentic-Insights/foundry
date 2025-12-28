import { useState, useEffect } from 'react';
import { loadPluginReadme } from '../data/marketplaceLoader';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';

export function PluginDetail({ plugin, onClose }) {
  const [readme, setReadme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadPluginReadme(plugin.name)
      .then(content => {
        setReadme(content);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load README:', err);
        setLoading(false);
      });
  }, [plugin.name]);

  const installCommand = `/plugin install ${plugin.name}@agentic-insights`;

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 overflow-y-auto">
      <div className="min-h-screen px-4 py-8">
        <div className="max-w-4xl mx-auto bg-[var(--ai-card)] border border-[var(--ai-border)] shadow-2xl">
          {/* Header */}
          <div className="p-6 border-b border-[var(--ai-border)]">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="text-xs font-mono text-[var(--ai-gray-500)] mb-2">
                  <span className="text-[var(--ai-green)]">$</span> cat {plugin.name}/README.md
                </div>
                <h2 className="text-2xl font-bold font-mono text-white mb-2">{plugin.name}</h2>
                <p className="text-[var(--ai-gray-300)] text-sm">{plugin.description}</p>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-[var(--ai-border)] transition-colors text-[var(--ai-gray-500)] hover:text-white"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Installation */}
            <div className="bg-black border border-[var(--ai-border)] p-4 mb-4 glow-green-box">
              <div className="text-xs text-[var(--ai-gray-500)] mb-2 font-mono uppercase tracking-wider">Claude Code Installation</div>
              <div className="flex items-center gap-2">
                <code className="flex-1 text-[var(--ai-green)] font-mono text-sm">{installCommand}</code>
                <button
                  onClick={() => navigator.clipboard.writeText(installCommand)}
                  className="px-3 py-1.5 bg-[var(--ai-green)] hover:bg-[var(--ai-green-dim)] text-black font-mono text-xs font-semibold transition-colors"
                >
                  COPY
                </button>
              </div>
            </div>

            {/* Metadata */}
            <div className="flex flex-wrap gap-6 text-sm font-mono">
              <div className="flex items-center gap-2">
                <span className="text-[var(--ai-gray-500)]">version:</span>
                <span className="text-white">{plugin.version}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[var(--ai-gray-500)]">license:</span>
                <span className="text-white">{plugin.license}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[var(--ai-gray-500)]">author:</span>
                <span className="text-white">@{plugin.author?.name}</span>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="border-b border-[var(--ai-border)]">
            <div className="flex gap-0 px-0">
              {['overview', 'features', 'documentation'].map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`py-3 px-6 font-mono text-xs uppercase tracking-wider transition-colors border-b-2 ${
                    activeTab === tab
                      ? 'border-[var(--ai-green)] text-[var(--ai-green)] bg-[var(--ai-green-subtle)]'
                      : 'border-transparent text-[var(--ai-gray-500)] hover:text-[var(--ai-gray-300)] hover:bg-black/50'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Feature counts */}
                <div className="grid grid-cols-3 gap-4">
                  {plugin.skillCount > 0 && (
                    <div className="bg-[var(--ai-green-subtle)] border border-[var(--ai-green)]/20 p-4">
                      <div className="text-2xl font-bold font-mono text-[var(--ai-green)]">{plugin.skillCount}</div>
                      <div className="text-xs text-[var(--ai-gray-500)] font-mono uppercase">Skill{plugin.skillCount !== 1 ? 's' : ''}</div>
                    </div>
                  )}
                  {plugin.commandCount > 0 && (
                    <div className="bg-[var(--ai-green-subtle)] border border-[var(--ai-green)]/20 p-4">
                      <div className="text-2xl font-bold font-mono text-[var(--ai-green)]">{plugin.commandCount}</div>
                      <div className="text-xs text-[var(--ai-gray-500)] font-mono uppercase">Command{plugin.commandCount !== 1 ? 's' : ''}</div>
                    </div>
                  )}
                  {plugin.agentCount > 0 && (
                    <div className="bg-[var(--ai-green-subtle)] border border-[var(--ai-green)]/20 p-4">
                      <div className="text-2xl font-bold font-mono text-[var(--ai-green)]">{plugin.agentCount}</div>
                      <div className="text-xs text-[var(--ai-gray-500)] font-mono uppercase">Agent{plugin.agentCount !== 1 ? 's' : ''}</div>
                    </div>
                  )}
                </div>

                {/* Tags */}
                {plugin.tags && plugin.tags.length > 0 && (
                  <div>
                    <h3 className="text-sm font-mono font-semibold text-white mb-3 uppercase tracking-wider">Tags</h3>
                    <div className="flex flex-wrap gap-1.5">
                      {plugin.tags.map(tag => (
                        <span
                          key={tag}
                          className="px-2 py-1 bg-black text-[var(--ai-gray-300)] text-xs font-mono border border-[var(--ai-border)] hover:border-[var(--ai-border-hover)] transition-colors"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Repository link */}
                {plugin.repository && (
                  <div>
                    <h3 className="text-sm font-mono font-semibold text-white mb-3 uppercase tracking-wider">Repository</h3>
                    <a
                      href={plugin.repository}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-[var(--ai-green)] hover:underline font-mono text-sm transition-colors"
                    >
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                        <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                      </svg>
                      github.com →
                    </a>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'features' && (
              <div className="space-y-6">
                <FeatureSection title="Skills" count={plugin.skillCount} />
                <FeatureSection title="Commands" count={plugin.commandCount} />
                <FeatureSection title="Agents" count={plugin.agentCount} />

                {plugin.keywords && plugin.keywords.length > 0 && (
                  <div>
                    <h3 className="text-sm font-mono font-semibold text-white mb-3 uppercase tracking-wider">Keywords</h3>
                    <div className="flex flex-wrap gap-1.5">
                      {plugin.keywords.map(keyword => (
                        <span
                          key={keyword}
                          className="px-2 py-1 bg-black text-[var(--ai-gray-500)] text-xs font-mono"
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'documentation' && (
              <div className="prose prose-invert max-w-none">
                {loading ? (
                  <div className="flex items-center justify-center py-12 font-mono text-sm text-[var(--ai-green)]">
                    <span className="opacity-60">$</span> loading docs<span className="cursor-blink"></span>
                  </div>
                ) : readme ? (
                  <div className="markdown-content">
                    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
                      {readme}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <div className="text-center py-12 text-[var(--ai-gray-500)] font-mono">
                    <p className="text-sm">No documentation available</p>
                    <p className="text-xs mt-2">
                      <a
                        href={`https://github.com/agentic-insights/foundry/tree/main/plugins/${plugin.name}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[var(--ai-green)] hover:underline"
                      >
                        View on GitHub →
                      </a>
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureSection({ title, count }) {
  if (count === 0) return null;

  return (
    <div>
      <h3 className="text-sm font-mono font-semibold text-white mb-3 uppercase tracking-wider">{title}</h3>
      <div className="flex items-center gap-3 p-4 border border-[var(--ai-green)]/20 bg-[var(--ai-green-subtle)]">
        <div className="text-2xl font-bold font-mono text-[var(--ai-green)]">
          {count}
        </div>
        <div className="text-xs text-[var(--ai-gray-500)] font-mono">
          {title.toLowerCase()} available in this plugin
        </div>
      </div>
    </div>
  );
}
