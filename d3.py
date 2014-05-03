#!/usr/bin/env python

import urllib2, json, sys

def getChars(acc, loc):
    global region, bnet
    bnet = acc
    region = loc
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
 
def retrieveItem(item_id):
    url = 'http://' + region + '.battle.net/api/d3/data/' + item_id
    response = urllib2.urlopen(url)
    json_item = json.load(response)
    return json_item
    
def checkHeroes(characters):
    heroes = {}
    for c in characters:
        h = retrieveHero(characters[c])
        heroes[h['name']] = ' '.join([str(h['level']), h['class']])
    return heroes

def checkGear(hero):
    c = retrieveHero(hero)
    fire, cold, lightning, holy, poison, physical = 0, 0, 0, 0, 0, 0
    skills = {'Fire': 0, 'Cold': 0, 'Holy': 0, 'Poison': 0, 'Physical': 0, 'Lightning': 0}
    gearset = c['items']
    for slot in gearset:
        i = retrieveItem(gearset[slot]['tooltipParams'])
        for att in i['attributes']['primary']:
            text_line = att['text']
            type = text_line.split(' ')
            for element in skills:
                if type[0] == element:
                    skills[element] += int(type[3].split('%')[0])
            
            if 'Increases' in type and 'Damage' in type:
                new_skill = ''.join(type[1:type.index('Damage')])
                damage_loc = text_line.index('%')
                damage_increase = text_line[damage_loc-2:damage_loc].strip(' ')
                if new_skill in skills:
                    skills[new_skill] += int(damage_increase)
                else:
                    skills[new_skill] = int(damage_increase)              
    return skills

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