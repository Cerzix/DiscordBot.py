import discord
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL

#-----------------Main---------------------------

api_url = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
app_url = "https://maker.ifttt.com/trigger/bitcoin/with/key/bz7bCPAUZGqVtlhEoDItFy"
token = "token goes here"
botname = "GHG-Bot"
vclient = discord.VoiceState

bot = commands.Bot(command_prefix='!', description='The Official GameHuntGuild Bot, written by Cerzix', owner_id='206811900317663232', case_insensitive=True)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='!help'))

#---------------Commands------------------

@bot.command(pass_context=True, usage="Usage: !poll <Question> | Answer1 Answer2 etc...")
async def poll(ctx, question, *options: str):
    question_body = ctx.message.content.split(" ", 1)
    question_head = question_body[1].split("|")[0]
    print(question_body)
    question = ctx.message.content.split("|")[1]
    print(question)
    options = question.split(" ")

    del options[0]

    print(options)

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

#@bot.command(pass_context=True)
#async def delpoll(self, poll_id):
#            await self.message.channel.purge(limit=100, check=id_check)

# Role-Self-Assign

@bot.command(pass_context=True)
async def addrole(ctx, role_id):
    user = ctx.message.author
    try:
        role = discord.utils.get(ctx.message.guild.roles, name = role_id)
    except:
        ctx.send("Role" + str(role) + "not found")
    await user.add_roles(role)
    await ctx.send( "Role: " + "**" + str(role) + "**" + " has been assigned.")

@bot.command(pass_context=True)
async def creator(ctx):
    user = ctx.message.guild.get_member(206811900317663232)
   #pfp = user.avatar
    creator = discord.Embed(title="This bot was written by:", description='@Cerzix#0017', color=0xC27C0E)
    creator.set_thumbnail(url=user.avatar_url)
    creator.set_footer(text="also known as Eevee")
    print(user.avatar_url)
    await ctx.message.channel.send(embed=creator)

@bot.command(pass_context=True)
async def join(ctx):
    author = ctx.message.author
    voice_channel = author.voice.channel
    vclient = await voice_channel.connect()
    return vclient

@bot.command(pass_context=True)
async def play(ctx, url, vc = vclient):
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

@bot.command(pass_context=True, usage="Usage: !invite <Announcement> | <Role to assign> <Reaction Emoji>")
async def invite(ctx):
    body = ctx.message.content.split(" ", 1)
    content = body[1].split("|")[0]
    rest = body[1].split("|")[1]
    role = rest.split(" ")[1]
    emoji = rest.split(" ")[2]
    emojis = await ctx.message.guild.fetch_emojis()
    for emj in emojis:
        print(emj)
        if emj.name == emoji:
            print(emj.name)
            emoji = emj
    sender_pic = ctx.message.author.avatar_url
    await ctx.message.delete()
    reaction = emoji
    event = discord.Embed(title=content)
    event.set_thumbnail(url=sender_pic)
    event_message = await ctx.message.channel.send(embed=event)
    await event_message.add_reaction(reaction)

#-------------------Events---------------------

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name = "Adventurer")
    await member.add_roles(role)

@bot.event
async def on_raw_reaction_add(payload):
    print("payload_id" + payload.message_id)

#-------------------Finish---------------------

bot.run(token)
