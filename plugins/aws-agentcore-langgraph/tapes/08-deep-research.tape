# Deep Research Agent Demo

Output recordings/08-deep-research.gif
Output recordings/08-deep-research.mp4

Source tapes/_settings.tape

Type "cd examples/deep-research-agent"
Enter
Sleep 500ms

Type "ls"
Enter
Sleep 1s

# Show the architecture
Type "cat README.md | head -60"
Enter
Sleep 3s

# Show the agent code
Type "cat agent.py | head -100"
Enter
Sleep 4s

# Show the tools
Type "grep -A 15 '@tool' agent.py | head -40"
Enter
Sleep 3s
