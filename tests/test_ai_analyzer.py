"""
Unit tests for the AI analyzer module.
Tests use mocked responses to avoid API calls.
"""

import pytest
from unittest.mock import Mock, patch
from ai_analyzer import AIAnalyzer


class TestAIAnalyzer:
    """Test the AIAnalyzer class."""
    
    @patch('ai_analyzer.genai.configure')
    @patch('ai_analyzer.genai.GenerativeModel')
    def test_initialization(self, mock_model, mock_configure):
        """Test AIAnalyzer initialization."""
        analyzer = AIAnalyzer(api_key="test_key")
        mock_configure.assert_called_once_with(api_key="test_key")
    
    @patch('ai_analyzer.genai.configure')
    @patch('ai_analyzer.genai.GenerativeModel')
    def test_analyze_changes_success(self, mock_model_class, mock_configure):
        """Test successful analysis."""
        # Mock the AI response
        mock_response = Mock()
        mock_response.text = """{
            "new_features": ["Feature A", "Feature B"],
            "removed_features": ["Old Feature"],
            "modified_features": ["Modified Feature"],
            "significance": "high",
            "summary": "Major update with new features"
        }"""
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        analyzer = AIAnalyzer(api_key="test_key")
        
        result = analyzer.analyze_changes(
            code_diff="+ new code\n- old code",
            pr_description="Added new features",
            changed_files=["src/main.py"]
        )
        
        assert len(result['new_features']) == 2
        assert "Feature A" in result['new_features']
        assert result['significance'] == 'high'
        assert result['summary'] == "Major update with new features"
    
    @patch('ai_analyzer.genai.configure')
    @patch('ai_analyzer.genai.GenerativeModel')
    def test_analyze_changes_with_markdown_json(self, mock_model_class, mock_configure):
        """Test parsing JSON wrapped in markdown code blocks."""
        mock_response = Mock()
        mock_response.text = """Here's the analysis:
        
```json
{
    "new_features": ["Feature X"],
    "removed_features": [],
    "modified_features": [],
    "significance": "medium",
    "summary": "Added Feature X"
}
```
        """
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        analyzer = AIAnalyzer(api_key="test_key")
        
        result = analyzer.analyze_changes("diff", "desc", ["file.py"])
        
        assert len(result['new_features']) == 1
        assert "Feature X" in result['new_features']
    
    @patch('ai_analyzer.genai.configure')
    @patch('ai_analyzer.genai.GenerativeModel')
    def test_should_update_readme_with_features(self, mock_model_class, mock_configure):
        """Test README update decision with features."""
        analyzer = AIAnalyzer(api_key="test_key")
        
        analysis = {
            'new_features': ["New feature"],
            'removed_features': [],
            'significance': 'low'
        }
        
        assert analyzer.should_update_readme(analysis) is True
    
    @patch('ai_analyzer.genai.configure')
    @patch('ai_analyzer.genai.GenerativeModel')
    def test_should_update_readme_high_significance(self, mock_model_class, mock_configure):
        """Test README update decision with high significance."""
        analyzer = AIAnalyzer(api_key="test_key")
        
        analysis = {
            'new_features': [],
            'removed_features': [],
            'significance': 'high'
        }
        
        assert analyzer.should_update_readme(analysis) is True
    
    @patch('ai_analyzer.genai.configure')
    @patch('ai_analyzer.genai.GenerativeModel')
    def test_should_not_update_readme(self, mock_model_class, mock_configure):
        """Test README update decision with no significant changes."""
        analyzer = AIAnalyzer(api_key="test_key")
        
        analysis = {
            'new_features': [],
            'removed_features': [],
            'significance': 'low'
        }
        
        assert analyzer.should_update_readme(analysis) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
