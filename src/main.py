#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from flask import Flask
from flask import request
from flask import abort

import os
import json
import yaml
from subprocess import Popen, PIPE

CONFIG_FILE = "secrets.yaml"

# Welcome Message
print("")
print("")
print("======= RUNNING GIT AUDIT SCRIPT =======")


# LOAD THROUGH ENVIRONMENT VIRABLES
# SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
# GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY')
def load_config():
    global API_KEYS, SENDGRID_API_KEY, GITHUB_API_KEY
    # LOAD THROUGH CONFIG FILE
    if os.path.exists(CONFIG_FILE):
        print("Config '{}' found. Loading...".format(CONFIG_FILE))
        with open(CONFIG_FILE, 'r') as stream:
            CONFIG = yaml.safe_load(stream)
            # print(CONFIG)
            SENDGRID_API_KEY = CONFIG['sendgrid_api']
            SENDGRID_FROM = CONFIG['email_from']
            SENDGRID_SUBJECT = CONFIG['email_subject']
            SENDGRID_TEMPLATE = CONFIG['email_template']
            SENDGRID_NOTIFY = json.dumps(CONFIG['email_notify'])
            GITHUB_API_KEY = CONFIG['github_api']
            GITHUB_WHITELIST = json.dumps(CONFIG['github_whitelist'])
            GITHUB_SCAN = json.dumps(CONFIG['github_scan'])
            API_KEYS = CONFIG['controller_apikeys']

            os.environ["SENDGRID_API_KEY"] = str(SENDGRID_API_KEY)
            os.environ["SENDGRID_NOTIFY"] = (SENDGRID_NOTIFY)
            os.environ["SENDGRID_FROM"] = (SENDGRID_FROM)
            os.environ["SENDGRID_SUBJECT"] = (SENDGRID_SUBJECT)
            os.environ["SENDGRID_TEMPLATE"] = (SENDGRID_TEMPLATE)
            os.environ["GITHUB_API_KEY"] = str(GITHUB_API_KEY)
            os.environ["GITHUB_WHITELIST"] = (GITHUB_WHITELIST)
            os.environ["GITHUB_SCAN"] = (GITHUB_SCAN)


def maskme(_STR, show_len=-4):
    return len(str(_STR)[:show_len])*"#"+str(_STR)[show_len:]

# print(type(GITHUB_SCAN))
def run_scan():
    cmd = ['python', 'scan.py']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    print(stdout.decode())
    print(stderr.decode())


load_config()
run_scan()


# app = Flask(__name__)
# @app.route("/")
# def index():
#     if request.headers.get('api-key') not in API_KEYS:
#         abort(401)
#     else:
#         # printsettings()
#         cmd = ['python', 'scan.py']
#         p = Popen(cmd, stdout=PIPE, stderr=PIPE)
#         stdout, stderr = p.communicate()
#         if stderr.decode():
#             output = stderr.decode()
#         else:
#             output = stdout.decode()
#
#         return output
#
#
# app.run(host="0.0.0.0", port=8080)
