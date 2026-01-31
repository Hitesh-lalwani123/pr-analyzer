# 🚀 Using the Reusable Workflow (Zero File Copying!)

This is the **easiest way** to add PR Analyzer to any repository - just add ONE workflow file!

## ✨ How It Works

The reusable workflow:
1. **Downloads** analyzer scripts on-the-fly
2. **Runs** analysis on your PR
3. **Updates** your README  
4. **Cleans up** - leaves no trace!

**No files to copy, no maintenance needed!** 🎉

---

## 📋 Setup Steps

### Step 1: Add Workflow to Your Repository

Create this file: `.github/workflows/pr-analyzer.yml`

```yaml
name: PR Analyzer

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main

jobs:
  analyze-pr:
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

**That's it!** Just 11 lines of YAML.

### Step 2: Add Groq API Key Secret

1. Get FREE key: https://console.groq.com/
2. Go to: **Settings → Secrets → Actions**
3. Add secret:
   - Name: `GROQ_API_KEY`
   - Value: Your Groq API key

### Step 3: Test!

```bash
# Commit the workflow
git add .github/workflows/pr-analyzer.yml
git commit -m "Add PR analyzer"
git push origin main

# Create test PR
git checkout -b feature/test
echo "# Test" >> test.py
git add test.py
git commit -m "feat: test analyzer"
git push origin feature/test
```

Create the PR and watch it work! ✨

---

## ⚙️ Configuration (Optional)

You can customize the behavior with inputs:

```yaml
jobs:
  analyze-pr:
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
    with:
      # Change AI model
      analysis_model: 'mixtral-8x7b-32768'  # Faster model
      
      # Adjust sensitivity
      min_significance: 'high'  # Only update for major changes
```

### Available Models

- `llama-3.3-70b-versatile` (default) - Best quality
- `llama-3.1-70b-versatile` - Fast & capable  
- `mixtral-8x7b-32768` - Very fast
- `llama3-8b-8192` - Fastest

### Significance Levels

- `low` - Update for any changes
- `medium` (default) - Notable features only
- `high` - Major functionality only

---

## 🎯 Benefits Over Manual Copy

| Manual Copy | Reusable Workflow |
|-------------|-------------------|
| Copy 6 files | Add 1 YAML file |
| Maintain dependencies | Auto-updated |
| Manually update | Pull latest automatically |
| Files in your repo | Zero footprint |
| ~30KB of code | ~500 bytes of YAML |

---

## 🔄 How Updates Work

When we improve the analyzer:

**Manual Copy:**
```bash
# You have to manually update all files
curl -O new_analyzer.py
curl -O new_ai_analyzer.py
# ... repeat for all files
```

**Reusable Workflow:**
```yaml
# Already using latest! Nothing to do! ✨
uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
```

The `@main` means it always pulls the latest version automatically.

### Pin to Specific Version

For stability, you can pin to a release:

```yaml
uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@v1.0.0
```

---

## 🛡️ Security

The reusable workflow:
- ✅ Downloads scripts from trusted source only
- ✅ Runs in isolated GitHub Actions environment  
- ✅ Uses your repository's secrets securely
- ✅ Cleans up all temporary files
- ✅ Only has access to PR permissions you grant

**Your GROQ_API_KEY never leaves GitHub's secure environment.**

---

## 🌐 Multiple Repositories

### Option 1: Organization Secret

Set `GROQ_API_KEY` as an **organization secret**:

1. Organization Settings → Secrets → Actions
2. Add `GROQ_API_KEY` once
3. All repos inherit it automatically! ✨

Then all your repos can use:

```yaml
jobs:
  analyze-pr:
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets: inherit  # ← Use org secret
```

### Option 2: Copy & Paste

Same workflow YAML works across all repos:

```bash
# In each repo
cp .github/workflows/pr-analyzer.yml ~/other-repo/.github/workflows/
```

---

## 📊 Comparison: 3 Methods

| Method | Ease | Maintenance | Best For |
|--------|------|-------------|----------|
| **Reusable Workflow** | ⭐⭐⭐ | Auto | **Multiple repos** |
| Manual Copy | ⭐⭐ | Manual | Single repo customization |
| Git Submodule | ⭐ | Manual | Advanced users |

**Recommendation:** Use reusable workflow for 99% of cases! 🚀

---

## 🎬 Quick Start Commands

```bash
# 1. Create workflow file
mkdir -p .github/workflows
cat > .github/workflows/pr-analyzer.yml << 'EOF'
name: PR Analyzer
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]
jobs:
  analyze-pr:
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
EOF

# 2. Commit and push
git add .github/workflows/pr-analyzer.yml
git commit -m "Add PR analyzer"
git push origin main

# 3. Add secret (do this in GitHub UI)
# Settings → Secrets → Actions → New secret: GROQ_API_KEY

# Done! ✅
```

---

## 🔍 Troubleshooting

### "Workflow not found"
- Ensure this repo (`pr-analyzer`) is **public**
- Or grant access if using private repo workflow

### "GROQ_API_KEY not found"
- Check secret name is exactly `GROQ_API_KEY`
- Verify secret exists in Settings → Secrets

### Workflow doesn't trigger
- Ensure caller workflow is on `main` branch
- Check Actions are enabled in repo settings

### Want to customize filtering?
- Use manual copy method instead
- Or fork this repo and modify the reusable workflow

---

## 📚 See Also

- [REUSABLE_GUIDE.md](REUSABLE_GUIDE.md) - Other installation methods
- [README.md](README.md) - Full documentation
- [USAGE_SUMMARY.md](USAGE_SUMMARY.md) - Configuration reference

---

**That's it! One YAML file and you're done! 🎉**
