import discord, json, aiohttp, asyncio, io, os, random
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps


class Photos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #User Avatar
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member=None):
        member = member or ctx.author
        userAvatarUrl = member.avatar_url

        embedava = discord.Embed(colour = discord.Colour.blue())
        embedava.set_image(url=f'{userAvatarUrl}')
        embedava.set_author(name=f"{member.name}'s Avatar", icon_url=member.avatar_url)
        await ctx.send(embed=embedava)


    #Send Cutty pic
    @commands.command(aliases=['cuty', 'meow', 'cutty'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://nekos.life/api/v2/img/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(colour = 0x66ffff)
                    embed.set_author(name=f'Here is your cutty {ctx.author.name}', icon_url=ctx.author.avatar_url)
                    embed.set_image(url=js['url'])
                    await ctx.send(embed=embed)
                else:
                    print(f"Api responded with {r.status}")


    #Dog pic
    @commands.command(aliases=['duggu', 'dugu'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(colour = 0x66ffff)
                    embed.set_author(name=f'Here is your duggu {ctx.author.name}', icon_url=ctx.author.avatar_url)
                    embed.set_image(url=js['message'])
                    await ctx.send(embed=embed)
                else:
                    print(f"Api responded with {r.status}")


    #Foxy pic
    @commands.command(aliases=['foxy'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://randomfox.ca/floof/') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(colour = 0x66ffff)
                    embed.set_author(name=f'Here is your foxy {ctx.author.name}', icon_url=ctx.author.avatar_url)
                    embed.set_image(url=js['image'])
                    await ctx.send(embed=embed)
                else:
                    print(f"Api responded with {r.status}")


    #Memes piccccc
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def meme(self, ctx):
        author = ctx.author
        subreddits = ["dankmemes", "memes"]
        subreddit = random.choice(subreddits)
        meme = await getMeme(subreddit=subreddit)
        count = 0
        while meme == False or meme["nsfw"] == True:
            meme = await getMeme(subreddit=subreddit)
            count += 1
            if count == 5:
                await ctx.send("An error occurred. Please join our discord server to let us know.")
                print(f"An error occurred whilst getting a meme. This happened to {ctx.author}\nin guild {ctx.guild.name}")
                return
        embed = discord.Embed(title=meme["title"], description=f"[Post link]({meme['postLink']})", colour=0x33cc33)
        embed.set_image(url=meme['url'])
        embed.set_footer(text=f'Posted on: r/{meme["subreddit"]}\nRequested by: {author.name}')
        await ctx.send(embed=embed)
    
    @commands.command()
    #@commands.cooldown(1, 4, commands.BucketType.user)
    async def nsfw(self, ctx, *subreddit_user):
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(title="NSFW Content", description="To use this command you need to have **NSFW Channel Enabled!**", colour=0x990099)
            await ctx.send(embed=embed)
            return
       
        subreddit_user = subreddit_user or ("nsfw",)
        author = ctx.author
        subreddits = {"boobs": "BoobsAndTities", "ass": "ass", "gay": "GayGifs", "gifs": "gifsgonewild", "furry": "FurryPornSubreddit", "blowjob": "Sluts_Blowjobs", "stockings": "stockings"}
        list_p = ""
        subreddit_user = subreddit_user[0]
        
        if subreddit_user.lower() in subreddits:
            subreddit = subreddits[subreddit_user.lower()]
        
        elif subreddit_user.lower() == "list":
            for categorie in subreddits:
                list_p = list_p + categorie + ", "
            await ctx.send(f"You can choose between: **{list_p[:-2]}**")
            return
        else:
            subreddit = random.choice(list(subreddits))
            while subreddit == "gay":
                subreddit = subreddits[random.choice(list(subreddits))]

        nsfw = await getMeme(subreddit=subreddit)
        count = 0
        while nsfw == False:
            nsfw = await getMeme(subreddit=subreddit)
            count += 1
            if count == 5:
                await ctx.send("An error occurred. Please join our discord server to let us know.")
                print(f"An error occurred whilst getting an nsfw image. This happened to {ctx.author}\nin guild {ctx.guild.name}")
                return
        embed = discord.Embed(colour=0x33cc33)
        embed.set_image(url=nsfw['url'])
        embed.set_footer(text=f'Requested by: {author.name}')
        await ctx.send(embed=embed)

    #Print cool text message
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def text(self, ctx, *, message): 
        loop = self.bot.loop()
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            def pillow_block():
                fnt = ImageFont.truetype(f'arial.pil', 26)
                fnt_c = ImageFont.truetype(f'arial.pil', 18)

                message_credit = f"by {ctx.author.name}"
                w,h = fnt.getsize(message)
                w_c,h_c = fnt_c.getsize(message_credit)
                
                width_image = w + 120
                height_image = h + 60

                img = Image.new('RGBA', (width_image, height_image), color=(0, 0, 0, 0))
                
                d = ImageDraw.Draw(img)
                d.text(((width_image-w)/2, ((height_image-h)-20)/2), message, font=fnt, fill=(255, 255, 255))
                d.text(((width_image-w_c)/2, ((height_image-h_c)+35)/2), message_credit, font=fnt_c, fill=(211, 211, 211))
                
                imgByteArr = io.BytesIO()
                img.save(imgByteArr, format='PNG')
                imgByteArr.seek(0)
                return imgByteArr

            img = await loop.run_in_executor(None, pillow_block)
            print('default thread pool', img)
            await ctx.send(file=discord.File(img, f"{ctx.author.id}.png"))


    #mad user
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def mad(self, ctx, member:discord.Member=None):
        member = member or ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.avatar_url)) as response:
                avatar_bytes = await response.read()


        with Image.open(io.BytesIO(avatar_bytes)) as pfp:
            mad_img = Image.open("./photos/mad.jpg")
            
            divide_by = pfp.size[0]/130
            pfp = pfp.resize((int(pfp.size[0]/divide_by), int(pfp.size[1]/divide_by)))
            
            complete_img = mad_img.copy()
            complete_img.paste(pfp, (33, 73))
            output_buffer = io.BytesIO()
            complete_img.save(output_buffer, "PNG")  # or whatever format
            
            output_buffer.seek(0)

        # back in your async function
        await ctx.send(file=discord.File(fp=output_buffer, filename=f"{ctx.author.id}.png"))


async def getMeme(subreddit):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://meme-api.herokuapp.com/gimme/' + subreddit) as r:
            if r.status == 200:
                meme = await r.json()
                return meme
            else:
                print(r.status)
                return False


def setup(bot):
    bot.add_cog(Photos(bot))