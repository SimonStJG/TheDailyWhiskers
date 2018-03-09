#!/usr/bin/env python3

import json
import random
import string

from collections import namedtuple
from os import path

import logging
import requests
import sys

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='%(asctime)s;%(levelname)s;%(message)s')
config_file = path.join(path.dirname(path.dirname(__file__)), "config.json")

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
CatPicture = namedtuple("CatPicture", ["content", "content_type", "reddit_url"])


def parse_config(filename):
    raw = json.load(open(filename))
    recipients = raw["recipients"]
    assert type(recipients) == list  # I miss languages which handle types properly.
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
              "html": html})
    response.raise_for_status()

def get_url(url, **kwargs):
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    return response

def get_cat_picture(reddit_json):
    # 1 because 0 is very low res.
    url = reddit_json["data"]["preview"]["images"][0]["resolutions"][1]["url"]
    # For a reason known only to the API designer, this is necessary
    url = url.replace("&amp;", "&")

    reddit_url = "https://www.reddit.com" + reddit_json["data"]["permalink"]

    #  Without the headers, reddit gets very throttle-y.
    response = get_url(url, headers={"user-agent": generate_random_user_agent()})
    return CatPicture(content=response.content,
                      content_type=response.headers["Content-Type"],
                      reddit_url=reddit_url)

def build_html(cat_name, image_file, reddit_url):
    return """
    <h1 style="text-align: center;">{cat_name}</h1>
    <img style="display: block; margin: auto; width: 100%;" src="cid:{image_file}">
    <p><small>Credit: <a href="{reddit_url}">{reddit_url}</a></small></p>
    """.format(cat_name=cat_name,
               image_file=image_file,
               reddit_url=reddit_url).strip()

def retrieve_reddit_json(count=0):
    reddit_json = json.loads(get_url(
        # With HTTP, reddit will respond with a 302 to the HTTPS version.
        # flair='' only shows pics (ie. no mourning, no questions, etc).
        #   This used to be flair='default', changed for some reason.
        # restrict_sr=on restricts to the r/cats subreddit.
        # sort=top&t=day picks the top submissions for the last day.
        "https://www.reddit.com/r/cats/search.json?q=flair%253A%27default%27&restrict_sr=on&sort=top&t=day",
        headers={"user-agent": generate_random_user_agent()}).content.decode("UTF-8"))

    # Reddit seems to return empty results sometimes, for completely
    # identical requests.  Maybe it's a bug, or maybe they don't want me
    # scraping :(
    if len(reddit_json['data']['children']) == 0:
        if count >= 5:
            raise Exception("Reddit returned empty data: {}".format(reddit_json))
        else:
            logging.warning("Reddit returned empty data, retrying: {}".format(reddit_json))
            return retrieve_reddit_json(count + 1)
    return reddit_json["data"]["children"]

def main():
    logging.info("dailywhiskers started")
    (recipients, mailgun_config) = parse_config(config_file)

    children = retrieve_reddit_json()

    for i, recipient in enumerate(recipients):
        # + 1 because sometimes weird posts are stickied at the top
        try:
            cat_picture = get_cat_picture(children[i + 1])
        except (KeyError, IndexError):
            logging.debug("Failed to get cat pic from JSON, which was: \n{}".format(reddit_json))
            raise

        cat_name = get_cat_name()

        # This random string solves Jess's iPhone issue where new pictures clobber old ones.
        cat_pic_name = "cat_pic" + generate_random_string()

        logging.info("Sending cat pic {} with name {} to {}".format(cat_picture.reddit_url,
                                                                    cat_pic_name,
                                                                    recipient))
        send(mailgun_config=mailgun_config,
             to=recipient,
             html=build_html(cat_name, cat_pic_name, cat_picture.reddit_url),
             image_name=cat_pic_name,
             image_content=cat_picture.content,
             image_content_type=cat_picture.content_type)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("DailyWhiskers failed.")
