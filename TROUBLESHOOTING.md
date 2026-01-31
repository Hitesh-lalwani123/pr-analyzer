# ⚠️ Common Issues & Solutions

## Permissions Error

### Error Message
```
Invalid workflow file: .github/workflows/pr-analyzer.yml#L10
The workflow is not valid. .github/workflows/pr-analyzer.yml (Line: 10, Col: 3): 
Error calling workflow 'Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main'. 
The nested job 'analyze-pr' is requesting 'contents: write, pull-requests: write', 
but is only allowed 'contents: read, pull-requests: none'.
```

### ✅ Solution

Add `permissions` to your caller workflow:

```yaml
name: PR Analyzer

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]

jobs:
  analyze-pr:
    # ✅ ADD THIS - Required permissions
    permissions:
      contents: write        # Allows committing README updates
      pull-requests: write   # Allows posting PR comments
    
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

### Why This Happens

GitHub Actions reusable workflows inherit permissions from the caller, but by default they only get read-only access. Since our workflow needs to:
- **Commit README changes** → needs `contents: write`
- **Post PR comments** → needs `pull-requests: write`

You must explicitly grant these permissions in your workflow file.

---

## Other Common Issues

### Issue: "GROQ_API_KEY not found"

**Cause:** Secret not configured or named incorrectly

**Solution:**
1. Go to: `Settings → Secrets and variables → Actions`
2. Create secret named exactly: `GROQ_API_KEY`
3. Paste your Groq API key (starts with `gsk_`)

---

### Issue: Workflow doesn't trigger

**Cause:** Workflow file not on main branch

**Solution:**
```bash
# Make sure workflow is committed to main
git checkout main
git add .github/workflows/pr-analyzer.yml
git commit -m "Add PR analyzer workflow"
git push origin main
```

---

### Issue: "404: Repository not found" when calling reusable workflow

**Cause:** The pr-analyzer repository is private or doesn't exist

**Solution:**
- Ensure the repository `Hitesh-lalwani123/pr-analyzer` is **public**
- Or update the path to your fork: `YOUR_USERNAME/pr-analyzer`
- For private repos, you need to grant workflow access

---

### Issue: README not being updated

**Possible causes:**

1. **Changes are not significant**
   - Only test files changed → skipped
   - Only config files changed → skipped
   - Solution: Modify the significance threshold:
     ```yaml
     with:
       min_significance: 'low'  # Update for any changes
     ```

2. **Skip marker in commit**
   - Commit message contains `[skip-pr-analyzer]`
   - Solution: Remove the marker or create new commits

3. **README doesn't have Features section**
   - The updater looks for `## Features` or `## ✨ Features`
   - Solution: Add a Features section to your README

---

### Issue: Scripts not downloading (404 errors)

**Cause:** Files don't exist at expected URLs

**Solution:**

Check these URLs are accessible:
- `https://raw.githubusercontent.com/Hitesh-lalwani123/pr-analyzer/main/analyzer.py`
- `https://raw.githubusercontent.com/Hitesh-lalwani123/pr-analyzer/main/ai_analyzer.py`
- `https://raw.githubusercontent.com/Hitesh-lalwani123/pr-analyzer/main/filters.py`
- `https://raw.githubusercontent.com/Hitesh-lalwani123/pr-analyzer/main/readme_updater.py`

If using a fork, update the workflow:
```yaml
- name: Download Analyzer Scripts
  run: |
    BASE_URL="https://raw.githubusercontent.com/YOUR_USERNAME/pr-analyzer/main"
```

---

### Issue: "Invalid workflow file" syntax error

**Cause:** YAML indentation or syntax error

**Solution:**
- Use a YAML validator: https://www.yamllint.com/
- Check indentation (use spaces, not tabs)
- Ensure `if:` conditions use `|` for multiline

**Correct:**
```yaml
if: |
  github.event.pull_request.base.ref == 'main' &&
  startsWith(github.event.pull_request.head.ref, 'release-')
```

**Incorrect:**
```yaml
if: github.event.pull_request.base.ref == 'main' &&
    startsWith(github.event.pull_request.head.ref, 'release-')
```

---

## Still Having Issues?

1. **Check workflow logs**
   - Go to Actions tab → Select failed workflow run
   - Click on failed job to see detailed logs

2. **Test with simple workflow**
   ```yaml
   name: Test
   on:
     pull_request:
       branches: [main]
   jobs:
     test:
       permissions:
         contents: write
         pull-requests: write
       runs-on: ubuntu-latest
       steps:
         - run: echo "Testing permissions"
   ```

3. **Verify repository settings**
   - Actions → General → Workflow permissions
   - Should be set to "Read and write permissions"

---

## Quick Checklist

Before opening a new issue, verify:

- [ ] Workflow file is on `main` branch
- [ ] `permissions` section is included in caller workflow
- [ ] `GROQ_API_KEY` secret exists with correct name
- [ ] Repository has Actions enabled
- [ ] Source files exist in pr-analyzer repository
- [ ] YAML syntax is valid (no tabs, correct indentation)

---

**Most common fix:** Add permissions to your workflow! 🔧
