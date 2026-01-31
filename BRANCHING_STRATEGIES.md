# 🎯 Branching Strategy Examples

This guide shows how to configure the PR analyzer for different Git branching strategies.

---

## 🌳 Your Branching Strategy

**Flow:** `feature → develop → release-x.x.x → main`

**Requirement:** Only update documentation on `release-*` → `main` PRs

### ✅ Configuration

Create `.github/workflows/pr-analyzer.yml`:

```yaml
name: PR Analyzer (Release to Main)

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main

jobs:
  call-analyzer:
    # Only run on PRs from release-* to main
    if: |
      github.event.pull_request.base.ref == 'main' &&
      (startsWith(github.event.pull_request.head.ref, 'release-') || 
       startsWith(github.event.pull_request.head.ref, 'release/'))
    
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

### 📊 What Happens

| PR Type | Analyzer Runs? | Reason |
|---------|----------------|--------|
| `feature/xxx → develop` | ❌ No | Not targeting main |
| `develop → release-1.0.0` | ❌ No | Not targeting main |
| `release-1.0.0 → main` | ✅ **YES** | Perfect! Documentation updated |
| `hotfix/abc → main` | ❌ No | Not from release-* branch |

### 🎯 Why This Works

- Documentation only updates for **production releases**
- Keeps README in sync with what's actually in main
- No noise from feature or develop branches
- Clean, professional changelog

---

## 🌿 Alternative Branching Strategies

### Strategy 1: GitFlow (Classic)

**Flow:** `feature → develop → release → main`

```yaml
on:
  pull_request:
    branches: [main]

jobs:
  analyze:
    if: startsWith(github.event.pull_request.head.ref, 'release')
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

### Strategy 2: Trunk-Based (Simple)

**Flow:** `feature → main`

```yaml
on:
  pull_request:
    branches: [main]

jobs:
  analyze:
    # Run on ALL PRs to main
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

### Strategy 3: Multiple Release Branches

**Flow:** `feature → develop → (release-v1|release-v2) → main`

```yaml
on:
  pull_request:
    branches: [main]

jobs:
  analyze:
    if: |
      startsWith(github.event.pull_request.head.ref, 'release-v1') ||
      startsWith(github.event.pull_request.head.ref, 'release-v2')
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

### Strategy 4: Staging Before Production

**Flow:** `feature → develop → staging → production`

```yaml
on:
  pull_request:
    branches: [production]  # Your production branch

jobs:
  analyze:
    if: github.event.pull_request.head.ref == 'staging'
    uses: Hitesh-lalwani123/pr-analyzer/.github/workflows/reusable-pr-analyzer.yml@main
    secrets:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

---

## 🎛️ Advanced Filtering

### Exclude Specific Branches

```yaml
jobs:
  analyze:
    if: |
      startsWith(github.event.pull_request.head.ref, 'release-') &&
      !contains(github.event.pull_request.head.ref, 'beta')
    # Runs on release-* but NOT release-beta
```

### Include Multiple Patterns

```yaml
jobs:
  analyze:
    if: |
      startsWith(github.event.pull_request.head.ref, 'release-') ||
      startsWith(github.event.pull_request.head.ref, 'hotfix-') ||
      github.event.pull_request.head.ref == 'develop'
```

### Match Version Pattern

```yaml
jobs:
  analyze:
    if: |
      github.event.pull_request.base.ref == 'main' &&
      contains(github.event.pull_request.head.ref, 'release-') &&
      contains(github.event.pull_request.head.ref, '.')
    # Matches: release-1.0.0, release-2.3.1
    # Skips: release-dev, release-test
```

---

## 🔍 Testing Your Configuration

### Check the Condition Locally

Use GitHub's context to test:

```yaml
# Add this temporarily to see what values you're getting
- name: Debug PR Info
  run: |
    echo "Base ref: ${{ github.event.pull_request.base.ref }}"
    echo "Head ref: ${{ github.event.pull_request.head.ref }}"
    echo "Event name: ${{ github.event_name }}"
```

### Test Different PR Scenarios

1. **Create test PRs** from different branches:
   ```bash
   git checkout -b release-1.0.0
   git push origin release-1.0.0
   # Create PR: release-1.0.0 → main
   ```

2. **Check workflow run** in Actions tab

3. **Verify** it only runs when expected

---

## 📋 Common Patterns

### Pattern: Semantic Versioning Releases

```yaml
if: |
  contains(github.event.pull_request.head.ref, 'release-') &&
  contains(github.event.pull_request.head.ref, '.')
# Matches: release-1.0.0, release-2.3.4-rc1
```

### Pattern: Only Major Releases

```yaml
if: |
  contains(github.event.pull_request.head.ref, 'release-') &&
  !contains(github.event.pull_request.head.ref, '-rc') &&
  !contains(github.event.pull_request.head.ref, '-beta')
```

### Pattern: Exclude Dependabot

```yaml
if: |
  startsWith(github.event.pull_request.head.ref, 'release-') &&
  github.event.pull_request.user.login != 'dependabot[bot]'
```

---

## 💡 Best Practices

### 1. **Only Production Releases**
✅ Update docs when code hits production (main/master)  
❌ Don't update for every feature branch

### 2. **Clear Branch Naming**
✅ `release-1.0.0`, `release/v2.3.0`  
❌ `my-release`, `v1` (hard to pattern match)

### 3. **Test the Flow**
✅ Create dummy PRs to verify  
❌ Assume it works without testing

### 4. **Document Your Strategy**
Add to your README:
```markdown
## Branching Strategy
- `main` - Production
- `release-x.x.x` - Release candidates
- `develop` - Integration branch
- `feature/*` - New features

Documentation auto-updates on `release-*` → `main` PRs.
```

---

## 🚀 Quick Reference

| You Want | Use This Condition |
|----------|-------------------|
| Only release to main | `base == 'main' && startsWith(head, 'release-')` |
| Any PR to main | `base == 'main'` |
| Specific branches | `head == 'staging' \|\| head == 'develop'` |
| Version pattern | `contains(head, 'release-') && contains(head, '.')` |
| Exclude pattern | `!contains(head, 'beta')` |

---

**Your exact use case:**

```yaml
# ✅ Perfect for: main ← release-x.x.x ← develop ← feature
if: |
  github.event.pull_request.base.ref == 'main' &&
  startsWith(github.event.pull_request.head.ref, 'release-')
```

Done! 🎉
