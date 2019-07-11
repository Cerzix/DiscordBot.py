import discord
from discord.ext import commands
from discord.utils import get

class roles ()

def setup(bot):
    bot.add_cog(Basic(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file

@bot.command(pass_context=True)
async def addrole(ctx, role_id):
    user = ctx.message.author
    role = discord.utils.get(ctx.message.guild.roles, name = role_id)
    await user.add_roles(role)
    await ctx.send( "Role: " + "**" + str(role) + "**" + " has been assigned.")


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name = "Adventurer")
    await member.add_roles(role)