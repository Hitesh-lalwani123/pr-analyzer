# 🚀 Quick Start Guide - Using Grok AI

## Prerequisites

1. **Python 3.11+** installed
2. **GitHub repository** with Actions enabled
3. **xAI Grok API key** - Get it here: https://console.x.ai/

## Setup Steps

### 1. Get Your Grok API Key

1. Go to https://console.x.ai/
2. Sign in or create an account
3. Navigate to **API Keys** section
4. Click **"Create API Key"**
5. Copy your API key (starts with `xai-...`)

### 2. Add GitHub Secret

1. Go to your repository on GitHub
2. Navigate to: **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Add secret:
   - **Name**: `XAI_API_KEY`
   - **Value**: Your xAI API key

### 3. Push Code to Repository

```bash
cd E:\ai\pr_analysis

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Add PR analyzer with Grok AI"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to main
git branch -M main
git push -u origin main
```

### 4. Test the System

Create a test PR to verify everything works:

```bash
# Create feature branch
git checkout -b feature/test-grok-analyzer

# Add a new file with some functionality
echo "def awesome_feature():
    '''An amazing new feature'''
    return 'Powered by Grok!'
" > awesome_feature.py

# Commit and push
git add awesome_feature.py
git commit -m "Add awesome feature using Grok analyzer"
git push origin feature/test-grok-analyzer
```

### 5. Create Pull Request

1. Go to your repository on GitHub
2. Click **"Compare & pull request"**
3. Add a description like:
   ```
   This PR adds an awesome new feature.
   
   Features:
   - New function for amazing functionality
   - Powered by Grok AI analysis
   ```
4. Click **"Create pull request"**

### 6. Watch the Magic! ✨

The Grok-powered analyzer will:
1. ✅ Automatically trigger within seconds
2. ✅ Analyze your code changes using Grok
3. ✅ Update the README
4. ✅ Post a comment showing what changed
5. ✅ Commit the updated README to your branch

### 7. Review and Merge

1. Check the PR comment for Grok's analysis results
2. Review the README changes in the commit
3. If you're happy, merge the PR!

## Troubleshooting

### Workflow doesn't trigger?
- Check that the workflow file is in `.github/workflows/` on the main branch
- Verify GitHub Actions is enabled in repository settings

### "XAI_API_KEY not found" error?
- Make sure you added the secret correctly in GitHub Settings
- Secret name must be exactly `XAI_API_KEY`
- Verify your API key is valid at https://console.x.ai/

### README not updating?
- Check if changes were significant enough (no test-only changes)
- Look at workflow logs in Actions tab
- Verify Grok API key is valid and has available credits

### Rate limiting?
- xAI Grok has generous rate limits on the free tier
- Check your usage at https://console.x.ai/

## Advanced Configuration

### Change AI Model

Grok offers different models. Edit `.env.example` or update `ai_analyzer.py`:

Available models:
- **`grok-beta`** (default) - Latest model, best performance
- **`grok-vision-beta`** - With vision capabilities  
- **`grok-2-latest`** - Previous generation

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
# Edit .env and add your XAI_API_KEY

# Set environment variables
$env:XAI_API_KEY="xai-your-api-key-here"
$env:PR_NUMBER="1"
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

## Why Grok?

✅ **Free tier available** - Generous free credits for testing  
✅ **Fast responses** - Optimized for speed  
✅ **OpenAI-compatible** - Easy integration with existing tools  
✅ **Great at code understanding** - Built for developer tasks  
✅ **Latest technology** - State-of-the-art AI model  

## Need Help?

- **Grok API Docs**: https://docs.x.ai/
- **API Console**: https://console.x.ai/
- Check the full documentation in `README.md`

---

**You're all set! 🎉 Create your first PR and watch Grok analyze your code!**
