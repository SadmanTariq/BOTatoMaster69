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
            "title": self.word.capitalize(),
            "fields": [{
                        "name": self.part_of_speech +
                        (', ' if self.part_of_speech else '')
                        "value": f"{self.definition}\n*{self.example}*" 
                       }]
        })


@commands.command()
async def define(ctx: commands.Context, *args):
    print(ctx.author.name + ": " + ctx.message.content)

    definition = urban(" ".join(args))
    if definition.error:
        await ctx.send("wtf even is that")
    else:
        await ctx.send(embed=definition.get_embed())

define.description = "Gets the definition of your requested word from the most reputable dictionary on the internet, Urban Dictionary."
define.brief = "Search for the definition of a word or a phrase."


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

    def remove_brackets(string: str) -> str:
        return string.replace('[', '').replace(']', '').replace('{', '').replace('}', '')  # noqa

    definition.word = remove_brackets(data["word"])
    definition.definition = remove_brackets(data["definition"])
    if len(definition.definition) > 256:
        definition.definition = definition.definition[:253] + "..."
    definition.example = remove_brackets(data["example"])

    return definition
