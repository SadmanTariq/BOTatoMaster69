import discord  # noqa: F401
from os import environ

import on_message_commands
import calculator


# The fuck you looking at?


commands_list = [calculator.Calculator,
                 on_message_commands.Dadbot,
                 on_message_commands.Shutdown,
                 on_message_commands.TriggerResponse]


class OnMessageClient(discord.Client):
    async def on_ready(self):
        for command in commands_list:
            command.init()
        print("Ready.")

    async def on_message(self, message):
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

    client = OnMessageClient()
    client.run(token)
