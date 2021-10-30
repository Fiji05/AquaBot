import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
import aiosqlite
from datetime import datetime

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class Prefix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def setprefix(self, ctx: commands.Context,*, reason=None):
        guild_id = ctx.author.guild.id

        if reason == None:
            await ctx.send(f"{ctx.author.mention}, you did not give a prefix for me to change to. Please do something like this - `{ctx.prefix}setprefix hh`")

        cursor = await self.bot.db.execute("UPDATE prefix SET prefix = ? WHERE guild_id = ?", (reason, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO prefix (prefix, guild_id) VALUES(?, ?)", (reason, guild_id))
            await self.bot.db.commit()

        embed = nextcord.Embed(
            title = "Prefix Changed -",
            description = f"Prefix has been changed to `{reason}` for {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Prefix(bot))