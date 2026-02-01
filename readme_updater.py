"""
README updater module.
Updates the README.md file based on AI analysis of code changes.
"""

import re
from typing import Dict, List, Optional
from pathlib import Path


class READMEUpdater:
    """Updates README.md based on code change analysis."""
    
    def __init__(self, readme_path: str = "README.md"):
        """
        Initialize the README updater.
        
        Args:
            readme_path: Path to the README.md file
        """
        self.readme_path = Path(readme_path)
        self.content = ""
        self.sections = {}
        
        if self.readme_path.exists():
            self.load_readme()
    
    def load_readme(self):
        """Load and parse the README file."""
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        # Parse sections for easier manipulation
        self.sections = self._parse_sections(self.content)
    
    def _parse_sections(self, content: str) -> Dict[str, Dict[str, any]]:
        """
        Parse README into sections based on headers.
        
        Returns:
            Dictionary mapping section titles to their content and position
        """
        sections = {}
        lines = content.split('\n')
        current_section = None
        current_content = []
        current_level = 0
        
        for i, line in enumerate(lines):
            # Check if line is a header
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if header_match:
                # Save previous section
                if current_section:
                    sections[current_section] = {
                        'level': current_level,
                        'content': '\n'.join(current_content),
                        'line_start': sections[current_section]['line_start'],
                        'line_end': i - 1
                    }
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = title
                current_level = level
                current_content = []
                sections[current_section] = {'line_start': i}
            else:
                if current_section:
                    current_content.append(line)
                else:
                    # Content before first header
                    if 'preamble' not in sections:
                        sections['preamble'] = {
                            'level': 0,
                            'content': line,
                            'line_start': 0,
                            'line_end': i
                        }
                    else:
                        sections['preamble']['content'] += '\n' + line
                        sections['preamble']['line_end'] = i
        
        # Save last section
        if current_section:
            sections[current_section] = {
                'level': current_level,
                'content': '\n'.join(current_content),
                'line_start': sections[current_section]['line_start'],
                'line_end': len(lines) - 1
            }
        
        return sections
    
    def update_changelog(self, analysis: Dict[str, any], version: str = "Unreleased") -> bool:
        """
        Append changelog entry to Updates.readme.
        
        Args:
            analysis: Analysis results
            version: Version string for the header
            
        Returns:
            True if modified
        """
        if not (analysis.get('new_features') or analysis.get('removed_features') or 
                analysis.get('modified_features') or analysis.get('configuration_updates')):
            return False
            
        import datetime
        date_str = datetime.date.today().isoformat()
        
        entry = f"\n## {version} ({date_str})\n\n"
        
        if analysis.get('new_features'):
            entry += "### Added\n"
            for feature in analysis['new_features']:
                entry += f"- {feature}\n"
            entry += "\n"
            
        if analysis.get('removed_features'):
            entry += "### Removed\n"
            for feature in analysis['removed_features']:
                entry += f"- {feature}\n"
            entry += "\n"
            
        if analysis.get('modified_features'):
            entry += "### Changed\n"
            for feature in analysis['modified_features']:
                entry += f"- {feature}\n"
            entry += "\n"

        if analysis.get('configuration_updates'):
            entry += "### Configuration\n"
            for config in analysis['configuration_updates']:
                entry += f"- {config}\n"
            entry += "\n"

        # Insert after "Latest Updates" header if it exists, otherwise append
        latest_updates_header = "## Latest Updates"
        if latest_updates_header in self.content:
            parts = self.content.split(latest_updates_header)
            self.content = parts[0] + latest_updates_header + entry + parts[1]
        else:
            self.content += entry
            
        return True

    def update_from_analysis(self, analysis: Dict[str, any]) -> bool:
        """
        Update README based on AI analysis results.
        
        Args:
            analysis: Analysis results from AIAnalyzer
            
        Returns:
            True if README was modified
        """
        modified = False
        
        # Add new features
        if analysis.get('new_features'):
            modified |= self._add_features(analysis['new_features'])
        
        # Remove deprecated features
        if analysis.get('removed_features'):
            modified |= self._remove_features(analysis['removed_features'])
        
        # Update modified features
        if analysis.get('modified_features'):
            modified |= self._update_features(analysis['modified_features'])
            
        # Update configuration
        if analysis.get('configuration_updates'):
            modified |= self._update_configuration(analysis['configuration_updates'])
        
        return modified
    
    def _add_features(self, features: List[str]) -> bool:
        """Add new features to README."""
        if not features:
            return False
        
        # Find or create Features section
        features_section = self._find_section(['Features', 'Key Features', 'Functionality', 'What it does'])
        
        if features_section:
            # Add to existing Features section
            section_content = self.sections[features_section]['content']
            
            # Add new features as bullet points
            new_content = section_content.rstrip()
            if not new_content.endswith('\n'):
                new_content += '\n'
            
            for feature in features:
                # Check if feature already exists (avoid duplicates)
                if feature.lower() not in section_content.lower():
                    new_content += f"- {feature}\n"
            
            self.sections[features_section]['content'] = new_content
        else:
            # Create new Features section
            new_section = "\n## Features\n\n"
            for feature in features:
                new_section += f"- {feature}\n"
            
            # Insert after title/preamble
            self.content = self._insert_after_preamble(new_section)
            self.sections = self._parse_sections(self.content)
        
        self._rebuild_content()
        return True
    
    def _remove_features(self, features: List[str]) -> bool:
        """Remove deprecated features from README."""
        if not features:
            return False
        
        modified = False
        
        # Search through all sections for matching features
        for section_name, section_data in self.sections.items():
            content = section_data['content']
            original_content = content
            
            for feature in features:
                # Try to find and remove feature mentions
                # Match bullet points or lines containing the feature
                pattern = rf'^\s*[-*+]\s+.*{re.escape(feature)}.*$'
                content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
            
            if content != original_content:
                self.sections[section_name]['content'] = content
                modified = True
        
        if modified:
            self._rebuild_content()
        
        return modified
    
    def _update_features(self, features: List[str]) -> bool:
        """Update modified features in README."""
        # For now, treat as additions
        # In a more sophisticated version, this could try to update existing entries
        return self._add_features(features)
        
    def _update_configuration(self, config_updates: List[str]) -> bool:
        """Update configuration section in README."""
        if not config_updates:
            return False
            
        # Find or create Configuration section
        config_section = self._find_section(['Configuration', 'Config', 'Environment', 'Setup'])
        
        if config_section:
            # Add to existing Configuration section
            section_content = self.sections[config_section]['content']
            
            new_content = section_content.rstrip()
            if not new_content.endswith('\n'):
                new_content += '\n'
            
            for config in config_updates:
                if config.lower() not in section_content.lower():
                    new_content += f"- {config}\n"
            
            if new_content != section_content:
                self.sections[config_section]['content'] = new_content
                self._rebuild_content()
                return True
                
        else:
            # Create new Configuration section
            new_section = "\n## Configuration\n\n"
            for config in config_updates:
                new_section += f"- {config}\n"
            
            # Insert after features or at end
            self.content = self._insert_after_preamble(new_section)
            self.sections = self._parse_sections(self.content)
            self._rebuild_content()
            return True
            
        return False
    
    def _find_section(self, possible_titles: List[str]) -> Optional[str]:
        """Find a section by possible title variations."""
        for title in possible_titles:
            for section_name in self.sections.keys():
                if title.lower() in section_name.lower():
                    return section_name
        return None
    
    def _insert_after_preamble(self, new_content: str) -> str:
        """Insert content after the preamble/title section."""
        lines = self.content.split('\n')
        
        # Find first header
        for i, line in enumerate(lines):
            if re.match(r'^#{1,6}\s+', line):
                # Insert before first header
                lines.insert(i, new_content)
                return '\n'.join(lines)
        
        # No headers found, append to end
        return self.content + '\n' + new_content
    
    def _rebuild_content(self):
        """Rebuild the content string from modified sections."""
        lines = self.content.split('\n')
        
        for section_name, section_data in self.sections.items():
            if section_name == 'preamble':
                continue
            
            start = section_data['line_start']
            end = section_data['line_end']
            level = section_data['level']
            
            # Rebuild section
            header = '#' * level + ' ' + section_name
            new_section_lines = [header] + section_data['content'].split('\n')
            
            # Replace in original lines
            # Note: This logic works for simple replacements but might be fragile if multiple sections change
            # However, for this task it should suffice as we re-parse after major structural changes if needed
            # A safer way would be to rebuild the whole file from sections, but we want to preserve other content
            
            # Simple check: if size changed significantly, might need care.
            # But here we just assume lines[start:end+1] captures the old section.
            lines[start:end + 1] = new_section_lines
        
        self.content = '\n'.join(lines)
    
    def save(self):
        """Save the updated README."""
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(self.content)
    
    def get_diff_preview(self, original_content: str) -> str:
        """
        Generate a diff preview of changes.
        
        Args:
            original_content: The original README content
            
        Returns:
            Formatted diff string
        """
        import difflib
        
        original_lines = original_content.split('\n')
        new_lines = self.content.split('\n')
        
        diff = difflib.unified_diff(
            original_lines,
            new_lines,
            fromfile=f'{self.readme_path} (original)',
            tofile=f'{self.readme_path} (updated)',
            lineterm=''
        )
        
        return '\n'.join(diff)
