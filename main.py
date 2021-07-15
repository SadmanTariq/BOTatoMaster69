import discord
from discord.ext import commands

from database import db

import on_message_commands
import calculator
import jokes
import dictionary
import vote_command
import trigger_response


COMMANDS = [
    trigger_response.ReloadTriggers,
    jokes.Jokes,
    calculator.Calculator,
    on_message_commands.Dadbot,
    on_message_commands.Shutdown,
    on_message_commands.RandomPing,
    on_message_commands.TtTest,
    trigger_response.TriggerResponse
]


class Client(commands.Bot):
    async def on_ready(self):
        for command in COMMANDS:
            command.init()
        print("Ready.")

    async def on_message(self, message):
        await commands.Bot.on_message(self, message)

        for command in self.commands:
            if message.content.startswith(self.command_prefix + command.name):
                return

        # Dont respond if sender is a bot account.
        if message.author.bot:
            return

        for command in COMMANDS:
            if command.exec_check(message):
                await command.respond(message)
                return


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True

    client = Client(command_prefix='>', intents=intents)
    client.add_command(dictionary.define)
    client.add_command(vote_command.vote)
    client.run(db.get_api_key('Discord'))
