import discord  # noqa: F401
from random import randint

token_path = "token"
token = ""
try:
    with open(token_path, 'r') as token_file:
        token = token_file.read()
except FileNotFoundError:
    print("Token file not found. Quitting.")
    quit()


client = discord.Client()

authorized_user_ids = [340115550208262145]
responses = {
    "fuck u": ["no, fuck you",
               "fuck you harder",
               "fuck you {0}"],
    "fuck you": ["no, fuck you",
                 "fuck you harder",
                 "fuck you {0}"],
    "mahdi gay": ["i agree"]],
    "Do black lives matter?": ["No"],
    "What is the meaning of life?": ["Error file not found!!!"],
    "Hi": ["Fuck you"],
    "Hello": ["Your existance is trivial."],
    "Why are you gay?": ["Because Mahadi","Don't you have anything vetter to do? "],
    "Whats the time?": ["Time is relative"]
    "Why is Mahadi gay?": ["Result of severe childhood trauma, and years of getting sexually abused by his brother."]
}


@client.event
async def on_message(message):
    print(message.author.id)
    if message.content == "!!shutdown":
        if message.author.id in authorized_user_ids:
            await message.channel.send("Shutting down my lord.")
            quit()
        else:
            await message.channel.send("Fuck off " + message.author.name)

    for trigger, response_list in responses.items():
        if message.content.lower().find(trigger) != -1:
            response = response_list[randint(len(response_list))]
            response = response.format(message.author.name)
            await message.channel.send(response)
            return

client.run(token)
