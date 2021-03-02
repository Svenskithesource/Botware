import discord, asyncio, aiosqlite
from discord.ext import commands
from discord.utils import get

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def logs(self, ctx, channel:discord.TextChannel = None):
        async with aiosqlite.connect('./database/main.db') as users:
            cursor = await users.cursor()
        
            if channel != None:

                await cursor.execute("SELECT guildID FROM logs WHERE guildID=:id", {'id': ctx.guild.id})
                guildID = await cursor.fetchone()
                await cursor.execute("SELECT chatID FROM logs WHERE guildID=:id", {'id': ctx.guild.id})
                chatID = await cursor.fetchone()
                await cursor.execute("SELECT log FROM logs WHERE guildID=:id", {'id': ctx.guild.id})
                log = await cursor.fetchone()

                if guildID == None:
                    await cursor.execute('INSERT INTO logs(guildID) VALUES(:id)', {"id": ctx.guild.id})
                    await users.commit()
                    await cursor.execute("SELECT guildID FROM logs WHERE guildID=:id", {'id':ctx.guild.id})
                    guildID = await cursor.fetchone()

                if log == None:
                    await cursor.execute('UPDATE logs SET log=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                    await users.commit()
                    await cursor.execute("SELECT log FROM logs WHERE guildID=:id", {'id': ctx.guild.id})
                    log = await cursor.fetchone()
                
                if log[0] == 0:
                    
                    await cursor.execute('UPDATE logs SET chatID=:val WHERE guildID=:id', {'val':channel.id, 'id': ctx.guild.id})
                    await cursor.execute('UPDATE logs SET log=:val WHERE guildID=:id', {'val': 1, 'id': ctx.guild.id})
                    embed = discord.Embed(description = f"Logs are set to **#{channel}**", colour = 0x0033cc)
                    await ctx.send(embed=embed)
                
                elif log[0] == 1:

                    embed = discord.Embed(description = f"Logs are already on <#{chatID[0]}>, type **]log off** to turn it off", colour = 0x660000)
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description = f'You need to choose a **#channel**', colour = 0x660000)
                await ctx.send(embed=embed)
            
            await users.commit()

    @logs.command()
    @commands.has_permissions(manage_channels=True)
    async def off(self, ctx):
        async with aiosqlite.connect('./database/main.db') as users:
            cursor = await users.cursor()
            
            await cursor.execute("SELECT guildID FROM logs WHERE guildID=:id", {'id': ctx.guild.id})
            guildID = await cursor.fetchone()
            await cursor.execute("SELECT log FROM logs WHERE guildID=:id", {'id': ctx.guild.id})
            log = await cursor.fetchone()

            if guildID == None:
                embed = discord.Embed(description = f"Logs are already off, enable them using **]logs #channel**", colour = 0x660000)
                await ctx.send(embed=embed)
                return
            
            if log == None:
                await cursor.execute('UPDATE logs SET log=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                await users.commit()
                await cursor.execute("SELECT log FROM logs WHERE guildID=:id", {'id': ctx.guild.id})
                log = await cursor.fetchone()

            if log[0] == 1:

                await cursor.execute('UPDATE logs SET log=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                await users.commit()
                embed = discord.Embed(description = 'Logs are now **OFF**', colour = discord.Colour.blue())
                await ctx.send(embed=embed)

            elif log[0] == 0:

                embed = discord.Embed(description = 'Logs are already off, enable them using **]logs #channel**', colour = 0x660000)
                await ctx.send(embed=embed)
                

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def welcome(self, ctx, channel:discord.TextChannel=None):
        async with aiosqlite.connect('./database/main.db') as users:
            c = await users.cursor()

            if channel != None:
                
                await c.execute("SELECT guildID FROM welcome WHERE guildID=:id", {"id": ctx.guild.id})
                guildID = await c.fetchone()
                await c.execute("SELECT chatID FROM welcome WHERE guildID=:id", {"id": ctx.guild.id})
                chatID = await c.fetchone()
                await c.execute("SELECT sett FROM welcome WHERE guildID=:id", {"id": ctx.guild.id})
                set_swich = await c.fetchone()

                if guildID == None:
                    await c.execute('INSERT INTO welcome(guildID) VALUES(:id)', {"id": ctx.guild.id})
                    await users.commit()
                    await c.execute("SELECT guildID FROM welcome WHERE guildID=:id", {'id':ctx.guild.id})
                    guildID = await c.fetchone()
                
                if set_swich == None:
                    await c.execute('UPDATE welcome SET sett=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                    await users.commit()
                    await c.execute("SELECT sett FROM welcome WHERE guildID=:id", {"id": ctx.guild.id})
                    set_swich = await c.fetchone()
                
                if set_swich[0] == 0:

                    await c.execute('UPDATE welcome SET chatID=:val WHERE guildID=:id', {'val': channel.id, 'id': ctx.guild.id})
                    await c.execute('UPDATE welcome SET sett=:val WHERE guildID=:id', {'val': 1, 'id': ctx.guild.id})
                    await users.commit()

                    embed = discord.Embed(title=None, description = f"Channel set to **#{channel}**", colour = discord.Colour.blue())
                    await ctx.send(embed=embed)

                elif set_swich[0] == 1:

                    embed = discord.Embed(description = f"Welcome messages are already enabled on <#{chatID[0]}>, type **]welcome off**", colour = 0x660000)
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title=None, description="You need to specify a **#channel**", colour = 0x660000)
                await ctx.send(embed=embed)

    @welcome.command(aliases=['off', 'OFF'])
    @commands.has_permissions(manage_channels=True)
    async def _off(self, ctx):
        async with aiosqlite.connect('./database/main.db') as users:
            cursor = await users.cursor()
            
            await cursor.execute("SELECT guildID FROM welcome WHERE guildID=:id", {'id':ctx.guild.id})
            guildID = await cursor.fetchone()
            await cursor.execute("SELECT sett FROM welcome WHERE guildID=:id", {'id': ctx.guild.id})
            set_swich = await cursor.fetchone()

            if guildID == None:
                embed = discord.Embed(description = f"Welcome messages are already off, enable them using **]welcome #channel <msg>**", colour = 0x660000)
                await ctx.send(embed=embed)
                return
            
            if set_swich == None:
                await cursor.execute('UPDATE welcome SET sett=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                await users.commit()
                await cursor.execute("SELECT sett FROM welcome WHERE guildID=:id", {'id': ctx.guild.id})
                set_swich = await cursor.fetchone()

            if set_swich[0] == 1:

                await cursor.execute('UPDATE welcome SET sett=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                await users.commit()
                embed = discord.Embed(description = 'Welcome messages are now **OFF**', colour = discord.Colour.blue())
                await ctx.send(embed=embed)

            elif set_swich[0] == 0:

                embed = discord.Embed(description = 'Welcome messages are already off, enable them using **]welcome #channel <msg>**', colour = 0x660000)
                await ctx.send(embed=embed)


    @commands.group(invoke_without_command=True,aliases = ['auto-role'])
    @commands.has_permissions(manage_channels=True)
    async def autorole(self, ctx, role:discord.Role=None):
        async with aiosqlite.connect('./database/main.db') as users:
            c = await users.cursor()


            if role != None:
                
                await c.execute("SELECT guildID FROM roleguild WHERE guildID=:id", {"id": ctx.guild.id})
                guildID = await c.fetchone()
                await c.execute("SELECT sett FROM roleguild WHERE guildID=:id", {"id": ctx.guild.id})
                set_swich = await c.fetchone()

                if guildID == None:
                    await c.execute('INSERT INTO roleguild(guildID) VALUES(:id)', {"id": ctx.guild.id})
                    await users.commit()
                    await c.execute("SELECT guildID FROM roleguild WHERE guildID=:id", {'id':ctx.guild.id})
                    guildID = await c.fetchone()
                
                if set_swich == None:
                    await c.execute('UPDATE roleguild SET sett=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                    await users.commit()
                    await c.execute("SELECT sett FROM roleguild WHERE guildID=:id", {"id": ctx.guild.id})
                    set_swich = await c.fetchone()

                if set_swich[0] == 0:

                    await c.execute('UPDATE roleguild SET roleID=:val WHERE guildID=:id', {'val': role.id, 'id': ctx.guild.id})
                    await c.execute('UPDATE roleguild SET sett=:val WHERE guildID=:id', {'val': 1, 'id': ctx.guild.id})
                    await users.commit()

                    embed = discord.Embed(description=f"Auto-Role set to **{role}**", colour=0x0073e6)
                    await ctx.send(embed=embed)
                
                elif set_swich[0] == 1:

                    embed = discord.Embed(description=f"Auto-Role is already **ENABLED**", colour=0x660000)
                    await ctx.send(embed=embed)
            
            else:
                embed = discord.Embed(description=f"You need to specify a role!", colour=0x660000)
                await ctx.send(embed=embed)

    @autorole.command(aliases=['off', 'OFF'])
    @commands.has_permissions(manage_channels=True)
    async def off_(self, ctx):
        async with aiosqlite.connect('./database/main.db') as users:
            c = await users.cursor()

            await c.execute("SELECT guildID FROM roleguild WHERE guildID=:id", {"id": ctx.guild.id})
            guildID = await c.fetchone()
            await c.execute("SELECT sett FROM roleguild WHERE guildID=:id", {"id": ctx.guild.id})
            set_swich = await c.fetchone()

            
            if guildID[0] == None:
                embed = discord.Embed(description = f"Auto-Role is already off, enable them using **]autorole @role**", colour = 0x660000)
                await ctx.send(embed=embed)
                return

            if set_swich[0] == None:
                await c.execute('UPDATE roleguild SET sett=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                await users.commit()
                await c.execute("SELECT sett FROM roleguild WHERE guildID=:id", {'id': ctx.guild.id})
                set_swich = await c.fetchone()
            
            if set_swich[0] == 1:
                
                await c.execute('UPDATE roleguild SET sett=:val WHERE guildID=:id', {'val': 0, 'id': ctx.guild.id})
                await users.commit()
                embed = discord.Embed(description = 'Auto-Role is **OFF** now', colour = discord.Colour.blue())
                await ctx.send(embed=embed)
            
            elif set_swich[0] == 0:
                
                embed = discord.Embed(description = f"Auto-Role is already off, enable them using **]autorole @role**", colour = 0x660000)
                await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        async with aiosqlite.connect('./database/main.db') as users:
            c = await users.cursor()
            
            await c.execute("UPDATE setguild SET prefix=:val WHERE guildID=:id", {"val": prefix, "id": ctx.guild.id})
            await users.commit()

            await ctx.send(f"Prefix set to **{prefix}**")

def setup(bot):
    bot.add_cog(AutoMod(bot))