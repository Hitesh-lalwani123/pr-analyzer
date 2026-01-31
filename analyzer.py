"""
Main PR analyzer orchestrator.
Coordinates GitHub API interaction, AI analysis, and README updates.
"""

import os
import sys
from typing import List, Dict, Optional
from github import Github, PullRequest
from dotenv import load_dotenv

from filters import ChangeFilter, should_skip_analysis
from ai_analyzer import AIAnalyzer
from readme_updater import READMEUpdater


class PRAnalyzer:
    """Main orchestrator for PR analysis and README updates."""
    
    def __init__(self):
        """Initialize the PR analyzer with GitHub and AI clients."""
        load_dotenv()
        
        # Get environment variables
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.pr_number = int(os.getenv("PR_NUMBER", "0"))
        self.repo_name = os.getenv("REPO_NAME", "")
        self.base_ref = os.getenv("BASE_REF", "main")
        self.head_ref = os.getenv("HEAD_REF", "")
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN not found")
        
        if not self.pr_number or not self.repo_name:
            raise ValueError("PR_NUMBER and REPO_NAME must be set")
        
        # Initialize clients
        self.github = Github(self.github_token)
        self.repo = self.github.get_repo(self.repo_name)
        self.filter = ChangeFilter()
        self.ai_analyzer = AIAnalyzer()
        self.readme_updater = READMEUpdater()
    
    def run(self):
        """Main execution flow."""
        print(f"🔍 Analyzing PR #{self.pr_number} in {self.repo_name}")
        
        try:
            # Get PR details
            pr = self.repo.get_pull(self.pr_number)
            print(f"📋 PR Title: {pr.title}")
            
            # Check if we should skip analysis
            if should_skip_analysis(pr.title):
                print("⏭️  Skipping analysis (skip marker found in title)")
                return
            
            # Get changed files
            changed_files = self._get_changed_files(pr)
            print(f"📁 Total files changed: {len(changed_files)}")
            
            # Check if README-only changes
            if self.filter.is_readme_only_commit(changed_files):
                print("⏭️  Skipping analysis (README-only changes)")
                return
            
            # Filter out test files and README
            code_files = self.filter.get_code_files(changed_files)
            print(f"💻 Code files to analyze: {len(code_files)}")
            
            if not code_files:
                print("⏭️  No code files to analyze")
                return
            
            # Get PR diff
            diff = self._get_pr_diff(pr, code_files)
            
            # Analyze with AI
            print("🤖 Running AI analysis...")
            analysis = self.ai_analyzer.analyze_changes(
                code_diff=diff,
                pr_description=pr.body or "",
                changed_files=code_files
            )
            
            print(f"📊 Analysis complete:")
            print(f"  - New features: {len(analysis['new_features'])}")
            print(f"  - Removed features: {len(analysis['removed_features'])}")
            print(f"  - Significance: {analysis['significance']}")
            
            # Check if README update is needed
            if not self.ai_analyzer.should_update_readme(analysis):
                print("⏭️  No significant changes requiring README update")
                return
            
            # Save original README for diff
            original_readme = self.readme_updater.content
            
            # Update README
            print("📝 Updating README...")
            readme_modified = self.readme_updater.update_from_analysis(analysis)
            
            if readme_modified:
                # Generate diff preview
                diff_preview = self.readme_updater.get_diff_preview(original_readme)
                
                # Save README
                self.readme_updater.save()
                print("✅ README updated successfully")
                
                # Post comment to PR with changes
                self._post_pr_comment(pr, analysis, diff_preview)
                
            else:
                print("ℹ️  README update attempted but no changes made")
        
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def _get_changed_files(self, pr: PullRequest) -> List[str]:
        """Get list of changed files in the PR."""
        files = pr.get_files()
        return [f.filename for f in files]
    
    def _get_pr_diff(self, pr: PullRequest, files_to_include: List[str]) -> str:
        """
        Get the unified diff for specified files in the PR.
        
        Args:
            pr: PullRequest object
            files_to_include: List of file paths to include in diff
            
        Returns:
            Combined diff string
        """
        diff_parts = []
        files = pr.get_files()
        
        for file in files:
            if file.filename in files_to_include:
                if file.patch:  # patch contains the diff
                    diff_parts.append(f"--- {file.filename} ---\n{file.patch}\n")
        
        return '\n'.join(diff_parts)
    
    def _post_pr_comment(self, pr: PullRequest, analysis: Dict, diff_preview: str):
        """
        Post a comment to the PR with README update details.
        
        Args:
            pr: PullRequest object
            analysis: Analysis results
            diff_preview: README diff preview
        """
        # Build comment message
        comment = f"""## 📚 README Update Preview

The PR analyzer has detected significant changes and updated the README documentation.

### Analysis Summary
**Significance:** {analysis['significance'].upper()}

"""
        
        if analysis['new_features']:
            comment += "**New Features Added:**\n"
            for feature in analysis['new_features']:
                comment += f"- {feature}\n"
            comment += "\n"
        
        if analysis['removed_features']:
            comment += "**Features Removed:**\n"
            for feature in analysis['removed_features']:
                comment += f"- {feature}\n"
            comment += "\n"
        
        if analysis['summary']:
            comment += f"**Summary:**\n{analysis['summary']}\n\n"
        
        comment += """### README Changes

<details>
<summary>Click to view README diff</summary>

```diff
"""
        
        # Limit diff preview to avoid huge comments
        diff_lines = diff_preview.split('\n')[:100]
        comment += '\n'.join(diff_lines)
        
        if len(diff_preview.split('\n')) > 100:
            comment += "\n... (diff truncated)"
        
        comment += """
```

</details>

---

The README has been automatically updated and committed to this branch.

*🤖 Generated by PR Analyzer Bot*
"""
        
        try:
            pr.create_issue_comment(comment)
            print("💬 Posted comment to PR")
        except Exception as e:
            print(f"⚠️  Failed to post PR comment: {e}")


def main():
    """Entry point for the analyzer."""
    analyzer = PRAnalyzer()
    analyzer.run()


if __name__ == "__main__":
    main()
