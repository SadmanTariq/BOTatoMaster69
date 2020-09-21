from asyncio import sleep
import json
from random import randrange
from math import exp
import discord.errors


class OnMessageCommands():
    """Placeholder class for all command classes that respond to the
    content in a message"""

    @classmethod
    def init(cls):
        pass

    @classmethod
    def on_call(cls, message):
        print(f"{cls.__name__}, {message.author.name}: {message.content}")

    @classmethod
    def exec_check(cls, parameter_list):
        raise NotImplementedError

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)
        raise NotImplementedError


class Dadbot(OnMessageCommands):
    """If message is some variation of 'I am ...' then respond with
    'Hi, ...'."""

    starter_variations = ["i am ", "i'm ", "im ", "i m "]

    @classmethod
    def _prepare_response(cls, text):
        text = text.lower()

        for starter in cls.starter_variations:
            if text.startswith(starter):
                starterless = text[len(starter):]  # After Starter to end
                response = "Hi, " + starterless
                return response, starterless

        return None

    @classmethod
    def exec_check(cls, message):
        for starter in cls.starter_variations:
            if message.content.lower().startswith(starter):
                return True
        return False

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)
        response, new_name = cls._prepare_response(message.content)

        if response is not None:
            await message.channel.send(response)

        if new_name is not None:
            try:
                await message.author.edit(nick=new_name)
            except discord.errors.Forbidden:
                print("Missing nick permissions.")


class Shutdown(OnMessageCommands):
    """Quit the program when an authorised user types '!!shutdown'"""

    _authorized_user_ids = [340115550208262145]

    @classmethod
    def exec_check(cls, message):
        if message.content == "!!shutdown":
            return True
        else:
            return False

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)
        if message.author.id in cls._authorized_user_ids:
            await message.channel.send("Shutting down my lord.")
            quit()
        else:
            await message.channel.send("Fuck off " + message.author.name)


class TriggerResponse(OnMessageCommands):
    """If a message contains a trigger from responses.json then reply
    with a randomly selected response for that trigger."""

    _responses = None

    @classmethod
    def init(cls):
        responses_json_path = "responses.json"
        try:
            with open(responses_json_path) as responses_json:
                cls._responses = json.load(responses_json)
                print("Responses loaded.")
        except FileNotFoundError:
            print(responses_json_path + "does not exist. Quitting.")
            quit()

    @classmethod
    def exec_check(cls, message):
        for trigger, _ in cls._responses.items():
            if message.content.lower().find(trigger) != -1:
                return True
        return False

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)
        for trigger, response_list in cls._responses.items():
            if message.content.lower().find(trigger) != -1:
                response = response_list[randrange(len(response_list))]
                response = response.format(message.author.name)
                print(f"Trigger: {trigger}, response: {response}")
                await message.channel.send(response)
                return


class RandomPing(OnMessageCommands):
    """Ping a random user on @someone"""

    # @classmethod
    # def init(cls):
    #     pass

    @classmethod
    def exec_check(cls, message):
        if message.content == "@someone":
            return True
        else:
            return False

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)
        if randrange(10) < 3:  # 30% chance
            await cls.on_success(message)
        else:
            await cls.on_fail(message)

    @classmethod
    async def on_success(cls, message):
        members = message.guild.members
        iters = 4

        random_member = lambda m: m[randrange(len(members))]  # noqa: E731
        duration = lambda i: exp(float(i) / 3.0) * 0.01  # noqa: E731

        shuffling_message = await message.channel.send(random_member(members).name)  # noqa
        for i in range(iters):
            await sleep(duration(i))
            await shuffling_message.edit(content=random_member(members).name)

        await shuffling_message.delete()
        await message.channel.send(random_member(members).mention)

    @classmethod
    async def on_fail(cls, message):
        try:
            await message.delete()
        except discord.errors.Forbidden:
            response = await message.channel.send("No spam 😠.\nAlso mods pls give me Manage Messages permissions so that I can auto delete these.")  # noqa: E501
            await response.delete(delay=5)
        else:
            response = await message.channel.send("No spam 😠.")
            await response.delete(delay=5)
