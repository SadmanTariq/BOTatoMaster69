# import discord
from discord.ext import commands
from os import environ

import on_message_commands
import calculator
import jokes
import dictionary
import vote_command

# The fuck you looking at? Im looking at ur mum


commands_list = [jokes.Jokes,
                 calculator.Calculator,
                 on_message_commands.MahdiOk,
                 on_message_commands.Dadbot,
                 on_message_commands.Shutdown,
                 on_message_commands.RandomPing,
                 on_message_commands.TriggerResponse,
                 on_message_commands.TashfinReadRoW]
#                 on_message_commands.RikthPlayHollowKnight]


class Client(commands.Bot):
    async def on_ready(self):
        for command in commands_list:
            command.init()
        print("Ready.")

    async def on_message(self, message):
        await commands.Bot.on_message(self, message)

        for command in self.commands:
            if message.content.startswith(self.command_prefix + command.name):
                return

        if message.author == client.user:
            return

        for command in commands_list:
            if command.exec_check(message):
                await command.respond(message)
                return


if __name__ == "__main__":
    TOKEN_VARIABLE_NAME = "DISCORD_TOKEN"
    token = ""
    try:
        token = environ[TOKEN_VARIABLE_NAME]
    except KeyError:
        print("Token variable not set. Quitting.")
        quit()

    client = Client(command_prefix='>')
    client.add_command(dictionary.define)
    client.add_command(vote_command.vote)
    client.run(token)
