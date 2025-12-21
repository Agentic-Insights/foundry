# Live recording: hero
Output "/home/vaskin/projects/agentcore-lg/recordings/live-hero.gif"
Output "/home/vaskin/projects/agentcore-lg/recordings/live-hero.mp4"

Set Width 1200
Set Height 676
Set FontSize 16
Set FontFamily "JetBrainsMono Nerd Font"
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


Env AWS_PROFILE "ag"

Type "cd /home/vaskin/projects/agentcore-lg/examples/langgraph-web-search"
Enter
Sleep 500ms

Type "head -50 agent.py"
Enter
Sleep 3s

Type "uv run agentcore status"
Enter
Sleep 3s

Type `uv run agentcore invoke {"prompt": "What are the top AI trends in 2024?"}`
Enter
Sleep 15s

