import discord, random, asyncio, aiohttp, io
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Love Checker
    # @commands.command(aliases=['luv'])
    # async def love(slef, ctx, member:discord.Member=None):
    #     member = member or ctx.author
    #     r = random.randint(0, 100)
        
    
    #Funny 8ball game
    @commands.command(aliases=['8ball', '8'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                    'It is decidedly so.',
                    'Without a doubt.',
                    'Yes - definitely.',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes.',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    "Don't count on it.",
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Very doubtful.']
        embed8 = discord.Embed(title=None, description = f'{random.choice(responses)}', colour = 0x738c8c)
        await ctx.send(embed=embed8)

    #PP checker
    @commands.command(aliases=['peepee', 'pepe'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def pp(self, ctx, member:discord.Member = None):
        member = member or ctx.author
        r = random.randint(0, 12)
        size = '=' * r
        embed = discord.Embed(title=f'**{member.name}** Peepee', description = f"8{size}D")
        await ctx.send(embed=embed)

    #Iq Checker
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def iq(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        r = random.randint(-20, 200)
        embediq = discord.Embed(title='IQ Check', description=f'**{member.name}** has **{r}** iq', colour = 0x002080)
        await ctx.send(embed=embediq)

    #Gay Check
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def gay(self, ctx, member:discord.Member = None):
        member = member or ctx.author
        r = random.randint(1, 125)
        r1 = r / 1.04
        embed = discord.Embed(title = 'Gay Check', description = f"**{member.name}**, you are **{r1:.2f}%** gay.", colour = 0xff33cc)
        await ctx.send(embed=embed)

    #Pettu checker
    @commands.command(aliases=['petu'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def pettu(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        texts = {f"Stoopid pettu hater **{member}**": random.randint(0, 10), f"Pettus don't love you **{member}**": random.randint(11, 20), f"10 meters away from my pettu **{member}**": random.randint(21, 30), 
                f"Don't even watch my pettu **{member}**": random.randint(31, 40), f"Please don't touch my pettu **{member}**": random.randint(40, 50), f"Only 5 minutes near my pettu **{member}**": random.randint(51, 60), 
                f"Atleast don't kiss my pettu **{member}**": random.randint(61, 70), f"Give some attension to pettus **{member}**": random.randint(71, 80), f"Go pet my pettu **{member}**": random.randint(81, 90), 
                f"Luv my pettu **{member}**": random.randint(91, 95), f"Please become my pettu god **{member}**": random.randint(96, 100)}
        text, randint = random.choice(list(texts.items()))
        embed = discord.Embed(title=f'Pet {randint}%', description=text, colour = 0x0000ff)
        await ctx.send(embed=embed)


def setup(bot): 
    bot.add_cog(Fun(bot))