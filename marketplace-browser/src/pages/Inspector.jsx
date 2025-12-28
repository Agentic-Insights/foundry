import { useState } from 'react'
import { Link } from 'react-router-dom'
import { PluginCard } from '../components/PluginCard'
import { PluginDetail } from '../components/PluginDetail'

export function Inspector() {
  const [marketplaceUri, setMarketplaceUri] = useState('')
  const [marketplace, setMarketplace] = useState(null)
  const [selectedPlugin, setSelectedPlugin] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const exampleUris = [
    { label: 'Superpowers', uri: 'obra/superpowers-marketplace' },
    { label: 'Foundry', uri: 'agentic-insights/foundry' },
  ]

  async function loadMarketplace(uri) {
    setLoading(true)
    setError(null)
    setMarketplace(null)

    try {
      // Parse the URI - support multiple formats
      let url
      if (uri.startsWith('http')) {
        // Direct URL
        url = uri
      } else if (uri.includes('/')) {
        // GitHub owner/repo format
        const [owner, repo] = uri.split('/')
        url = `https://raw.githubusercontent.com/${owner}/${repo}/main/.claude-plugin/marketplace.json`
      } else {
        throw new Error('Invalid URI format. Use owner/repo or a direct URL.')
      }

      const response = await fetch(url)
      if (!response.ok) {
        // Try refs/heads/main for some repos
        if (url.includes('/main/')) {
          const altUrl = url.replace('/main/', '/master/')
          const altResponse = await fetch(altUrl)
          if (altResponse.ok) {
            const data = await altResponse.json()
            setMarketplace(enhanceMarketplaceData(data, uri))
            setLoading(false)
            return
          }
        }
        throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      setMarketplace(enhanceMarketplaceData(data, uri))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function enhanceMarketplaceData(data, sourceUri) {
    return {
      ...data,
      sourceUri,
      plugins: (data.plugins || []).map(plugin => ({
        ...plugin,
        // Compute feature counts
        skillCount: countFeatures(plugin, 'skills'),
        commandCount: countFeatures(plugin, 'commands'),
        agentCount: countFeatures(plugin, 'agents'),
        // Search terms
        searchTerms: [
          ...(plugin.tags || []),
          ...(plugin.keywords || []),
          plugin.name,
          plugin.description,
          plugin.category || ''
        ].filter(Boolean).join(' ').toLowerCase(),
        // Category color
        categoryColor: getCategoryColor(plugin.category),
      }))
    }
  }

  function countFeatures(plugin, type) {
    const value = plugin[type]
    if (!value) return 0
    if (Array.isArray(value)) return value.length
    if (typeof value === 'string') return 1
    if (typeof value === 'object') return Object.keys(value).length
    return 0
  }

  function getCategoryColor(category) {
    const colors = {
      'development': 'blue',
      'dev-tools': 'blue',
      'cloud': 'purple',
      'productivity': 'green',
      'tools': 'yellow',
      'ai': 'pink',
      'security': 'red',
    }
    return colors[category?.toLowerCase()] || 'gray'
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (marketplaceUri.trim()) {
      loadMarketplace(marketplaceUri.trim())
    }
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="border-b border-[var(--ai-border)] bg-[var(--ai-card)]">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <Link to="/" className="text-[var(--ai-green)] hover:underline text-sm mb-4 inline-block font-mono">
            ← cd /foundry
          </Link>
          <div className="flex items-center gap-3 mb-4">
            <h1 className="text-2xl font-bold font-mono">Marketplace Inspector</h1>
            <span className="px-2 py-0.5 bg-[var(--ai-green-subtle)] text-[var(--ai-green)] border border-[var(--ai-green)]/20 text-xs font-mono uppercase">
              BETA
            </span>
          </div>
          <p className="text-[var(--ai-gray-300)] text-sm">
            Inspect any public Claude Code marketplace. Enter a GitHub owner/repo or direct URL.
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-12">
        {/* Search Form */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--ai-gray-500)] font-mono text-sm">$</span>
              <input
                type="text"
                placeholder="e.g., obra/superpowers-marketplace or https://..."
                value={marketplaceUri}
                onChange={(e) => setMarketplaceUri(e.target.value)}
                className="w-full pl-8 pr-4 py-3 bg-black border border-[var(--ai-border)] text-white placeholder-[var(--ai-gray-500)] font-mono text-sm focus:outline-none focus:border-[var(--ai-green)] transition-colors"
              />
            </div>
            <button
              type="submit"
              disabled={loading || !marketplaceUri.trim()}
              className="px-6 py-3 bg-[var(--ai-green)] hover:bg-[var(--ai-green-dim)] disabled:bg-[var(--ai-gray-700)] disabled:text-[var(--ai-gray-500)] text-black font-mono font-semibold transition-colors text-sm"
            >
              {loading ? 'LOADING...' : 'INSPECT'}
            </button>
          </div>
        </form>

        {/* Quick Examples */}
        <div className="mb-8">
          <div className="text-xs text-[var(--ai-gray-500)] mb-2 font-mono uppercase tracking-wider">Try these examples:</div>
          <div className="flex gap-2 flex-wrap">
            {exampleUris.map(example => (
              <button
                key={example.uri}
                onClick={() => {
                  setMarketplaceUri(example.uri)
                  loadMarketplace(example.uri)
                }}
                className="px-3 py-1.5 bg-[var(--ai-card)] hover:bg-[var(--ai-card-hover)] text-[var(--ai-gray-300)] border border-[var(--ai-border)] hover:border-[var(--ai-border-hover)] text-sm font-mono transition-colors"
              >
                {example.label}
              </button>
            ))}
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 p-4 mb-8">
            <div className="text-red-400 font-mono font-medium text-sm mb-1">ERROR: Failed to load marketplace</div>
            <div className="text-red-300 text-sm font-mono">{error}</div>
            <div className="text-[var(--ai-gray-500)] text-xs mt-2 font-mono">
              Note: Only public repositories are supported. The marketplace.json must be at .claude-plugin/marketplace.json
            </div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center font-mono">
              <div className="text-[var(--ai-green)] text-sm mb-4">
                <span className="opacity-60">$</span> fetching marketplace<span className="cursor-blink"></span>
              </div>
            </div>
          </div>
        )}

        {/* Marketplace Results */}
        {marketplace && !loading && (
          <div>
            {/* Marketplace Header */}
            <div className="bg-[var(--ai-card)] border border-[var(--ai-border)] p-6 mb-8">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-xl font-bold font-mono text-white mb-1">{marketplace.name}</h2>
                  {marketplace.metadata?.description && (
                    <p className="text-[var(--ai-gray-300)] text-sm">{marketplace.metadata.description}</p>
                  )}
                </div>
                {marketplace.metadata?.version && (
                  <span className="px-2 py-1 bg-black text-[var(--ai-gray-300)] text-xs font-mono border border-[var(--ai-border)]">
                    v{marketplace.metadata.version}
                  </span>
                )}
              </div>

              <div className="flex flex-wrap gap-6 text-sm font-mono">
                {marketplace.owner?.name && (
                  <div>
                    <span className="text-[var(--ai-gray-500)]">owner:</span>{' '}
                    <span className="text-white">@{marketplace.owner.name}</span>
                  </div>
                )}
                <div>
                  <span className="text-[var(--ai-gray-500)]">plugins:</span>{' '}
                  <span className="text-[var(--ai-green)]">{marketplace.plugins?.length || 0}</span>
                </div>
                <div>
                  <span className="text-[var(--ai-gray-500)]">source:</span>{' '}
                  <code className="text-[var(--ai-green)] text-xs">{marketplace.sourceUri}</code>
                </div>
              </div>

              {/* Install Command */}
              <div className="mt-4 pt-4 border-t border-[var(--ai-border)]">
                <div className="text-xs text-[var(--ai-gray-500)] mb-2 font-mono uppercase tracking-wider">Add this marketplace to Claude Code</div>
                <div className="flex items-center gap-2">
                  <code className="text-[var(--ai-green)] font-mono text-sm">
                    /plugin marketplace add {marketplace.sourceUri}
                  </code>
                  <button
                    onClick={() => navigator.clipboard.writeText(`/plugin marketplace add ${marketplace.sourceUri}`)}
                    className="px-3 py-1.5 bg-[var(--ai-green)] hover:bg-[var(--ai-green-dim)] text-black font-mono text-xs font-semibold transition-colors"
                  >
                    COPY
                  </button>
                </div>
              </div>
            </div>

            {/* Plugins Grid */}
            <div className="mb-4 text-[var(--ai-gray-500)] text-sm font-mono">
              <span className="text-[var(--ai-green)]">{marketplace.plugins?.length || 0}</span> plugin{marketplace.plugins?.length !== 1 ? 's' : ''} in this marketplace
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {marketplace.plugins?.map(plugin => (
                <PluginCard
                  key={plugin.name}
                  plugin={plugin}
                  onSelect={setSelectedPlugin}
                />
              ))}
            </div>

            {(!marketplace.plugins || marketplace.plugins.length === 0) && (
              <div className="text-center py-12 text-[var(--ai-gray-500)] font-mono">
                <p className="text-sm">No plugins found in this marketplace</p>
              </div>
            )}

            {/* Raw JSON Toggle */}
            <details className="mt-8">
              <summary className="text-[var(--ai-gray-500)] text-sm cursor-pointer hover:text-[var(--ai-gray-300)] font-mono">
                View raw marketplace.json
              </summary>
              <pre className="mt-4 bg-black border border-[var(--ai-border)] p-4 overflow-x-auto text-xs text-[var(--ai-green)] font-mono">
                {JSON.stringify(marketplace, null, 2)}
              </pre>
            </details>
          </div>
        )}

        {/* Empty State */}
        {!marketplace && !loading && !error && (
          <div className="text-center py-16 text-[var(--ai-gray-500)] font-mono">
            <div className="text-4xl mb-4 text-[var(--ai-green)]">&gt;_</div>
            <p className="text-sm mb-2">Enter a marketplace URI to inspect</p>
            <p className="text-xs">Supports GitHub owner/repo format or direct URLs to marketplace.json</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-[var(--ai-border)] py-8 mt-12 bg-[var(--ai-card)]">
        <div className="max-w-6xl mx-auto px-6 text-center text-[var(--ai-gray-500)] text-sm font-mono">
          <p className="mb-2">
            <Link to="/" className="text-[var(--ai-green)] hover:underline">
              Foundry Marketplace
            </Link>
            <span className="text-[var(--ai-gray-700)] mx-2">|</span>
            <Link to="/history" className="text-[var(--ai-green)] hover:underline">
              History
            </Link>
          </p>
          <p className="text-xs text-[var(--ai-gray-700)]">Only public repositories are supported in this beta.</p>
        </div>
      </footer>

      {/* Plugin Detail Modal */}
      {selectedPlugin && (
        <PluginDetail
          plugin={selectedPlugin}
          onClose={() => setSelectedPlugin(null)}
        />
      )}
    </div>
  )
}
