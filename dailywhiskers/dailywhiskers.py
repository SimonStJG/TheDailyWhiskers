#!/usr/bin/env python3

import json
import random
import string

from collections import namedtuple
from os import path

import requests

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

def parse_config(filename):
    raw = json.load(open(filename))
    recipients = raw["recipients"]
    assert type(recipients) == list  # I miss langages which handle types properly.
    raw_mailgun = raw["mailgun"]
    mailgun_config = MailgunConfig(url=raw_mailgun["url"],
                                   api_key=raw_mailgun["api-key"],
                                   from_address=raw_mailgun["from_address"])
    return (recipients, mailgun_config)

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

def cat_picture(reddit_json):
    # 1 because 0 is very low res.
    url = reddit_json["data"]["preview"]["images"][0]["resolutions"][1]["url"]
    # For a reason known only to the API designer, this is necessary
    url = url.replace("&amp;", "&")
    #  Without the headers, reddit gets very throttle-y.
    response = get_url(url, headers={"user-agent": generate_random_user_agent()})
    return (response.content, response.headers["Content-Type"])

def build_html(cat_name, image_file):
    return """
    <h1 style="text-align: center;">{}</h1>
    <img style="display: block; margin: auto; width: 100%;" src="cid:{}">
    """.format(cat_name, image_file).strip()

def main():
    (recipients, mailgun_config) = parse_config(config_file)
    reddit_json = json.loads(get_url(
        # With HTTP, reddit will respond with a 302 to the HTTPS version.
        # flair='default' only shows pics (ie. no mourning, no questions, etc).
        # restrict_sr=on restricts to the r/cats subreddit.
        # sort=top&t=day picks the top submissions for the last day.
        "https://www.reddit.com/r/cats/search.json?q=flair%3A%27default%27&restrict_sr=on&sort=top&t=day",
        headers={"user-agent": generate_random_user_agent()}).content.decode("UTF-8"))

    try:
        children = reddit_json["data"]["children"]
    except KeyError as e:
        raise Exception("Unexpected respone: {}".format(reddit_json), e)
    for i, recipient in enumerate(recipients):
        # + 1 because sometimes weird posts are stickied at the top
        (image_content, image_content_type) = cat_picture(children[i + 1])
        cat_name = get_cat_name()

        # I have a feeling this random string will solve Jess's iPhone issue where
        # new pictures clobber old ones.  Need to test.
        cat_pic_name = "cat_pic" + generate_random_string()
        send(mailgun_config=mailgun_config,
             to=recipient,
             html=build_html(cat_name, cat_pic_name),
             image_name=cat_pic_name,
             image_content=image_content,
             image_content_type=image_content_type)

if __name__ == "__main__":
    main()
