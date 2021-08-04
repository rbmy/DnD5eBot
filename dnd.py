import requests
import json
import DnD5eAPIUrls

### Get Character Data ###
def get_abilities(abilityName):
    response = requests.get(DnD5eAPIUrls.abilityQuery + abilityName)
    return format_response(response)

def get_skills(skillName):
    response = requests.get(DnD5eAPIUrls.skillsQuery + skillName)
    return format_response(response)

def get_proficiencies(proficiencyName):
    response = requests.get(DnD5eAPIUrls.proficienciesQuery + proficiencyName)
    return format_response(response)

def get_languages(languageName):
    response = requests.get(DnD5eAPIUrls.languagesQuery + languageName)
    return format_response(response)

### Get Spells Data ###
def get_spells(spellName):
    response = requests.get(DnD5eAPIUrls.spellsQuery + spellName)
    return format_response(response)

### Get Monsters Data ###
def get_monster(monsterName):
    response = requests.get(DnD5eAPIUrls.monsterQuery + monsterName)
    return format_response(response)

## Helper Functions ###
def format_response(response):
    json_content = json.loads(response.text)
    textReturned = ""
    for key in json_content:
        if key.lower() == "index":
            continue
        value = json_content[key]
        print(key)
        if type(value) is dict:
            format_dict(key, json_content, textReturned)
        if type(value) is list:
            if type(value[0]) is dict:
              for list_val in value: #dictionary
                print(list_val)
                for dicts in list_val:
                  format_dict(dicts, list_val, textReturned)
            textReturned += "**{0}**: {1}\n".format(key, "".join(value))
        if type(value) is str:
            textReturned += "**{0}**: {1}\n".format(key, value)
    return textReturned

def format_dict(key, json_content, textReturned):
    print("formating dict...")
    print(key)
    print(json_content)
    textReturned += "**{0}**:\n".format(key)
    for dict_key in json_content[key]:
        if dict_key.lower() == "index" or dict_key.lower() == "url":
            continue
        textReturned += "> **{0}**: {1}\n".format(
            dict_key, json_content[key][dict_key])