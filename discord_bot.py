import discord
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
import json

#--------------------Main------------------------

with open('./config/config.json', 'r') as f:
    config = json.load(f)

token = config['token']
botname = config['info']['name']

vclient = discord.VoiceState

bot = commands.Bot(command_prefix='!', description='The Official GameHuntGuild Bot, written by Cerzix', owner_id='206811900317663232', case_insensitive=True)

#---------------Cogs Experiments-----------------

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        await bot.change_presence(activity=discord.Game(name='!help'))
        
    @commands.command(pass_context=True)
    async def creator(self, ctx):
        user = ctx.message.guild.get_member(206811900317663232)
        creator = discord.Embed(title="This bot was written by:", description='@Cerzix#0017', color=0xC27C0E)
        creator.set_thumbnail(url=user.avatar_url)
        creator.set_footer(text="also known as Eevee")
        print(user.avatar_url)
        await ctx.message.channel.send(embed=creator)

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def addrole(self, ctx, role_id):
        user = ctx.message.author
        try:
            role = discord.utils.get(ctx.message.guild.roles, name = role_id)
        except:
            ctx.send("Role" + str(role) + "not found")
        await user.add_roles(role)
        await ctx.send( "Role: " + "**" + str(role) + "**" + " has been assigned.")

   
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name = "Adventurer")
        await member.add_roles(role)

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, usage="Usage: !poll <Question> | Answer1 Answer2 etc...")
    async def poll(self, ctx, question, *options: str):
        question_body = ctx.message.content.split(" ", 1)
        question_head = question_body[1].split("|")[0]
        question = ctx.message.content.split("|")[1]
        options = question.split(" ")
        del options[0]
        await ctx.message.delete()
        if len(options) <= 1:
            await ctx.message.channel.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.message.channel.send('You cannot make a poll for more than 10 things!')
            return
        if options[0] == "yes" and options[1] == "no":

            reactions = ['✅', '❌']

        else:

            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question_head, description=''.join(description))
        react_message = await ctx.message.channel.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def join(self, ctx):
        author = ctx.message.author
        voice_channel = author.voice.channel
        vclient = await voice_channel.connect()
        return vclient

    @commands.command(pass_context=True)
    async def play(self, ctx, url, vc = vclient):
        author = ctx.message.author
        voice_channel = author.voice.channel
        if  vc.channel is "":
            channel = await voice_channel.connect()
            player = await vc.create_ytdl_player(url)
            player.play()
        else:
            player = await vc.create_ytdl_player(url)
            player.play()

        def is_connected(ctx):
            voice_client = ctx.author.voice.channel
            return voice_client.is_connected()

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(pass_context=True, usage="Usage: !invite <Announcement> | <Role to assign> <Reaction Emoji>")
    async def invite(self, ctx):
        body = ctx.message.content.split(" ", 1)
        content = body[1].split("|")[0]
        rest = body[1].split("|")[1]
        role = rest.split(" ")[1]
        emoji = rest.split(" ")[2]
        emojis = await ctx.message.guild.fetch_emojis()
        for emj in emojis:
            if emj.name == emoji:
                emoji = emj
        sender_pic = ctx.message.author.avatar_url
        await ctx.message.delete()
        reaction = emoji
        role_assigned = "By reacting you will receive the following Role: " + role
        event = discord.Embed(title=content, description=role_assigned)
        event.set_thumbnail(url=sender_pic)
        event_message = await ctx.message.channel.send(embed=event)
        await event_message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload.user_id)
        print(payload.message_id)
        if payload.user_id == bot.user.id:
            return #do nothing
        else:
            msg_id = payload.message_id
            channel = bot.get_channel(payload.channel_id)
            print(channel)
            msg = await channel.fetch_message(msg_id)
            msg_desc = (msg.embeds[0].description).split(":")[1]
            role = msg_desc.split(" ")[1]
            role_id = discord.utils.get(bot.guilds[0].roles, name = role)
            user = bot.guilds[0].get_member(payload.user_id)
            print(user.roles)
            if role_id in user.roles:
                #User already has the role
                return
            else:
                print("add role")
                await user.add_roles(role_id)

    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print(payload.user_id)
        print(payload.message_id)
        if payload.user_id == bot.user.id:
            return #do nothing
        else:
            msg_id = payload.message_id
            channel = bot.get_channel(payload.channel_id)
            print(channel)
            msg = await channel.fetch_message(msg_id)
            msg_desc = (msg.embeds[0].description).split(":")[1]
            role = msg_desc.split(" ")[1]
            role_id = discord.utils.get(bot.guilds[0].roles, name = role)
            user = bot.guilds[0].get_member(payload.user_id)
            print(user.roles)
            if role_id in user.roles:
                await user.remove_roles(role_id)
            else:
                #User doesnt have the role
                return

#-------------------Commands-----------------------


#@bot.command(pass_context=True)
#async def delpoll(self, poll_id):
#            await self.message.channel.purge(limit=100, check=id_check)

# Role-Self-Assign




# # ------------------------

#         question_body = ctx.message.content.split(" ", 1)
#         question_head = question_body[1].split("|")[0]
#         print(question_body)
#         question = ctx.message.content.split("|")[1]
#         print(question)
#         options = question.split(" ")

#         del options[0]

#         print(options)

#         await ctx.message.delete()
#         if len(options) <= 1:
#             await ctx.message.channel.send('You need more than one option to make a poll!')
#             return
#         if len(options) > 10:
#             await ctx.message.channel.send('You cannot make a poll for more than 10 things!')
#             return
#         if options[0] == "yes" and options[1] == "no":

#             reactions = ['✅', '❌']

#         else:

#             reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

#         description = []
#         for x, option in enumerate(options):
#             description += '\n {} {}'.format(reactions[x], option)
#         embed = discord.Embed(title=question_head, description=''.join(description))
#         react_message = await ctx.message.channel.send(embed=embed)
#         for reaction in reactions[:len(options)]:
#             await react_message.add_reaction(reaction)
#         embed.set_footer(text='Poll ID: {}'.format(react_message.id))
#         await react_message.edit(embed=embed)


#-------------------Events---------------------


#-----------------Load Cogs--------------------

bot.add_cog(Basic(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Polls(bot))
bot.add_cog(Events(bot))

#-------------------Finish---------------------

bot.run(token)
