from discord import Member
from discord.ext import commands
from random import randrange


@commands.command()
async def vote(ctx: commands.Context, member: Member):
    await ctx.message.delete()
    decision_line = f"{member.nick} was {'Not' if randrange(1) == 1 else ''} The Impostor."
    response_text = (f"*{ctx.author.nick} has voted.*\n" +
                     ".      　。　　　　•　    　ﾟ　　。\n" +
                     "　　.　　　.　　　  　　.　　　　　。　　   。　.\n" +
                     " 　.　　      。　        ඞ   。　    .    •\n" +
                     f" •          {decision_line}　 。　.\n" +
                     "　 　　。　　　　　　ﾟ　　　.　　　　　.\n" +
                     ",　　　　.　 .　　       .               。\n")
    await ctx.send(response_text)


@vote.error
async def vote_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Who the fuck is that?")


vote.description = "Vote to kick someone off."
vote.brief = "Vote to kick someone off."
