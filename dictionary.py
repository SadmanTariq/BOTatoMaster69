import discord
from discord.ext import commands
import requests


class Definition:
    word = ""
    pronunciation = ""
    part_of_speech = ""
    definition = ""
    example = ""
    error = False

    def get_embed(self) -> discord.Embed:
        return discord.Embed.from_dict({
            "title": self.word,
            "fields": [{
                        "name": self.part_of_speech +
                        (', ' if self.part_of_speech else '') +
                        self.definition,
                        "value": self.example
                       }]
        })


@commands.command()
async def define(ctx: commands.Context, phrase: str):
    ctx.send(embed=urban(phrase).get_embed())


def urban(phrase: str) -> Definition:
    definition = Definition()

    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

    query = {"term": phrase}

    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "5adea85577msh59b06b5fa5af3bap149422jsnfc9bdd40a2ce"
        }

    request = requests.request("GET", url, headers=headers, params=query)

    try:
        data = request.json()["list"][0]
    except IndexError:
        definition.error = True
        return definition

    definition.word = data["word"]
    definition.definition = data["definition"]
    definition.example = data["example"]

    return definition
