import discord
import datetime

from discord.ext import commands


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def dateDiff(self, first, second):
        dayDiffInSecond = (first-second).total_seconds()
        year = divmod(dayDiffInSecond, 3.154e+7)
        months = divmod(year[1], 2.628e+6)
        days = divmod(months[1], 86400)
        return int(year[0]), int(months[0]), int(days[0])

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        user = ctx.author if not user else user
        roles = [role for role in user.roles]

        def status_to_emoji(status):
            switch = {
                'online': '🟢',
                'offline': '⚫',
                'idle': '🟡',
                'dnd': '⛔',
            }
            return switch.get(status.value.lower(), '⚫')

        year, months, days = self.dateDiff(
            datetime.datetime.now(), user.created_at)

        embed = discord.Embed(title=f'{user}', color=user.color.value)
        embed.add_field(name="User Information",
                        value=f'Created: {year} years, {months}months, {days}days ago\nProfile<@{user.id}>\nID: {user.id}', inline=False)

        year, months, days = self.dateDiff(
            datetime.datetime.now(), user.joined_at)

        embed.add_field(name="Menber Information",
                        value=f'Joined: {year} years, {months}months, {days}days ago\nRoles{" ".join(role.mention for role in roles)}', inline=False)
        embed.add_field(name='Top Role', value=f'{user.top_role.mention}')
        embed.add_field(
            name='Type', value=f'{"🟢" if user.bot == False else "🔴"} User\n{"🟢" if user.bot else "🔴"} Bot', inline=False)
        embed.add_field(
            name="Status", value=f'{status_to_emoji(user.desktop_status)} Destop\n{status_to_emoji(user.web_status)} Web\n{status_to_emoji(user.mobile_status)} Mobile')

        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(
            text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def server(self, ctx):
        embed = discord.Embed()
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        year, months, days = self.dateDiff(
            datetime.datetime.now(), ctx.guild.created_at)
        embed.add_field(
            name="Server information", value=f'Created: {year} years, {months}months, {days}days ago\nOwner: {ctx.guild.owner}\nVoice region: {ctx.guild.region}', inline=False)
        embed.add_field(
            name="Channel counts", value=f'Category channels: {len(ctx.guild.categories)}\nText channels: {len(ctx.guild.text_channels)}\nVoice channels: {len(ctx.guild.voice_channels)}', inline=False)
        embed.add_field(
            name="Channel counts", value=f'Members: {ctx.guild.member_count}\nRoles: {len(ctx.guild.roles)}', inline=False)
        embed.set_footer(
            text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
    print("Profile is loaded")
