import discord
import requests
from discord.ext import commands
from discord.utils import get

api_url = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
app_url = "https://maker.ifttt.com/trigger/bitcoin/with/key/bz7bCPAUZGqVtlhEoDItFy"
token = "NTk2Mjk1MDkxOTMzNDEzNDE2.XR3dOQ.9jeCsp5c6Mz-iYFGmEUSyzQ74RQ"
botname = "test-bot"

bot = commands.Bot(command_prefix='!', description='A bot that greets the user back.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='!help'))

@bot.command(pass_context=True)
async def addrole(ctx, role_id):
    user = ctx.message.author
    role = discord.utils.get(ctx.message.guild.roles, name = role_id)
    await user.add_roles(role)
    await ctx.send( "Role: " + "**" + str(role) + "**" + " has been assigned.")

#@bot.command(pass_context=True)
#async def delpoll(self, poll_id):
#            await self.message.channel.purge(limit=100, check=id_check)

@bot.command(pass_context=True)
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

    if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
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

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name = "Adventurer")
    await member.add_roles(role)

bot.run(token)