# Agentic Insights Plugin Marketplace - Task Runner
# Usage: just <recipe>

set shell := ["bash", "-cu"]

# Default recipe - show available commands
default:
    @just --list

# Bump a specific plugin version (patch/minor/major)
bump-plugin plugin level="patch":
    #!/usr/bin/env bash
    set -euo pipefail

    PLUGIN="{{plugin}}"
    LEVEL="{{level}}"
    MARKETPLACE=".claude-plugin/marketplace.json"
    PLUGIN_JSON="plugins/${PLUGIN}/.claude-plugin/plugin.json"

    if [[ ! -f "$PLUGIN_JSON" ]]; then
        echo "❌ Plugin not found: $PLUGIN"
        echo "Available plugins:"
        ls -1 plugins/
        exit 1
    fi

    # Get current version from marketplace.json
    CURRENT=$(jq -r --arg name "$PLUGIN" '.plugins[] | select(.name == $name) | .version // "0.0.0"' "$MARKETPLACE")

    # Parse version parts
    IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

    # Bump based on level
    case "$LEVEL" in
        major) NEW="$((MAJOR + 1)).0.0" ;;
        minor) NEW="${MAJOR}.$((MINOR + 1)).0" ;;
        patch) NEW="${MAJOR}.${MINOR}.$((PATCH + 1))" ;;
        *) echo "❌ Invalid level: $LEVEL (use patch/minor/major)"; exit 1 ;;
    esac

    echo "📦 Bumping $PLUGIN: $CURRENT → $NEW"

    # Update marketplace.json
    jq --arg name "$PLUGIN" --arg version "$NEW" \
        '(.plugins[] | select(.name == $name) | .version) = $version' \
        "$MARKETPLACE" > "${MARKETPLACE}.tmp" && mv "${MARKETPLACE}.tmp" "$MARKETPLACE"

    # Update plugin's own plugin.json
    jq --arg version "$NEW" '.version = $version' \
        "$PLUGIN_JSON" > "${PLUGIN_JSON}.tmp" && mv "${PLUGIN_JSON}.tmp" "$PLUGIN_JSON"

    echo "✅ Updated:"
    echo "   - $MARKETPLACE"
    echo "   - $PLUGIN_JSON"
    echo ""
    echo "Next: git add -A && git commit -m 'chore($PLUGIN): bump to $NEW'"

# Bump marketplace catalog version
bump-marketplace level="patch":
    #!/usr/bin/env bash
    set -euo pipefail

    LEVEL="{{level}}"
    MARKETPLACE=".claude-plugin/marketplace.json"
    ROOT_PLUGIN=".claude-plugin/plugin.json"
    MANIFEST=".release-please-manifest.json"

    # Get current version
    CURRENT=$(jq -r '.metadata.version // "0.0.0"' "$MARKETPLACE")

    # Parse and bump
    IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"
    case "$LEVEL" in
        major) NEW="$((MAJOR + 1)).0.0" ;;
        minor) NEW="${MAJOR}.$((MINOR + 1)).0" ;;
        patch) NEW="${MAJOR}.${MINOR}.$((PATCH + 1))" ;;
        *) echo "❌ Invalid level: $LEVEL"; exit 1 ;;
    esac

    echo "📦 Bumping marketplace: $CURRENT → $NEW"

    # Update all marketplace version locations
    jq --arg v "$NEW" '.metadata.version = $v' "$MARKETPLACE" > "${MARKETPLACE}.tmp" && mv "${MARKETPLACE}.tmp" "$MARKETPLACE"
    jq --arg v "$NEW" '.version = $v' "$ROOT_PLUGIN" > "${ROOT_PLUGIN}.tmp" && mv "${ROOT_PLUGIN}.tmp" "$ROOT_PLUGIN"
    jq --arg v "$NEW" '."."] = $v' "$MANIFEST" > "${MANIFEST}.tmp" && mv "${MANIFEST}.tmp" "$MANIFEST"

    echo "✅ Updated marketplace to $NEW"

# Release a plugin (bump + commit + push)
release-plugin plugin level="patch" message="":
    #!/usr/bin/env bash
    set -euo pipefail

    PLUGIN="{{plugin}}"
    LEVEL="{{level}}"
    MSG="{{message}}"

    # Bump the version
    just bump-plugin "$PLUGIN" "$LEVEL"

    # Get new version for commit message
    NEW=$(jq -r --arg name "$PLUGIN" '.plugins[] | select(.name == $name) | .version' .claude-plugin/marketplace.json)

    # Build commit message
    if [[ -z "$MSG" ]]; then
        COMMIT_MSG="chore($PLUGIN): release v$NEW"
    else
        COMMIT_MSG="chore($PLUGIN): release v$NEW - $MSG"
    fi

    # Commit and push
    git add -A
    git commit -m "$COMMIT_MSG"
    git push origin main

    echo ""
    echo "🚀 Released $PLUGIN v$NEW"

# Show current versions of all plugins
versions:
    @echo "📦 Plugin Versions:"
    @echo ""
    @jq -r '.plugins[] | "  \(.name): \(.version // "unversioned")"' .claude-plugin/marketplace.json
    @echo ""
    @echo "📦 Marketplace: $(jq -r '.metadata.version' .claude-plugin/marketplace.json)"

# Validate plugin structure
validate plugin:
    #!/usr/bin/env bash
    set -euo pipefail

    PLUGIN="{{plugin}}"
    DIR="plugins/$PLUGIN"

    echo "🔍 Validating $PLUGIN..."

    ERRORS=0

    # Check required files
    [[ -f "$DIR/.claude-plugin/plugin.json" ]] || { echo "❌ Missing .claude-plugin/plugin.json"; ERRORS=$((ERRORS+1)); }
    [[ -f "$DIR/README.md" ]] || { echo "❌ Missing README.md"; ERRORS=$((ERRORS+1)); }

    # Check plugin.json has required fields
    if [[ -f "$DIR/.claude-plugin/plugin.json" ]]; then
        jq -e '.name' "$DIR/.claude-plugin/plugin.json" > /dev/null || { echo "❌ plugin.json missing 'name'"; ERRORS=$((ERRORS+1)); }
        jq -e '.description' "$DIR/.claude-plugin/plugin.json" > /dev/null || { echo "❌ plugin.json missing 'description'"; ERRORS=$((ERRORS+1)); }
    fi

    # Check marketplace.json has entry
    if ! jq -e --arg name "$PLUGIN" '.plugins[] | select(.name == $name)' .claude-plugin/marketplace.json > /dev/null 2>&1; then
        echo "❌ Plugin not in marketplace.json"
        ERRORS=$((ERRORS+1))
    fi

    # Validate skills with skills-ref (Agent Skills spec)
    if [[ -d "$DIR/skills" ]]; then
        echo "🔍 Validating skills with skills-ref..."
        for skill_dir in "$DIR/skills"/*; do
            if [[ -d "$skill_dir" ]]; then
                skill_name=$(basename "$skill_dir")
                if ! uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
                    skills-ref validate "$skill_dir" 2>&1; then
                    echo "❌ Skill validation failed: $skill_name"
                    ERRORS=$((ERRORS+1))
                fi
            fi
        done
    fi

    if [[ $ERRORS -eq 0 ]]; then
        echo "✅ $PLUGIN is valid"
    else
        echo ""
        echo "❌ $ERRORS error(s) found"
        exit 1
    fi

# Validate all plugins
validate-all:
    #!/usr/bin/env bash
    for plugin in plugins/*/; do
        name=$(basename "$plugin")
        just validate "$name" || true
        echo ""
    done

# Add a new plugin to marketplace.json
add-plugin plugin:
    #!/usr/bin/env bash
    set -euo pipefail

    PLUGIN="{{plugin}}"
    PLUGIN_JSON="plugins/$PLUGIN/.claude-plugin/plugin.json"
    MARKETPLACE=".claude-plugin/marketplace.json"

    if [[ ! -f "$PLUGIN_JSON" ]]; then
        echo "❌ Plugin not found: $PLUGIN"
        exit 1
    fi

    # Check if already in marketplace
    if jq -e --arg name "$PLUGIN" '.plugins[] | select(.name == $name)' "$MARKETPLACE" > /dev/null 2>&1; then
        echo "⚠️  Plugin already in marketplace.json"
        exit 0
    fi

    # Extract info from plugin.json
    NAME=$(jq -r '.name' "$PLUGIN_JSON")
    DESC=$(jq -r '.description // "No description"' "$PLUGIN_JSON")
    VERSION=$(jq -r '.version // "0.1.0"' "$PLUGIN_JSON")
    LICENSE=$(jq -r '.license // "Apache-2.0"' "$PLUGIN_JSON")

    # Add to marketplace
    jq --arg name "$NAME" \
       --arg source "./plugins/$PLUGIN" \
       --arg desc "$DESC" \
       --arg version "$VERSION" \
       --arg license "$LICENSE" \
       '.plugins += [{
         "name": $name,
         "source": $source,
         "description": $desc,
         "version": $version,
         "author": {"name": "agentic-insights"},
         "license": $license
       }]' "$MARKETPLACE" > "${MARKETPLACE}.tmp" && mv "${MARKETPLACE}.tmp" "$MARKETPLACE"

    echo "✅ Added $PLUGIN to marketplace.json"
