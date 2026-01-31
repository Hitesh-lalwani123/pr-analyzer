# 🎯 Making PR Analyzer Reusable - Complete Guide

## ✅ What We Did

Transformed the PR Analyzer into a **reusable workflow** that can be easily added to any GitHub repository.

### Files Created

1. **REUSABLE_GUIDE.md** - Comprehensive guide with 3 installation methods
2. **setup.py** - Automated installation script
3. **Updated README.md** - Emphasizes reusability

### Files Cleaned Up

Removed temporary/test files:
- GEMINI_FIX.md
- GROK_MIGRATION.md  
- TESTING_CHECKLIST.md
- TEST_PR_INSTRUCTIONS.md
- awesome_feature.py
- email_validator.py

---

## 🚀 How to Use in Other Repositories

### Method 1: Automated Setup Script (Easiest!)

```bash
# In your target repository
curl -O https://raw.githubusercontent.com/Hitesh-lalwani123/pr-analyzer/main/setup.py
python setup.py
```

The script will:
- Copy all necessary files
- Create `.github/workflows` directory
- Guide you through next steps

### Method 2: Manual File Copy

Copy these 6 files to your repository:

```
your-repo/
├── .github/workflows/pr-analyzer.yml  ← Workflow definition
├── analyzer.py                         ← Main orchestrator  
├── ai_analyzer.py                     ← Groq AI integration
├── filters.py                          ← File filtering logic
├── readme_updater.py                  ← README manipulation
└── requirements.txt                   ← Dependencies (or merge)
```

### Method 3: Git Submodule (For Multiple Repos)

```bash
# Add as submodule
git submodule add https://github.com/Hitesh-lalwani123/pr-analyzer .pr-analyzer

# Symlink the workflow
ln -s ../.pr-analyzer/.github/workflows/pr-analyzer.yml .github/workflows/

# Copy Python files
cp .pr-analyzer/*.py .
```

---

## 📋 Setup Steps (All Methods)

After copying files:

### 1. Get FREE Groq API Key

```
1. Visit: https://console.groq.com/
2. Sign in with Google/GitHub  
3. Go to "API Keys" → "Create API Key"
4. Copy the key (starts with gsk_...)
```

### 2. Add GitHub Secret

```
1. Go to your repo: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: GROQ_API_KEY
4. Value: <paste your key>
```

### 3. Push to Main Branch

```bash
git add .github/workflows/pr-analyzer.yml *.py requirements.txt
git commit -m "Add PR analyzer with Groq AI"
git push origin main
```

### 4. Test It!

```bash
# Create test branch
git checkout -b feature/test-analyzer

# Make a change
echo "# New Feature" >> newfile.py
git add newfile.py
git commit -m "feat: add new feature"
git push origin feature/test-analyzer

# Create PR on GitHub
# ✨ Watch the magic happen!
```

---

## ⚙️ Configuration Options

### Change AI Model

Edit `ai_analyzer.py`:

```python
def __init__(self, api_key: Optional[str] = None, model: str = "mixtral-8x7b-32768"):
    # Change model here ▲
```

**Available FREE models:**
- `llama-3.3-70b-versatile` - Best quality (default)
- `llama-3.1-70b-versatile` - Fast & capable
- `mixtral-8x7b-32768` - Very fast
- `llama3-8b-8192` - Fastest

### Customize File Filters

Edit `filters.py` to add more patterns:

```python
# Add your test patterns
TEST_PATTERNS = [
    r'spec/.*\.rb$',      # Ruby specs
    r'.*\.spec\.ts$',     # TypeScript tests
    # Add more...
]
```

### Adjust Sensitivity

Edit `ai_analyzer.py` → `should_update_readme()`:

```python
# Only update for high significance
return analysis.get('significance') == 'high'
```

---

## 🔄 Workflow Behavior

### When It Runs

✅ PR opened/updated to main  
✅ PR approved (if previously skipped)

### What It Skips

⏭️ README-only changes  
⏭️ Test-only changes  
⏭️ Commits with `[skip-pr-analyzer]`  
⏭️ Its own README commits

### What It Does

1. Analyzes code changes with Groq AI
2. Detects new/removed features
3. Updates README Features section
4. Posts PR comment with analysis
5. Commits changes to PR branch

---

## 💡 Pro Tips

### Multiple Repositories?

Set `GROQ_API_KEY` as an **Organization Secret**:
1. Organization Settings → Secrets → Actions
2. Add `GROQ_API_KEY` once
3. All repos can use it! ✨

### Private Repositories?

Works the same! Just ensure:
- Actions are enabled
- Workflows have write permissions

### Custom README Structure?

Modify `readme_updater.py`:

```python
# Change section names
FEATURES_HEADERS = [
    '## Features',
    '## ✨ Features', 
    '## 🚀 Capabilities',  # Add yours
]
```

---

## 📦 Core Files Explained

| File | Purpose |
|------|---------|
| `pr-analyzer.yml` | GitHub Actions workflow definition |
| `analyzer.py` | Main orchestrator, coordinates everything |
| `ai_analyzer.py` | Groq API integration & prompt engineering |
| `filters.py` | Determines which files to analyze |
| `readme_updater.py` | Parses and updates README structure |
| `requirements.txt` | Python dependencies |

**Total Size:** ~30KB of Python + 1 YAML file

---

## 🛠️ Troubleshooting

### "GROQ_API_KEY not found"
- Check secret name is exactly `GROQ_API_KEY`
- Verify it's in the correct repository
- For orgs, check repository has access to org secret

### Workflow doesn't trigger
- Ensure workflow file is on `main` branch
- Check Actions are enabled (Settings → Actions)
- Verify workflow has correct permissions

### README not updating
- Check workflow logs in Actions tab
- Verify changes are significant (not just tests)
- Ensure README file exists in repository

### Analysis seems off
- Try different model (edit `ai_analyzer.py`)
- Adjust prompts in `_build_analysis_prompt()`
- Check PR description is informative

---

## 📚 Additional Resources

- [REUSABLE_GUIDE.md](REUSABLE_GUIDE.md) - Detailed installation guide
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [README.md](README.md) - Full documentation
- Groq Docs: https://console.groq.com/docs

---

## ✨ Success Story

This workflow is now production-ready! You've transformed a single-repo tool into a reusable component that can:

✅ Be installed in minutes  
✅ Work with any GitHub repository  
✅ Use 100% free Groq API  
✅ Require zero maintenance  
✅ Save hours of documentation work  

**Next step:** Share this with your team and start using it across all your projects! 🚀
