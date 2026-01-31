#!/usr/bin/env python3
"""
Setup script to install PR Analyzer in any repository.
Run this script in your target repository to set up the analyzer.
"""

import os
import shutil
import sys
from pathlib import Path

REQUIRED_FILES = [
    '.github/workflows/pr-analyzer.yml',
    'analyzer.py',
    'ai_analyzer.py',
    'filters.py',
    'readme_updater.py',
    'requirements.txt'
]

def main():
    print("🚀 PR Analyzer Setup Script")
    print("=" * 50)
    
    # Check if running in a git repo
    if not os.path.exists('.git'):
        print("❌ Error: Not in a git repository!")
        print("   Please run this script from the root of your git repository.")
        sys.exit(1)
    
    print("✅ Git repository detected")
    
    # Get source directory
    source_dir = input("\n📂 Enter path to pr-analyzer source (or press Enter for current dir): ").strip()
    if not source_dir:
        source_dir = "."
    
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"❌ Error: Source directory '{source_dir}' not found!")
        sys.exit(1)
    
    # Check if all required files exist in source
    missing_files = []
    for file in REQUIRED_FILES:
        if not (source_path / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Error: Missing files in source directory:")
        for file in missing_files:
            print(f"   - {file}")
        sys.exit(1)
    
    print("\n✅ All required files found in source")
    
    # Confirm installation
    print(f"\n📋 Will install PR Analyzer to: {os.getcwd()}")
    response = input("   Continue? (y/n): ").strip().lower()
    
    if response != 'y':
        print("❌ Installation cancelled")
        sys.exit(0)
    
    # Create .github/workflows directory if it doesn't exist
    workflows_dir = Path('.github/workflows')
    workflows_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n✅ Created {workflows_dir}")
    
    # Copy files
    print("\n📦 Copying files...")
    for file in REQUIRED_FILES:
        src = source_path / file
        dst = Path(file)
        
        # Create parent directory if needed
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file already exists
        if dst.exists():
            response = input(f"   ⚠️  {file} already exists. Overwrite? (y/n): ").strip().lower()
            if response != 'y':
                print(f"   ⏭️  Skipping {file}")
                continue
        
        shutil.copy2(src, dst)
        print(f"   ✅ Copied {file}")
    
    print("\n" + "=" * 50)
    print("✅ Installation complete!")
    print("\n📝 Next steps:")
    print("   1. Get your FREE Groq API key: https://console.groq.com/")
    print("   2. Add GitHub secret GROQ_API_KEY to your repository")
    print("   3. Commit and push the new files:")
    print(f"      git add {' '.join(REQUIRED_FILES)}")
    print("      git commit -m 'Add PR analyzer'")
    print("      git push origin main")
    print("   4. Create a test PR to see it in action!")
    print("\n📖 For detailed instructions, see REUSABLE_GUIDE.md")
    print("=" * 50)

if __name__ == "__main__":
    main()
