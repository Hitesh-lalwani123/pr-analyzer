"""
File path filtering utilities for the PR analyzer.
Detects test files, README-only changes, and non-functional modifications.
"""

import re
from pathlib import Path
from typing import List, Set


class ChangeFilter:
    """Filters out changes that should not trigger README updates."""
    
    # Test file patterns
    TEST_PATTERNS = [
        r'.*[_\.]test\.py$',
        r'^test_.*\.py$',
        r'.*\.test\.js$',
        r'.*\.test\.ts$',
        r'.*\.spec\.js$',
        r'.*\.spec\.ts$',
        r'.*/tests?/.*',
        r'.*/\_\_tests\_\_/.*',
        r'.*[_\.]test\.go$',
        r'.*_test\.go$',
    ]
    
    # README patterns
    README_PATTERNS = [
        r'^readme\.md$',
        r'^readme\.txt$',
        r'^readme$',
        r'.*/readme\.md$',
        r'.*\.readme$',  # Added for Documentation.readme and Updates.readme
    ]
    
    # Documentation patterns (optional filtering)
    DOC_PATTERNS = [
        r'.*\.md$',
        r'.*/docs?/.*',
    ]
    
    def __init__(self):
        self.test_regex = re.compile('|'.join(self.TEST_PATTERNS), re.IGNORECASE)
        self.readme_regex = re.compile('|'.join(self.README_PATTERNS), re.IGNORECASE)
        self.doc_regex = re.compile('|'.join(self.DOC_PATTERNS), re.IGNORECASE)
    
    def is_test_file(self, filepath: str) -> bool:
        """Check if the file is a test file."""
        return bool(self.test_regex.match(filepath))
    
    def is_readme_file(self, filepath: str) -> bool:
        """Check if the file is a README."""
        return bool(self.readme_regex.match(filepath))
    
    def is_doc_file(self, filepath: str) -> bool:
        """Check if the file is a documentation file."""
        return bool(self.doc_regex.match(filepath))
    
    def filter_files(self, filepaths: List[str], exclude_tests: bool = True, 
                     exclude_readme: bool = True) -> List[str]:
        """
        Filter out files based on criteria.
        
        Args:
            filepaths: List of file paths to filter
            exclude_tests: Whether to exclude test files
            exclude_readme: Whether to exclude README files
            
        Returns:
            Filtered list of file paths
        """
        filtered = []
        
        for filepath in filepaths:
            # Skip test files
            if exclude_tests and self.is_test_file(filepath):
                continue
            
            # Skip README files
            if exclude_readme and self.is_readme_file(filepath):
                continue
            
            filtered.append(filepath)
        
        return filtered
    
    def is_readme_only_commit(self, changed_files: List[str]) -> bool:
        """
        Check if a commit only contains README changes.
        
        Args:
            changed_files: List of changed file paths
            
        Returns:
            True if only README files were changed
        """
        if not changed_files:
            return False
        
        # Filter out README files
        non_readme_files = [f for f in changed_files if not self.is_readme_file(f)]
        
        # If no non-README files remain, it's a README-only commit
        return len(non_readme_files) == 0
    
    def get_code_files(self, filepaths: List[str]) -> List[str]:
        """
        Get files to analyze (excludes tests and documentation).
        
        Args:
            filepaths: List of file paths
            
        Returns:
            List of files to analyze
        """
        files_to_analyze = []
        
        for filepath in filepaths:
            # Skip test files
            if self.is_test_file(filepath):
                continue
            
            # Skip README/doc files
            if self.is_readme_file(filepath) or self.is_doc_file(filepath):
                continue
            
            # We now WANT to include config files, so we don't filter them out anymore.
            
            files_to_analyze.append(filepath)
        
        return files_to_analyze


def should_skip_analysis(commit_message: str) -> bool:
    """
    Check if analysis should be skipped based on commit message.
    
    Args:
        commit_message: The commit message to check
        
    Returns:
        True if analysis should be skipped
    """
    skip_markers = [
        '[skip-pr-analyzer]',
        '[skip-analyzer]',
        '[no-analyze]',
        'docs: update README based on PR changes',
    ]
    
    return any(marker in commit_message for marker in skip_markers)
