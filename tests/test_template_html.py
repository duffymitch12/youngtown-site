"""
Validate generated HTML against HTML5 W3C spec.

EECS 485 Project 1

Andrew DeOrio <awdeorio@umich.edu>
"""
import subprocess
from pathlib import Path
import utils


def test_html(tmpdir):
    """Validate generated HTML5 in insta485/html/ .

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)

    # Verify expected files are present
    assert Path(outdir/"index.html").exists()
    assert Path(
        # Drew
        outdir/"uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg"
    ).exists()
    assert Path(
        # Jag
        outdir/"uploads/73ab33bd357c3fd42292487b825880958c595655.jpg"
    ).exists()
    assert Path(
        # Mike
        outdir/"uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg"
    ).exists()
    assert Path(
        # Jason
        outdir/"uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg"
    ).exists()
    assert Path(
        # Post 1
        outdir/"uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg"
    ).exists()
    assert Path(
        # Post 2
        outdir/"uploads/ad7790405c539894d25ab8dcf0b79eed3341e109.jpg"
    ).exists()
    assert Path(
        # Post 3
        outdir/"uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg"
    ).exists()
    assert Path(
        # Post 4
        outdir/"uploads/2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg"
    ).exists()

    # Verify HTML5
    subprocess.run([
        "html5validator",
        "--root", outdir,
        "--ignore", "JAVA_TOOL_OPTIONS",
    ], check=True)
