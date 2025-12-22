# VHS Recording Examples

Real-world examples demonstrating common VHS recording patterns.

## Complete CLI Tool Demo

Full-featured example with setup, main content, and cleanup:

```tape
# demo.tape - Complete CLI tool demonstration

# Outputs
Output demo.gif
Output demo.mp4

# Configuration
Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Catppuccin Mocha"
Set Padding 40
Set TypingSpeed 50ms

# Dependencies
Require git
Require node

# Hidden Setup
Hide
Type "cd /tmp && rm -rf demo-project"
Enter
Sleep 500ms
Type "git clone https://github.com/example/demo-project"
Enter
Sleep 3s
Type "cd demo-project"
Enter
Type "clear"
Enter
Show

# Main Recording
Type "# Let's explore this project"
Enter
Sleep 1s

Type "ls -la"
Enter
Wait
Sleep 2s

Type "cat package.json"
Enter
Wait
Sleep 3s

Type "# Install dependencies"
Enter
Type "npm install"
Enter
Wait /added/
Sleep 2s

Type "# Run the demo"
Enter
Type "npm run demo"
Enter
Wait /Demo complete/
Sleep 3s

# Hidden Cleanup
Hide
Type "cd /tmp && rm -rf demo-project"
Enter
Show
```

## Quick README Demo

Minimal example for README hero animation:

```tape
# readme-demo.tape

Output demo.gif

Set Width 1200
Set Height 600
Set FontSize 36
Set Theme "Catppuccin Mocha"
Set Padding 40

Hide
Type "clear"
Enter
Show

Type "npx create-awesome-app my-app"
Enter
Wait /Success/
Sleep 2s

Type "cd my-app"
Enter
Sleep 500ms

Type "npm start"
Enter
Wait /Server started/
Sleep 3s
```

## Docker Workflow

Demonstrating Docker commands:

```tape
# docker-demo.tape

Output docker-demo.gif
Output docker-demo.mp4

Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Dracula"
Set Padding 40

Require docker

Hide
Type "clear"
Enter
Show

Type "# Build the Docker image"
Enter
Sleep 1s

Type "docker build -t myapp:latest ."
Enter
Wait /Successfully built/
Sleep 2s

Type "# Run the container"
Enter
Type "docker run -d -p 8080:8080 myapp:latest"
Enter
Wait
Sleep 1s

Type "# Check running containers"
Enter
Type "docker ps"
Enter
Wait
Sleep 3s

Type "# View logs"
Enter
Type "docker logs $(docker ps -q -n 1)"
Enter
Wait
Sleep 2s

Hide
Type "docker stop $(docker ps -q)"
Enter
Sleep 2s
Show
```

## Git Workflow Tutorial

Step-by-step Git demonstration:

```tape
# git-tutorial.tape

Output git-tutorial.mp4

Set Width 1400
Set Height 800
Set FontSize 28
Set Theme "GitHub Dark"
Set Padding 30
Set TypingSpeed 100ms  # Slower for tutorial

Require git

Hide
Type "cd /tmp && rm -rf git-demo && mkdir git-demo && cd git-demo"
Enter
Type "git init"
Enter
Sleep 500ms
Type "clear"
Enter
Show

Type "# Initialize a new Git repository"
Enter
Sleep 1s

Type "git init"
Enter
Wait
Sleep 2s

Type "# Create a README file"
Enter
Type "echo '# My Project' > README.md"
Enter
Sleep 1s

Type "# Check status"
Enter
Type "git status"
Enter
Wait
Sleep 3s

Type "# Stage the file"
Enter
Type "git add README.md"
Enter
Sleep 1s

Type "git status"
Enter
Wait
Sleep 2s

Type "# Commit changes"
Enter
Type "git commit -m 'Initial commit'"
Enter
Wait
Sleep 2s

Type "# View commit history"
Enter
Type "git log --oneline"
Enter
Wait
Sleep 3s

Hide
Type "cd /tmp && rm -rf git-demo"
Enter
Show
```

## API Testing Demo

Demonstrating curl/API interactions:

```tape
# api-demo.tape

Output api-demo.gif

Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Nord"
Set Padding 40

Require curl

Hide
Type "clear"
Enter
Show

Type "# Test API endpoints"
Enter
Sleep 1s

Type "curl -s https://api.github.com/zen"
Enter
Wait
Sleep 2s

Type "# Get user information"
Enter
Type "curl -s https://api.github.com/users/octocat | jq '.name, .bio'"
Enter
Wait
Sleep 3s

Type "# Check API rate limit"
Enter
Type "curl -s https://api.github.com/rate_limit | jq '.rate.remaining'"
Enter
Wait
Sleep 2s
```

## Multi-Pane Split Terminal

Simulating split terminal workflow:

```tape
# split-terminal.tape

Output split.gif

Set Width 1400
Set Height 800
Set FontSize 28
Set Theme "Tokyo Night"
Set Padding 40

Hide
Type "clear"
Enter
Show

Type "# Left pane - Start server"
Enter
Type "npm run server"
Enter
Sleep 1s
Wait /Server listening/

# Simulate switching panes with visual separator
Type ""
Enter
Type "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Enter
Type "# Right pane - Run tests"
Enter
Sleep 1s

Type "npm test"
Enter
Wait /Tests passed/
Sleep 3s
```

## Error Recovery Demo

Showing mistake and correction:

```tape
# error-recovery.tape

Output error-recovery.gif

Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Dracula"
Set Padding 40

Hide
Type "clear"
Enter
Show

Type "# Be careful with rm!"
Enter
Sleep 1s

Type "rm -rf production-database/"
Sleep 2s          # Let danger sink in
Backspace 100     # Undo the command

Type "rm -rf test-database/"
Enter
Sleep 2s

Type "# Phew, that was close!"
Enter
Sleep 2s
```

## Keyboard Shortcut Demo

Demonstrating editor shortcuts:

```tape
# shortcuts-demo.tape

Output shortcuts.gif

Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Gruvbox Dark"
Set Padding 40

Hide
Type "nvim demo.txt"
Enter
Sleep 1s
Show

Type "i"  # Enter insert mode
Sleep 500ms

Type "Hello, World!"
Sleep 1s

Escape
Sleep 500ms

Type ":wq"
Enter
Wait
Sleep 1s

Type "cat demo.txt"
Enter
Wait
Sleep 2s

Hide
Type "rm demo.txt"
Enter
Show
```

## Package Installation Comparison

Comparing different package managers:

```tape
# package-managers.tape

Output package-managers.gif

Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Catppuccin Mocha"
Set Padding 40

Hide
Type "clear"
Enter
Show

Type "# npm install"
Enter
Type "time npm install lodash"
Enter
Wait /added/
Sleep 2s

Type ""
Enter
Type "# pnpm install (faster)"
Enter
Type "time pnpm install lodash"
Enter
Wait /done/
Sleep 2s

Type ""
Enter
Type "# bun install (even faster)"
Enter
Type "time bun install lodash"
Enter
Wait /done/
Sleep 3s
```

## Screenshot Sequence

Capturing multiple frames:

```tape
# screenshot-sequence.tape

Output sequence.gif

Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Nord"
Set Padding 40

Hide
Type "clear"
Enter
Show

Type "# Step 1: Initialize"
Enter
Type "make init"
Enter
Wait
Screenshot screenshots/step1-init.png
Sleep 2s

Type "# Step 2: Build"
Enter
Type "make build"
Enter
Wait
Screenshot screenshots/step2-build.png
Sleep 2s

Type "# Step 3: Deploy"
Enter
Type "make deploy"
Enter
Wait
Screenshot screenshots/step3-deploy.png
Sleep 2s
```

## Clipboard Demo

Using copy/paste functionality:

```tape
# clipboard-demo.tape

Output clipboard.gif

Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Dracula"
Set Padding 40

Hide
Type "clear"
Enter
Show

Type "# Generate a token"
Enter
Type "openssl rand -hex 32"
Enter
Wait
Sleep 1s

Copy "export SECRET_TOKEN="
Paste
Enter
Sleep 1s

Type "# Token saved to environment"
Enter
Sleep 2s
```

## Common Pattern: Before/After

Show problem, then solution:

```tape
# before-after.tape

Output before-after.gif

Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "GitHub Dark"
Set Padding 40

Hide
Type "clear"
Enter
Show

Type "# Before: Slow query"
Enter
Sleep 1s

Type "time node slow-query.js"
Enter
Wait /Execution time/
Sleep 3s

Type "# After: Optimized query"
Enter
Sleep 1s

Type "time node optimized-query.js"
Enter
Wait /Execution time/
Sleep 3s

Type "# 10x faster!"
Enter
Sleep 2s
```

## Pattern Library

### Clean Start

```tape
Hide
Type "clear"
Enter
Show
```

### Section Separator

```tape
Type ""
Enter
Type "# Next section"
Enter
Sleep 1s
```

### Dramatic Pause

```tape
Type "important command here"
Sleep 3s  # Build anticipation
Enter
```

### Quick Command Sequence

```tape
Type "git add ."
Enter
Wait
Sleep 500ms

Type "git commit -m 'update'"
Enter
Wait
Sleep 500ms

Type "git push"
Enter
Wait
Sleep 1s
```

### Wait for Long Process

```tape
Type "npm install"
Enter
Wait /added/    # Wait for completion
Sleep 2s        # Let user read summary
```

## Testing Tips

### Quick Iteration with ASCII

```tape
Output test.ascii

# ... your recording commands

# Then run:
# vhs test.tape && cat test.ascii
```

### Debug Timing

Add extra sleep to inspect specific moments:

```tape
Type "command"
Enter
Wait
Sleep 10s  # <-- Long pause to review this moment
```

Remove or reduce the sleep once timing is correct.

## Resources

- Main documentation: [SKILL.md](../SKILL.md)
- VHS syntax: [vhs-syntax.md](./vhs-syntax.md)
- Timing control: [timing-control.md](./timing-control.md)
- Settings reference: [settings.md](./settings.md)
