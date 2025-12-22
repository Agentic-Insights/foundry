/**
 * Load marketplace data from the parent repository
 * This runs client-side and fetches marketplace.json
 */

export async function loadMarketplace() {
  try {
    // In production, this will fetch from GitHub raw content
    // In development, we'll use the local file via Vite's public dir
    const isDev = import.meta.env.DEV;

    const url = isDev
      ? '../.claude-plugin/marketplace.json'
      : 'https://raw.githubusercontent.com/Agentic-Insights/claude-plugins-marketplace/main/.claude-plugin/marketplace.json';

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch marketplace: ${response.statusText}`);
    }

    const data = await response.json();
    return enhanceMarketplaceData(data);
  } catch (error) {
    console.error('Error loading marketplace:', error);
    throw error;
  }
}

/**
 * Enhance marketplace data with computed fields
 */
function enhanceMarketplaceData(data) {
  return {
    ...data,
    plugins: data.plugins.map(plugin => ({
      ...plugin,
      // Compute feature counts
      skillCount: countFeatures(plugin, 'skills'),
      commandCount: countFeatures(plugin, 'commands'),
      agentCount: countFeatures(plugin, 'agents'),
      // Parse tags/keywords
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
  };
}

function countFeatures(plugin, type) {
  const value = plugin[type];
  if (!value) return 0;
  if (Array.isArray(value)) return value.length;
  if (typeof value === 'string') return 1;
  if (typeof value === 'object') return Object.keys(value).length;
  return 0;
}

function getCategoryColor(category) {
  const colors = {
    'development': 'blue',
    'cloud': 'purple',
    'productivity': 'green',
    'tools': 'yellow',
    'ai': 'pink',
    'security': 'red',
  };
  return colors[category?.toLowerCase()] || 'gray';
}

/**
 * Load plugin README content
 */
export async function loadPluginReadme(pluginName) {
  try {
    const isDev = import.meta.env.DEV;

    const url = isDev
      ? `../plugins/${pluginName}/README.md`
      : `https://raw.githubusercontent.com/Agentic-Insights/claude-plugins-marketplace/main/plugins/${pluginName}/README.md`;

    const response = await fetch(url);
    if (!response.ok) {
      return null;
    }

    return await response.text();
  } catch (error) {
    console.error(`Error loading README for ${pluginName}:`, error);
    return null;
  }
}
