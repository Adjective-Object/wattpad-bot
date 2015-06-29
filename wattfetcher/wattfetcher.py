#!/usr/bin/python

import requests
import codecs
import os
from bs4 import BeautifulSoup
from threading import Thread

import logging
logging.captureWarnings(True)


DATA_DIR = "./data/parts"
AUTH_KEY = "oFruc7MoS8iAYiU5g5lSFhCzejz1AV1MQKnmlmgPjbQa"
REQUEST_BLOCK_SIZE = 10
STARTING_OFFSET = 0
NUM_STORIES_TO_SCRAPE = 2000


def mkdir_recursive(dirname):
    """ makes all the directories along a given path, if they do not exist
    """
    parent = os.path.dirname(dirname)
    if not os.path.exists(parent):
        os.mkdir(parent)
    if not os.path.exists(dirname):
        os.mkdir(dirname)


def scrape_part(url):
    textpart_response = requests.get(url)
    textpart_tree = BeautifulSoup(textpart_response.text, 'html.parser')
    textpart_body = textpart_tree.find_all("div", {"class": "page"})
    
    # for all body papers, DO IT
    body_text = ""
    for elem in textpart_body:
        body_text += reduce(
            lambda a, b: a + "\n" + b,
            (p.text.strip() for p in elem.find_all("p")),
            "")

    next_part_links = textpart_tree.find_all(
        "a", {"class": ["next-page", "next-part"]})

    next_part_url = (next_part_links[0]['href']
                     if len(next_part_links) > 0
                     else None)

    next_part_url = ("http://www.wattpad.com" + next_part_url
        if (next_part_url and 
            not next_part_url.startswith("http://www.wattpad.com"))
        else next_part_url)

    return body_text, next_part_url


def mkfilename(story, part):
    return os.path.join(
        DATA_DIR,
        "%d-p%04d-%s" % (story["id"],
                         part,
                         story["title"]
                            .replace(" ", "_")
                            .replace("/", "\/")))


def scrape_story(story):
    print "==== %s : %s" % (story["id"], story["title"])

    summary_response = requests.get(
        "http://www.wattpad.com/story/%s" % story["id"])
    summary_tree = BeautifulSoup(summary_response.text, 'html.parser')
    story_part_url = (
        "http://www.wattpad.com" +
        summary_tree(text="Start Reading")[0].parent['href'])

    cur_part = 1
    while story_part_url:
        content, story_part_url = scrape_part(story_part_url)

        if content:
            file_name = mkfilename(story, cur_part)
            print "    %s" % file_name
            with codecs.open(file_name, 'w', "utf-8") as f:
                f.write(content)
        cur_part += 1


def fetch_recent():
    stories_url = 'https://api.wattpad.com:443/v4/stories'

    mkdir_recursive(DATA_DIR)

    r = None
    n = 0

    while n < NUM_STORIES_TO_SCRAPE:
        print "offset: %s (%s/%s)" % (
            STARTING_OFFSET + n, n, NUM_STORIES_TO_SCRAPE)

        request_header = {
            "Authorization": AUTH_KEY
        }
        parameters = {
            "filter": "new",
            "limit": REQUEST_BLOCK_SIZE,
            "offset": STARTING_OFFSET + n
        }

        r = requests.get(stories_url,
                         headers=request_header,
                         params=parameters)

        if r.status_code != 200:
            print "status code: %s" % (r.status_code)
            print r.text
            exit(1)


        stories_dict = r.json()

        for story in stories_dict["stories"]:
            #scrape_story(story)
            thread = Thread(target=scrape_story, args=(story,))
            thread.start()

        n += REQUEST_BLOCK_SIZE


if __name__ == "__main__":
    fetch_recent()
    # scrape_story({
    #     "id": 43270514,
    #     "title": "Alpha's loner mate"
    #     })
