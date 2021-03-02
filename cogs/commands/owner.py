import discord, aiosqlite, typing, asyncio
from discord.ext import commands
from ..function import MainDef


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases = ['sl'])
    async def setlevel(self, ctx, member:typing.Optional[discord.Member], exp:int=None, level:int=None):
        member = member or ctx.author
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            await MainDef.setExpLevel(self, guildid=int(ctx.guild.id),memberid=int(member.id), exp_i=exp, level_i=level)
            if exp == None:
                await ctx.send(f"{member.name}'s level has being set to {level}!")
            if level == None:
                await ctx.send(f"{member.name}'s exp has being set to {exp}!")
            else:
                await ctx.send(f"{member.name}'s level has being set to {level} and his exp to {exp}!")
        else:
            msg = await ctx.send("You can't use that...")
            await asyncio.sleep(2.5)
            await msg.delete()

    @commands.command(aliases = ['gm'])
    async def givemoney(self, ctx, member:typing.Optional[discord.Member], value:int):
        member = member or ctx.author
        await MainDef.checkAddUser(self, memberid=member.id, table="economy")
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            await MainDef.addMoney(self, memberid=member.id, value=value)
            await ctx.send(f"**{member}**, we added **{value}$** to your account")
        else:
            msg = await ctx.send("You can't use that...")
            await asyncio.sleep(2.5)
            await msg.delete()

    @commands.command(aliases=['sm'])
    async def setmoney(self, ctx, member:typing.Optional[discord.Member], value:int):
        member = member or ctx.author
        await MainDef.checkAddUser(self, memberid=member.id, table="economy")
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            await MainDef.setMoney(self,memberid=member.id, value=value)
            await ctx.send(f"**{member}**'s money was set to **{value}$**")
        else:
            msg = await ctx.send("You can't use that...")
            await asyncio.sleep(2.5)
            await msg.delete()

    @commands.command(aliases=['cl'])
    async def cooldown(self, ctx, member:discord.Member = None):
        member = member or ctx.author
        await MainDef.checkAddUser(self, memberid=member.id, table="economy") 
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            async with aiosqlite.connect('./database/main.db') as users:
                cursor = await users.cursor()
                await ctx.send(f"**{member.name}** cooldowns was set to **0**")
                await cursor.execute("UPDATE economy SET dailycd=:cd WHERE userID=:id", {"cd": 0, "id": member.id})
                #await cursor.execute("UPDATE economy SET jobcd=:cd WHERE userID=:id", {"cd": 0, "id": member.id})
                #await cursor.execute("UPDATE economy SET repcd=:cd WHERE userID=:id", {"cd": 0, "id": member.id})
                await users.commit()
        else:
            msg = await ctx.send("You can't use that...")
            await asyncio.sleep(2.5)
            await msg.delete()

    @commands.command(aliases=['pr'])
    async def premium(self, ctx, member:typing.Optional[discord.Member], value:int):
        member = member or ctx.author
        await MainDef.checkAddUser(self, memberid=member.id, table="users")
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            async with aiosqlite.connect('./database/main.db') as users:
                cursor = await users.cursor()
                if value == 0:
                    await ctx.send(f"**{member.name}**'s premium got removed!")

                    await cursor.execute("UPDATE users SET premium=:pr WHERE userID=:id", {"pr": value, "id": member.id})
                    await users.commit()
                elif value == 1:
                    await ctx.send(f"**{member.name}** got premium!")
                    await cursor.execute("UPDATE users SET premium=:pr WHERE userID=:id", {"pr": value, "id": member.id})
                    await users.commit()
                else:
                    await ctx.send(f"0 - NoPremium | 1 - Premium")
        else:
            msg = await ctx.send("You can't use that...")
            await asyncio.sleep(2.5)
            await msg.delete()

    @commands.command(aliases=['sr', 'setrep'])
    async def setreps(self, ctx, member:typing.Optional[discord.Member], value:int):
        member = member or ctx.author
        await MainDef.checkAddUser(self, memberid=member.id, table="bank")
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            async with aiosqlite.connect('./database/main.db') as users:
                cursor = await users.cursor()
                await cursor.execute("UPDATE bank SET rep=:r WHERE userID=:id", {"r": value, "id": member.id})
                await users.commit()
                await ctx.send(f"**{member}**'s reps was set to **{value}$**")
        else:
            msg = await ctx.send("You can't use that...")
            await asyncio.sleep(2.5)
            await msg.delete()
    
    @commands.command()
    async def error(self, ctx, error_code:int):
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            async with aiosqlite.connect("./database/errors.db") as errors_db:
                c = await errors_db.cursor()
                await c.execute("SELECT userID FROM errors WHERE errorCode=:ec", {"ec": error_code})
                user = c.fetchone()
                await c.execute("SELECT error FROM errors WHERE errorCode=:ec", {"ec": error_code})
                error = c.fetchone()
                try:
                    if error[0]==None:
                        await ctx.send("Error code not found")
                        return
                except:
                    await ctx.send("Error code not found")
                    return
                await ctx.send(f"Error:\n```{error[0]}```\ncaused by: {user[0]}")


def setup(bot):
    bot.add_cog(Owner(bot))