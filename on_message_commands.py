import json
from random import randint


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
                response = text[len(starter):]  # After Starter to end
                response = "Hi, " + response
                return response

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
        response = cls._prepare_response(message.content)

        if response is not None:
            await message.channel.send(response)


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
                response = response_list[randint(0, len(response_list) - 1)]
                response = response.format(message.author.name)
                print(f"Trigger: {trigger}, response: {response}")
                await message.channel.send(response)
                return
