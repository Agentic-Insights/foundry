# git-workflow.tape
# Shows a complete git workflow from commit to push

# Output
Output git-workflow.gif

# Configuration
Set Width 1200
Set Height 700
Set FontSize 30
Set Theme "Dracula"
Set Padding 40
Set TypingSpeed 50ms
Set BorderRadius 10

# Dependencies
Require git

# Hidden Setup
Hide
Type "cd /tmp && rm -rf demo-repo"
Enter
Sleep 500ms
Type "mkdir demo-repo && cd demo-repo"
Enter
Type "git init"
Enter
Sleep 500ms
Type "echo '# Demo Project' > README.md"
Enter
Type "echo 'console.log(\"Hello\")' > index.js"
Enter
Type "clear"
Enter
Show

# Main Recording - Stage 1: Check status
Type "# Let's commit our changes"
Enter
Sleep 1s

Type "git status"
Enter
Wait
Sleep 2s

# Stage 2: Add files
Type "# Add files to staging"
Enter
Sleep 1s

Type "git add ."
Enter
Sleep 500ms

Type "git status"
Enter
Wait
Sleep 2s

# Stage 3: Commit
Type "# Create the commit"
Enter
Sleep 1s

Type "git commit -m 'feat: initial project setup'"
Enter
Wait
Sleep 2s

# Stage 4: Verify
Type "# Verify commit history"
Enter
Sleep 1s

Type "git log --oneline"
Enter
Wait
Sleep 2s

Type "# Perfect! ✨"
Enter
Sleep 2s

# Hidden Cleanup
Hide
Type "cd /tmp && rm -rf demo-repo"
Enter
Show
