import discord, aiosqlite, asyncio, re, typing
from discord.ext import commands
from discord.utils import get
from ..function import MainDef


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await CheckMutedRole(guild=guild)


    #kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member=None, *, msg = 'Nothing'):
        down = await MainDef.downCheck(self, ctx=ctx, file='moderation') #Check for downtime
        if down == 'down': #Get the "down" text so the command is not executing
            return

        author = ctx.author

        if member != None: #Check if member is not None
            if member != author: #Check if member is not author
                if author.top_role < member.top_role or author.top_role == member.top_role: #Check if author role is smaller or equal with member
                    embed = discord.Embed(description=f"**{author.name}**, you can't kick **{member.name}**", colour=0x660000)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f"**{member}** got kicked for **{msg}**", colour=0x004d99)
                    await ctx.send(embed=embed)

                    try: #Trying to send a private message
                        embed = discord.Embed(title=ctx.guild.name, description=f"Kicked by **{author}** for **{msg}**", colour=0xb30047)
                        await member.send(embed=embed)
                    except:
                        pass

                    await ctx.guild.kick(user=member, reason=f"by {author} for {msg}") #Kick the user with reason
            else:
                embed = discord.Embed(description=f"Sorry **{author.name}**, but you can't kick yourself.", colour=0x660000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'**{author.name}**, You need to specify an user.', colour=0x660000)
            await ctx.send(embed=embed)

        
    #ban command 
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, memberID:typing.Optional[int], member:typing.Optional[discord.Member], *, reason='Nothing'):  
        down = await MainDef.downCheck(self, ctx=ctx, file='moderation')
        if down == 'down':
            return
        author = ctx.author
        valid = 0
        if memberID is not None:
            member = await self.bot.fetch_user(memberID)
            valid = 1
        if member != None:
            if member != author:
                if valid == 0:
                    if author.top_role < member.top_role or author.top_role == member.top_role:
                        embed = discord.Embed(description=f"Sorry **{author.name.title()}**, but you can't ban **{member.name.title()}**", colour=0x660000)
                        await ctx.send(embed=embed)
                        return
                embed = discord.Embed(description=f"**{member}** got banned for **{reason}**", colour=0x004d99)
                embed.set_footer(text=f"banned by {author}")
                await ctx.send(embed=embed)
                try:
                    embed = discord.Embed(title=author.guild, description=f"banned by **{author}** for **{reason}**", colour=0xb30000)
                    await member.send(embed=embed)
                except:
                    pass
                await author.guild.ban(user=member, reason=f"by {author} for {reason}")
            else:
                embed = discord.Embed(description="You can't ban yourself.", colour=0x660000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="You need to ban someone!", colour=0x660000)
            await ctx.send(embed=embed)


    #Unban command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unban(self, ctx):
        bannedUsers = await ctx.guild.bans()
        for user in bannedUsers:
            await ctx.send(user)

    #Chat Purge
    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, channel:typing.Optional[discord.TextChannel], limit=5):
        channel = channel or ctx.channel
        await ctx.message.delete()
        await channel.purge(limit=limit)
        embed = discord.Embed(description=f"Purged **{limit}** messages", colour=0x003d99)
        msg = await channel.send(embed=embed)
        await msg.delete(delay=3)

    #Chat Lock
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel:typing.Optional[discord.TextChannel], reason=None):
        channel = channel or ctx.channel
        overwrite = discord.PermissionOverwrite(send_messages=False)
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.channel.type(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(title = None, description = f"**{ctx.channel}** is locked...", colour = 0x0054ff)
        embed.set_footer(text = f'Chat locked by {ctx.author}')
        await ctx.send(embed=embed)

    #Chat unLock
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):

        if ctx.author.id == 0:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
            embed = discord.Embed(title = None, description = f"**{ctx.channel}** is unlocked...", colour = 0x0054ff)
            embed.set_footer(text = f'Chat unlocked by {ctx.author}')
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry but this command is in maintenance.")

    
    #Nuke command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel:discord.TextChannel=None):
        channel_to_nuke = channel or ctx.channel

        embed = discord.Embed(title=None, description = f"**{ctx.author}**, you need to **Accept** to Nuke **{channel_to_nuke}**!")
        msg = await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.content.lower() in ['accept', 'accept!']
        
        try:
            await self.bot.wait_for("message", check=check, timeout=15.0)
        
        except asyncio.TimeoutError:
            embed = discord.Embed(description =f"**{ctx.author.name}**, didn't accept...", colour = 0x660000)
            await msg.delete()
            msg = await ctx.send(embed=embed)
            return

        await msg.delete()

        previous_channel = channel_to_nuke
        pos_previous = channel_to_nuke.position
        new_channel = await previous_channel.clone()
        await new_channel.edit(position=pos_previous)
        await previous_channel.delete()

        embed = discord.Embed(title=f"Channel Nuked by **{ctx.author}**", colour = 0x0054ff)
        embed.set_image(url="https://media.giphy.com/media/cRBRQf8syLUyY/giphy.gif")
        await new_channel.send(embed=embed)
        

    #Mute Command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member:discord.Member, *, reason = 'Nothing'):
        if member is not None: 
            if ctx.author is not member:
                muted_role = await CheckMutedRole(guild=ctx.author.guild)
                if muted_role == 'error0':
                    return

                if muted_role in member.roles:
                    embed = discord.Embed(title=None, description = f"**{member.name}**, is already muted!", colour = 0x660000)
                    await ctx.send(embed=embed)
                    return
                    
                if ctx.author.top_role < member.top_role or ctx.author.top_role == member.top_role:
                    embed = discord.Embed(title= None, description = f"**{ctx.author.name}**, you can't mute higher/equal members.", colour = 0x0054ff)
                    await ctx.send(embed=embed)
                
                else:

                    embed = discord.Embed(title=None, description = f"**{member}** got muted for **{reason}**", colour = 0x0054ff)
                    await ctx.send(embed=embed)
                    await member.add_roles(muted_role)

            else:
                embed = discord.Embed(tile=None, description = f"**{ctx.author},** you can't mute yourself.", colour = 0x660000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"**{ctx.author.name}**, You need to tag someone!", color = 0x660000)
            await ctx.send(embed = embed)

    
    #TempMute command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def tempmute(self, ctx, member: discord.Member, time, reason="Nothing"):
        time_transformed = transformTime(time=time)
       
        if str(ctx.author.id) == '658111206711623686' or str(ctx.author.id) == '385485309246177290':
            if int(time_transformed) < 1814400:
                print("idc")
            else:
                await ctx.send('Please enter a lower amount of time.')
        else:
            await ctx.send("We are working on this command...Until that you can't use it :slight_smile:")

    
    #Unmute Command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member:discord.Member):
        if member is not None:
            if ctx.author is not member:
                muted_role = await CheckMutedRole(guild=ctx.author.guild)
                if muted_role == "error0":
                    return
                
                if muted_role in member.roles:
                    
                    embed = discord.Embed(title=None, description = f"**{member}** is now unmuted!", colour = 0x0054ff)
                    await ctx.send(embed=embed)
                    await member.remove_roles(muted_role)
                
                else:
                    embed = discord.Embed(tile=None, description = f"**{member.name}**, is not muted!", colour = 0x660000)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(tile=None, description = f"**{ctx.author}**, you can't unmute yourself...Nice try.", colour = 0x660000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"**{ctx.author.name}**, You need to tag someone!", color = 0x660000)
            await ctx.send(embed = embed)


def transformTime(time):
    if str(time[-1]).isdigit():  # check for letters
        time_transformed = int(time)
    else:
        if str(time).endswith("s") or str(time).endswith("second") or str(time).endswith(" second") or str(
                time).endswith(" seconds") or str(time).endswith("seconds"):
            print(str(time).split(" |s")[0])
            time_num = int(re.split(" |s", str(time))[0])
            time_transformed = int(time_num)

        elif str(time).endswith("m") or str(time).endswith("minute") or str(time).endswith(" minute") or str(
                time).endswith(" minutes") or str(time).endswith("minutes"):
            time_num = int(re.split(" |m", str(time))[0])
            time_num *= 60
            time_transformed = int(time_num)

        elif str(time).endswith("h") or str(time).endswith("hour") or str(time).endswith(" hour") or str(
                time).endswith(" hours") or str(time).endswith("hours"):
            time_num = int(re.split(" |h", str(time))[0])
            time_num *= 3600
            time_transformed = int(time_num)

        elif str(time).endswith("d") or str(time).endswith("day") or str(time).endswith(" day") or str(
                time).endswith(" days") or str(time).endswith("days"):
            time_num = int(re.split(" |d", str(time))[0])
            time_num *= 216000
            time_transformed = int(time_num)
        elif str(time).endswith("w") or str(time).endswith("week") or str(time).endswith(" week") or str(
                time).endswith(" weeks") or str(time).endswith("weeks"):
            time_num = int(re.split(" |w", str(time))[0])
            time_num *= 604800
            time_transformed = int(time_num)
        else:
            return False
    return time_transformed

async def CheckMutedRole(guild):
    if get(guild.roles, name="Muted"):
        return
    else:
        try: 
            muted_role = await guild.create_role(name="Muted", colour =discord.Colour.greyple())
            
            for text_channel in guild.text_channels:
                await text_channel.set_permissions(muted_role, send_messages=False)
            for voice_channel in guild.voice_channels:
                await voice_channel.set_permissions(muted_role, speak = False)
            return muted_role
            
        except:
            await guild.send("I couldn't create the role **Muted**")
            return "error0"

def setup(bot):
    bot.add_cog(Moderation(bot))