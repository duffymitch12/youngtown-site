"""Public unit tests for insta485generator.

EECS 485 Project 1

Andrew DeOrio <awdeorio@umich.edu>

"""
import re
import shutil
import textwrap
import subprocess
from pathlib import Path
from utils import TESTDATA_DIR


def test_help():
    """Verify insta485generator --help output."""
    output = subprocess.run(
        ["insta485generator", "--help"],
        check=True, stdout=subprocess.PIPE, universal_newlines=True,
    ).stdout
    assert output == textwrap.dedent("""\
        Usage: insta485generator [OPTIONS] INPUT_DIR

          Templated static website generator.

        Options:
          -o, --output PATH  Output directory.
          -v, --verbose      Print more output.
          --help             Show this message and exit.
    """)


def test_output(tmpdir):
    """Verify insta485generator --output changes output dir.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    shutil.copytree(TESTDATA_DIR/"hello", tmpdir/"hello")

    # Run insta485generator using the --output option
    subprocess.run(
        ["insta485generator", "--output", "myout", "hello"],
        check=True,
        cwd=tmpdir,
    )

    # Verify files are present in "myout/" direcotry
    assert (tmpdir/"myout").exists()
    assert (tmpdir/"myout/index.html").exists()


def test_hello(tmpdir):
    """Test insta485generator with published "hello" input.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    shutil.copytree(TESTDATA_DIR/"hello", tmpdir/"hello")

    # Run insta485generator in tmpdir
    subprocess.run(["insta485generator", "hello"], check=True, cwd=tmpdir)

    # Make sure generated files exist
    output_dir = tmpdir/"hello/html"
    index_path = output_dir/"index.html"
    assert output_dir.exists()
    assert index_path.exists()

    # Verify output file content, normalized for whitespace
    actual = index_path.read_text(encoding="utf-8")
    correct = textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en">
           <head>
             <title>
               Hello world
             </title>
           </head>
           <body>
             hello
             world
           </body>
        </html>
    """)
    correct = re.sub(r"\s+", "", correct)
    actual = re.sub(r"\s+", "", actual)
    assert actual == correct


def test_hello_css(tmpdir):
    """Test insta485generator with published "hello_css" input.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    shutil.copytree(TESTDATA_DIR/"hello_css", tmpdir/"hello_css")

    # Run insta485generator in tmpdir
    subprocess.run(["insta485generator", "hello_css"], check=True, cwd=tmpdir)

    # Make sure generated files exist
    output_dir = tmpdir/"hello_css/html"
    output_html = output_dir/"index.html"
    output_css = output_dir/"css/style.css"
    assert output_dir.exists()
    assert output_html.exists()
    assert output_css.exists()

    # Verify output file content, normalized for whitespace
    actual_html = output_html.read_text(encoding="utf-8")
    correct_html = textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en">
          <head>
             <title>Hello world</title>
             <link rel="stylesheet" type="text/css" href="/css/style.css">
          </head>
          <body>
            <div class="important">hello</div>
            <div class="important">world</div>
          </body>
        </html>
    """)
    correct_html = re.sub(r"\s+", "", correct_html)
    actual_html = re.sub(r"\s+", "", actual_html)
    assert actual_html == correct_html

    # Verify CSS content
    correct_css = textwrap.dedent("""
        body {
            background: pink;
        }

        div.important {
            font-weight: bold;
            font-size: 1000%;
        }
    """)
    actual_css = Path(output_css).read_text(encoding='utf-8')
    correct_css = re.sub(r"\s+", "", correct_css)
    actual_css = re.sub(r"\s+", "", actual_css)
    assert actual_css == correct_css
