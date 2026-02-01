
from readme_updater import READMEUpdater
import os

# Setup test files
if os.path.exists("Documentation.readme"):
    os.remove("Documentation.readme")
if os.path.exists("Updates.readme"):
    os.remove("Updates.readme")

with open("Documentation.readme", "w") as f:
    f.write("# Doc Title\n\n## Features\n- Old Feature\n")

with open("Updates.readme", "w") as f:
    f.write("# Changelog\n\n## Latest Updates\n")

# Analysis data
analysis = {
    'new_features': ['New Cool Feature'],
    'removed_features': ['Old Feature'],
    'modified_features': ['Modified Feature'],
    'significance': 'medium',
    'summary': 'Test summary'
}

# Test Updates.readme (Changelog)
print("Testing Updates.readme...")
changelog_updater = READMEUpdater("Updates.readme")
changelog_modified = changelog_updater.update_changelog(analysis, version="v1.0.0")
changelog_updater.save()

with open("Updates.readme", "r") as f:
    content = f.read()
    print("Updates.readme content:\n" + content)
    assert "v1.0.0" in content
    assert "New Cool Feature" in content
    assert "### Added" in content

# Test Documentation.readme (Features)
print("\nTesting Documentation.readme...")
doc_updater = READMEUpdater("Documentation.readme")
doc_modified = doc_updater.update_from_analysis(analysis)
doc_updater.save()

with open("Documentation.readme", "r") as f:
    content = f.read()
    print("Documentation.readme content:\n" + content)
    assert "New Cool Feature" in content
    assert "Old Feature" not in content # Should be removed

print("\nSUCCESS: Both files updated correctly.")
