import discord  # noqa: F401
from random import randint
from os import environ

token_variable_name = "DISCORD_TOKEN"
token = ""
try:
    token = environ[token_variable_name]
except KeyError:
    print("Token variable not set. Quitting.")
    quit()


client = discord.Client()

authorized_user_ids = [340115550208262145]
bot_user_id = 593359969806712861
responses = {
    "fuck u": ["no, fuck you",
               "fuck you harder",
               "fuck you {0}"],
    "fuck you": ["no, fuck you",
                 "fuck you harder",
                 "fuck you {0}"],
    "mahdi gey": ["i agree"],
    "do black lives matter": ["No"],
    "what is the meaning of life": ["Error file not found!!!"],
    "hi": ["Fuck you"],
    "hello": ["You're existance is trivial"],
    "why are you gay": ["Because Mahadi", "Don't you have anything better to do? "],  # noqa
    "why is mahdi gay": ["Result of severe childhood trauma, and years of getting sexually abused by his brother."],  # noqa
    "mahdi": ["~~mahdi~~ mah**a**di"],
    "dumb bot": [":("]
}


@client.event
async def on_message(message):
    if message.author.id == bot_user_id:
        return

    print(message.author.id)
    if message.content == "!!shutdown":
        if message.author.id in authorized_user_ids:
            await message.channel.send("Shutting down my lord.")
            quit()
        else:
            await message.channel.send("Fuck off " + message.author.name)

    for trigger, response_list in responses.items():
        if message.content.lower().find(trigger) != -1:
            response = response_list[randint(0, len(response_list) - 1)]
            response = response.format(message.author.name)
            print(trigger, response)
            await message.channel.send(response)
            return

client.run(token)
