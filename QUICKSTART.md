# 🚀 Quick Start Guide - Using Groq AI

## Prerequisites

1. **Python 3.11+** installed
2. **GitHub repository** with Actions enabled
3. **Groq API key** (FREE!) - Get it here: https://console.groq.com/

## Setup Steps

### 1. Get Your FREE Groq API Key

1. Go to https://console.groq.com/
2. Sign in with Google, GitHub, or email
3. Navigate to **API Keys** section  
4. Click **"Create API Key"**
5. Copy your API key (starts with `gsk_...`)

> [!NOTE]
> Groq offers **FREE API access** with generous rate limits! Perfect for this project.

### 2. Add GitHub Secret

1. Go to your repository on GitHub
2. Navigate to: **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Add secret:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your Groq API key

### 3. Push Code to Repository

```bash
cd E:\ai\pr_analysis

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Add PR analyzer with Groq AI"

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
git checkout -b feature/test-groq-analyzer

# Add a new file with some functionality
echo "def awesome_feature():
    '''An amazing new feature'''
    return 'Powered by Groq - Lightning Fast!'
" > awesome_feature.py

# Commit and push
git add awesome_feature.py
git commit -m "Add awesome feature with Groq analyzer"
git push origin feature/test-groq-analyzer
```

### 5. Create Pull Request

1. Go to your repository on GitHub
2. Click **"Compare & pull request"**
3. Add a description like:
   ```
   This PR adds an awesome new feature.
   
   Features:
   - New function for amazing functionality
   - Lightning-fast analysis powered by Groq
   ```
4. Click **"Create pull request"**

### 6. Watch the Magic! ⚡

The Groq-powered analyzer will (blazingly fast!):
1. ✅ Automatically trigger within seconds
2. ✅ Analyze your code using **Llama 3.3 70B** model
3. ✅ Update the README
4. ✅ Post a comment showing what changed
5. ✅ Commit the updated README to your branch

### 7. Review and Merge

1. Check the PR comment for Groq's analysis results
2. Review the README changes in the commit
3. If you're happy, merge the PR!

## Troubleshooting

### Workflow doesn't trigger?
- Check that the workflow file is in `.github/workflows/` on the main branch
- Verify GitHub Actions is enabled in repository settings

### "GROQ_API_KEY not found" error?
- Make sure you added the secret correctly in GitHub Settings
- Secret name must be exactly `GROQ_API_KEY`
- Verify your API key is valid at https://console.groq.com/

### README not updating?
- Check if changes were significant enough (no test-only changes)
- Look at workflow logs in Actions tab
- Verify Groq API key is valid

### Rate limiting?
- Groq has very generous free tier limits
- Check your usage at https://console.groq.com/settings/limits

## Advanced Configuration

### Change AI Model

Groq offers multiple high-speed models. Edit `ai_analyzer.py` to change model:

**Available FREE models:**
- **`llama-3.3-70b-versatile`** (default) - Best balance, smartest
- **`llama-3.1-70b-versatile`** - Fast and capable
- **`llama3-70b-8192`** - Large context window
- **`mixtral-8x7b-32768`** - Very fast, good quality
- **`llama3-8b-8192`** - Fastest, smaller model

All models are **FREE** with Groq! 🎉

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
# Edit .env and add your GROQ_API_KEY

# Set environment variables
$env:GROQ_API_KEY="gsk-your-api-key-here"
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

## Why Groq?

✅ **100% FREE** - No credit card required, generous limits  
✅ **Blazingly Fast** - Up to 10x faster than other APIs  
✅ **OpenAI-compatible** - Easy integration with existing tools  
✅ **Powerful models** - Llama 3.3 70B, Mixtral, and more  
✅ **Zero configuration** - Just add your API key  

## Need Help?

- **Groq API Docs**: https://console.groq.com/docs
- **API Console**: https://console.groq.com/
- Check the full documentation in `README.md`

---

**You're all set! 🎉 Create your first PR and watch Groq's lightning-fast analysis!**
