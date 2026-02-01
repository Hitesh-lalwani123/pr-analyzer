
from readme_updater import READMEUpdater
import os

# Setup test files
if os.path.exists("Documentation.readme"):
    os.remove("Documentation.readme")
if os.path.exists("Updates.readme"):
    os.remove("Updates.readme")

with open("Documentation.readme", "w") as f:
    f.write("# Doc Title\n\n## Features\n- Existing Feature\n")

with open("Updates.readme", "w") as f:
    f.write("# Changelog\n\n## Latest Updates\n")

# Analysis data with configuration updates
analysis = {
    'new_features': [],
    'removed_features': [],
    'modified_features': [],
    'configuration_updates': ['Updated requirements.txt: requests>=2.31.0', 'Added GROQ_API_KEY env var'],
    'significance': 'medium',
    'summary': 'Config updates'
}

# Test Updates.readme (Changelog)
print("Testing Updates.readme...")
changelog_updater = READMEUpdater("Updates.readme")
changelog_modified = changelog_updater.update_changelog(analysis, version="v1.1.0")
changelog_updater.save()

with open("Updates.readme", "r") as f:
    content = f.read()
    print("Updates.readme content:\n" + content)
    assert "v1.1.0" in content
    assert "### Configuration" in content
    assert "requests>=2.31.0" in content

# Test Documentation.readme (Configuration)
print("\nTesting Documentation.readme...")
doc_updater = READMEUpdater("Documentation.readme")
doc_modified = doc_updater.update_from_analysis(analysis)
doc_updater.save()

with open("Documentation.readme", "r") as f:
    content = f.read()
    print("Documentation.readme content:\n" + content)
    assert "## Configuration" in content
    assert "GROQ_API_KEY" in content

print("\nSUCCESS: Both files updated correct with configuration changes.")
