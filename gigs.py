#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from mastodon import Mastodon
import os
import logging

logger = logging.getLogger("gigs")
logging.basicConfig(level=logging.INFO)

URL = "https://sydneymusic.net/gig-guide"
server = os.environ.get("SERVER", "https://localhost")
token = os.environ.get("TOKEN", "insert coin")
max_len = 500
template = """Gigs in Sydney today: '{acts}'.

Check https://sydneymusic.net/gig-guide for details.

#sydney #music"""

def get_acts():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    month = soup.find("div", class_="guide-month")
    day = month.find("div", class_="day")
    titles = day.find_all("h4")
    todays_headline_acts = [title.text for title in titles]
    acts = ", ".join(todays_headline_acts)
    return acts

def format_toot(acts):
    # trim acts if we will blow car limit.
    if (len(acts) + len(template) > max_len):
        trim = max_len - len(template) - 1
        acts = "{acts}…".format(acts=acts[0:trim])
    return template.format(acts=acts)

def send_toot(toot):
    # https://github.com/halcy/Mastodon.py
    # Create an instance of the Mastodon class
    mastodon = Mastodon(
        access_token=token,
        api_base_url=server
    )
    mastodon.status_post(toot)

if __name__ == "__main__":
    logger.info("Beginning run.")
    acts = get_acts()
    toot = format_toot(acts)
    send_toot(toot)
    logger.info(toot)