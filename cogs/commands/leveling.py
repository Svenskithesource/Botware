import discord, asyncio, aiosqlite, time, random, io, aiohttp
from discord.ext import commands
from collections import OrderedDict
from discord.ext.commands.core import command
from ..function import MainDef

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['levelreset', 'resetlevel'])
    async def resetlevels(self, ctx):
        author = ctx.author
        if not author.bot:
            async with aiosqlite.connect('./database/main.db') as db:
                c = await db.cursor()
                await c.execute("DELETE FROM leveling WHERE guildID=:id", {"id":ctx.guild.id})
                await db.commit()
        else:
            embed = discord.Embed(description="Robokops are not allowed to reset the database!", colour=0x660000)
            msg = await ctx.send(embed=embed)
        try:
            await msg.delete(delay=8)
            await ctx.message.delete(delay=8)
        except:
            pass


def setup(bot):
    bot.add_cog(Levels(bot))
