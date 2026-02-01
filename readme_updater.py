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
    def update_changelog(self, analysis: Dict[str, any], version: str = "Unreleased") -> bool:
        """
        Append changelog entry to RELEASES.md.
        
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
        version_header = f"## {version}"
        
        # Helper to generate bullet points
        def get_bullets(items):
            return "".join([f"- {item}\n" for item in items])

        changes = {}
        if analysis.get('new_features'): changes['Added'] = get_bullets(analysis['new_features'])
        if analysis.get('removed_features'): changes['Removed'] = get_bullets(analysis['removed_features'])
        if analysis.get('modified_features'): changes['Changed'] = get_bullets(analysis['modified_features'])
        if analysis.get('configuration_updates'): changes['Configuration'] = get_bullets(analysis['configuration_updates'])

        if not changes:
            return False

        # Regex to find existing version section
        # Matches "## Version (Date)" until the next "## " or End of string
        pattern = re.compile(rf"({re.escape(version_header)}[^\n]*\n)(.*?)(?=\n## |\Z)", re.DOTALL)
        match = pattern.search(self.content)
        
        if match:
            # Merge into existing section
            full_match = match.group(0)
            header_line = match.group(1)
            body = match.group(2)
            
            new_body = body
            
            for category, bullets in changes.items():
                cat_header = f"### {category}"
                if cat_header in new_body:
                    # Append to existing category
                    # Find category block
                    cat_pattern = re.compile(rf"({re.escape(cat_header)}\n)(.*?)(?=\n### |\n## |\Z)", re.DOTALL)
                    cat_match = cat_pattern.search(new_body)
                    if cat_match:
                        # Add new bullets to existing bullets
                        existing_bullets = cat_match.group(2)
                        # Avoid duplicates
                        new_unique_bullets = ""
                        for line in bullets.splitlines(keepends=True):
                             if line.strip() not in existing_bullets:
                                 new_unique_bullets += line
                        
                        if new_unique_bullets:
                            # Replace the category block with old + new
                            new_cat_block = cat_match.group(1) + existing_bullets.rstrip() + "\n" + new_unique_bullets
                            new_body = new_body.replace(cat_match.group(0), new_cat_block)
                else:
                    # Add new category
                    new_body = new_body.rstrip() + f"\n\n{cat_header}\n{bullets}"
            
            if new_body != body:
                self.content = self.content.replace(full_match, header_line + new_body)
                return True
                
        else:
            # Create new version entry
            new_entry = f"\n{version_header} ({date_str})\n\n"
            for category, bullets in changes.items():
                new_entry += f"### {category}\n{bullets}\n"
                
            # Insert logic
            if "Release Notes" in self.content:
                # Insert after "Release Notes" header line
                # Find the line "Release Notes"
                lines = self.content.splitlines(keepends=True)
                inserted = False
                for i, line in enumerate(lines):
                    if "# Release Notes" in line:
                         lines.insert(i + 1, new_entry)
                         inserted = True
                         break
                if inserted:
                    self.content = "".join(lines)
                else:
                    self.content += new_entry
            else:
                 self.content = "# Release Notes\n" + new_entry + self.content
            
            return True
            
        return False

    def update_from_analysis(self, analysis: Dict[str, any]) -> bool:
        """
        Update README based on AI analysis results.
        
        Args:
            analysis: Analysis results from AIAnalyzer
            
        Returns:
            True if README was modified
        """
        modified = False
        
        # Update documentation entries (Structured features)
        if analysis.get('documentation_entries'):
            modified |= self._update_documentation_entries(analysis['documentation_entries'])
        # Fallback to simple features if no structured docs (or add them too if needed, but per request, strict separation)
        elif analysis.get('new_features'):
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
        
        # Special case: If "Release Notes" is the title, insert after it.
        # Check first line
        if lines and "Release Notes" in lines[0]:
             # Insert after line 0 (Title)
             lines.insert(1, new_content)
             return '\n'.join(lines)
        
        # Find first header
        for i, line in enumerate(lines):
            if re.match(r'^#{1,6}\s+', line):
                # If this header is "Release Notes", insert AFTER it 
                # (Assuming "Release Notes" is a section container, and we want entries inside it)
                # But actually, usually "Release Notes" is the H1, and we want "## v1.0" as H2s after it.
                
                if "Release Notes" in line:
                     lines.insert(i + 1, new_content)
                     return '\n'.join(lines)
                
                # Otherwise, insert before first header (as preamble)
                lines.insert(i, new_content)
                return '\n'.join(lines)
        
        # No headers found, append to end
        return self.content + '\n' + new_content
    
    def _rebuild_content(self):
        """Rebuild the content string from modified sections."""
        # Robust rebuild by concatenating sections instead of line slicing
        new_lines = []
        
        # Ensure preamble is first if it exists
        if 'preamble' in self.sections:
            new_lines.append(self.sections['preamble']['content'])
            
        for section_name, section_data in self.sections.items():
            if section_name == 'preamble':
                continue
                
            level = section_data['level']
            header = '#' * level + ' ' + section_name
            new_lines.append(header)
            
            content = section_data['content']
            if content:
                new_lines.append(content)
                
        self.content = '\n'.join(new_lines)
    
    def _update_documentation_entries(self, entries: List[Dict[str, str]]) -> bool:
        """
        Update structured documentation entries in README.
        
        Args:
            entries: List of dicts with name, description, input, output
        """
        if not entries:
            return False
            
        # Find or create Features section
        features_section = self._find_section(['Features', 'Key Features', 'Functionality', 'What it does'])
        
        formatted_entries = []
        for entry in entries:
            # Format: 
            # ### Name
            # Description
            # - **Input**: ...
            # - **Output**: ...
            
            content = f"\n### {entry.get('name', 'Feature')}\n"
            content += f"{entry.get('description', '')}\n\n"
            if entry.get('input'):
                content += f"- **Input**: {entry['input']}\n"
            if entry.get('output'):
                content += f"- **Output**: {entry['output']}\n"
            formatted_entries.append(content)
            
        if features_section:
            # Append to existing Features section
            # Logic: Check if feature name already exists to avoid duplicates
            current_content = self.sections[features_section]['content']
            new_content = current_content
            
            added_any = False
            for i, entry in enumerate(entries):
                name = entry.get('name', '')
                if f"### {name}" not in current_content:
                    new_content += formatted_entries[i]
                    added_any = True
            
            if added_any:
                self.sections[features_section]['content'] = new_content
                self._rebuild_content()
                return True
        else:
            # Create new Features section
            new_section_content = "\n## Features\n" + "".join(formatted_entries)
            self.content = self._insert_after_preamble(new_section_content)
            self.sections = self._parse_sections(self.content)
            self._rebuild_content()
            return True
            
        return False

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
