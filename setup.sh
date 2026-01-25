#!/bin/bash
# Setup script for VIPER Claude Code configuration
# Run this after cloning claude-code-skills to your GitHub folder

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Setting up VIPER Claude Code configuration..."

# Create symlink for shared CLAUDE.md in parent directory
if [ -f "$PARENT_DIR/CLAUDE.md" ] && [ ! -L "$PARENT_DIR/CLAUDE.md" ]; then
    echo "Warning: $PARENT_DIR/CLAUDE.md already exists and is not a symlink."
    echo "Please remove it manually and re-run this script."
    exit 1
elif [ -L "$PARENT_DIR/CLAUDE.md" ]; then
    echo "Symlink already exists at $PARENT_DIR/CLAUDE.md"
else
    ln -s "$SCRIPT_DIR/CLAUDE.md" "$PARENT_DIR/CLAUDE.md"
    echo "Created symlink: $PARENT_DIR/CLAUDE.md -> $SCRIPT_DIR/CLAUDE.md"
fi

echo ""
echo "Setup complete!"
echo ""
echo "The shared CLAUDE.md will now be read automatically when working in any"
echo "VIPER repo (viper-metrics-v2-0, viper-operator, viper-inspect)."
echo ""
echo "To copy agents and commands to another repo, run:"
echo "  cp -r $SCRIPT_DIR/.claude/agents /path/to/your/repo/.claude/"
echo "  cp -r $SCRIPT_DIR/.claude/commands /path/to/your/repo/.claude/"
