#!#!/usr/bin/env python
import os
from github import Github
from libraries.notify import Notify

import json
print("")
print("Scanning Github repos")

GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY')
WHITELIST = json.loads(os.environ.get('GITHUB_WHITELIST').lower())
GITHUB_SCAN = json.loads(os.environ.get('GITHUB_SCAN'))
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_FROM = os.environ.get('SENDGRID_FROM')
SENDGRID_SUBJECT = os.environ.get('SENDGRID_SUBJECT')
SENDGRID_TEMPLATE = os.environ.get('SENDGRID_TEMPLATE')
SENDGRID_NOTIFY = json.loads(os.environ.get('SENDGRID_NOTIFY'))


results = []
print(" Target: {}".format(GITHUB_SCAN))
print(" Github:{}".format(len(GITHUB_API_KEY[:-4])*"#"+GITHUB_API_KEY[-4:]))
print(" Whitelist: {}".format(WHITELIST))
print("")

def load_template(_file):
    try:
        with open(_file) as f:
            # print(f.readlines())
            return f.readlines()
    except IOError:
        print("Template file not accessible")

# or using an access token
g = Github(GITHUB_API_KEY)

for ITEM in GITHUB_SCAN:
    print("Checking {}".format(ITEM))
    for repo in g.get_user(ITEM).get_repos():
        if repo.name.lower() in WHITELIST:
            print(" [-] {}".format(repo.name))
            # commits = repo.get_commits()
            # for com in commits:
            #    print(com)
        else:
            print(" [+] {}".format(repo.name))
            results.append("{}/{}".format(ITEM,repo.name))

if results:
    print("FOUND NEW REPOs!!! SENDING EMAIL!!!")
    #exit()
    notify = Notify(SENDGRID_API_KEY)
    notify.add_from(SENDGRID_FROM)
    notify.add_mailto(SENDGRID_NOTIFY)
    notify.add_subject(SENDGRID_SUBJECT)
    notify.add_content_html(load_template(SENDGRID_TEMPLATE))
    notify.update_content_html("<!--RESULTS-->", results)
    notify.send_mail()
else:
    print("Nothing found, going to sleep")
