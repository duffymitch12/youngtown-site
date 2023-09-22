"""
Test /users/<user_url_slug/following/index.html URLs.

EECS 485 Project 1

Andrew DeOrio <awdeorio@umich.edu>
"""
import subprocess
from pathlib import Path
import bs4
import utils


def test_files(tmpdir):
    """Verify all expected files exist.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/following.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)
    assert Path(outdir/"users/awdeorio/following/index.html").exists()
    assert Path(outdir/"users/michjc/following/index.html").exists()
    assert Path(outdir/"users/jag/following/index.html").exists()
    assert Path(outdir/"users/jflinn/following/index.html").exists()


def test_awdeorio_following(tmpdir):
    """Check content at /users/awdeorio/following/index.html URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)

    # Parse HTML, then convert all whitespace to single spaces
    with open(outdir/"users/awdeorio/following/index.html", encoding='utf-8')\
         as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    srcs = [x.get("src") for x in soup.find_all('img')]
    links = [x.get("href") for x in soup.find_all("a")]

    # Every page should have these
    assert "/" in links
    assert "/explore/" in links
    assert "/users/awdeorio/" in links

    # Check for text
    assert text.count("following") == 2
    assert "not following" not in text

    # Check for images
    assert "/uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg" in srcs
    assert "/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg" in srcs
    assert "/uploads/73ab33bd357c3fd42292487b825880958c595655.jpg" not in srcs

    # Links specific to /users/awdeorio/followers/
    assert "/users/jflinn/" in links
    assert "/users/michjc/" in links
    assert "/users/jag/" not in links


def test_michjc_following(tmpdir):
    """Check content at /users/michjc/following/index.html URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/following.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)
    with open(outdir/"users/michjc/following/index.html", encoding='utf-8')\
         as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    srcs = [x.get("src") for x in soup.find_all('img')]
    links = [x.get("href") for x in soup.find_all("a")]

    # Every page should have these
    assert "/" in links
    assert "/explore/" in links
    assert "/users/awdeorio/" in links

    # Links specific to /users/michjc/followers/
    assert "/users/jflinn/" not in links
    assert "/users/michjc/" not in links

    # Check for images
    assert "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg" in srcs
    assert "/uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg" not in srcs
    assert "/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg" not in srcs


def test_jag_following(tmpdir):
    """Check content at /users/jag/following/index.html URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/following.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)
    with open(outdir/"users/jag/following/index.html", encoding='utf-8')\
         as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    srcs = [x.get("src") for x in soup.find_all('img')]
    links = [x.get("href") for x in soup.find_all("a")]

    # Every page should have these
    assert "/" in links
    assert "/explore/" in links
    assert "/users/awdeorio/" in links

    # Links specific to /users/michjc/followers/
    assert "/users/jflinn/" not in links
    assert "/users/jag/" not in links
    assert "/users/michjc/" in links

    # Check for images
    assert "/uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg" in srcs
    assert "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg" not in srcs
    assert "/uploads/73ab33bd357c3fd42292487b825880958c595655.jpg" not in srcs
    assert "/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg" not in srcs

    # Check for text
    assert "following" in text
    assert "not following" not in text


def test_jflinn_following(tmpdir):
    """Check content at /users/jflinn/following/index.html URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/following.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)
    with open(outdir/"users/jflinn/following/index.html", encoding='utf-8')\
         as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    srcs = [x.get("src") for x in soup.find_all('img')]
    links = [x.get("href") for x in soup.find_all("a")]

    # Every page should have these
    assert "/" in links
    assert "/explore/" in links
    assert "/users/awdeorio/" in links
    # Links specific to /users/michjc/followers/
    assert "/users/michjc/" in links
    assert "/users/jflinn/" not in links
    assert "/users/jag/" not in links

    # Check for images
    assert "/uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg" in srcs
    assert "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg" in srcs

    assert "/uploads/73ab33bd357c3fd42292487b825880958c595655.jpg" not in srcs
    assert "/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg" not in srcs

    # Check for text
    assert "not following" not in text
    assert text.count("following") == 1
