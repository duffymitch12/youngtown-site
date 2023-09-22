"""
Check hand coded user page in html/users/awdeorio/index.html file.

EECS 485 Project 1

Andrew DeOrio <awdeorio@umich.edu>
"""
import re
import bs4


def test_images():
    """Verify all images are present in /users/awdeorio/index.html."""
    with open("html/users/awdeorio/index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    srcs = [x.get("src") for x in soup.find_all('img')]
    assert "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg" in srcs
    assert "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg" in srcs


def test_links():
    """Verify expected links in /users/awdeorio/index.html."""
    with open("html/users/awdeorio/index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    links = [x.get("href") for x in soup.find_all("a")]
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)
    assert "/" in links
    assert "/users/awdeorio/" in links
    assert "/users/awdeorio/followers/" in links
    assert "/users/awdeorio/following/" in links
    assert "/posts/1/" in links
    assert "/posts/3/" in links
    assert "/posts/4/" not in links
    assert "/users/jag/" not in links
    assert "/explore/" in links


def test_likes():
    """No likes on this page /users/awdeorio/index.html."""
    with open("html/users/awdeorio/index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)
    assert "likes" not in text


def test_comments():
    """No comments on this page /users/awdeorio/index.html."""
    with open("html/users/awdeorio/index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)
    assert "awdeorio #chickensofinstagram" not in text
    assert "jflinn I <3 chickens" not in text
    assert "michjc Cute overload!" not in text
    assert "awdeorio Sick #crossword" not in text
    assert "jflinn Walking the plank #chickensofinstagram" not in text
    assert "awdeorio This was after trying \
            to teach them to do a #crossword" not in text


def test_timestamps():
    """No timestamps on this page /users/awdeorio/index.html."""
    with open("html/users/awdeorio/index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)
    assert "10 minutes ago" not in text
    assert "4 hours ago" not in text
    assert "a day ago" not in text


def test_user_info():
    """Verify name, posts, followers, following /users/awdeorio/index.html."""
    with open("html/users/awdeorio/index.html", encoding='utf-8') as infile:
        soup = bs4.BeautifulSoup(infile, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)
    assert "awdeorio" in text
    assert "2 posts" in text
    assert "2 followers" in text
    assert "2 following" in text
    assert "Andrew DeOrio" in text
