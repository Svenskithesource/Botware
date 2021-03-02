import discord, aiosqlite, random, time, sys
from discord.ext import commands
from discord.utils import get
from ..function import MainDef


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if message.channel.type is not discord.ChannelType.private:
            if not message.author.bot:
                await MainDef.checkAddUser(self, memberid=message.author.id, table="leveling", guildid=message.guild.id)
                async with aiosqlite.connect("./database/main.db") as db:
                    c = await db.cursor()
                    await c.execute("SELECT lvl FROM leveling WHERE userID=:id AND guildID=:gid", {"id": author.id, "gid": message.guild.id})
                    lvl = await c.fetchone()
                    await c.execute("SELECT exp FROM leveling WHERE userID=:id AND guildID=:gid", {"id": author.id, "gid": message.guild.id})
                    exp = await c.fetchone()
                    await c.execute("SELECT cooldown FROM leveling WHERE userID=:id AND guildID=:gid", {"id": author.id, "gid": message.guild.id})
                    cooldown = await c.fetchone()
                    exp_r = random.randint(1, 3)
                    curr_time = time.time()
                    delta = float(curr_time) - float(cooldown[0])
                    if delta >= 0 and delta > 0:
                        await c.execute('UPDATE leveling SET exp=:val WHERE userID=:id AND guildID=:gid', {'val': exp[0] + exp_r, 'id': author.id, "gid": message.guild.id})
                        await c.execute('UPDATE leveling SET cooldown=:val WHERE userID=:id AND guildID=:gid', {"val": curr_time, 'id': author.id, "gid": message.guild.id})
                        await db.commit()
                        await c.execute("SELECT exp FROM leveling WHERE userID=:id AND guildID=:gid", {'id': author.id, "gid": message.guild.id})
                        exp = await c.fetchone()
                    else:
                        return
                    lvlEnd = round(((lvl[0] + 1) ** 2) * 6)
                    if exp[0] >= lvlEnd:
                        await c.execute('UPDATE leveling SET lvl=:val WHERE userID=:id AND guildID=:gid', {"val": lvl[0] + 1, "id": author.id, "gid": message.guild.id})
                        await c.execute('UPDATE leveling SET exp=:val WHERE userID=:id AND guildID=:gid', {"val": 0, "id": author.id, "gid": message.guild.id})
                        await db.commit()
                        await message.channel.send(f"{message.author.mention} has leveled up to level {lvl[0] + 1}!")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        return
        async with aiosqlite.connect('./database/main.db') as users:
            c = await users.cursor()

            await c.execute("SELECT guildID FROM welcome WHERE guildID=:id", {'id': member.guild.id})
            guildID = await c.fetchone()
            await c.execute("SELECT chatID FROM welcome WHERE guildID=:id", {'id': member.guild.id})
            chatID = await c.fetchone()
            await c.execute("SELECT sett FROM welcome WHERE guildID=:id", {'id': member.guild.id})
            swich = await c.fetchone()
            
            await c.execute("SELECT guildID FROM roleguild WHERE guildID=:id", {'id': member.guild.id})
            role_guildID = await c.fetchone()
            await c.execute("SELECT roleID FROM roleguild WHERE guildID=:id", {'id': member.guild.id})
            role_choice = await c.fetchone()
            await c.execute("SELECT sett FROM roleguild WHERE guildID=:id", {"id": member.guild.id})
            role_swich = await c.fetchone()

            #Welcome messages
            if guildID != None:
                if swich[0] == 0:
                    pass
                elif swich[0] == 1:
                    
                    try:
                        channel = self.bot.get_channel(id=chatID[0])
                        await channel.send(f'Hello **{member.mention}**, welcome to **{member.guild.name}**. Have fun! :partying_face:')
                    except:
                        await c.execute('UPDATE logs SET log=:val WHERE guildID=:id', {'val': 0, 'id': member.guild.id})
                        await users.commit()
            
            #Auto-Role
            if role_guildID !=  None:
                if role_swich[0] == 0:
                    pass
                elif role_swich[0] == 1:

                    try:
                        result = role_choice[0]
                        role = get(member.guild.roles, id = result)
                        await member.add_roles(role)
                    except:
                        await c.execute("UPDATE roleguild SET sett=:val WHERE guildID=:id", {"val": 0, 'id': member.guild.id})
                        await users.commit()


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async with aiosqlite.connect('./database/main.db') as users:
            cursor = await users.cursor()
            
            await cursor.execute(f"SELECT guildID FROM setguild WHERE guildID=:guildid", {"guildid": guild.id})
            result = await cursor.fetchone()

            if result == None:
                await cursor.execute('INSERT INTO setguild(guildID) VALUES(:guildid)', {"guildid": guild.id})
            
            await users.commit()


def setup(bot):
    bot.add_cog(Events(bot))
