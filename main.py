import discord  # noqa: F401
from random import randint
from os import environ
import json

token_variable_name = "DISCORD_TOKEN"
token = ""
try:
    token = environ[token_variable_name]
except KeyError:
    print("Token variable not set. Quitting.")
    quit()


client = discord.Client()

authorized_user_ids = [340115550208262145]

responses_json_path = "responses.json"
responses = {}

try:
    with open(responses_json_path) as responses_json:
        responses = json.load(responses_json)
        print("Responses loaded.")
except FileNotFoundError:
    print(responses_json_path + "does not exist. Quitting.")
    quit()


@client.event
async def on_ready():
    print("Ready.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

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

    # DadBot clone:
    if message.content.lower().startswith("i am"):
        response = [message.content[i] for i in range(4, len(message.content))]
        response = "".join(response)
        await message.channel.send("Hi" + response)

client.run(token)
