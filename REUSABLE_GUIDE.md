# 📋 How to Use This in Your Own Repository

This guide shows you how to add the PR Analyzer & README Updater to **any GitHub repository**.

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your Groq API Key (FREE)

1. Go to https://console.groq.com/
2. Sign in with Google/GitHub
3. Navigate to **API Keys** → Click **"Create API Key"**
4. Copy your key (starts with `gsk_...`)

### Step 2: Copy Files to Your Repository

Copy these files from this repo to your target repository:

```
your-repo/
├── .github/
│   └── workflows/
│       └── pr-analyzer.yml      ← Copy this
├── analyzer.py                   ← Copy this
├── ai_analyzer.py               ← Copy this
├── filters.py                    ← Copy this
├── readme_updater.py            ← Copy this
└── requirements.txt             ← Copy this (or merge with yours)
```

### Step 3: Add GitHub Secret

In your target repository:

1. Go to **Settings → Secrets and variables → Actions**
2. Click **"New repository secret"**
3. Add:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your Groq API key from Step 1

### Step 4: Push & Test!

```bash
# Commit the files
git add .github/workflows/pr-analyzer.yml analyzer.py ai_analyzer.py filters.py readme_updater.py requirements.txt
git commit -m "Add PR analyzer with Groq AI"
git push origin main

# Create a test PR
git checkout -b feature/test-analyzer
echo "# New Feature" >> your_file.py
git add your_file.py
git commit -m "Add new feature"
git push origin feature/test-analyzer

# Create PR on GitHub
```

That's it! The analyzer will automatically run on every PR. 🎉

---

## 📦 Alternative: Use as a Template Repository

### Make This a Template

1. **Create a new repo** from this one:
   - Click "Use this template" on GitHub
   - Or fork this repo

2. **Clone to your project**:
   ```bash
   cd /path/to/your/project
   curl -O https://raw.githubusercontent.com/YOUR_USERNAME/pr-analyzer/main/.github/workflows/pr-analyzer.yml
   curl -O https://raw.githubusercontent.com/YOUR_USERNAME/pr-analyzer/main/analyzer.py
   curl -O https://raw.githubusercontent.com/YOUR_USERNAME/pr-analyzer/main/ai_analyzer.py
   curl -O https://raw.githubusercontent.com/YOUR_USERNAME/pr-analyzer/main/filters.py
   curl -O https://raw.githubusercontent.com/YOUR_USERNAME/pr-analyzer/main/readme_updater.py
   ```

3. **Add the secret** (Step 3 above)

4. **Done!**

---

## ⚙️ Configuration Options

### Change AI Model

Edit `ai_analyzer.py` line 14:

```python
def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
```

**Available FREE models:**
- `llama-3.3-70b-versatile` (default) - Best quality
- `llama-3.1-70b-versatile` - Fast & capable
- `mixtral-8x7b-32768` - Very fast

### Customize File Filters

Edit `filters.py` to add/remove file patterns:

```python
# Add more test patterns
TEST_PATTERNS = [
    r'test_.*\.py$',
    r'.*_test\.py$',
    r'.*\.spec\.ts$',     # Add TypeScript tests
    r'.*\.test\.tsx$',    # Add React tests
]
```

### Adjust Update Threshold

Edit `ai_analyzer.py` → `should_update_readme()`:

```python
def should_update_readme(self, analysis: Dict[str, any]) -> bool:
    # Only update for high significance
    return analysis.get('significance', 'low') == 'high'
```

---

## 🔄 Updating the Workflow

When you want to get updates from this repo:

```bash
# Add this repo as upstream
git remote add pr-analyzer https://github.com/YOUR_USERNAME/pr-analyzer.git

# Pull specific files
git fetch pr-analyzer main
git checkout pr-analyzer/main -- analyzer.py ai_analyzer.py filters.py readme_updater.py

# Commit the updates
git commit -m "Update PR analyzer to latest version"
```

---

## 📝 What It Does

When a PR is created:

1. ✅ Checks if changes are significant (ignores tests, config, README-only)
2. ✅ Analyzes code using Groq AI (Llama 3.3 70B)
3. ✅ Updates README with new/removed features
4. ✅ Posts comment with analysis
5. ✅ Commits README changes to PR branch

---

## 🛠️ Troubleshooting

### Workflow doesn't trigger?
- Ensure `.github/workflows/pr-analyzer.yml` is on main branch
- Check Actions are enabled in repo settings

### "GROQ_API_KEY not found"?
- Verify secret name is exactly `GROQ_API_KEY`
- Check secret is added in the correct repository

### README not updating?
- Check workflow logs in Actions tab
- Verify changes are significant (not just tests)
- Ensure README exists in repo

---

## 💡 Tips

- **Multiple repos?** Set `GROQ_API_KEY` as an organization secret
- **Private repos?** Works the same, just ensure Actions are enabled
- **Custom README structure?** Modify `readme_updater.py` section detection

---

**Need help?** Check the full [README.md](README.md) or open an issue!
