from discord import Member
from discord.ext import commands
from discord import errors
from random import randrange


@commands.command()
async def vote(ctx: commands.Context, member: Member):
    print("Vote " + ctx.author.name + ": " + ctx.message.content)
    try:
        await ctx.message.delete()
    except errors.Forbidden:
        print("No manage messages perms.")
    decision_line = f"{member.mention} was {'Not' if randrange(1) == 1 else ''} The Impostor."
    response_text = (f"*{ctx.author.mention} has voted.*\n" +
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
