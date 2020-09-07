import discord
from discord import embeds
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        embed = discord.Embed()
        if ctx.author.guild_permissions.kick_members:
            await user.kick(reason=reason)
            embed.description = f'Kick {user}: {reason}.'
        else:
            embed.description = 'Sorry you have not permission.'
        embed.set_footer(
            text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason=None, delete_message_days=7):
        embed = discord.Embed()
        if ctx.author.guild_permissions.ban_members:
            await user.ban(reason=reason, delete_message_days=delete_message_days)
            embed.description = f'Banned {user}: {reason}.'
        else:
            embed.description = 'Sorry you have not permission.'
        embed.set_footer(
            text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def unban(self, ctx, user):
        embed = discord.Embed()
        if ctx.author.guild_permissions.ban_members:
            banned_users = await ctx.guild.bans()
            user_name, user_discriminator = user.split('#')
            if len(banned_users) != 0:
                for ban_user in banned_users:
                    if (ban_user.user.name, ban_user.user.discriminator) == (user_name, user_discriminator):
                        await ctx.guild.unban(ban_user.user)
                        embed.description = f'Unbanned {ban_user.user.name}#{ban_user.user.discriminator}'
                        break
                    else:
                        embed.description = f'User {user_name}#{user_discriminator} doesn\'t exist.'
            else:
                embed.description = 'No user in the ban list.'

        else:
            embed.description = 'Sorry you have not permission.'
        embed.set_footer(
            text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def banned(self, ctx):
        embed = discord.Embed()
        if ctx.author.guild_permissions.ban_members:
            banned_users = await ctx.guild.bans()
            desc = ""
            for ban_user in banned_users:
                user = ban_user.user
                desc = f'{user.name}#{user.discriminator} - {ban_user.reason}\n'
            if len(banned_users) != 0:
                embed.description = desc
            else:
                embed.description = 'No user has been ban.'
        else:
            embed.description = 'Sorry you have not permission.'
        embed.set_footer(
            text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx, amount=1):
        embed = discord.Embed()
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.purge(limit=amount)
            embed.description = f'{amount} messages has been deleted.'
        else:
            embed.description = 'Sorry you have not permission.'
        embed.set_footer(
            text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
    print("Moderation is loaded")
