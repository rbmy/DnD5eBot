import os
import discord
import requests
import json

disc_token = os.environ['TOKEN']
client = discord.Client()

### D&D 5e Api ###
spellsQuery = "https://www.dnd5eapi.co/api/spells/"
monsterQuery = "https://www.dnd5eapi.co/api/monsters/"
abilityQuery = "https://www.dnd5eapi.co/api/ability-scores/"
skillsQuery = "https://www.dnd5eapi.co/api/skills/"
proficienciesQuery = "https://www.dnd5eapi.co/api/proficiencies/"
languageQuery = "https://www.dnd5eapi.co/api/languages/"



def get_spells(spellName):
    response = requests.get(spellsQuery + spellName)
    return format_response(response)


def get_monster(monsterName):
    response = requests.get(monsterQuery + monsterName)
    return format_response(response)

def get_abilities(abilityName):
    response = requests.get(abilityQuery + abilityName)
    return format_response(response)

def get_skills(skillName):
    response = requests.get(skillsQuery + skillName)
    return format_response(response)

def get_proficiencies(proficiencyName):
    response = requests.get(proficienciesQuery + proficiencyName)
    return format_response(response)

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('5eBot'):
        print("User requests: " + message.content)
        botRequest = message.content.split()

        if (len(botRequest) == 5 and botRequest[1].lower() == "what"
                and botRequest[2].lower() == "is"
                and botRequest[4].lower() != ""):
            apiResponse = ""

            if botRequest[3].lower() == "spell":
                print("Searching for spell: " + botRequest[4])
                apiResponse = get_spells(botRequest[4])

            if botRequest[3].lower() == "monster":
                print("Searching for monster: " + botRequest[4])
                apiResponse = get_monster(botRequest[4])

            if len(apiResponse) > 0:
                if len(apiResponse) > 2000:
                    chucks = [
                        apiResponse[i:i + 2000]
                        for i in range(0, len(apiResponse), 2000)
                    ]
                    for chuck in chucks:
                        await message.channel.send(str(chuck))
                else:
                    await message.channel.send(str(apiResponse))

        else:
            await message.channel.send(
                "Unable to determine your request. Try again.")


client.run(disc_token)
