import nextcord
import asyncio
import re
from nextcord.ext import commands
from datetime import datetime

from utils.helpers import *

log_channel_id = 889293946801516554
color = 0xc48aff
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class Mute_(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setmute(self, ctx: commands.Context, *, role_name: nextcord.Role):
        guild_id = ctx.author.guild.id
        role = role_name
        role_id = role.id

        cursor = await self.bot.db.execute("UPDATE mute SET role_id = ? WHERE guild_id = ?", (role_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO mute (role_id, guild_id) VALUES(?, ?)", (role_id, guild_id))
            await self.bot.db.commit()

        embed = nextcord.Embed(
            title = "Mute Role Changed -",
            description = f"<@&{role_id}> has been assigned as the mute role for {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @setmute.error
    async def setmute_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Role Not Found!",
                description = f"• That role wasn't found. Check your spelling, or simply just ping the role you want to assign as the muted role. Example: `{ctx.prefix}setmute @Muted`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Role Given!",
                description = f"• It seems you didn't provide a role for me. Heres an example on how to use the command: `{ctx.prefix}setmute @Muted`, or do `{ctx.prefix}help` for help."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def delmute(self, ctx: commands.Context, NULL:int = None):
        guild_id = ctx.author.guild.id
        cursor = await self.bot.db.execute("INSERT OR IGNORE INTO mute (guild_id, role_id) VALUES (?,?)", (guild_id, NULL))
        await self.bot.db.commit()
        embed = nextcord.Embed(
            title = "Mute Role Deleted -",
            description = f"The mute role for {ctx.author.guild.name} has been deleted.",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @delmute.error
    async def delmute_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def muterole(self, ctx: commands.Context):
        guild_id = ctx.author.guild.id
        async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            role_id = data[0]

        embed = nextcord.Embed(
            title = f"Mute role for {ctx.author.guild.name}",
            description= f'<@&{role_id}>'
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @muterole.error
    async def muterole_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Role Set!",
                description = f"• It seems you haven't set a muted role yet. Please go do that with `{ctx.prefix}setmute` before running this command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, ctx, member:nextcord.Member=None, *, argument=None): 
        log = self.bot.get_channel(log_channel_id)
        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Member!",
                description = f"• Please provide a member for me to mute. Example: `{ctx.prefix}mute @bob 3d 5h 7m 9s."
            )
            await ctx.send(embed=embed)

        elif argument == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Time!",
                description = f"• Please provide an amount of time for me to mute {member} for. Example: `{ctx.prefix}mute @bob 3d 5h 7m 9s`."
            )
            await ctx.send(embed=embed)

        elif argument != None and member != None:
            args = argument.lower()
            matches = re.findall(time_regex, args)
            time = 0
            for v, k in matches:
                time += time_dict[k]*float(v)
            guild_id = ctx.author.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = ctx.guild.get_role(role_id)
            role = nextcord.utils.get(ctx.guild.roles, name=f"{role_name}")
            await member.add_roles(role)
            embed = nextcord.Embed(
                title = f"**User {member} has been muted for {argument}.**",
                colour = nextcord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                args = argument.lower()
                matches = re.findall(time_regex, args)
                time = 0
                for v, k in matches:
                    time += time_dict[k]*float(v)
                guild_id = ctx.author.guild.id
                async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                    data = await cursor.fetchone()
                    role_id = data[0]
                role_name = ctx.guild.get_role(role_id)
                role = nextcord.utils.get(ctx.guild.roles, name=f"{role_name}")
                await member.add_roles(role)
                embed = nextcord.Embed(
                    title = f"**User {member} has been muted for {argument}.**",
                    colour = nextcord.Colour.red()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)

            if time:
                await asyncio.sleep(time)
                await member.remove_roles(role)

    
    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Role Set!",
                description = f"• It seems you haven't set a muted role yet. Please go do that with `{ctx.prefix}setmute` before running this command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command(aliases = ["mute"])
    @commands.has_permissions(manage_roles=True)
    async def mutecommand(self, ctx: commands.Context, member:nextcord.Member=None, *, reason=None): 
        log = self.bot.get_channel(log_channel_id)
        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Member!",
                description = f"• Please provide a member for me to mute. Example: `{ctx.prefix}mute @bob 3d 5h 7m 9s."
            )
            await ctx.send(embed=embed)

        elif member != None and reason != None:
            guild_id = ctx.author.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = ctx.guild.get_role(role_id)
            role = nextcord.utils.get(ctx.guild.roles, name=f"{role_name}")
            await member.add_roles(role)
            embed = nextcord.Embed(
                title = f"**User {member} has been muted for {reason}.**",
                colour = nextcord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**User {member} has been muted for {reason}.**",
                    colour = nextcord.Colour.red()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)
            
        elif member != None and reason == None:
            guild_id = ctx.author.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = ctx.guild.get_role(role_id)
            role = nextcord.utils.get(ctx.guild.roles, name=f"{role_name}")
            await member.add_roles(role)
            embed = nextcord.Embed(
                title = f"**User {member} has been muted with no given reason.**",
                colour = nextcord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                guild_id = ctx.author.guild.id
                async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                    data = await cursor.fetchone()
                    role_id = data[0]
                role_name = ctx.guild.get_role(role_id)
                role = nextcord.utils.get(ctx.guild.roles, name=f"{role_name}")
                await member.add_roles(role)
                embed = nextcord.Embed(
                    title = f"**User {member} has been muted with no given reason.**",
                    colour = nextcord.Colour.red()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @mutecommand.error
    async def mutecommand_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Role Set!",
                description = f"• It seems you haven't set a muted role yet. Please go do that with `{ctx.prefix}setmute` before running this command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx: commands.Context, member: nextcord.Member=None):
        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Member!",
                description = f"• Please provide a member for me to mute. Example: `{ctx.prefix}unmute @bob`."
            )
            await ctx.send(embed=embed)
        
        elif member != None:
            log = self.bot.get_channel(log_channel_id)
            guild_id = ctx.author.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = ctx.guild.get_role(role_id)
            role = nextcord.utils.get(ctx.guild.roles, name=f"{role_name}")
            embed = nextcord.Embed(
                title = f"**User {member} has been unmuted.**",
                colour = nextcord.Colour.green()
            )
            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)
            await member.remove_roles(role)

            if ctx.guild.id == 889027208964874240:
                embed = nextcord.Embed(
                    title = f"**User {member} has been unmuted.**",
                    colour = nextcord.Colour.green()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @unmute.error
    async def unmute_error(self, ctx):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Mute_(bot))