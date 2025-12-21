# VHS Recording Examples

This directory contains example tape files demonstrating various VHS recording patterns.

## Examples

### 1. Basic Demo (`basic-demo.tape`)

**Purpose**: Minimal example showing fundamental VHS concepts.

**Features**:
- Simple output declaration
- Basic configuration
- Typing and command execution
- Sleep for timing

**Generate**:
```bash
vhs basic-demo.tape
```

**Use case**: Quick introduction to VHS, README hero animations.

---

### 2. CLI Tool Demo (`cli-tool-demo.tape`)

**Purpose**: Demonstrate installing and using a CLI tool.

**Features**:
- Multiple output formats (GIF + MP4)
- Hidden setup and cleanup
- Dependency checking with `Require`
- Multi-stage demonstration
- WindowBar styling

**Generate**:
```bash
vhs cli-tool-demo.tape
```

**Use case**: Tool documentation, release announcements, tutorial videos.

---

### 3. Git Workflow (`git-workflow.tape`)

**Purpose**: Complete git workflow from status to commit.

**Features**:
- Multi-stage process demonstration
- Status checking between steps
- Wait for command completion
- Clean narrative structure

**Generate**:
```bash
vhs git-workflow.tape
```

**Use case**: Git tutorials, workflow documentation, teaching materials.

---

### 4. Tutorial with Errors (`tutorial-with-errors.tape`)

**Purpose**: Show realistic tutorials including mistakes and corrections.

**Features**:
- Demonstrating typos and fixes
- Educational narrative
- Showing wrong → right patterns
- Human-friendly pacing

**Generate**:
```bash
vhs tutorial-with-errors.tape
```

**Use case**: Teaching materials, showing common mistakes, realistic demos.

---

## Running Examples

### Generate All Examples

```bash
# Generate all recordings at once
for tape in examples/*.tape; do
  echo "Generating $tape..."
  vhs "$tape"
done
```

### Preview Before Rendering

Use ASCII output for quick iteration:

```bash
# Modify tape file temporarily
sed 's/Output .*/Output preview.ascii/' basic-demo.tape | vhs -
cat preview.ascii
```

## Customization

Feel free to modify these examples:

1. **Change themes**: See available themes with `vhs themes`
2. **Adjust dimensions**: Modify `Width` and `Height` for your needs
3. **Update timing**: Tweak `Sleep` durations and `TypingSpeed`
4. **Add content**: Extend with your own commands

## Best Practices Demonstrated

These examples showcase:

✅ **Structure**: Output → Settings → Content pattern
✅ **Hidden blocks**: Setup/cleanup with `Hide`/`Show`
✅ **Timing**: Appropriate use of `Sleep` and `Wait`
✅ **Narrative**: Comments explaining what's happening
✅ **Dependencies**: Checking requirements with `Require`
✅ **Cleanup**: Proper teardown of demo environments

## Common Patterns

### The Clean Slate Pattern
```tape
Hide
Type "clear"
Enter
Show
```

### The Multi-Stage Pattern
```tape
# Stage 1: Show problem
Type "command-with-issue"
Sleep 2s

# Stage 2: Fix it
Type "correct-command"
Sleep 2s

# Stage 3: Verify
Type "verification-command"
Sleep 3s
```

### The Hidden Setup Pattern
```tape
Hide
Type "cd /tmp && git clone repo"
Enter
Sleep 3s
Type "clear"
Enter
Show

# Now record the actual demo
```

## Tips

1. **Start simple**: Begin with `basic-demo.tape` and modify
2. **Test timing**: Run multiple times to find right pace
3. **Use ASCII**: Quick preview format for iteration
4. **Add comments**: Make tapes self-documenting
5. **Clean up**: Always use `Hide` for setup/teardown

## Resources

- [VHS Documentation](https://github.com/charmbracelet/vhs)
- [Plugin README](../README.md)
- [VHS Manual](https://github.com/charmbracelet/vhs/blob/main/README.md)

---

**Want more examples?** Check the [VHS GitHub repository](https://github.com/charmbracelet/vhs/tree/main/examples) for additional patterns and use cases.
