import discord, asyncio, aiosqlite
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    #Help Command
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def help(self, ctx):
        async with aiosqlite.connect("./database/main.db") as users:
            c = await users.cursor()
            await c.execute("SELECT prefix FROM setguild WHERE guildID=:id", {"id": ctx.guild.id})
            p = await c.fetchone()
            p = p[0]

            servers = list(self.bot.guilds)
            users = 0
            for guild in self.bot.guilds:
                if guild.id != '264445053596991498' or guild.id != '264445053596991498':
                    users += guild.member_count
            
            embed = discord.Embed(title='Commands', description = None, colour = 0x0054ff)
            embed.set_footer(text='Powered by Python3 and Love <3')      
            embed.add_field(name=":tools: Moderation", value=f'**{p}help mod**', inline=True)
            embed.add_field(name=":money_with_wings: Economy", value=f'**{p}help econ**', inline = True)
            embed.add_field(name=":trophy: Levels", value = f'**{p}help lvl**', inline = True)
            embed.add_field(name=":video_game: Games", value=f"**{p}help games**", inline = True)
            embed.add_field(name=":musical_note: Music", value=f"**{p}help music**", inline = True)
            embed.add_field(name=":frame_photo: Photos/Nsfw", value = f"**{p}help photos**", inline = True)
            embed.add_field(name=':space_invader: Fun', value = f"**{p}help fun**", inline = True)
            embed.add_field(name=":sunglasses: Premium", value = f"**{p}help premium**", inline=True)
            embed.add_field(name=":bust_in_silhouette: Info", value = f"**{p}help info**", inline=True)  
            embed.set_author(name=f'{users} Users  |  {str(len(servers))} Servers')
            embed.set_thumbnail(url="https://media2.giphy.com/media/j3DhlsXXBWzsjnn6lQ/giphy.gif")
            embed.add_field(name="Support", value = "[Discord Server](https://discord.gg/6xXQAZ3)", inline=True)
            embed.add_field(name="Bot", value="[Invite](https://discordapp.com/api/oauth2/authorize?client_id=699686254815608842&permissions=8&scope=bot)", inline = True)
            embed.add_field(name="Last Update", value="8/25/2020 Added 2 fun commands", inline=False)
            await ctx.send(embed=embed)

    @help.command(aliases = ['mod'])
    async def moderation(self, ctx):
        async with aiosqlite.connect("./database/main.db") as users:
            c = await users.cursor()
            await c.execute("SELECT prefix FROM setguild WHERE guildID=:id", {"id": ctx.guild.id})
            p = await c.fetchone()
            p = p[0]

            embed = discord.Embed(title=":tools: Moderation", description = None, colour = 0x002266)
            embed.add_field(name=f"{p}kick **@user** <reason>", value=f"Kick @user for <reason>", inline=False)
            embed.add_field(name=f"{p}ban **@user** <reason>", value = f"Ban @user for <reason>", inline=False)
            embed.add_field(name=f"{p}unban **user.id**", value=f"Unban user.id" ,inline = False)
            embed.add_field(name=f"{p}mute **@user** <reason>", value=f"Mute @user for <reason>", inline=False)
            embed.add_field(name=f"{p}tempmute **@user** <time> <reason> - Still Testing", value=f"Mute @user until <time> for <reason>", inline=False)
            embed.add_field(name=f"{p}unmute **@user**", value=f"Unmute @user", inline=False)
            embed.add_field(name=f"{p}nuke **#channel**", value = f"Purge every channel message", inline=False)
            embed.add_field(name=f"{p}clear **<int>**", value=f"Clear <int> channel messages", inline=False)
            embed.add_field(name=f"{p}lock", value = f"Lock channel", inline = False)
            embed.add_field(name=f"{p}unlock", value = f"Unlock channel", inline=False)
            embed.add_field(name=f"{p}logs **#channel / off**", value = f"Catch your abusive staff", inline=False)
            embed.add_field(name=f"{p}welcome **#channel / off** - Custom message soon", value = f"Greet guests as they enter", inline=False)
            embed.add_field(name=f"{p}autorole **@role / off**", value = "Give a role to newcomers", inline=False)
            await ctx.send(embed=embed)

    @help.command(aliases = ['econ'])
    async def economy(self, ctx):
        # async with aiosqlite.connect("./database/main.db") as users:
        #     c = await users.cursor()
        #     await c.execute("SELECT prefix FROM setguild WHERE guildID=:id", {"id": ctx.guild.id})
        #     p = await c.fetchone()
        p = "."

        embed = discord.Embed(title=":money_with_wings: Economy", colour = 0x002266)
        embed.add_field(name=f"{p}bank", value = "Check your 0$ balance.", inline=False)
        embed.add_field(name=f"{p}daily", value = "Take a daily bonus.", inline=False)
        embed.add_field(name=f"{p}dice **@user** <value>", value = "Lose your money.", inline=False)
        embed.add_field(name=f"{p}coin **@user** <value>", value = "Lose your money by a coin.", inline=False)
        embed.add_field(name=f"{p}fish <rod>", value = "Catch some fishes.", inline=False)
        embed.add_field(name=f"{p}shop", value = "Check the marketplace.", inline=False)
        embed.add_field(name=f"{p}inventory", value = "Check your items.", inline=False)
        embed.add_field(name=f"{p}transfer **@user** <value>", value = "Give something to Homeless people.", inline=False)
        embed.add_field(name=f"{p}buy <item>", value = "Buy something from marketplace.", inline=False)
        embed.add_field(name=f"{p}sell <item>", value = "Sell your items.", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases = ['lvls', 'lvl', 'level'])
    async def levels(self, ctx):
        embed = discord.Embed(title=":trophy: Levels", description = "Working on it", colour = 0x002266)
        await ctx.send(embed=embed)

    @help.command(aliases=['game'])
    async def games(self, ctx):
        async with aiosqlite.connect("./database/main.db") as users:
            c = await users.cursor()
            await c.execute("SELECT prefix FROM setguild WHERE guildID=:id", {"id": ctx.guild.id})
            p = await c.fetchone()
            p = p[0]

            embed = discord.Embed(title=":video_game: Games", colour = 0x002266)
            embed.add_field(name=f"{p}battle **@user**", value="Beat your best friend!")
            embed.set_footer(text="More soon! :3")
            await ctx.send(embed=embed)

    @help.command()
    async def music(self, ctx):
        embed = discord.Embed(title=":musical_note: Music", description = "Coming soon", colour = 0x002266)
        await ctx.send(embed=embed)

    @help.command(aliases=['photos', 'PHOTOS'])
    async def photo(self, ctx):
        async with aiosqlite.connect("./database/main.db") as users:
            c = await users.cursor()
            await c.execute("SELECT prefix FROM setguild WHERE guildID=:id", {"id": ctx.guild.id})
            p = await c.fetchone()
            p = p[0]

            embed = discord.Embed(title=":frame_photo: Photos/Nsfw", description = None, colour = 0x002266)
            embed.add_field(name="Commands", value = f'{p}avatar - User avatar\n{p}mad @user - Someone is mad', inline=False)
            embed.add_field(name="Photos :camera:", value = f"{p}cat - Cutty\n{p}dog - Duggu\n{p}fox - Foxy", inline=False)
            embed.add_field(name="NSFW :underage:", value = f"]nsfw [list]")
            await ctx.send(embed=embed)

    @help.command()
    async def fun(self, ctx):
        async with aiosqlite.connect("./database/main.db") as users:
            c = await users.cursor()
            await c.execute("SELECT prefix FROM setguild WHERE guildID=:id", {"id": ctx.guild.id})
            p = await c.fetchone()
            p = p[0]

            embed = discord.Embed(title=':space_invader: Fun', colour = 0x002266)
            embed.add_field(name='Funny Commands', value = f"{p}meme - Meme time\n{p}8 **<question>** - 8 Ball game", inline = False)
            embed.add_field(name="Checkers", value = f"{p}pettu - Pettu Check\n{p}pp - Pepee Check\n{p}gay - Gay Check\n{p}iq - IQ Check\n{p}trans lang1 lang2 - Translator\n{p}google - Google Search")
            await ctx.send(embed=embed)

    @help.command(aliases=['pr'])
    async def premium(self, ctx):
        async with aiosqlite.connect("./database/main.db") as users:
            c = await users.cursor()
            await c.execute("SELECT prefix FROM setguild WHERE guildID=:id", {"id": ctx.guild.id})
            p = await c.fetchone()
            p = p[0]

            embed = discord.Embed(title=":sunglasses: Premium", description = "To get premium and support our work, Join our discord Server!\n[Discord](https://discord.gg/6xXQAZ3)", colour = 0x002266)
            embed.add_field(name=f"{p}daily", value="Big Daily Bonus.", inline=False)
            embed.add_field(name=f"{p}work", value="Sexy job bonus from boss.", inline=False)
            embed.add_field(name="Cooldowns", value="Reduced Cooldowns.", inline=False)
        
            await ctx.send(embed=embed)

    @help.command()
    async def info(self, ctx):
        async with aiosqlite.connect("./database/main.db") as users:
            c = await users.cursor()
            await c.execute("SELECT prefix FROM setguild WHERE guildID=:id", {"id": ctx.guild.id})
            p = await c.fetchone()
            p = p[0]

            embed = discord.Embed(title=":bust_in_silhouette: Info", colour = 0x002266)
            embed.add_field(name=f"{p}vote", value=f"Support our discord Bot!", inline=False)
            embed.add_field(name=f"{p}prefix <value>", value="Change guild prefix", inline=False)
            embed.add_field(name="]resetprefix", value="Reset guild prefix, working for every prefix")
            embed.add_field(name=f"{p}ping", value="See bot ping", inline=False)
            embed.set_footer(text="AndreiRzv#0001 & svenskithesource#2815")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))