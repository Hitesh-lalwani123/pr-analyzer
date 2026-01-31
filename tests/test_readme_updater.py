"""
Unit tests for the README updater module.
"""

import pytest
from pathlib import Path
import tempfile
import os

from readme_updater import READMEUpdater


class TestREADMEUpdater:
    """Test the READMEUpdater class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary README file
        self.temp_dir = tempfile.mkdtemp()
        self.readme_path = Path(self.temp_dir) / "README.md"
        
        # Sample README content
        self.sample_readme = """# Test Project

A sample project for testing.

## Features

- Existing feature 1
- Existing feature 2

## Installation

Install via pip.

## Usage

Run the application.
"""
        
        with open(self.readme_path, 'w') as f:
            f.write(self.sample_readme)
        
        self.updater = READMEUpdater(str(self.readme_path))
    
    def teardown_method(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_readme(self):
        """Test README loading."""
        assert self.updater.content == self.sample_readme
        assert "Features" in self.updater.sections
    
    def test_parse_sections(self):
        """Test section parsing."""
        sections = self.updater.sections
        assert "Features" in sections
        assert "Installation" in sections
        assert "Usage" in sections
        assert sections["Features"]["level"] == 2
    
    def test_add_features(self):
        """Test adding new features."""
        analysis = {
            'new_features': ["New awesome feature", "Another cool feature"],
            'removed_features': [],
            'modified_features': []
        }
        
        modified = self.updater.update_from_analysis(analysis)
        assert modified
        
        # Check content includes new features
        assert "New awesome feature" in self.updater.content
        assert "Another cool feature" in self.updater.content
    
    def test_remove_features(self):
        """Test removing features."""
        analysis = {
            'new_features': [],
            'removed_features': ["Existing feature 1"],
            'modified_features': []
        }
        
        modified = self.updater.update_from_analysis(analysis)
        assert modified
        
        # Feature should be removed
        assert "Existing feature 1" not in self.updater.content
    
    def test_no_duplicate_features(self):
        """Test that duplicate features aren't added."""
        analysis = {
            'new_features': ["Existing feature 1"],
            'removed_features': [],
            'modified_features': []
        }
        
        original_content = self.updater.content
        self.updater.update_from_analysis(analysis)
        
        # Count occurrences - should still be just one
        count = self.updater.content.count("Existing feature 1")
        assert count == original_content.count("Existing feature 1")
    
    def test_save_readme(self):
        """Test saving README."""
        analysis = {
            'new_features': ["Test feature"],
            'removed_features': [],
            'modified_features': []
        }
        
        self.updater.update_from_analysis(analysis)
        self.updater.save()
        
        # Read back and verify
        with open(self.readme_path, 'r') as f:
            content = f.read()
        
        assert "Test feature" in content
    
    def test_get_diff_preview(self):
        """Test diff preview generation."""
        original = self.updater.content
        
        analysis = {
            'new_features': ["New feature"],
            'removed_features': [],
            'modified_features': []
        }
        
        self.updater.update_from_analysis(analysis)
        diff = self.updater.get_diff_preview(original)
        
        assert "+++" in diff or "---" in diff
        assert "New feature" in diff


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
