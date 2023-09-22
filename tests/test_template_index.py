"""
Check index page at /index.html URL.

EECS 485 Project 1

Andrew DeOrio <awdeorio@umich.edu>
"""
import re
import subprocess
from pathlib import Path
import bs4
import utils


def test_files(tmpdir):
    """Verify jinja is used properly.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/index.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)
    assert Path(outdir/"index.html").exists()


def test_images(tmpdir):
    """Verify all images are present in / URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/index.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)

    # Parse HTML, then extract image source urls
    with open(outdir/"index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    srcs = [x.get("src") for x in soup.find_all('img')]

    # Verify images present of Flinn, DeOrio, postid 1, postid 2, postid 3
    assert "/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg" in srcs
    assert "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg" in srcs
    assert "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg" in srcs
    assert "/uploads/ad7790405c539894d25ab8dcf0b79eed3341e109.jpg" in srcs
    assert "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg" in srcs


def test_links(tmpdir):
    """Verify expected links present in / URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/index.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)

    # Parse HTML, then extract image source urls
    with open(outdir/"index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    links = [x.get("href") for x in soup.find_all("a")]

    # Verify links are present
    assert "/" in links
    assert "/users/awdeorio/" in links
    assert "/users/jflinn/" in links
    assert "/users/michjc/" in links
    assert "/posts/1/" in links
    assert "/posts/2/" in links
    assert "/posts/3/" in links

    # Verify links are not present
    assert "/users/jag/" not in links
    assert "/posts/4/" not in links


def test_likes(tmpdir):
    """Verify expected "likes" are present in / URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/index.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)

    # Parse HTML, then convert all whitespace to single spaces
    with open(outdir/"index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)

    # Verify expected content is in text on generated HTML page
    assert "1 like" in text
    assert "2 likes" in text
    assert "3 likes" in text

    # Verify unexpected content is not in text on generated HTML page
    assert "1 likes" not in text
    assert "2 like " not in text
    assert "3 like " not in text
    assert "4 likes" not in text
    assert "0 likes" not in text


def test_timestamps(tmpdir):
    """Verify expected timestamps are present in / URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/index.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)

    # Parse HTML, then convert all whitespace to single spaces
    with open(outdir/"index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)

    # Verify expected content is in text on generated HTML page
    assert "10 minutes ago" in text
    assert "4 hours ago" in text
    assert "a day ago" in text


def test_comments(tmpdir):
    """Verify expected comments are present in / URL.

    Note: 'tmpdir' is a fixture provided by the pytest package.  It creates a
    unique temporary directory before the test runs, and removes it afterward.
    https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-fixture

    """
    utils.assert_config_not_modified("insta485")
    utils.assert_not_hardcoded("insta485/templates/index.html", tmpdir)
    outdir = tmpdir/"html"
    subprocess.run(["insta485generator", "insta485", "-o", outdir], check=True)

    # Parse HTML, then convert all whitespace to single spaces
    with open(outdir/"index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)

    # Verify expected content is in text on generated HTML page
    assert "awdeorio #chickensofinstagram" in text
    assert "jflinn I <3 chickens" in text
    assert "michjc Cute overload!" in text
    assert "awdeorio Sick #crossword" in text
    assert "jflinn Walking the plank #chickensofinstagram" in text
    assert "awdeorio This was after trying to teach them to do a #crossword" \
        in text
