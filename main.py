import discord, asyncio, os, aiosqlite, aiohttp, io, json
from discord.ext import commands
from discord.utils import get
TOKEN = "BOT TOKEN HERE"

bot = commands.Bot(command_prefix='..', case_insensitive=True)
@bot.remove_command('help')

#Bot Status
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=']help', type=2))
    servers = list(bot.guilds)
    print("-----")
    print(f"{bot.user.name} is Connected on {str(len(servers))} server(s):")
    print("-----")

    #Load Cogs
    for filename in os.listdir("./cogs/events"):
        if filename.endswith(".py"):
            if filename == "events.py":
                bot.load_extension(f"cogs.events.{filename[:-3]}")
                print(f"# {filename}  is loaded")

    for filename in os.listdir("./cogs/commands"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.commands.{filename[:-3]}")
            print(f"# {filename}  is loaded")

#Ping Check
@bot.command()
@commands.cooldown(1, 4, commands.BucketType.user)
async def ping(ctx):
    embed = discord.Embed(title=None, description=f"Bot ping is **{round(bot.latency * 1000)}ms**", colour = 0x66ccff)
    await ctx.send(embed=embed)  

#Bot Token
bot.run(TOKEN)