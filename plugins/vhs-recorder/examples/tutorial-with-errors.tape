# tutorial-with-errors.tape
# Shows how to handle errors and corrections in a tutorial

# Output
Output tutorial-with-errors.gif

# Configuration
Set Width 1200
Set Height 650
Set FontSize 32
Set Theme "Nord"
Set Padding 40
Set TypingSpeed 50ms

# Main Recording
Type "# Let's run a command"
Enter
Sleep 1s

# Make a typo
Type "ecko 'Hello World'"
Enter
Sleep 1s

# Show error
Type "# Oops! Typo..."
Enter
Sleep 2s

# Correct it
Type "echo 'Hello World'"
Enter
Wait
Sleep 2s

Type "# There we go! ✓"
Enter
Sleep 2s

# Another example - wrong flag
Type "ls --invalid-flag"
Enter
Sleep 1s

Type "# Wrong flag..."
Enter
Sleep 1s

Type "ls -la"
Enter
Wait
Sleep 3s

Type "# Much better!"
Enter
Sleep 2s
