# 📚 Documentation & Changelog Update Guide

The PR Analyzer has been updated to support a dual-file documentation system and advanced configuration tracking.

## 🗂️ New File Structure

Instead of updating a single `README.md`, the analyzer now maintains two distinct files:

### 1. `Updates.readme` (Changelog)
This file is automatically updated with each PR and serves as a running log of changes.

**Updates include:**
- **Added**: New features detected by AI.
- **Removed**: Deprecated or removed functionality.
- **Changed**: Modified behavior.
- **Configuration**: Updates to dependencies, environment variables, or workflows.

**Example Entry:**
```markdown
## PR #123 (2026-02-01)

### Added
- Automated changelog generation

### Configuration
- Added GROQ_API_KEY environment variable
```

### 2. `Documentation.readme` (Product Docs)
This file holds your static product documentation, architecture, and current configuration settings.

**Updates include:**
- **Features**: A consolidated list of key features.
- **Configuration**: Current setup instructions, dependencies, and environment variables.

---

## ⚙️ Configuration Tracking

The analyzer now intelligently detects and logs configuration changes:

- **Requirements**: Changes in `requirements.txt` or `package.json`.
- **Workflows**: Updates to GitHub Action files.
- **Environment**: References to new environment variables.
- **Settings**: Changes in config files (JSON, YAML, TOML).

### How it works
1. **Detection**: The filter now allows configuration files to be analyzed.
2. **Analysis**: The AI explicitly looks for configuration updates.
3. **Logging**: Updates are logged in `Updates.readme` under a `### Configuration` section.
4. **Documentation**: The "Configuration" section in `Documentation.readme` is updated to reflect the current state.

---

## 🚀 How to Use

**No manual action is required!**

The existing `reusable-pr-analyzer.yml` workflow has been updated to automatically handle these new files.

1. **Verify**: Check your repo for `Updates.readme` and `Documentation.readme` after the next PR analysis.
2. **Customize**: You can manually edit `Documentation.readme` to refine descriptions; the analyzer will respect existing content where possible.
