import os
import dnd
import discord

disc_token = os.environ['TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!dnd'):
        print("User requests: " + message.content)
        botRequest = message.content.split()

        if (len(botRequest) == 5 and botRequest[1].lower() == "what"
                and botRequest[2].lower() == "is"
                and botRequest[4].lower() != ""):
            apiResponse = ""

            if botRequest[3].lower() == "spell":
                print("Searching for spell: " + botRequest[4])
                apiResponse = dnd.get_spells(botRequest[4])

            if botRequest[3].lower() == "monster":
                print("Searching for monster: " + botRequest[4])
                apiResponse = dnd.get_monster(botRequest[4])

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
