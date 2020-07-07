from asyncio import sleep
import requests
from on_message_commands import OnMessageCommands
from random import randrange


class Jokes(OnMessageCommands):
    """Respond with a joke on 'Tell me a joke'"""

    # @classmethod
    # def init(cls):
    #     pass

    @classmethod
    def exec_check(cls, message: str) -> bool:
        if message.content.lower().find("tell me a joke") == -1:
            return False
        else:
            return True

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)

        joke_methods = [cls.joke_api, cls.icanhazdadjoke]

        await joke_methods[randrange(len(joke_methods))](message.channel)

    @classmethod
    async def joke_api(cls, channel):
        r = requests.get("https://sv443.net/jokeapi/v2/joke/Any")
        data = r.json()
        if data["error"]:
            return

        print(f"JokeAPI {data['id']}")

        if data["type"] == "single":
            await channel.send(data["joke"])
        else:
            await channel.send(data["setup"])
            await sleep(1)
            await channel.send(data["delivery"])

    @classmethod
    async def icanhazdadjoke(cls, channel):
        headers = {
            "User-Agent": "BOTatomaster69" +
            " (https://github.com/SadmanTariq/BOTatoMaster69)",
            "Accept": "application/json"
        }

        url = "https://icanhazdadjoke.com"

        r = requests.get(url, headers=headers)
        data = r.json()
        print(f"icanhazdadjoke {data['id']}")

        await channel.send(data["joke"])
