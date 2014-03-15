#!/usr/bin/env python

import urllib2, json, sys

bnet = raw_input('Enter your Bnet ID, ex. Name#1234: ')
region = raw_input('Enter your region. us/eu/kr: ')
bnet = bnet.replace('#', '-')

def getChars(bnet):
    url = 'http://' + region + '.battle.net/api/d3/profile/' + bnet + '/'

    response = urllib2.urlopen(url)
    json_profile = json.load(response)

    characters = {}
    for char in json_profile["heroes"]:
        characters[char['name']] = char['id']
    return characters

def retrieveHero(char_id):
    url = 'http://' + region + '.battle.net/api/d3/profile/' + bnet + '/hero/' + str(char_id)
    response = urllib2.urlopen(url)
    json_char = json.load(response)
    return json_char
    
def checkHeroes(characters):
    print '\n'
    for c in characters:
        d = retrieveHero(characters[c])
        print d['name'], 'level', d['level'], d['class']
    print '\n'
    
def checkSkills(hero):
    c = retrieveHero(hero)
    print '\n', c['name'], '-', c['level'], c['class'], '\n', '*'*24
    for i in range(len(c['skills']['active'])):
        try:
            print c['skills']['active'][i]['skill']['name'], '-', c['skills']['active'][i]['rune']['name']
        except KeyError:
            break
                
    for i in range(len(c['skills']['passive'])):
        try:
            print c['skills']['passive'][i]['skill']['name']
        except KeyError:
            break

d3_characters = getChars(bnet)
while True:
    checkHeroes(d3_characters)
    selected_char = raw_input('Enter the name of desired character: ')
    if selected_char == 'exit' or selected_char == 'quit':
        sys.exit()
    checkSkills(d3_characters[selected_char.capitalize()])