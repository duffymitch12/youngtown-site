"""P2 autograder utility functions."""
import json
import shutil
import subprocess
import filecmp
from pathlib import Path


# Directory containing unit tests
TEST_DIR = Path(__file__).parent

# Directory containing unit test input files
TESTDATA_DIR = TEST_DIR/"testdata"


def assert_not_hardcoded(template_path, tmpdir):
    """Raise an assertion if jinja template is hardcoded.

    Render the template with two different configurations.  If the output is
    different, then the template is not hardcoded.

    """
    tmpdir = Path(tmpdir)
    template_path = Path(template_path)

    # This only works for insta485 templates
    assert "insta485/templates" in str(template_path), \
        "Expected an insta485 template"

    # Create two sites dirs to run generator on with different configs
    stem = template_path.stem  # explore.html -> explore
    site1_dir = tmpdir/"template_not_hardcoded"/stem/"site1"
    site2_dir = tmpdir/"template_not_hardcoded"/stem/"site2"
    assert not site1_dir.exists()
    assert not site2_dir.exists()
    site1_dir.mkdir(parents=True)
    site2_dir.mkdir(parents=True)

    # Copy jinja_check_configs for the given template type
    config_1 = TESTDATA_DIR/"template_not_hardcoded"/stem/"1/config.json"
    config_2 = TESTDATA_DIR/"template_not_hardcoded"/stem/"2/config.json"
    shutil.copy(config_1, site1_dir)
    shutil.copy(config_2, site2_dir)

    # Copy ALL student templates.  We copy everything to ensure that
    # template inheritance works correctly, e.g., "base.html".
    shutil.copytree(template_path.parent, site1_dir/"templates")
    shutil.copytree(template_path.parent, site2_dir/"templates")

    # Generate the two single site pages
    subprocess.run(["insta485generator", site1_dir], check=True)
    subprocess.run(["insta485generator", site2_dir], check=True)

    # Verify that pages are created
    site1_index = site1_dir/"html/index.html"
    site2_index = site2_dir/"html/index.html"
    assert site1_index.exists()
    assert site2_index.exists()

    # Verify two rendered pages are different.  If they were hardcoded,
    # they would be the same.
    assert not filecmp.cmp(site1_index, site2_index, shallow=False), \
        "Templates fail to generate unique sites using different configs"


def assert_config_not_modified(input_dir):
    """Raise an assertion if insta485generator config is modified."""
    input_dir = Path(input_dir)
    assert str(input_dir) == input_dir.name, "Expected a basename"
    original_config_path = (TESTDATA_DIR/input_dir/"config.json").resolve()
    student_config_path = (input_dir/"config.json").resolve()
    assert student_config_path != original_config_path
    with student_config_path.open(encoding='utf-8') as infile:
        student_config = json.load(infile)
    with original_config_path.open(encoding='utf-8') as infile:
        original_config = json.load(infile)
    assert student_config == original_config, (
        "Modified config file.  These configs do not match:\n"
        f"student_config: {student_config}\n"
        f"original_config: {original_config}\n"
    )
