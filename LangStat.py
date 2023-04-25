#!/usr/bin/env python
# coding: utf-8

import requests
import matplotlib.pyplot as plt
import random

def getGithubUserRepos( uname ):
    return f'https://api.github.com/users/{uname}/repos'


myUsername = "zigpot"
myGithubUserRepoRequest = getGithubUserRepos(myUsername)


# TODO: Overcome low rate limit using authentication, ref: https://docs.github.com/en/apps/creating-github-apps/creating-github-apps/rate-limits-for-github-apps
response = requests.get(myGithubUserRepoRequest)


# TODO: Handle response error (using try catch)
def getLangsStat(response, ignoreForks=True):
    langs = {}
    if(response.status_code == 200):
        print("success!")
        print(response.json())
        for item in response.json():
            langResponse = requests.get(item['languages_url']);
            isForked = item['fork'];
            if(langResponse.status_code == 200):
                if(not(ignoreForks and isForked)):
                    print(langs)
                    A = langs
                    B = langResponse.json()
                    c = {x: A.get(x, 0) + B.get(x, 0) for x in set(A).union(B)}
                    langs = c
    else:
        # TODO: response error
        print("failed with status code: ", response.status_code)
        print(response.reason)
    return langs


langs = getLangsStat(response, ignoreForks=False)

sortedLangsRev = dict(sorted(langs.items(), key = lambda x: x[1], reverse=True))


langs


print(sortedLangsRev)


import json

# https://raw.githubusercontent.com/ozh/github-colors/master/colors.json
f = open('colors.json')

githubLangColors = json.load(f)


def getRandomColor():
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color


langsLabels = list(sortedLangsRev.keys())
langsValues = list(sortedLangsRev.values())
langsColors = []
for lang in langsLabels:
    color = ''
    if lang in githubLangColors:
        color =githubLangColors[lang]['color']
        #print(f'{lang} {color}')
    else:
        color = langsColors.append(getRandomColor())
        #print(f'{lang} {color} (color not found, randomly assigned)')
    langsColors.append(color)
    
patches, text = plt.pie(langsValues, labels=langsLabels, radius=3.3, colors=langsColors)
plt.legend(patches, langsLabels, loc="best")
plt.show()


langsLabels[5]

