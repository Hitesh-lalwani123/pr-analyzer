# 🚀 PR Analyzer Quickstart Guide

Add AI-powered PR analysis and automated changelogs to your repository in minutes.

## 📋 Features

- **Automated Analysis**: Generates summaries of code changes using LLMs (Groq).
- **Auto-Changelog**: Updates `Updates.readme` with new features, bug fixes, and configuration changes.
- **Product Docs**: Updates `Documentation.readme` with current configuration and features.
- **Robust**: Works with any branching strategy and ignores test files/spam.

## 🛠️ Setup (3 Minutes)

### 1. Get a Free Groq API Key
1. Visit [Groq Console](https://console.groq.com/).
2. Create a new API Key.
3. Copy it (starts with `gsk_...`).

### 2. Add Repository Secret
1. Go to your GitHub Repository > **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret**.
3. Name: `GROQ_API_KEY`
4. Value: Paste your key.

### 3. Add Workflow File
Create a file `.github/workflows/pr-analyzer.yml` in your repository:

```yaml
name: PR Analyzer
on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main, master]

jobs:
  call-analyzer:
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
    with:
      analysis_model: 'llama-3.3-70b-versatile' # Optional: change model
      min_significance: 'medium'               # Optional: low, medium, high
```

### 4. Push and Test
1. Push the workflow file to your main branch.
2. Create a new branch, verify the workflow runs on PRs.
3. The analyzer will automatically create/update `Updates.readme` and `Documentation.readme` in your PR branch.

---

## ⚠️ Important Note on "Writing to README.md"

If you notice the analyzer still updating `README.md` instead of `Updates.readme`:
it means the workflow is downloading an old version of the scripts.

**Solution:**
Ensure the `Hitesh-lalwani123/pr-analyzer` repository's `main` branch has the latest script changes. The reusable workflow downloads scripts dynamically from the source repo.

## ⚙️ Configuration
The analyzer ignores:
- `*test*` files
- `__pycache__`
- Dotfiles (except ignored .env)

It tracks changes in:
- `requirements.txt`, `package.json`
- `.github/workflows`
- Source code files (`.py`, `.js`, `.ts`, etc.)
