import discord, asyncio, time, json, aiosqlite
from discord.ext import commands

class MainDef:

    def __init__(self):
        print("functions loaded!")

    async def addMoney(self, memberid, value):
        async with aiosqlite.connect('./database/main.db') as db:
            c = await db.cursor()
            await c.execute("SELECT balance FROM economy WHERE userID=:id", {"id": memberid})
            result = await c.fetchone()
            await c.execute("UPDATE economy SET balance=:money WHERE userID=:id", {"money": int(result[0] + value), "id": memberid})
            await db.commit()

    async def checkAddUser(self, memberid, table, guildid=None):
        async with aiosqlite.connect('./database/main.db') as db:
            c = await db.cursor()
            if guildid == None:
                await c.execute(f"SELECT userID FROM {table} WHERE userID=:id", {"id": memberid})
                result = await c.fetchone()
                if result == None:
                    await c.execute(f"INSERT INTO {table}(userID) VALUES(:id)", {"id": memberid})
            else:
                await c.execute(f"SELECT userID FROM {table} WHERE userID=:id AND guildID=:gid", {"id": memberid, "gid": guildid})
                result = await c.fetchone()
                if result == None:
                    await c.execute(f'INSERT INTO {table}(guildID, userID) VALUES(:gid, :id)', {"gid": guildid, "id": memberid}) 
            await db.commit()

    async def slct(self, select, table, where, id):
        async with aiosqlite.connect('./database/main.db') as db:
            c = await db.cursor()
            try:
                await c.execute(f"SELECT {select} FROM {table} WHERE {where}=:id", {"id": id})
                result = await c.fetchone()
                result = result[0]
                return result
            except:
                return False

    async def setMoney(self, memberid:int, value:int):
        async with aiosqlite.connect('./database/main.db') as db:
            c = await db.cursor()
            await c.execute("UPDATE economy SET balance=:money WHERE userID=:id", {"money": value, "id": memberid})
            await db.commit()

    async def pm(self, ctx):
        if ctx.channel.type is discord.ChannelType.private:
            embed=discord.Embed(description=f"You are not allowed to use this command in pm!", colour=0x660000)
            await ctx.send(embed=embed)
            return True
        return False

    async def downCheck(self, ctx, file):
        with open("./database/down.json", "r") as f:
            downTime = json.load(f)

        if downTime["all"] == "down" or downTime[file] == 'down' or downTime[file] != 'up':        
            embed = discord.Embed(description=f"Sorry but **{file.title()}** is in maintenance.", colour=0x660000)
            await ctx.send(embed=embed)
            return True