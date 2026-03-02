# Project Instructions

## Critical Constraints
- **Command Style**: Never use subshells or command substitutions (e.g., avoid `$(...)` or backticks) in bash commands.
- **Git Commits**: For multi-line commit messages, consistently use multiple `-m` flags instead of `cat <<EOF` or subshells. This ensures auto-approval by the security filter.
- **Example**: `git commit -m "feat: core engine" -m "Detailed description here"`

## Design Document Reference Requirement
- When designing features, implementing code, debugging issues, or mitigating incidents, always check for relevant documentation in the `docs/` folder first.
- Treat documents in `docs/` as the primary source of truth for architecture, constraints, and intended behavior.
- If a relevant design doc exists, align decisions and fixes with it before proposing changes.
- If documentation is missing or outdated, explicitly note that and proceed with justified assumptions.

## Style Preferences
- Prefer clear, concise commit messages.
- Follow python best practices for AI/LLM integration.