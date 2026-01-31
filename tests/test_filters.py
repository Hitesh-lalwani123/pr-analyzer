"""
Unit tests for the filters module.
"""

import pytest
from filters import ChangeFilter, should_skip_analysis


class TestChangeFilter:
    """Test the ChangeFilter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.filter = ChangeFilter()
    
    def test_is_test_file_python(self):
        """Test Python test file detection."""
        assert self.filter.is_test_file("test_example.py")
        assert self.filter.is_test_file("example_test.py")
        assert self.filter.is_test_file("tests/test_utils.py")
        assert not self.filter.is_test_file("example.py")
    
    def test_is_test_file_javascript(self):
        """Test JavaScript test file detection."""
        assert self.filter.is_test_file("example.test.js")
        assert self.filter.is_test_file("example.spec.ts")
        assert not self.filter.is_test_file("example.js")
    
    def test_is_readme_file(self):
        """Test README detection."""
        assert self.filter.is_readme_file("README.md")
        assert self.filter.is_readme_file("readme.md")
        assert self.filter.is_readme_file("docs/README.md")
        assert not self.filter.is_readme_file("READTHIS.md")
    
    def test_filter_files(self):
        """Test file filtering."""
        files = [
            "src/main.py",
            "test_main.py",
            "README.md",
            "src/utils.py"
        ]
        
        filtered = self.filter.filter_files(files)
        assert "src/main.py" in filtered
        assert "src/utils.py" in filtered
        assert "test_main.py" not in filtered
        assert "README.md" not in filtered
    
    def test_is_readme_only_commit(self):
        """Test README-only commit detection."""
        # Only README changed
        assert self.filter.is_readme_only_commit(["README.md"])
        
        # README + code changes
        assert not self.filter.is_readme_only_commit(["README.md", "src/main.py"])
        
        # No README
        assert not self.filter.is_readme_only_commit(["src/main.py"])
        
        # Empty list
        assert not self.filter.is_readme_only_commit([])
    
    def test_get_code_files(self):
        """Test code file extraction."""
        files = [
            "src/main.py",
            "test_main.py",
            "README.md",
            ".gitignore",
            "package.json",
            "setup.py",
            "docs/guide.md"
        ]
        
        code_files = self.filter.get_code_files(files)
        assert "src/main.py" in code_files
        assert "setup.py" in code_files
        assert "test_main.py" not in code_files
        assert "README.md" not in code_files
        assert ".gitignore" not in code_files


class TestSkipAnalysis:
    """Test the skip analysis function."""
    
    def test_skip_markers(self):
        """Test various skip markers."""
        assert should_skip_analysis("[skip-pr-analyzer] Update docs")
        assert should_skip_analysis("Fix bug [skip-analyzer]")
        assert should_skip_analysis("[no-analyze] Minor change")
        assert not should_skip_analysis("Add new feature")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
