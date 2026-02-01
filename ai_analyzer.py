"""
AI-powered code analysis using Groq.
Analyzes code changes to detect new features, removals, and significant modifications.
"""

import os
from typing import Dict, List, Optional
from groq import Groq


class AIAnalyzer:
    """Analyzes code changes using Groq AI (fast LLM inference)."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize the AI analyzer with Groq.
        
        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var)
            model: Model name to use (default: llama-3.3-70b-versatile - free tier)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        self.model = model
        
        print(f"✅ Initialized Groq model: {model}")
    
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
        return f"""ROLE: Senior Software Engineer & Code Auditor.

TASK: Analyze the provided code changes and generate a high-level, noise-free summary for changelogs and documentation.

INPUT DATA:
- PR Description: {pr_description if pr_description else "None"}
- Changed Files: {', '.join(changed_files)}
- Code Diff:
{code_diff[:8000]}  # Limited to avoid token limits

STRICT SIGNAL-TO-NOISE RATIO:
- IGNORE: formatting changes, whitespace, added/removed empty lines, typo fixes in comments.
- IGNORE: "Added new line", "Removed space", "Fixed indentation". These are NOT changelog items.
- FOCUS: Logic changes, new features, bug fixes that affect behavior, configuration updates.

OUTPUT RULES:

1. 'documentation_entries' [Target: DOCUMENTATION.md]:
   - Content: ONLY significant, NEW, USER-FACING features.
   - Requirement: Must be a clear functional addition.
   - Format: Structured input/output.

2. 'new_features' / 'modified_features' / 'removed_features' [Target: RELEASES.md]:
   - Content: Technical changelog items for other engineers.
   - 'modified_features': Includes bug fixes ("Fixed NPE in X"), refactors ("Optimized Y loop"), functional changes.
   - DO NOT report trivialities like "Added newline at EOF".

3. 'configuration_updates':
   - CRITICAL: Detect ALL changes to:
     - Requirements/Dependencies (version bumps, new packages).
     - Workflows (GitHub Actions, CI/CD).
     - Environment variables or config files.
   - Format: "Updated requirement X to v1.2", "Added workflow Y".

RESPONSE FORMAT (JSON):
{{
    "documentation_entries": [
        {{
            "name": "function_name",
            "description": "What it does.",
            "input": "Args",
            "output": "Returns"
        }}
    ],
    "new_features": ["Added feature X"],
    "modified_features": ["Fixed logic in Y", "Optimized Z"],
    "removed_features": [],
    "configuration_updates": ["Updated numpy", "Added CI step"],
    "significance": "low|medium|high",
    "summary": "Executive summary."
}}
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
                'configuration_updates': data.get('configuration_updates', []),
                'documentation_entries': data.get('documentation_entries', []),
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
            len(analysis.get('removed_features', [])) > 0 or
            len(analysis.get('configuration_updates', [])) > 0
        )
        
        is_significant = analysis.get('significance', 'low') in ['medium', 'high']
        
        return has_changes or is_significant
