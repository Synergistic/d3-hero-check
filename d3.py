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
 
def retrieveItem(item_id):
    url = 'http://' + region + '.battle.net/api/d3/data/' + item_id
    response = urllib2.urlopen(url)
    json_item = json.load(response)
    return json_item
    
def checkHeroes(characters):
    global possible_options
    print '\n'
    for c in characters:
        d = retrieveHero(characters[c])
        print d['name'], 'level', d['level'], d['class']
        possible_options.append(d['name'])
    print '\n'

def checkGear(hero):
    c = retrieveHero(hero)
    fire, cold, lightning, holy, poison, physical = 0, 0, 0, 0, 0, 0
    skills = {}
    gearset = c['items']
    for slot in gearset:
        i = retrieveItem(gearset[slot]['tooltipParams'])
        for att in i['attributes']['primary']:
            text_line = att['text']
            type = text_line.split(' ')
            if type[0] == 'Fire': 
                fire += int(type[3].split('%')[0])
            elif type[0] == 'Cold':
                cold += int(type[3].split('%')[0])
            elif type[0] == 'Holy':
                holy += int(type[3].split('%')[0])
            elif type[0] == 'Poison': 
                poison += int(type[3].split('%')[0])
            elif type[0] == 'Physical':
                physical += int(type[3].split('%')[0])
            elif type[0] == 'Lightning':
                lightning += int(type[3].split('%')[0])
            
            elif 'Increases' in type and 'Damage' in type:
                new_skill = ''.join(type[1:type.index('Damage')])
                damage_loc = text_line.index('%')
                damage_increase = text_line[damage_loc-2:damage_loc].strip(' ')
                if new_skill in skills:
                    skills[new_skill] += int(damage_increase)
                else:
                    skills[new_skill] = int(damage_increase)              
   
    print 'Fire Damage: ' + str(fire)
    print 'Cold Damage: ' + str(cold)
    print 'Holy Damage: ' + str(holy)
    print 'Poison Damage: ' + str(poison)
    print 'Physical Damage: ' + str(physical)
    print 'Lightning Damage: ' + str(lightning)
    for skill in skills:
        print skill + ' Damage: ' + str(skills[skill])
        
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
    possible_options = []
    checkHeroes(d3_characters)
    selected_char = raw_input('Enter the name of desired character: ')
    if selected_char == 'exit' or selected_char == 'quit':
        sys.exit()
    if selected_char in possible_options:
    #checkSkills(d3_characters[selected_char.capitalize()])
        checkGear(d3_characters[selected_char])
    else:
        print 'Try again.'