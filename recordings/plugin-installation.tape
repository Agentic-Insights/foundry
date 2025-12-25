# VHS documentation: https://github.com/charmbracelet/vhs
#
# Demo: Installing Agentic Insights plugins using Claude Code
#

Output recordings/plugin-installation.gif
Output recordings/plugin-installation.mp4

Set Shell "bash"
Set FontFamily "Ubuntu Mono"
Set Theme "Catppuccin Mocha"
Set FontSize 14
Set Width 1200
Set Height 700
Set Padding 20
Set TypingSpeed 50ms
Set PlaybackSpeed 1.0

# Step 1: Start Claude
Type "claude" Sleep 600ms
Enter
Sleep 4s

# Step 2: Install the marketplace
Type "/plugin marketplace add Agentic-Insights/claude-plugins-marketplace" Sleep 500ms
Enter
Sleep 4s

# Step 3: Install a plugin from the marketplace
Type "/plugin install aws-agentcore-langgraph@agentic-insights" Sleep 500ms
Enter
Sleep 4s

# Step 4: Quit (Ctrl+C twice)
Ctrl+C
Ctrl+C
Sleep 2s

# Step 5: Restart Claude
Type "claude /plugins" Sleep 500ms
Enter
Type "agentcore"
Sleep 3s

# Step 6: Tab to see Marketplaces
Tab
Tab
Sleep 2s
Ctrl+C
Ctrl+C

# Final message
Sleep 1s
Type "# ✓ Marketplace installed - plugins ready to discover!" Sleep 500ms Enter
Type "# Visit: https://github.com/Agentic-Insights/claude-plugins-marketplace" Sleep 500ms Enter

Sleep 3s
