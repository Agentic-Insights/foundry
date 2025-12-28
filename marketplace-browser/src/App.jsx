import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { loadMarketplace } from './data/marketplaceLoader'
import { PluginCard } from './components/PluginCard'
import { PluginDetail } from './components/PluginDetail'
import { History } from './pages/History'
import { Inspector } from './pages/Inspector'
import './App.css'

function Marketplace() {
  const [marketplace, setMarketplace] = useState(null)
  const [selectedPlugin, setSelectedPlugin] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadMarketplace()
      .then(data => {
        setMarketplace(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  const categories = marketplace?.plugins
    ? [...new Set(marketplace.plugins.map(p => p.category).filter(Boolean))]
    : []

  const filteredPlugins = marketplace?.plugins?.filter(plugin => {
    const matchesSearch = !searchQuery ||
      plugin.searchTerms?.includes(searchQuery.toLowerCase())
    const matchesCategory = !selectedCategory ||
      plugin.category === selectedCategory
    return matchesSearch && matchesCategory
  }) || []

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading marketplace...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center text-red-400">
          <p className="text-xl mb-2">Failed to load marketplace</p>
          <p className="text-sm text-gray-500">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Hero Section */}
      <header className="border-b border-gray-800 bg-gray-900/50">
        <div className="max-w-6xl mx-auto px-6 py-16">
          <div className="text-center mb-8">
            <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              Agentic Insights Foundry
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Where agentic tools are forged. Claude Code plugins for AI engineering.
            </p>
          </div>

          {/* Philosophy */}
          <div className="bg-gray-800/30 border border-gray-700/50 rounded-lg p-6 mb-8 max-w-3xl mx-auto">
            <p className="text-gray-300 leading-relaxed text-center">
              Context is everything. Before agents can act, they must understand.
            </p>
            <p className="text-gray-500 text-sm mt-4 text-center">
              From{' '}
              <Link to="/history" className="text-blue-400 hover:text-blue-300">
                Codebase Context
              </Link>{' '}
              to{' '}
              <a href="https://agents.md" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                AGENTS.md
              </a>{' '}
              to{' '}
              <a href="https://agentskills.io" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                Skills
              </a>
              {' '}— open standards for context engineering.{' '}
              <Link to="/history" className="text-gray-400 hover:text-gray-300 underline">
                Read the story →
              </Link>
            </p>
          </div>

          {/* Quick Install */}
          <div className="bg-gray-950 border border-gray-800 rounded-lg p-4 max-w-xl mx-auto">
            <div className="text-xs text-gray-500 mb-2 text-center">Add this marketplace to Claude Code:</div>
            <div className="flex items-center justify-center gap-2">
              <code className="text-green-400 font-mono text-sm">/plugin marketplace add agentic-insights/foundry</code>
              <button
                onClick={() => navigator.clipboard.writeText('/plugin marketplace add agentic-insights/foundry')}
                className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded text-xs transition-colors"
              >
                Copy
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        {/* Search and Filter */}
        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search plugins..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-3 bg-gray-900 border border-gray-800 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                !selectedCategory
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              All
            </button>
            {categories.map(category => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors capitalize ${
                  selectedCategory === category
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Plugin Count */}
        <div className="mb-6 text-gray-500 text-sm">
          {filteredPlugins.length} plugin{filteredPlugins.length !== 1 ? 's' : ''} available
        </div>

        {/* Plugin Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredPlugins.map(plugin => (
            <PluginCard
              key={plugin.name}
              plugin={plugin}
              onSelect={setSelectedPlugin}
            />
          ))}
        </div>

        {filteredPlugins.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <p className="text-xl mb-2">No plugins found</p>
            <p className="text-sm">Try adjusting your search or filter</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8 mt-12">
        <div className="max-w-6xl mx-auto px-6 text-center text-gray-500 text-sm">
          <p className="mb-2">
            <a href="https://github.com/agentic-insights/foundry" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
              GitHub
            </a>
            {' · '}
            <Link to="/history" className="text-blue-400 hover:text-blue-300">
              History
            </Link>
            {' · '}
            <Link to="/inspect" className="text-blue-400 hover:text-blue-300">
              Inspector
              <span className="ml-1 text-yellow-400 text-xs">β</span>
            </Link>
            {' · '}
            <a href="https://agentskills.io" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
              Agent Skills Spec
            </a>
          </p>
          <p>Apache-2.0 Licensed</p>
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

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Marketplace />} />
        <Route path="/history" element={<History />} />
        <Route path="/inspect" element={<Inspector />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
