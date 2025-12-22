import { useState } from 'react';

const categoryColors = {
  blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  green: 'bg-green-500/10 text-green-400 border-green-500/20',
  yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  pink: 'bg-pink-500/10 text-pink-400 border-pink-500/20',
  red: 'bg-red-500/10 text-red-400 border-red-500/20',
  gray: 'bg-gray-500/10 text-gray-400 border-gray-500/20',
};

export function PluginCard({ plugin, onSelect }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const categoryClass = categoryColors[plugin.categoryColor] || categoryColors.gray;

  const hasFeatures = plugin.skillCount > 0 || plugin.commandCount > 0 || plugin.agentCount > 0;

  return (
    <div
      className="bg-gray-900/50 border border-gray-800 rounded-lg p-6 hover:border-gray-700 transition-all cursor-pointer group"
      onClick={() => onSelect(plugin)}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-xl font-semibold text-white group-hover:text-blue-400 transition-colors">
              {plugin.name}
            </h3>
            {plugin.category && (
              <span className={`px-2 py-1 rounded-md text-xs font-medium border ${categoryClass}`}>
                {plugin.category}
              </span>
            )}
          </div>
          <p className="text-sm text-gray-400">v{plugin.version}</p>
        </div>

        {plugin.license && (
          <span className="px-2 py-1 bg-gray-800 text-gray-300 rounded text-xs font-mono">
            {plugin.license}
          </span>
        )}
      </div>

      <p className="text-gray-300 mb-4 leading-relaxed">
        {plugin.description}
      </p>

      {hasFeatures && (
        <div className="flex gap-4 mb-4 text-sm">
          {plugin.skillCount > 0 && (
            <div className="flex items-center gap-1 text-green-400">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{plugin.skillCount} skill{plugin.skillCount !== 1 ? 's' : ''}</span>
            </div>
          )}

          {plugin.commandCount > 0 && (
            <div className="flex items-center gap-1 text-blue-400">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{plugin.commandCount} command{plugin.commandCount !== 1 ? 's' : ''}</span>
            </div>
          )}

          {plugin.agentCount > 0 && (
            <div className="flex items-center gap-1 text-purple-400">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>{plugin.agentCount} agent{plugin.agentCount !== 1 ? 's' : ''}</span>
            </div>
          )}
        </div>
      )}

      {plugin.tags && plugin.tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {plugin.tags.slice(0, isExpanded ? undefined : 5).map(tag => (
            <span
              key={tag}
              className="px-2 py-1 bg-gray-800/50 text-gray-400 rounded text-xs hover:bg-gray-800 transition-colors"
            >
              {tag}
            </span>
          ))}
          {!isExpanded && plugin.tags.length > 5 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                setIsExpanded(true);
              }}
              className="px-2 py-1 text-blue-400 text-xs hover:underline"
            >
              +{plugin.tags.length - 5} more
            </button>
          )}
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-gray-800 flex items-center justify-between">
        <div className="text-xs text-gray-500">
          by {plugin.author?.name || 'Unknown'}
        </div>

        <button
          className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded text-sm font-medium transition-colors"
          onClick={(e) => {
            e.stopPropagation();
            onSelect(plugin);
          }}
        >
          View Details →
        </button>
      </div>
    </div>
  );
}
