import { useState } from 'react';

export function PluginCard({ plugin, onSelect }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const hasFeatures = plugin.skillCount > 0 || plugin.commandCount > 0 || plugin.agentCount > 0;

  return (
    <div
      className="bg-[var(--ai-card)] border border-[var(--ai-border)] p-6 hover:border-[var(--ai-green)] transition-all cursor-pointer group"
      onClick={() => onSelect(plugin)}
    >
      {/* Header line like terminal prompt */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-lg font-mono font-semibold text-white group-hover:text-[var(--ai-green)] transition-colors">
              {plugin.name}
            </h3>
            {plugin.category && (
              <span className="px-2 py-0.5 bg-[var(--ai-green-subtle)] text-[var(--ai-green)] text-xs font-mono uppercase border border-[var(--ai-green)]/20">
                {plugin.category}
              </span>
            )}
          </div>
          <p className="text-xs text-[var(--ai-gray-500)] font-mono">v{plugin.version}</p>
        </div>

        {plugin.license && (
          <span className="px-2 py-1 bg-black text-[var(--ai-gray-500)] text-xs font-mono border border-[var(--ai-border)]">
            {plugin.license}
          </span>
        )}
      </div>

      <p className="text-[var(--ai-gray-300)] mb-4 leading-relaxed text-sm">
        {plugin.description}
      </p>

      {hasFeatures && (
        <div className="flex gap-4 mb-4 text-xs font-mono">
          {plugin.skillCount > 0 && (
            <div className="flex items-center gap-1.5 text-[var(--ai-green)]">
              <span className="opacity-60">›</span>
              <span>{plugin.skillCount} skill{plugin.skillCount !== 1 ? 's' : ''}</span>
            </div>
          )}

          {plugin.commandCount > 0 && (
            <div className="flex items-center gap-1.5 text-[var(--ai-green)]">
              <span className="opacity-60">›</span>
              <span>{plugin.commandCount} cmd{plugin.commandCount !== 1 ? 's' : ''}</span>
            </div>
          )}

          {plugin.agentCount > 0 && (
            <div className="flex items-center gap-1.5 text-[var(--ai-green)]">
              <span className="opacity-60">›</span>
              <span>{plugin.agentCount} agent{plugin.agentCount !== 1 ? 's' : ''}</span>
            </div>
          )}
        </div>
      )}

      {plugin.tags && plugin.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {plugin.tags.slice(0, isExpanded ? undefined : 5).map(tag => (
            <span
              key={tag}
              className="px-2 py-0.5 bg-black text-[var(--ai-gray-500)] text-xs font-mono hover:text-[var(--ai-gray-300)] transition-colors"
            >
              #{tag}
            </span>
          ))}
          {!isExpanded && plugin.tags.length > 5 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                setIsExpanded(true);
              }}
              className="px-2 py-0.5 text-[var(--ai-green)] text-xs font-mono hover:underline"
            >
              +{plugin.tags.length - 5}
            </button>
          )}
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-[var(--ai-border)] flex items-center justify-between">
        <div className="text-xs text-[var(--ai-gray-500)] font-mono">
          @{plugin.author?.name || 'unknown'}
        </div>

        <button
          className="px-3 py-1.5 bg-[var(--ai-green)] hover:bg-[var(--ai-green-dim)] text-black text-xs font-mono font-semibold transition-colors"
          onClick={(e) => {
            e.stopPropagation();
            onSelect(plugin);
          }}
        >
          VIEW →
        </button>
      </div>
    </div>
  );
}
