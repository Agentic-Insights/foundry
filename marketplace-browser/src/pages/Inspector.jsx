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
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <Link to="/" className="text-blue-400 hover:text-blue-300 text-sm mb-4 inline-block">
            ← Back to Foundry
          </Link>
          <div className="flex items-center gap-3 mb-4">
            <h1 className="text-3xl font-bold">Marketplace Inspector</h1>
            <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 rounded text-xs font-medium">
              BETA
            </span>
          </div>
          <p className="text-gray-400">
            Inspect any public Claude Code marketplace. Enter a GitHub owner/repo or direct URL.
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-12">
        {/* Search Form */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="e.g., obra/superpowers-marketplace or https://..."
              value={marketplaceUri}
              onChange={(e) => setMarketplaceUri(e.target.value)}
              className="flex-1 px-4 py-3 bg-gray-900 border border-gray-800 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors font-mono text-sm"
            />
            <button
              type="submit"
              disabled={loading || !marketplaceUri.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg font-medium transition-colors"
            >
              {loading ? 'Loading...' : 'Inspect'}
            </button>
          </div>
        </form>

        {/* Quick Examples */}
        <div className="mb-8">
          <div className="text-sm text-gray-500 mb-2">Try these examples:</div>
          <div className="flex gap-2 flex-wrap">
            {exampleUris.map(example => (
              <button
                key={example.uri}
                onClick={() => {
                  setMarketplaceUri(example.uri)
                  loadMarketplace(example.uri)
                }}
                className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded text-sm transition-colors"
              >
                {example.label}
              </button>
            ))}
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-8">
            <div className="text-red-400 font-medium mb-1">Failed to load marketplace</div>
            <div className="text-red-300 text-sm">{error}</div>
            <div className="text-gray-500 text-xs mt-2">
              Note: Only public repositories are supported. The marketplace.json must be at .claude-plugin/marketplace.json
            </div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <p className="text-gray-400">Loading marketplace...</p>
            </div>
          </div>
        )}

        {/* Marketplace Results */}
        {marketplace && !loading && (
          <div>
            {/* Marketplace Header */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6 mb-8">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-2xl font-bold text-white mb-1">{marketplace.name}</h2>
                  {marketplace.metadata?.description && (
                    <p className="text-gray-400">{marketplace.metadata.description}</p>
                  )}
                </div>
                {marketplace.metadata?.version && (
                  <span className="px-2 py-1 bg-gray-800 text-gray-300 rounded text-sm font-mono">
                    v{marketplace.metadata.version}
                  </span>
                )}
              </div>

              <div className="flex flex-wrap gap-4 text-sm">
                {marketplace.owner?.name && (
                  <div>
                    <span className="text-gray-500">Owner:</span>{' '}
                    <span className="text-white">{marketplace.owner.name}</span>
                  </div>
                )}
                <div>
                  <span className="text-gray-500">Plugins:</span>{' '}
                  <span className="text-white">{marketplace.plugins?.length || 0}</span>
                </div>
                <div>
                  <span className="text-gray-500">Source:</span>{' '}
                  <code className="text-green-400 text-xs">{marketplace.sourceUri}</code>
                </div>
              </div>

              {/* Install Command */}
              <div className="mt-4 pt-4 border-t border-gray-800">
                <div className="text-xs text-gray-500 mb-2">Add this marketplace to Claude Code:</div>
                <div className="flex items-center gap-2">
                  <code className="text-green-400 font-mono text-sm">
                    /plugin marketplace add {marketplace.sourceUri}
                  </code>
                  <button
                    onClick={() => navigator.clipboard.writeText(`/plugin marketplace add ${marketplace.sourceUri}`)}
                    className="px-2 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded text-xs transition-colors"
                  >
                    Copy
                  </button>
                </div>
              </div>
            </div>

            {/* Plugins Grid */}
            <div className="mb-4 text-gray-500 text-sm">
              {marketplace.plugins?.length || 0} plugin{marketplace.plugins?.length !== 1 ? 's' : ''} in this marketplace
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
              <div className="text-center py-12 text-gray-500">
                <p>No plugins found in this marketplace</p>
              </div>
            )}

            {/* Raw JSON Toggle */}
            <details className="mt-8">
              <summary className="text-gray-500 text-sm cursor-pointer hover:text-gray-400">
                View raw marketplace.json
              </summary>
              <pre className="mt-4 bg-gray-900 border border-gray-800 rounded-lg p-4 overflow-x-auto text-xs text-gray-300">
                {JSON.stringify(marketplace, null, 2)}
              </pre>
            </details>
          </div>
        )}

        {/* Empty State */}
        {!marketplace && !loading && !error && (
          <div className="text-center py-16 text-gray-500">
            <div className="text-6xl mb-4">🔍</div>
            <p className="text-xl mb-2">Enter a marketplace URI to inspect</p>
            <p className="text-sm">Supports GitHub owner/repo format or direct URLs to marketplace.json</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8 mt-12">
        <div className="max-w-6xl mx-auto px-6 text-center text-gray-500 text-sm">
          <p className="mb-2">
            <Link to="/" className="text-blue-400 hover:text-blue-300">
              Foundry Marketplace
            </Link>
            {' · '}
            <Link to="/history" className="text-blue-400 hover:text-blue-300">
              History
            </Link>
          </p>
          <p className="text-xs">Only public repositories are supported in this beta.</p>
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
