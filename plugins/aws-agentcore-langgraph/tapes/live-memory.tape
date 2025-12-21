# Live recording: memory
Output recordings/live-memory.gif
Output recordings/live-memory.mp4

Set Width 1200
Set Height 676
Set FontSize 16
Set FontFamily "Ubuntu Mono"
Set LineHeight 1.3
Set Theme "Dracula"
Set Padding 15
Set Margin 10
Set MarginFill "#282a36"
Set BorderRadius 8
Set WindowBar Colorful
Set TypingSpeed 30ms
Set Framerate 30
Set Shell bash

# Setup
Type "cd examples/memory-demo"
Enter
Sleep 500ms
# Use the known-good user with existing memories
Type "export USER_ID=test-fix-1766271018"
Enter
Type "export BEDROCK_AGENTCORE_MEMORY_ID=memory_demo_20251220154641-3KGouIC202"
Enter
Type "clear"
Enter

# --- SESSION 1: THE INPUT ---
# Use --no-recall to simulate a fresh start (ignoring existing LTM)
Type "uv run python memory_demo.py --interactive --no-recall"
Enter
Sleep 6s

# 1. State facts (re-typing what the agent essentially already knows)
Type "Hi! My name is Alex and I strictly only wear polka dot socks on Tuesdays."
Enter
Sleep 6s

Type "quit"
Enter
Sleep 1s
Type "clear"
Enter

# --- THE TRANSITION ---
Type "# (Simulating a new session later that day...)"
Sleep 2s
Type "clear"
Enter

# --- SESSION 2: THE RECALL ---
# Run normally (with LTM enabled). It will work INSTANTLY because of the pre-seeded data.
Type "uv run python memory_demo.py --interactive"
Enter
# Wait for greeting - should acknowledge "Alex"
Sleep 10s

# Interaction: Querying LTM
Type "Do you remember my rule about socks?"
Enter
Sleep 6s

# Cleanup
Type "quit"
Enter
Sleep 2s