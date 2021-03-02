from operator import xor
from os import name
import discord, asyncio, time, random, typing, io, aiohttp, json, aiosqlite, string
from discord import colour
from discord.embeds import Embed
from discord.enums import try_enum
from discord.ext import commands
from ..function import MainDef
from PIL import Image, ImageDraw, ImageFont, ImageOps
from itertools import cycle

class Econsys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Check Bank Acc
    @commands.command(aliases=["level", "lvl"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bank(self, ctx, member:discord.Member=None):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        member = member or ctx.author
        if member.bot:
            embed = discord.Embed(title=None, description = "You can't check bots accounts!", colour = 0x660000)
            await ctx.send(embed=embed)
            return
        else:
            await MainDef.checkAddUser(self, memberid=member.id, table="economy")
            await MainDef.checkAddUser(self, memberid=member.id, table="users")
            await MainDef.checkAddUser(self, memberid=member.id, table="leveling", guildid=ctx.guild.id)
            async with aiosqlite.connect('./database/main.db') as db:
                c = await db.cursor()
                await c.execute(f"SELECT balance FROM economy WHERE userID=:id", {"id":member.id})
                balance = await c.fetchone()
                await c.execute(f"SELECT premium FROM users WHERE userID=:id", {"id":member.id})
                premium = await c.fetchone()
                await c.execute("SELECT lvl FROM leveling WHERE userID=:id AND guildID=:gid", {"id": member.id, "gid": ctx.guild.id})
                level = await c.fetchone()
                await c.execute("SELECT exp FROM leveling WHERE userID=:id AND guildID=:gid", {"id": member.id, "gid": ctx.guild.id})
                exp = await c.fetchone()
                fnt = ImageFont.truetype(f'./photos/radj.ttf', 64)
                async with aiohttp.ClientSession() as s:
                    async with s.get(str(member.avatar_url)) as response:
                        avatar = await response.read()
                with Image.open(io.BytesIO(avatar)) as pfp:
                    img = Image.open("./photos/bank.png")
                    divide_by = pfp.size[0]/200
                    pfp = pfp.resize((int(pfp.size[0]/divide_by), int(pfp.size[1]/divide_by)))
                    draw = ImageDraw.Draw(img)
                    draw.text((300, 120), member.name, font=fnt, fill=(255, 255, 255))
                    draw.text((350, 490), f"{balance[0]}$", font=fnt, fill=(255, 255, 255))
                    draw.text((350, 270), str(level[0]), font=fnt, fill=(255, 255, 255))
                    draw.text((350, 360), str(exp[0]), font=fnt, fill=(255, 255, 255))
                    draw.text((350, 600), "Soon..", font=fnt, fill=(255, 255, 255))
                    draw.text((450, 889), "Soon..", font=fnt, fill=(255, 255, 255))
                    if premium[0] == 0:
                        draw.text((350, 715), "No", font=fnt, fill=(255, 255, 255))
                    elif premium[0] == 1:
                        draw.text((350, 715), "Yes", font=fnt, fill=(255, 255, 255))
                    complete_img = img.copy()
                    complete_img.paste(pfp, (31, 36))
                    output_buffer = io.BytesIO()
                    complete_img.save(output_buffer, "PNG")
                    output_buffer.seek(0)
                await ctx.send(file=discord.File(fp=output_buffer, filename=f"{member.id}.png"))


    #Daily bonus
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def daily(self, ctx):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        author = ctx.author
        if not author.bot:
            await MainDef.checkAddUser(self, memberid=author.id, table="economy")
            await MainDef.checkAddUser(self, memberid=author.id, table="users")
            premium = await MainDef.slct(self, "premium", "users", "userID", author.id)
            cooldown = await MainDef.slct(self, "dailycd", "economy", "userID", author.id)
            boost = await MainDef.slct(self, "boost", "economy", "userID", author.id)
            curr_time = time.time()
            delta = float(curr_time) - float(cooldown)
            if delta >= 86400.0 and delta > 0:
                if premium == 0:
                    bonus = 125 * boost
                    embed = discord.Embed(description=f"**{author.name}**, Good job you got **{bonus}$** | **x{boost}**", colour=0x0059b3)
                elif premium == 1:
                    bonus = 300 * boost
                    embed = discord.Embed(title="Premium Bonus!", description=f"**{author.name}**, Good job you got **{bonus}$** | **x{boost}** Boost", colour=0x664400)
                hint = random.randint(1, 3)
                if hint == 1:
                    embed.set_footer(text="You can use this command every 24h!")
                await MainDef.addMoney(self, author.id, bonus)
                async with aiosqlite.connect('./database/main.db') as db:
                    c = await db.cursor()
                    await c.execute("UPDATE economy SET dailycd=:val WHERE userID=:id", {"val": curr_time, "id": author.id})
                    await db.commit()
                    await ctx.send(embed=embed)
            else:
                await cl(self, ctx, "bonus", delta)
        else:
            embed = discord.Embed(description=f"Robokops are not allowed!", colour=0x660000)
            msg = await ctx.send(embed=embed)
            try:
                await msg.delete(delay=8)
                await ctx.message.delay(delay=8)
            except:
                pass


    #Dice Command
    @commands.command()
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def dice(self, ctx, member:typing.Optional[discord.Member], money=None):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        author = ctx.author
        if member != None:
            if member.bot:
                embed = discord.Embed(description=f"Bots are not allowed to dice.", colour=0x660000)
                msg = await ctx.send(embed=embed)
                try:
                    await msg.delete(delay=8)
                    await ctx.message.delete(delay=8)
                except:
                    pass
                return
            if member == author:
                embed = discord.Embed(description=f"**{author.name}**, you can't gamble yourself!", colour=0x660000)
                msg = await ctx.send(embed=embed)
                try:
                    await msg.delete(delay=8)
                    await ctx.message.delete(delay=8)
                except:
                    pass
                return
        if not author.bot:
            if money != None:
                await MainDef.checkAddUser(self, author.id, "economy")
                if member != None:
                    await MainDef.checkAddUser(self, member.id, "economy")
                auth_balance = await MainDef.slct(self, "balance", "economy", "userID", author.id)
                
                if money.endswith("$"):
                    money = money[:-1]
                if money.lower() == "all":
                    money = auth_balance
                else:
                    try:
                        money = int(money)
                    except:
                        embed = discord.Embed(description=f"**{author.name}**, you can't bet letters!", colour=0x660000)
                        msg = await ctx.send(embed=embed)
                        await msg.delete(delay=8)
                        await ctx.message.delete(delay=8)
                        return
                if member != None:
                    member_balance = await MainDef.slct(self, "balance", "economy", "userID", member.id)
                    if member_balance < money:
                        embed = discord.Embed(description=f"**{member.name}** is too poor :sob:", colour=0x660000)
                        embed.add_field(name="Balance", value=f"{member_balance}$", inline=True)
                        embed.add_field(name="Bet", value=f"{money}$", inline=True)
                        msg = await ctx.send(embed=embed)
                        try:
                            await msg.delete(delay=8)
                            await ctx.message.author(delay=8)
                        except:
                            pass
                        return
                if money >= 25:
                    if auth_balance >= money:
                        acc = 0
                        if member != None:
                            embed = discord.Embed(title=f"{member.name}", description=f"Please type **accept** to start!", colour=0x003399)
                            msg = await ctx.send(embed=embed)
                            def check(m):
                                return m.author == member and m.content.lower() in ['accept', 'accept!']
                            try:
                                await self.bot.wait_for("message", check=check, timeout=10.0)
                            except:
                                embed = discord.Embed(description=f"**{member.name}**, didn't accept...", colour = 0x660000)
                                await msg.delete()
                                msg = await ctx.send(embed=embed)
                                try:
                                    await msg.delete(delay=8)
                                    await ctx.message.delete(delay=8)
                                except:
                                    pass
                                return
                            acc = 1
                        rint1 = random.randint(1, 12)
                        rint2 = random.randint(1, 12)
                        bot_name = self.bot.user.name
                        if acc == 1:
                            embed = discord.Embed(title=f'Bet **{money}$**', description =f'{member.name} **{random.randint(100, 999)}**\n{author.name} **{random.randint(100, 999)}**', colour = 0x99ccff)
                        else:
                            embed = discord.Embed(title=f'Bet **{money}$**', description =f'{bot_name} **{random.randint(100, 999)}**\n{author.name} **{random.randint(100, 999)}**', colour = 0x99ccff)
                        msg = await ctx.send(embed=embed)
                        await asyncio.sleep(1.4)
                        if acc == 1:
                            embed = discord.Embed(title=f'Bet **{money}$**', description =f'{member.name} **{random.randint(100, 999)}**\n{author.name} **{random.randint(100, 999)}**', colour = 0x003d99)
                        else:
                            embed = discord.Embed(title=f'Bet **{money}$**', description =f'{bot_name} **{random.randint(100, 999)}**\n{author.name} **{random.randint(100, 999)}**', colour = 0x003d99)
                        await msg.edit(embed=embed)
                        await asyncio.sleep(1.2)
                        if acc == 1:
                            embed = discord.Embed(title=f'Bet **{money}$**', description =f'{member.name} **{random.randint(100, 999)}**\n{author.name} **{random.randint(100, 999)}**', colour = 0x00004d)
                        else:
                            embed = discord.Embed(title=f'Bet **{money}$**', description =f'{bot_name} **{random.randint(100, 999)}**\n{author.name} **{random.randint(100, 999)}**', colour = 0x00004d)
                        await msg.edit(embed=embed)
                        await asyncio.sleep(1)
                        
                        if rint1 > rint2:
                            await MainDef.setMoney(self, author.id, int(auth_balance - money))
                            if acc == 1:
                                await MainDef.addMoney(self, member.id, int(money))

                            if acc == 0:
                                name = bot_name
                            elif acc == 1:
                                name = member.name

                            embed = discord.Embed(title=f'{name} - Winner', description =f'{name} **{rint1}**\n{author.name} **{rint2}**', colour = 0x00ffff)
                            embed.add_field(name='**Winner**', value = f'{name} **+{money}$**', inline=True)
                            embed.add_field(name = '**Loser**', value = f'{author.name} **-{money}$**')
                            await msg.edit(embed=embed)
                        elif rint1 < rint2:
                            await MainDef.addMoney(self, author.id, int(money))
                            if acc == 1:
                                await MainDef.setMoney(self, member.id, int(member_balance - money))

                            if acc == 0:
                                name = bot_name
                            elif acc == 1:
                                name = member.name

                            embed = discord.Embed(title=f'{author.name} - Winner', description =f'{author.name} **{rint2}**\n{name} **{rint1}**', colour = 0x005c99)
                            embed.add_field(name='**Winner**', value = f'{author.name} **+{money}$**', inline=True)
                            embed.add_field(name = '**Loser**', value = f'{name} **-{money}$**')
                            await msg.edit(embed=embed)
                        else:
                            if acc == 0:
                                name = bot_name
                            elif acc == 1:
                                name = member.name

                            embed = discord.Embed(title=f'Tie', description =f'{author.name} **{rint2}**\n{name} **{rint1}**', colour = 0x006666)
                            await msg.edit(embed=embed)
                        return
                    else:
                        embed = discord.Embed(description=f"**{author.name}** is too poor :sob:", colour=0x660000)
                        embed.add_field(name="Balance", value=f"{auth_balance}$", inline=True)
                        embed.add_field(name="Bet", value=f"{money}$", inline=True)
                        msg = await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f"**{author.name}**, you need to bet more then **24$**", colour=0x660000)
                    msg = await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"**{author.name}**, you need to bet some money!", colour=0x660000)
                msg = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="You robokop", colour=0x660000)
            msg = await ctx.send(embed=embed)
        try:
            await msg.delete(delay=8)
            await ctx.message.delete(delay=8)
        except:
            pass


    @commands.command(aliases=['coinflip'])
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def coin(self, ctx, member:typing.Optional[discord.Member], money=None):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        author = ctx.author
        if money != None:
            if money.endswith('$'):
                money = money[:-1]
        if member != None:
            if member.bot:
                embed = discord.Embed(description=f"Robokops are not allowed to flip coins!", colour=0x660000)
                msg = await ctx.send(embed=embed)
                try:
                    await msg.delete(delay=8)
                    await ctx.message.delete(delay=8)
                except:
                    pass
                return
            if member == author:
                embed = discord.Embed(description=f"**{author}**, you can't flip a coin by yourself.", colour=0x660000)
                msg = await ctx.send(embed=embed)
                try:
                    await msg.delete(delay=8)
                    await ctx.message.delete(delay=8)
                except:
                    pass
                return
        if author.bot:
            embed = discord.Embed(description=f"You are a robokop!", colour=0x660000)
            msg = await msg.send(embed=embed)
            try:
                await msg.delete(delay=8)
                await ctx.message.delete(delay=8)
            except:
                pass
            return
        if money != None:
            await MainDef.checkAddUser(self, author.id, "economy")
            if member != None:
                await MainDef.checkAddUser(self, author.id, "economy")
            author_balance = await MainDef.slct(self, "balance", "economy", "userID", author.id)
            if money.lower() == 'all':
                money = author_balance
            else:
                try:
                    money = int(money)
                except:
                    embed = discord.Embed(description="You can't bet letters!", colour=0x660000)
                    await ctx.send(embed=embed)
                    return
            if member != None:
                member_balance = await MainDef.slct(self, "balance", "economy", "userID", member.id)
                if member_balance < money:
                    embed = discord.Embed(description=f"**{member.name}** is too poor :sob:", colour = 0x660000)
                    embed.add_field(name='Balance', value= f"**{member_balance}$**", inline = True)
                    embed.add_field(name='Bet', value=f'**{money}$**', inline = True)
                    await ctx.send(embed=embed)
                    return
            if money > 0:
                if author_balance >= money:
                    acc = 0
                    if member != None:
                        embed = discord.Embed(title=f"{member.name}", description =f"Please type **accept** to start!", colour = 0x003399)
                        msg = await ctx.send(embed=embed)
                        def check(m):
                            return m.author == member and m.content.lower() in ['accept', 'accept!']
                        try:
                            await self.bot.wait_for("message", check=check, timeout=10.0)
                        except asyncio.TimeoutError:
                            embed = discord.Embed(description=f"**{member.name}**, didn't accept...", colour = 0x660000)
                            msg = await ctx.send(embed=embed)
                            try:
                                await msg.delete(delay=8)
                                await ctx.message.delete(delay=8)
                            except:
                                pass
                            return
                        acc = 1
                    coin = ['head', 'tail']
                    auth_face = random.choice(coin)
                    for face in coin:
                        if face != auth_face:
                            enemy_face = face
                            break
                    if acc == 1:
                        embed = discord.Embed(title="Players", description=f"{author.name.title()} | **{auth_face.upper()}**\n{member.name.title()} | **{enemy_face.upper()}**", colour=0x0066cc)
                    elif acc == 0:
                        embed = discord.Embed(title="Players", description=f"{author.name.title()} | **{auth_face.upper()}**\n{self.bot.user.name.title()} | **{enemy_face.upper()}**", colour=0x0066cc)
                    msg = await ctx.send(embed=embed)
                    await asyncio.sleep(3.2)
                    for x in range(1, 4):
                        embed = discord.Embed(description=f"Result x{x}: **{random.choice(coin).upper()}**", colour=0x3333ff)
                        embed.add_field(name=author.name, value=f"**{auth_face.upper()}**", inline=True)
                        if acc == 1:
                            embed.add_field(name=member.name, value=f"**{enemy_face}**")
                        elif acc == 0:
                            embed.add_field(name=self.bot.user.name, value=f"**{enemy_face}**")
                        await msg.edit(embed=embed)
                        await asyncio.sleep(2)
                    won = random.choice(coin)
                    if auth_face == won:
                        await MainDef.addMoney(self, author.id, int(money))
                        if acc == 1:
                            await MainDef.setMoney(self, member.id, int(member_balance - money))
                        embed = discord.Embed(description=f"**{author.name}** won **+{money}$**", colour = 0x00b377)
                        embed.add_field(name="Coin face", value=won, inline=True)
                        if acc == 1:
                            embed.add_field(name=member.name, value=enemy_face, inline=True)
                        elif acc == 0:
                            embed.add_field(name=self.bot.user.name, value=enemy_face, inline=True)
                        await msg.edit(embed=embed)
                    elif enemy_face == won:
                        await MainDef.setMoney(self, author.id, int(author_balance - money))
                        if acc == 1:
                            await MainDef.addMoney(self, member.id, int(money))
                        if acc == 1:
                            embed = discord.Embed(description=f"**{member.name}** won **+{money}$**", colour = 0x339933)
                        elif acc == 0:
                            embed = discord.Embed(description=f"**{self.bot.user.name}** won **+{money}$**", colour = 0x339933)
                        embed.add_field(name="Coin face", value=won, inline=True)
                        embed.add_field(name=author.name, value=auth_face, inline=True)
                        await msg.edit(embed=embed)
                    else:
                        await ctx.send("Something went wrong")
                    return
                else:
                    embed = discord.Embed(description=f"**{author.name.title()}**, is too poor :sob:", colour = 0x660000)
                    embed.add_field(name='Balance', value= f"**{author_balance}$**", inline = True)
                    embed.add_field(name='Bet', value=f'**{money}$**', inline = True)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"**{author.name.title()}**, you can't bet **0$**.. you can bet a cat")
                msg = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"**{author.name.title()}**, you need to bet some money!", colour=0x660000)
            msg = await ctx.send(embed=embed)
        try:
            await msg.delete(delay=5)
            await ctx.message.delete(delay=5)
        except:
            pass


    @commands.command(aliases=["give"])
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def transfer(self, ctx, member:typing.Optional[discord.Member], obj:str=None):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        author = ctx.author
        if member is not None:
            if member.id is not author.id:
                if not member.bot:
                    if not author.bot:
                        if obj is not None:
                            if obj.endswith("$"):
                                obj = obj[:-1]
                            try:
                                obj = int(obj)
                                is_int = True
                            except:
                                is_int = False
                            valid = False
                            if not is_int:
                                with open("./database/prices.json", "r") as f:
                                    p = json.load(f)
                                db_list = list(p)
                                item_list = [x for x in db_list if x.startswith("item")]
                                num = 0
                                for x in item_list:
                                    item_list[num] = x.replace("item_", "")
                                    num += 1
                                for x in  item_list:
                                    check = obj
                                    check1 = obj.replace("_", "")
                                    check2 = obj.replace(" ", "")
                                    check3 = obj.split("rod")
                                    check3 = check3[0] + "_rod"
                                    check3 = check3.replace(" ", "")
                                    checkers = [check.lower(), check1.lower(), check2.lower(), check3.lower()]
                                    if x in checkers:
                                        valid = True
                                        item = x
                                        item_name = x.replace("_", " ")
                                        break
                            if not is_int:
                                if not valid:
                                    embed = discord.Embed(description=f"This item doen't exist!", colour=0x660000)
                                    msg = await ctx.send(embed=embed)
                                    await msg.delete(delay=5)
                                    await ctx.message.delete()
                                    return
                            if is_int:
                                if obj >= 50:
                                    await MainDef.checkAddUser(self, member.id, "economy")
                                    auth_balance = await MainDef.slct(self, "balance", "economy", "userID", author.id)
                                    member_balance = await MainDef.slct(self, "balance", "economy", "userID", member.id)
                                    auth_premium = await MainDef.slct(self, "premium", "users", "userID", author.id)
                                    if auth_balance >= obj:
                                        if auth_premium == 0:
                                            vat = (obj * 25)//100
                                            vat_per = 25
                                        elif auth_premium == 1:
                                            vat = (obj * 15)//100
                                            vat_per = 15
                                        await MainDef.setMoney(self, author.id, auth_balance - obj)
                                        await MainDef.setMoney(self, member.id, member_balance+(obj-vat))
                                        embed = discord.Embed(description=f"**{author.name.title()}** donated **{obj-vat}$** to **{member.name.title()}**", colour=0x206020)
                                        embed.add_field(name="Taxes", value=f"{vat_per}% | -{vat}$")
                                        await ctx.send(embed=embed)
                                        return
                                    else:
                                        embed = discord.Embed(description=f"{author.name.title()}, you are poor :sob:", colour=0x660000)
                                        embed.add_field(name="Balance", value=f'{auth_balance}$', inline=True)
                                        embed.add_field(name="Transfer", value=f"{obj}$", inline=True)
                                        msg = await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(description=f"**{author.name.title()}**, you can't transfer less then **50$**", colour=0x660000)
                                    msg = await ctx.send(embed=embed)
                            elif not is_int:
                                itemID = await GetItemID(self, item, author.id)
                                if itemID is None:
                                    embed = discord.Embed(description=f"**{author.name.title()}**, you don't have this item!", colour=0x660000)
                                    msg = await ctx.send(embed=embed)
                                else:
                                    async with aiosqlite.connect('./database/main.db') as db:
                                        c = await db.cursor()
                                        await c.execute("UPDATE items SET userID=:userid WHERE itemID=:itemid", {"userid": member.id, "itemid": itemID})
                                        await db.commit()
                                        embed = discord.Embed(description=f"**{author.name.title()}** transfered **{item_name}** to **{member.name.title()}**")
                                        await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f"{author.name.title()}, you need to transfer an item/money!", colour=0x660000)
                            msg = await ctx.send(embed=embed)
                    else:
                        msg = await ctx.send("You robokop")
                else:
                    embed = discord.Embed(description=f"**{author.name.title()}**, you can't transfer stuff to bots!", colour=0x660000)
                    msg = await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"**{author.name.title()}** you can't transfer stuff to yourself!", colour=0x660000)
                msg = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"**{author.name.title()}**, you need to mention someone!", colour=0x660000)
            embed.set_footer(text="]transfer @user [item]")
            msg = await ctx.send(embed=embed)
        try:
            await msg.delete(delay=5)
            await ctx.message.delete(delay=5)
        except:
            pass

    @commands.command()
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def shop(self, ctx):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        with open("./database/prices.json", "r") as f:
            p = json.load(f)
        shop_list = list(p)
        shop_list = [x for x in shop_list if x.startswith("item")]
        embed = discord.Embed(title="Shop", colour=0x6699ff)
        for x in shop_list:
            if x.startswith("item"):
                price = x.replace("item", "price")
                sale = x.replace("item", "sale")
                text = x.replace("item", "text")
                if p[sale] != 0:
                    desc = p[x] + " | Sale from ~~|sale|$~~"
                    desc = desc.replace("|price|", str(p[price]))
                    desc = desc.replace("|sale|", str(p[sale]))
                else:
                    desc = p[x]
                    desc = desc.replace("|price|", str(p[price]))
            embed.add_field(name=desc, value=p[text], inline=False)
        await ctx.send(embed=embed)


    #Show inventory
    @commands.command(aliases=['inv'])
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def inventory(self, ctx, member:discord.Member=None):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        pm = await MainDef.pm(self, ctx)
        if pm is True:
            return
        member = member or ctx.author
        if not member.bot:
            async with aiosqlite.connect("./database/main.db") as db:
                c = await db.cursor()
                await c.execute("SELECT item FROM items WHERE userID=:id", {"id": member.id})
                items = await c.fetchall()
                if len(items) == 0:
                    itm = "No items!"
                else:
                    itm = ", ".join(x[0] for x in items)
                    itm = itm.replace("_", " ")
                embed = discord.Embed(title="Inventory", description=itm.title(), colour=0x006600)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description=f"Robokops are not allowed!", colour=0x660000)
            msg = await ctx.send(embed=embed)
        try:
            await msg.delete(delay=8)
            await ctx.message.delete(delay=8)
        except:
            pass


    #Buy Items
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def buy(self, ctx, *, arg=None):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down:
            return
        author = ctx.author
        if not author.bot:
            if arg != None:
                with open("./database/prices.json", "r") as f:
                    p = json.load(f)
                shop_list = list(p)
                price_list = [x for x in shop_list if x.startswith("price")]
                item_list = []
                for x in price_list:
                    x = x.replace("price_", "")
                    item_list.append(x)
                valid = False
                for x in item_list:
                    check = arg
                    check1 = arg.replace("_", "")
                    check2 = arg.replace(" ", "")
                    check3 = arg.split("rod")
                    check3 = check3[0] + "_rod"
                    check3 = check3.replace(" ", "")
                    checkers = [check.lower(), check1.lower(), check2.lower(), check3.lower()]
                    if x in checkers:
                        valid = True
                        item = x
                        break
                if not valid:
                    embed = discord.Embed(description="This item does't exist!", colour=0x660000)
                    await ctx.send(embed=embed)
                    return
                async with aiosqlite.connect("./database/main.db") as db:
                    c = await db.cursor()
                    await c.execute("SELECT balance FROM economy WHERE userID=:id", {"id": author.id})
                    auth_bal = await c.fetchone()
                    item_price = p["price_" + item]

                    if auth_bal[0] >= item_price:
                        smth = item.replace("_", " ")
                        embed = discord.Embed(description=f"Thank you for purchasing **{smth}**", colour=0x006bb3)  
                        embed.add_field(name="Price", value=f"-{str(item_price)}$", inline=True)
                        embed.add_field(name="Balance", value=f"{str(int(auth_bal[0] - item_price))}$", inline=True)
                        await ctx.send(embed=embed)

                        await c.execute("UPDATE economy SET balance=:val WHERE userID=:id", {"val":int(auth_bal[0] - item_price), "id":author.id})
                        await db.commit()     
                        await AddItem(self, item, author.id)
                    else:
                        embed = discord.Embed(description=f"Sorry **{author.name.title()}**, you don't have enought money. :sob:", colour=0x660000)
                        embed.add_field(name="Price", value=f"{str(item_price)}$", inline=True)
                        embed.add_field(name="Balance", value=f"{str(auth_bal[0])}$", inline=True)
                        r = random.randint(1, 3)
                        if r == 1:
                            embed.set_footer(text="Make sure you got the daily bonus!")
                        await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description="You need to buy an item.. check our shop!", colour=0x660000)
                msg = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"Robokops are not allowed!", colour=0x660000)
            msg = await ctx.send(embed=embed)
        try:
            await msg.delete(delay=8)
            await ctx.message(delay=8)
        except:
            pass


    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def sell(self, ctx, *, arg=None):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        author = ctx.author
        if not author.bot:
            if arg != None:
                with open("./database/prices.json", "r") as f:
                    p = json.load(f)
                shop_list = list(p)
                price_list = [x for x in shop_list if x.startswith("price")]
                item_list = []
                for x in price_list:
                    x = x.replace("price_", "")
                    item_list.append(x)
                valid = False
                for x in item_list:
                    check = arg
                    check1 = arg.replace("_", "")
                    check2 = arg.replace(" ", "")
                    check3 = arg.split("rod")
                    check3 = check3[0] + "_rod"
                    check3 = check3.replace(" ", "")
                    checkers = [check.lower(), check1.lower(), check2.lower(), check3.lower()]
                    if x in checkers:
                        valid = True
                        item = x
                        break
                if not valid:
                    embed = discord.Embed(description="This item does't exist!", colour=0x660000)
                    await ctx.send(embed=embed)
                    return
                itemID = await GetItemID(self, item, author.id)
                if itemID is None:
                    embed = discord.Embed(description="You don't have this item!", colour=0x660000)
                    await ctx.send(embed=embed)
                    return

                item_health = await MainDef.slct(self, "health", "items", "itemID", itemID)
                auth_bal = await MainDef.slct(self, "balance", "economy", "userID", author.id)

                if item_health < 85:
                    embed = discord.Embed(description=f"Sorry **{author.name}**, but you can only sell items with **+85HP**", colour=0x660000)
                    await ctx.send(embed=embed)
                    return

                price = p["price_" + item]
                item_sell = int(price - ((price*45)//100))

                await MainDef.addMoney(self, author.id, auth_bal + item_sell)
                await RemoveItem(self, itemID)
                embed = discord.Embed(description=f"Item sold for **{item_sell}$**", colour=0x002699)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f"Sorry **{author.name.title()}**, but you can't sell air.", colour=0x660000)
                await ctx.send(embed=embed)
        else:
            await ctx.send("You robokop.")


    #Get some spicy Fishes
    @commands.command()
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def fish(self, ctx, *, msg=None):
        down = await MainDef.downCheck(self, ctx, "econsys")
        if down == 'down':
            return
        author = ctx.author
        if author.bot:
            await ctx.send("Ummm u robokop.")
            return

        if msg != None:
            await MainDef.checkAddUser(self, memberid=author.id, table="economy")
            async with aiosqlite.connect('./database/main.db') as db:
                c = await db.cursor()
                rods = ['wood_rod', 'wood rod', 'woodrod', 'wood',
                    'iron_rod', 'iron rod', 'ironrod', 'iron',
                    'gold_rod', 'gold rod', 'goldrod', 'gold']
                valid = None
                for x in rods:
                    if x == msg.lower():
                        msg = msg.lower()
                        msg = msg.replace("_", "")
                        msg = msg.replace(" ", "")
                        msg = msg.split("rod")
                        msg = msg[0] + "_rod"
                        valid = 1
                        break
                
                if valid == None:
                    embed = discord.Embed(description=f"**{msg}** is not a valid Rod", colour=0x660000)
                    await ctx.send(embed=embed)
                    return

                w_fish = ['delta', 'nugget', 'cici', 'nokia', 'boots']
                i_fish = ['flipper', 'bait', 'shark', 'sushi', 'samsung']
                g_fish = ['nemo', 'salty', 'iron_rod', 'iphone', 'wood_rod']

                itemID = await GetItemID(self, msg, author.id)
                if itemID == None:
                    embed = discord.Embed(description=f"You don't have this rod :sob:", colour=0x660000)
                    await ctx.send(embed=embed)
                    return

                w_fish = random.choice(w_fish)
                i_fish = random.choice(i_fish)
                g_fish = random.choice(g_fish)
                rod = msg.replace("_", " ")
                embed = discord.Embed(title="Fishing", description=f"Waiting for fish.", colour=0x66ccff)
                embed.set_footer(text=f"Rod: {rod.title()}")
                prop = await ctx.send(embed=embed)
                await asyncio.sleep(1.5)
                
                dots = ""
                tryes = 0
                while True:

                    if tryes == 6:
                        won = False
                        break

                    dots += "."
                    embed = discord.Embed(title=f"Fishing{dots}", description="Waiting for fish.", colour=0x0033cc)
                    embed.set_footer(text=f"Rod: {rod.title()}")
                    await prop.edit(embed=embed)
                    await asyncio.sleep(2.4)

                    fish = random.randint(1, 100)

                    if fish <= 30:
                        embed = discord.Embed(description=f"You caught a fish! Type **catch** to get it!", colour=0x330000)
                        await prop.edit(embed=embed)

                        def check(m):
                            return m.author == ctx.author and m.content.lower() in ['catch', 'catch!']

                        try:
                            await self.bot.wait_for("message", check=check, timeout=random.randint(2, 4))
                            won = True
                            break

                        except asyncio.TimeoutError:
                            embed = discord.Embed(description =f"**{author.name}**, the fish escaped :sob:", colour = 0x660000)
                            await prop.edit(embed=embed)
                            await asyncio.sleep(2)

                    tryes += 1
                await prop.delete()
                damage = random.randint(5, 20)
                await c.execute("SELECT health FROM items WHERE itemID=:id", {"id": itemID})
                item_health = await c.fetchone()
                await c.execute("SELECT balance FROM economy WHERE userID=:id", {"id": author.id})
                auth_bal = await c.fetchone()
                
                if won == False:
                    embed = discord.Embed(description="There are no fishes anymore.. :sob:", colour=0x660000)
                    if damage >= item_health[0]:
                        await RemoveItem(self, itemID)
                        damage = item_health
                    else:
                        await c.execute("UPDATE items SET health=:val WHERE itemID=:id", {"val": int(item_health[0]-damage), "id": itemID})
                        await db.commit()
                    embed.add_field(name="Rod Damage", value=f"-{damage}HP")
                    await ctx.send(embed=embed)
                    return

                fish_list = [{"delta": [85, 160], "nugget": [55, 90], "cici": [45, 100], "nokia": [100, 230], "boots": [25, 50]}, 
                            {"flipper": [170, 230], "bait": [130, 175], "shark": [260, 390], "sushi": [210, 320], "samsung": [400, 550]}, 
                            {"nemo": [570, 800], "salty": [480, 650], "iron_rod": "iron_rod", "iPhone": [850, 1100], "wood_rod": "wood_rod"}]
                wood, wood_price = random.choice(list(fish_list[0].items()))
                iron, iron_price = random.choice(list(fish_list[1].items()))
                gold, gold_price = random.choice(list(fish_list[2].items()))
                
                wood_price = random.choice(wood_price)
                wood_des = f"Woo, you caught a **{wood.title()}** and sold it for **{wood_price}**!"
                iron_price = random.choice(iron_price)
                iron_des = f"Woo, you caught a **{iron.title()}** and sold it for **{iron_price}**!"
                item_valid = False
                try:
                    gold_price = int(random.choice(gold_price))
                    gold_des = f"WOO, you caught a **{gold}** and sold it for **{gold_price}**!"
                except:
                    item_valid = True
                    gold_price = gold_price
                    item_name = gold.replace("_", " ")
                    gold_des = f"WOOOO, you caught a **{item_name.title()}** and added it to inventory!"
                if msg == "wood_rod":
                    price = wood_price
                    des = wood_des
                elif msg == "iron_rod":
                    r = random.randint(1, 3)
                    if r == 1:
                        price = iron_price
                        des = iron_des
                    else:
                        price = wood_price
                        des = wood_des
                elif msg == "gold_rod":
                    r = random.randint(1, 5)
                    if r == 1:
                        price = gold_price
                        des = gold_des
                    elif r > 1 and r <= 3:
                        price = iron_price
                        des = iron_des
                    else:
                        price = wood_price
                        des = wood_des
                else:
                    await ctx.send("I guess you found an error.. Report it to our support server!\nhttps://botware.club")

                embed = discord.Embed(description=des, colour=0x002db3)
                
                if damage >= item_health[0]:
                    damage = item_health[0]
                    await RemoveItem(self, itemID)
                    embed.add_field(name="Broken Rod", value="Rod got broken due damage", inline=True)
                else:
                    await c.execute("UPDATE items SET health=:val WHERE itemID=:id", {"val": int(item_health[0]-damage), "id": itemID})
                    await db.commit()
                
                if item_valid == True:
                    await AddItem(self, price, author.id)
                else:
                    await c.execute("UPDATE economy SET balance=:val WHERE userID=:id", {"val": int(auth_bal[0]+price), "id": author.id})
                    await db.commit()
                
                embed.add_field(name="Rod Damage", value=f"-{damage}HP", inline=True)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description="You need to use a rod! Please type **]fish [rod name]**", colour=0x660000)
            await ctx.send(embed=embed)

async def cl(self, ctx, cl, delta):
    seconds = 86400 - delta
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    embed = discord.Embed(title=f':rotating_light: {cl.title()} Cooldown :rotating_light:', description = f'You need to wait **{int(h)}h {int(m)}m {int(s)}s**', colour = 0x660000)
    await ctx.send(embed=embed)

async def AddItem(self, item, memberid):
    async with aiosqlite.connect('./database/main.db') as db:
        c = await db.cursor()
        checker = True
        while checker == True:
            await c.execute("SELECT itemID FROM items")
            itemID_check = await c.fetchall()
            rid = "".join(random.choice(string.ascii_letters + string.digits) for x in range(6))
            if rid not in itemID_check:
                checker = False
        await c.execute("INSERT INTO items(itemID, userID, item) VALUES(:itemid, :id, :item)", {"itemid": rid, "id": memberid, "item": item})
        await db.commit()

async def GetItemID(self, item, memberid):
    async with aiosqlite.connect('./database/main.db') as users:
        c = await users.cursor()
        try:
            await c.execute("SELECT itemID FROM items WHERE item=:it and userID=:id", {"it": item, "id": memberid})
            id = await c.fetchone()
            return id[0]      
        except:
            return None      

async def RemoveItem(self, itemID):
    async with aiosqlite.connect('./database/main.db') as db:
        c = await db.cursor()
        await c.execute("DELETE FROM items WHERE itemID=:id", {"id": itemID})
        await db.commit()

def setup(bot):
    bot.add_cog(Econsys(bot))