#!/usr/bin/env python3

import json
import random
import string
import logging
import requests

from collections import namedtuple
from os import path


logger = logging.getLogger()

config_file = path.join(path.dirname(path.dirname(__file__)), "config.json")
requests_timeout = 10

titles = [
    "dr", "mr", "cheeky", "duchess", "duke", "lord", "fluffy",
    "reverend", "the right reverend", "the right honorable", "count",
    "blind", "daddy", "mamma", "howlin'", "", "professor", "herr",
    "frau", "scratchy", "admiral", "your lord and saviour", "madam",
    "sir"]
first_names = [
    "fluffington", "meowmeow", "mittington", "patrick", "clawdia",
    "paws", "strange", "tom", "old tom", "beverly", "socks", "sybil",
    "claws", "dusty", "poo-foot", "litterbox", "socky", "teeth",
    "fangs", "yumyums", "super", "keith", "pussington", "fido",
    "alan", "catty", "fluffulus", "hamcat"]
last_names = [
    "of tunatown", "the fourth", "the seventh", "bumfluff",
    "the minger", "the crackhead", "kibblesocks", "biscuits",
    "cuteington", "bumtrousers", "of dustbath", "esquire",
    "the shrew beheader", "the maimer", "the nocturnal", "shitwiskers",
    "the bastard", "the disembowler", "the mouse botherer",
    "the shrew killer", "the salmon shredder", "the vomiter"]

MailgunConfig = namedtuple("MailgunConfig", ["url", "api_key", "from_address"])
CatPicture = namedtuple("CatPicture", ["url", "reddit_url"])


def parse_config(filename):
    raw = json.load(open(filename))
    recipients = raw["recipients"]
    assert type(recipients) == list
    raw_mailgun = raw["mailgun"]
    mailgun_config = MailgunConfig(url=raw_mailgun["url"],
                                   api_key=raw_mailgun["api-key"],
                                   from_address=raw_mailgun["from_address"])
    return recipients, mailgun_config


def generate_random_string(length=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_random_user_agent():
    return "TheDailyWhiskers" + generate_random_string()


def get_cat_name():
    return " ".join([random.choice(titles), random.choice(first_names), random.choice(last_names)])


def send(mailgun_config, to, html, image_name, image_content, image_content_type):
    response = requests.post(
        mailgun_config.url,
        auth=("api", mailgun_config.api_key),
        files=[("inline", (image_name, image_content, image_content_type))],
        data={"from": mailgun_config.from_address,
              "to": to,
              "subject": "The Daily Whiskers",
              "html": html},
        timeout=requests_timeout)
    response.raise_for_status()


def get_cat_picture(json_child):
    try:
        data = json_child["data"]
        link_flair_text = data["link_flair_text"]
        if link_flair_text != "Cat Picture":
            logger.debug("Wrong link_flair_text: %s", link_flair_text)
            return None

        if "preview" in data:
            logger.debug("Found single preview image")
            # 1 because 0 is very low res.
            url = data["preview"]["images"][0]["resolutions"][1]["url"]
        elif "gallery_data" in data:
            logger.debug("Found preview image gallery")
            first_media_id = data["gallery_data"]["items"][0]["media_id"]
            # Number 3 looks like a reasonable resolution?  I'm not sure how these resolutions are chosen!
            url = data["media_metadata"][first_media_id]["p"][3]["u"]
        else:
            raise ValueError("Not sure how to extract image from this JSON")

        # For a reason known only to the API designer, this is necessary
        url = url.replace("&amp;", "&")

        reddit_url = "https://www.reddit.com" + data["permalink"]
        return CatPicture(url=url,
                          reddit_url=reddit_url)
    except (KeyError, IndexError):
        logger.exception("Failed to get cat pic from JSON, which was: \n%s", json_child)
        return None


def get_cat_pictures(top_cats):
    children = top_cats["data"]["children"]

    # + 1 because sometimes weird posts are stickied at the top
    for json_child in children[1:]:
        cat_picture = get_cat_picture(json_child)
        if cat_picture is not None:
            yield cat_picture


def build_html(cat_name, image_file, reddit_url):
    return """
    <h1 style="text-align: center;">{cat_name}</h1>
    <img style="display: block; margin: auto; width: 100%;" src="cid:{image_file}">
    <p><small>Credit: <a href="{reddit_url}">{reddit_url}</a></small></p>
    """.format(cat_name=cat_name,
               image_file=image_file,
               reddit_url=reddit_url).strip()


def main():
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)

    logger.info("Dailywhiskers started")
    (recipients, mailgun_config) = parse_config(config_file)
    logger.debug("Loaded config")

    session = requests.Session()
    # Without this reddit gets very throttle-y
    session.headers = {"user-agent": generate_random_user_agent()}

    top_cats_resp = session.get("https://www.reddit.com/r/cats/top.json?t=day", timeout=requests_timeout)
    top_cats_resp.raise_for_status()

    for recipient, cat_picture in zip(recipients, get_cat_pictures(top_cats_resp.json())):
        response = session.get(cat_picture.url, timeout=requests_timeout)
        response.raise_for_status()

        logger.debug("Processing recipient: %s", recipient)
        cat_name = get_cat_name()

        # This random string solves Jess's iPhone issue where new pictures clobber old ones.
        cat_pic_name = "cat_pic" + generate_random_string()

        logger.info("Sending cat pic %s with name %s to %s", cat_picture.reddit_url, cat_pic_name, recipient)
        send(mailgun_config=mailgun_config,
             to=recipient,
             html=build_html(cat_name, cat_pic_name, cat_picture.reddit_url),
             image_name=cat_pic_name,
             image_content=response.content,
             image_content_type=response.headers["Content-Type"])


if __name__ == "__main__":
    main()


def handler(event, context):
    try:
        main()
    except:
        logger.exception("DailyWhiskers failed :(")
