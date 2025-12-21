# Live recording: lifecycle
Output recordings/live-lifecycle.gif
Output recordings/live-lifecycle.mp4

Set Width 1200
Set Height 800
Set FontSize 16
Set FontFamily "Ubuntu Mono"
Set LineHeight 1.3
Set Theme "Dracula"
Set Padding 15
Set Margin 10
Set MarginFill "#282a36"
Set BorderRadius 8
Set WindowBar Colorful
Set TypingSpeed 40ms
Set Framerate 30
Set Shell bash

# Setup
Type "cd examples/runtime-demo"
Enter
Sleep 500ms
Type "clear"
Enter

# Narrative
Type "# Let's deploy a LangGraph agent from scratch."
Sleep 1.5
Enter
Type "# The 'agentcore' CLI manages the full lifecycle."
Sleep 1.5
Enter
Sleep 1s
Type "clear"
Enter

# Run the Mock Script which simulates user typing the commands
# Actually, the mock script just prints the output.
# To make it look like *I* am typing the commands, the mock script uses `type_cmd`.
# So I just run the script silently? No, the script prints `$ command`.
# So I should run the script and let IT drive the visuals.

Type "./mock_lifecycle.sh"
Enter

# The script handles the sleeps and output.
# We just wait for it to finish.
# Based on the script, it takes about:
# 1s + 1s + 0.5s + 0.5s + 0.5s + 1s = 4.5s (Config)
# 1s + 1s + 1.5s + 1s + 0.5s + 0.5s + 0.5s + 0.8s + 0.5s + 2s = 9.3s (Launch)
# 1s + 1s + 1s + 2s = 5s (Invoke)
# 1s + 1s + 1.5s = 3.5s (Destroy)
# Total ~22-25s.

Sleep 28s

# Ending
Type "# Infrastructure as Code, simplified."
Sleep 2s
Enter
Sleep 2s
