# cli-tool-demo.tape
# Demonstrates a CLI tool installation and usage

# Outputs
Output cli-tool-demo.gif
Output cli-tool-demo.mp4

# Configuration
Set Width 1400
Set Height 800
Set FontSize 28
Set Theme "GitHub Dark"
Set Padding 40
Set TypingSpeed 50ms
Set WindowBar Colorful

# Dependencies
Require node
Require npm

# Hidden Setup
Hide
Type "cd /tmp && rm -rf demo-cli"
Enter
Sleep 500ms
Type "mkdir demo-cli && cd demo-cli"
Enter
Type "npm init -y > /dev/null 2>&1"
Enter
Sleep 1s
Type "clear"
Enter
Show

# Main Recording - Installation
Type "# Let's install the CLI tool"
Enter
Sleep 1s

Type "npm install -g awesome-cli"
Enter
Sleep 2s
Type "# (simulated - in real demo this would actually install)"
Enter
Sleep 2s

# Usage demonstration
Type "# Now let's use it"
Enter
Sleep 1s

Type "awesome-cli --help"
Enter
Sleep 3s

Type "awesome-cli init my-project"
Enter
Sleep 2s

Type "# Check what was created"
Enter
Type "ls -la my-project"
Enter
Sleep 3s

Type "# Success! 🎉"
Enter
Sleep 2s

# Hidden Cleanup
Hide
Type "cd /tmp && rm -rf demo-cli"
Enter
Show
