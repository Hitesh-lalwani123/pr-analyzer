"""
AI-powered code analysis using xAI's Grok.
Analyzes code changes to detect new features, removals, and significant modifications.
"""

import os
from typing import Dict, List, Optional
from openai import OpenAI


class AIAnalyzer:
    """Analyzes code changes using xAI Grok AI."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "grok-beta"):
        """
        Initialize the AI analyzer with Grok.
        
        Args:
            api_key: Grok API key (defaults to XAI_API_KEY env var)
            model: Model name to use (default: grok-beta - free tier)
        """
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("XAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI client with xAI endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1"
        )
        self.model = model
        
        print(f"✅ Initialized Grok model: {model}")
    
    def analyze_changes(
        self, 
        code_diff: str, 
        pr_description: str,
        changed_files: List[str]
    ) -> Dict[str, any]:
        """
        Analyze code changes and PR description to detect significant modifications.
        
        Args:
            code_diff: The git diff of changed files
            pr_description: The pull request description
            changed_files: List of changed file paths
            
        Returns:
            Dictionary containing analysis results:
            {
                'new_features': List[str],
                'removed_features': List[str],
                'modified_features': List[str],
                'summary': str,
                'significance': str  # 'low', 'medium', 'high'
            }
        """
        prompt = self._build_analysis_prompt(code_diff, pr_description, changed_files)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a code analysis assistant that provides structured JSON responses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            return self._parse_analysis_response(response.choices[0].message.content)
        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return {
                'new_features': [],
                'removed_features': [],
                'modified_features': [],
                'summary': '',
                'significance': 'low',
                'error': str(e)
            }
    
    def _build_analysis_prompt(
        self, 
        code_diff: str, 
        pr_description: str,
        changed_files: List[str]
    ) -> str:
        """Build the prompt for AI analysis."""
        return f"""You are a code analysis assistant. Analyze the following pull request changes and provide a structured analysis.

PULL REQUEST DESCRIPTION:
{pr_description if pr_description else "No description provided"}

CHANGED FILES:
{', '.join(changed_files)}

CODE DIFF:
{code_diff[:8000]}  # Limit to avoid token limits

INSTRUCTIONS:
1. Identify NEW FEATURES or functionality added in this PR
2. Identify REMOVED or DEPRECATED features
3. Identify MODIFIED features (significant changes to existing functionality)
4. Determine the significance level: LOW (minor changes), MEDIUM (notable features), HIGH (major functionality)
5. Provide a brief summary suitable for documentation

Focus on user-facing features and significant architectural changes. Ignore:
- Test file changes
- Minor refactoring without functional impact
- Code style changes
- Configuration updates

Respond in the following JSON format:
{{
    "new_features": ["Feature 1 description", "Feature 2 description"],
    "removed_features": ["Removed feature description"],
    "modified_features": ["Modified feature description"],
    "significance": "low|medium|high",
    "summary": "Brief summary of changes suitable for documentation"
}}

Be concise and focus on what matters to end users and developers reading the documentation.
"""
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, any]:
        """
        Parse the AI response into structured data.
        
        Args:
            response_text: The raw text response from AI
            
        Returns:
            Parsed analysis dictionary
        """
        import json
        import re
        
        try:
            # Try to extract JSON from the response
            # Sometimes AI wraps JSON in markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON object directly
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    raise ValueError("No JSON found in response")
            
            data = json.loads(json_str)
            
            # Validate and normalize the response
            return {
                'new_features': data.get('new_features', []),
                'removed_features': data.get('removed_features', []),
                'modified_features': data.get('modified_features', []),
                'significance': data.get('significance', 'medium').lower(),
                'summary': data.get('summary', '')
            }
        
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            print(f"Response text: {response_text[:500]}")
            
            # Fallback: return empty analysis
            return {
                'new_features': [],
                'removed_features': [],
                'modified_features': [],
                'significance': 'low',
                'summary': 'Unable to analyze changes automatically.',
                'parse_error': str(e)
            }
    
    def should_update_readme(self, analysis: Dict[str, any]) -> bool:
        """
        Determine if README should be updated based on analysis.
        
        Args:
            analysis: The analysis results dictionary
            
        Returns:
            True if README should be updated
        """
        # Update if there are new features, removed features, or medium/high significance
        has_changes = (
            len(analysis.get('new_features', [])) > 0 or
            len(analysis.get('removed_features', [])) > 0
        )
        
        is_significant = analysis.get('significance', 'low') in ['medium', 'high']
        
        return has_changes or is_significant
