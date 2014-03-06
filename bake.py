#!/usr/bin/env python

import requests
import sys
from subprocess import check_call

class TeamRequester:
    def __init__(self):
        self.teams = requests.get("https://www.studentrobotics.org/resources/2014/teams.json").json()

    def keys(self):
        return self.teams.keys()

    def __getitem__(self, team_name):
        return self.teams[team_name]

def make_tex(tla, long_name):
    text = unicode(open("comp-explainer.tex", "r").read())
    text = text.replace(u"SCHOOL_LONG_NAME", long_name)
    text = text.replace(u"SCHOOL_TLA", tla)
    text = text.replace(u" " + tla + " ", u" {\\bf " + tla + "} ")
    with open("bakes/tex/" + tla + ".tex", "wb") as fp:
        fp.write(text.encode("utf8"))

def make_image(tla):
    pass


def make_pdf(tla):
    print tla
    check_call(
        [
            "pdflatex",
            "bakes/tex/" + tla + ".tex",
            "-output-directory",
            "bakes/pdf",
        ]
    )

    check_call(["rm *.aux *.log"], shell=True)
    check_call(["mv " + tla + ".pdf bakes/pdf"], shell=True)


def make_document(tla, long_name):
    make_tex(tla, long_name)
    make_image(tla)
    make_pdf(tla)

if __name__ == "__main__":
    tr = TeamRequester()
    for idx, key in enumerate(tr.keys()):
        if idx > 2:
            break
        print key
        sys.stdout.write("\rMaking document for team: " + str(idx) + "/" + str(len(tr.keys())) + "         \r")
        sys.stdout.flush()
        make_document(key, tr[key]["name"])

    print "Done"
