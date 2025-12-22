# VHS Timing Control Reference

Complete guide to controlling timing, pacing, and speed in VHS recordings.

## The 3-2-1 Timing Rule

| Situation | Recommended Timing |
|-----------|-------------------|
| After commands | `Sleep 3s` or `Wait` |
| Between actions | `Sleep 2s` |
| Quick pause | `Sleep 1s` |
| Dramatic pause | `Sleep 5s` |

## Global TypingSpeed

Set the default typing speed for all `Type` commands:

```tape
Set TypingSpeed 50ms   # Natural, readable (default)
Set TypingSpeed 100ms  # Slow, tutorial style
Set TypingSpeed 25ms   # Fast, experienced user
Set TypingSpeed 10ms   # Instant (setup/cleanup)
```

**Guidelines**:
- **50ms** - Natural, readable (good default)
- **100ms** - Slow, tutorial style for teaching
- **25ms** - Fast, experienced user feel
- **10ms** - Nearly instant (use for setup/cleanup)

## Per-Command Speed Overrides

Override the global TypingSpeed for individual commands:

```tape
Type@500ms "Pay attention to this!"  # Slow emphasis
Type@10ms "boilerplate code here"   # Fast filler
Type@100ms "npm install --verbose"  # Tutorial pace
Type@25ms "ls -la && cat file.txt"  # Quick succession
```

**Use cases**:
- **Slow typing** (@500ms or @1s) - Emphasize important commands
- **Fast typing** (@10ms) - Skip over boilerplate or known patterns
- **Tutorial pace** (@100ms) - Teaching mode for complex commands

## Wait vs Sleep

### Wait (Dynamic)

Wait for shell prompt or specific output:

```tape
# Wait for shell prompt to return
Type "npm install"
Enter
Wait                    # Waits until prompt reappears

# Wait for specific output text
Type "npm run build"
Enter
Wait /Build succeeded/  # Waits for this text in output

# Wait for text anywhere on screen
Type "docker logs app"
Enter
Wait+Screen /Ready/     # Waits for text on screen

# Wait with timeout (default is 15s)
Type "slow-command"
Enter
Wait@30s /Complete/     # Custom 30 second timeout
```

**When to use Wait**:
- Command duration is variable
- Need to sync with actual output
- Want resilient recordings

### Sleep (Fixed)

Fixed duration pause:

```tape
Sleep 1s    # 1 second
Sleep 2s    # 2 seconds
Sleep 500ms # 500 milliseconds
Sleep 3s    # 3 seconds
```

**When to use Sleep**:
- Known fixed delays
- Pause for viewer to read
- Dramatic effect
- Between unrelated actions

## Timing Patterns

### Pattern: Command-Wait-Pause

```tape
Type "command"
Enter
Wait           # Wait for command to complete
Sleep 2s       # Give viewer time to read output
```

This is the most common pattern for readable recordings.

### Pattern: Quick Succession

```tape
Type "git add ."
Enter
Wait
Sleep 500ms    # Brief pause

Type "git commit -m 'update'"
Enter
Wait
Sleep 500ms
```

For related commands that flow together.

### Pattern: Dramatic Pause

```tape
Type "rm -rf production-database"
Sleep 3s          # Let the danger sink in
Backspace 100     # Phew, that was close!

Type "rm -rf test-database"
Enter
```

### Pattern: Fast Setup

```tape
Hide
Type@10ms "cd /tmp && mkdir demo && cd demo"
Enter
Sleep 500ms
Type@10ms "npm install --silent"
Enter
Sleep 5s
Type "clear"
Enter
Show
```

## Timing Anti-Patterns

### ❌ Too Fast

```tape
# Commands run before output appears
Type "npm install"
Enter
Type "npm start"  # Runs before install finishes!
Enter
```

### ✅ Proper Timing

```tape
Type "npm install"
Enter
Wait /added/      # Wait for install to finish
Sleep 1s          # Give viewer time to read
Type "npm start"
Enter
```

### ❌ Inconsistent Pacing

```tape
Type "command1"
Enter
Type "command2"  # No pause!
Enter
Sleep 5s         # Random long pause
Type "command3"
Enter
```

### ✅ Consistent Pacing

```tape
Type "command1"
Enter
Wait
Sleep 2s

Type "command2"
Enter
Wait
Sleep 2s

Type "command3"
Enter
Wait
Sleep 2s
```

## PlaybackSpeed

Control final video playback speed:

```tape
Set PlaybackSpeed 1.0   # Normal speed (default)
Set PlaybackSpeed 0.5   # Slow motion (50%)
Set PlaybackSpeed 2.0   # Double speed
```

**Use cases**:
- **0.5** - Tutorial/teaching mode
- **1.0** - Normal (default)
- **1.5-2.0** - Fast-paced demo

## Framerate

Set output framerate:

```tape
Set Framerate 60    # Smooth (default)
Set Framerate 30    # Standard
Set Framerate 24    # Cinematic
```

**Guidelines**:
- **60fps** - Smooth, modern (larger file size)
- **30fps** - Standard, good balance
- **24fps** - Smaller files, still acceptable

## Complete Timing Example

```tape
# Configuration
Set TypingSpeed 50ms
Set PlaybackSpeed 1.0
Set Framerate 60

# Fast setup (hidden)
Hide
Type@10ms "cd /tmp/demo"
Enter
Sleep 500ms
Show

# Main content with proper timing
Type "ls -la"
Enter
Wait
Sleep 2s              # Let viewer read output

Type@100ms "# This is important"
Enter
Sleep 1s

Type "cat important-file.txt"
Enter
Wait
Sleep 3s              # More time for important content

Type@25ms "echo 'quick action'"
Enter
Wait
Sleep 1s
```

## Timing Checklist

- [ ] Set global `TypingSpeed` appropriate for content
- [ ] Use `Wait` for variable-duration commands
- [ ] Use `Sleep` for fixed pauses and reading time
- [ ] Apply `@speed` overrides for emphasis
- [ ] Allow 2-3 seconds after important output
- [ ] Use 1 second for quick transitions
- [ ] Fast speed (@10ms) for hidden setup
- [ ] Consistent pacing throughout recording
- [ ] Test timing with actual playback

## Resources

- Main documentation: [SKILL.md](../SKILL.md)
- VHS syntax reference: [vhs-syntax.md](./vhs-syntax.md)
- Settings reference: [settings.md](./settings.md)
