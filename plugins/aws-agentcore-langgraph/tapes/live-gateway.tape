# Live recording: gateway
Output recordings/live-gateway.gif
Output recordings/live-gateway.mp4

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
Type "cd examples/gateway-demo"
Enter
Sleep 500ms
Type "clear"
Enter

# Show the code
Type "cat gateway_demo.py | head -n 15"
Enter
Sleep 2s
Type "clear"
Enter

# Run the Demo
Type "uv run python mock_gateway_demo.py"
Enter

# The demo has its own sleep/timing, so we just wait for it to finish
Sleep 25s

# Finish
Type "# All tools unified behind a single AWS endpoint."
Sleep 2s
Enter
Sleep 2s