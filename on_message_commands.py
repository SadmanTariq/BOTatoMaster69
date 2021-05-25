from asyncio import sleep
import json
from random import randrange, randint
from math import exp
import discord.errors
import string


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

        if randrange(10) < 5:  # 5 in 10
            await message.channel.send("No you're not.")
            return

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


class MahdiOk(OnMessageCommands):
    """ Responds to when Mahdi says ok """

#     @classmethod
#     def init(cls):
#         pass

#     @classmethod
#     def on_call(cls, message):
#         print(f"{cls.__name__}, {message.author.name}: {message.content}")

    @classmethod
    def exec_check(cls, message):
        return message.content.lower().strip() == "ok"

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)
        MAHDI_ID = 396236347171667970
        if message.author.id == MAHDI_ID:
            # print("Responded")
            await message.channel.send("Yes we get it you exist")


class RikthPlayHollowKnight(OnMessageCommands):
    """Rikth play Hollow Knight 😤"""
    RIKTH_ID = 190756291558375424

    @classmethod
    def exec_check(cls, message):
        return message.author.id == cls.RIKTH_ID and randrange(10) < 2

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)
        await message.channel.send("Rikth play Hollow Knight 😤")

class TashfinReadRoW(OnMessageCommands):
    """Tashfin read RoW 😤😠😡"""
    TASHFIN_ID = 232798874652246016

    @classmethod
    def exec_check(cls, message):
        return message.author.id == cls.TASHFIN_ID and randrange(10) < 1

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)
        await message.channel.send("Tashfin read RoW 😤😠😡")

class TtTest(OnMessageCommands):
    """If the message is some variation of tt, tTtT, t etc. then send ttt and delete the original message after 5 seconds."""

    @classmethod
    def exec_check(cls, message):
        stripped = ''
        for c in message.content.lower().strip():
            if c not in string.punctuation + string.whitespace:
                stripped += c

        if stripped == '':
            return False

        for c in stripped:
            if c not in 't':
                return False

        return True

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)

        await message.delete(delay=5)
        resp = await message.channel.send('t' * (2000 if len(message.content) * 2 > 2000 else len(message.content) * 2))
        await resp.delete(delay=5)

###class TashfinDontForgetLaptop(OnMessageCommands):
    ###"""Tashfin DONT FUCKING FORGET LAPTOP 😤😤😤😤😤😤😤😤😤"""
    ###TASHFIN_ID = 232798874652246016

    ###@classmethod
    ###def exec_check(cls, message):
        ###return message.author.id == cls.TASHFIN_ID

   ###@classmethod
    ###async def respond(cls, message):
        ###cls.on_call(message)
        ###await message.channel.send("Tashfin DONT FUCKING FORGET LAPTOP 😤😤😤😤😤😤😤😤😤")
