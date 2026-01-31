# 🚀 Quick Start Guide

## Prerequisites

1. **Python 3.11+** installed
2. **GitHub repository** with Actions enabled
3. **Google Gemini API key** - Get it here: https://makersuite.google.com/app/apikey

## Setup Steps

### 1. Add GitHub Secret

1. Go to your repository on GitHub
2. Navigate to: **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Add secret:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key

### 2. Push Code to Repository

```bash
cd E:\ai\pr_analysis

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Add PR analyzer and README updater"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to main
git branch -M main
git push -u origin main
```

### 3. Test the System

Create a test PR to verify everything works:

```bash
# Create feature branch
git checkout -b feature/test-analyzer

# Add a new file with some functionality
echo "def new_feature():
    '''A new amazing feature'''
    return 'This is new!'
" > new_feature.py

# Commit and push
git add new_feature.py
git commit -m "Add new feature for testing analyzer"
git push origin feature/test-analyzer
```

### 4. Create Pull Request

1. Go to your repository on GitHub
2. Click **"Compare & pull request"**
3. Add a description like:
   ```
   This PR adds a new feature that does XYZ.
   
   Features:
   - New function for amazing functionality
   - Improves user experience
   ```
4. Click **"Create pull request"**

### 5. Watch the Magic! ✨

The analyzer will:
1. ✅ Automatically trigger within seconds
2. ✅ Analyze your code changes
3. ✅ Update the README
4. ✅ Post a comment showing what changed
5. ✅ Commit the updated README to your branch

### 6. Review and Merge

1. Check the PR comment for analysis results
2. Review the README changes in the commit
3. If you're happy, merge the PR!
4. If you want changes, edit the README directly

## Troubleshooting

### Workflow doesn't trigger?
- Check that the workflow file is in `.github/workflows/` on the main branch
- Verify GitHub Actions is enabled in repository settings

### "GEMINI_API_KEY not found" error?
- Make sure you added the secret correctly in GitHub Settings
- Secret name must be exactly `GEMINI_API_KEY`

### README not updating?
- Check if changes were significant enough (no test-only changes)
- Look at workflow logs in Actions tab
- Verify Gemini API key is valid

### Getting rate limited?
- Gemini free tier has limits
- Consider upgrading or spacing out PRs

## Advanced Configuration

### Change AI Model

Edit `.github/workflows/pr-analyzer.yml`:

```yaml
env:
  ANALYSIS_MODEL: gemini-1.5-flash  # Free tier model (recommended)
```

### Adjust Sensitivity

Edit `ai_analyzer.py` → `should_update_readme()` function to change when README gets updated.

### Customize Filters

Edit `filters.py` to add/remove file patterns that should be ignored.

## Local Testing (Optional)

To test locally before pushing:

```bash
# Install dependencies
python -m pip install -r requirements.txt --user

# Create .env file
copy .env.example .env
# Edit .env and add your keys

# Set environment variables
$env:PR_NUMBER="123"
$env:REPO_NAME="YOUR_USERNAME/YOUR_REPO"
$env:BASE_REF="main"
$env:HEAD_REF="feature-branch"

# Run analyzer
python analyzer.py
```

## What Gets Analyzed?

### ✅ Analyzed
- New Python/JS/TS/Go/etc. files
- Modified source code
- PR descriptions with feature info

### ⏭️ Skipped
- Test files (`test_*.py`, `*.test.js`)
- README-only changes
- Config file updates (`.json`, `.yaml`)
- Documentation files

## Need Help?

Check the full documentation in [README.md](README.md) and [walkthrough.md](C:\Users\HITESH\.gemini\antigravity\brain\ea063e15-0c80-438c-92e8-4b82174c5117\walkthrough.md)

---

**You're all set! 🎉 Create your first PR and watch the analyzer work its magic!**
