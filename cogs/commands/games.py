import discord, asyncio, random, time
from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 90, commands.BucketType.user)
    async def battle(self, ctx, member:discord.Member=None):
        if ctx.author is member:
            await ctx.send("You can't fight yourself, psycho.")
            return
        member = member or self.bot.user
        author_health = 100
        member_health = 100
        b_round = 0
        embed = discord.Embed(title=f'Battle!', colour=0x00997a)
        embed.add_field(name=ctx.author.name, value=f"**{author_health}HP**", inline=True)
        embed.add_field(name=member.name, value=f"**{member_health}HP**", inline=True)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        while (author_health >= 1) and (member_health >= 1):
            b_round += 1
            author_damage  = random.randint(12, 22)
            member_damage = random.randint(12, 22)
            author_mortal = random.randint(25, 35)
            member_mortal = random.randint(25, 35)
            author_heal = random.randint(6, 12)
            member_heal = random.randint(6, 12)
            random_act = random.randint(1, 6)
            random_act1 = random.randint(1, 6)
            if author_health == 0:
                pass
            elif member_health == 0:
                pass
            else:
                if random_act <= 5:
                    r = random.randint(1, 6)
                    #Mortal Hit
                    if r == 1:
                        mortal = author_damage + author_mortal
                        if mortal >= member_health:
                            mortal = member_health
                        member_health -= mortal
                        embed = discord.Embed( title=f'Round {b_round}', description = f"!!Mortal Hit!! **{ctx.author.name}** punched **{member.name}** for **{mortal} DMG**", colour=0x997300)
                        embed.add_field(name=ctx.author.name, value=f"**{author_health} HP**", inline=True)
                        embed.add_field(name=member.name, value=f"**{member_health} HP**", inline=True)
                        await msg.edit(embed=embed)
                        await asyncio.sleep(5)
                    else:
                        if member_damage >= member_health:
                            author_damage = member_health
                        member_health -= author_damage
                        embed = discord.Embed( title=f'Round {b_round}', description = f"**{ctx.author.name}** punched **{member.name}** for **{author_damage} DMG**", colour=0x800000)
                        embed.add_field(name=ctx.author.name, value=f"**{author_health} HP**", inline=True)
                        embed.add_field(name=member.name, value=f"**{member_health} HP**", inline=True)
                        await msg.edit(embed=embed)
                        await asyncio.sleep(5)
                else:
                    author_health += author_heal
                    embed = discord.Embed( title=f'Round {b_round}', description = f"**{ctx.author.name}** healed himself for **{author_heal} HP**", colour=0x0073e6)
                    embed.add_field(name=ctx.author.name, value=f"**{author_health} HP**", inline=True)
                    embed.add_field(name=member.name, value=f"**{member_health} HP**", inline=True)
                    await msg.edit(embed=embed)
                    await asyncio.sleep(5)
            if member_health == 0:
                pass
            elif author_health == 0:
                pass
            else:
                if random_act1 <= 5:
                    r1 = random.randint(1, 6)
                    #Mortal Hit
                    if r1 == 1:
                        mortal = member_damage + member_mortal
                        if mortal >= author_health:
                            mortal = author_health
                        author_health -= mortal
                        embed = discord.Embed( title=f'Round {b_round}', description = f"!!Mortal Hit!! **{member.name}** punched **{ctx.author.name}** for **{mortal} DMG**", colour=0xffff00)
                        embed.add_field(name=ctx.author.name, value=f"**{author_health} HP**", inline=True)
                        embed.add_field(name=member.name, value=f"**{member_health} HP**", inline=True)
                        await msg.edit(embed=embed)
                        await asyncio.sleep(5)
                    else:
                        if member_damage >= author_health:
                            member_damage = author_health
                        author_health -= member_damage
                        embed = discord.Embed( title=f'Round {b_round}', description = f"**{member.name}** punched **{ctx.author.name}** for **{member_damage} DMG**", colour=0xcc0066)
                        embed.add_field(name=ctx.author.name, value=f"**{author_health} HP**", inline=True)
                        embed.add_field(name=member.name, value=f"**{member_health} HP**", inline=True)
                        await msg.edit(embed=embed)
                        await asyncio.sleep(5)
                else:
                    member_health += member_heal
                    embed = discord.Embed( title=f'Round {b_round}', description = f"**{member.name}** healed himself for **{member_heal} HP**", colour=0x00ffff)
                    embed.add_field(name=ctx.author.name, value=f"**{author_health} HP**", inline=True)
                    embed.add_field(name=member.name, value=f"**{member_health} HP**", inline=True)
                    await msg.edit(embed=embed)
                    await asyncio.sleep(5)
        if member_health < author_health:
            embed = discord.Embed(title=f"{ctx.author.name} Won!", description = f"Good job **{ctx.author.name}** you won some applause!", colour = 0x66ccff)
            embed.add_field(name=ctx.author.name, value=f"{author_health} HP", inline=True)
            embed.add_field(name=member.name, value=f"{member_health} HP", inline=True)
            await msg.edit(embed=embed)
        elif member_health > author_health:
            embed = discord.Embed(title=f"{member.name} Won!", description = f"Good job **{member.name}** you won Nothing!", colour = 0x66ccff)
            embed.add_field(name=member.name, value=f"{member_health} HP", inline=True)
            embed.add_field(name=ctx.author.name, value=f"{author_health} HP", inline=True)
            await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))