import nextcord
from nextcord import Color
from nextcord.ext import commands
import aiosqlite
import math
import asyncio
from datetime import datetime

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff


class messageCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_message(self, message):
        self.bot.multiplier = 1
        guild_id = message.author.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                return
                
        if channel_id == None or 0 and not data:
            return

        cursor = await self.bot.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1)) 

        if cursor.rowcount == 0:
            await self.bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            cur = await self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / self.bot.multiplier
        
            if lvl.is_integer():
                channel = self.bot.get_channel(channel_id)
                await channel.send(f"{message.author.mention} well done! You're now level: {int(lvl)}.")

        await self.bot.db.commit()


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setlvl(self, ctx: commands.Context, *, channel_name: nextcord.TextChannel):
        guild_id = ctx.author.guild.id
        channel = channel_name
        channel_id = channel.id

        cursor = await self.bot.db.execute("UPDATE level_channel SET channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO level_channel (channel_id, guild_id) VALUES(?, ?)", (channel_id, guild_id))
            await self.bot.db.commit()

        embed = nextcord.Embed(
            title = "Level Channel Changed -",
            description = f"<#{channel_id}> has been assigned as the level-up message channel for {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @setlvl.error
    async def setlvl_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lvlreset(self, ctx: commands.Context):
        guild_id = ctx.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = nextcord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed)
                
        if channel_id == None or 0 and not data:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                color=0xa3a3ff, 
                title = ":warning: ALERT :warning: ", 
                description=f"{ctx.author.mention}, are you sure you want to delete the levels for everyone in this server? y/n",
            )
            embed.set_footer(text="Send either `y` or `n` in order to continue.")
            
            await ctx.send(embed=embed)

            a = ["y", "yes", "Yes", "YEs", "YES"]
            b = ["n", "no", "No", "NO"] 

            msg = await self.bot.wait_for('message', check=lambda message:message.author == ctx.author and message.channel.id == ctx.channel.id)
            if msg.content in a:
                embed = nextcord.Embed(
                    title=f"All levels have just been DELETED!", 
                    description=f"Levels deleted by: {ctx.author.name}#{ctx.author.discriminator}",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await self.bot.db.execute("DELETE FROM guildData WHERE guild_id = ?", (guild_id,))
                await ctx.send(embed=embed)

            elif msg.content in b:
                embed = nextcord.Embed(
                    title = ":red_circle: NOTICE :red_circle:", 
                    description = f"All levels were NOT deleted!",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)

            else:
                embed = nextcord.Embed(
                    title = ":red_circle: NOTICE :red_circle:", 
                    description = "All levels were NOT deleted!",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)


    @lvlreset.error
    async def lvlreset_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def dellevel(self, ctx: commands.Context, NULL:int = None):
        guild_id = ctx.author.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = nextcord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed)
                
        if channel_id == None or 0 and not data:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        else:
            cursor = await self.bot.db.execute("UPDATE level_channel SET channel_id = NULL WHERE guild_id = ?", (guild_id,))
            await self.bot.db.commit()
            embed = nextcord.Embed(
                title = "Leveling Channel Deleted -",
                description = f"The level channel for {ctx.author.guild.name} has been deleted.",
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @dellevel.error
    async def dellevel_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lvlchannel(self, ctx: commands.Context):
        guild_id = ctx.author.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = nextcord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed)
                
        if channel_id == None or 0 and not data:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                title = f"Leveling Channel For {ctx.author.guild.name}",
                description= f'<#{channel_id}>'
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @lvlchannel.error
    async def lvlchannel_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command(aliases=["lvl"])
    async def level(self, ctx, member: nextcord.Member=None):
        self.bot.multiplier = 1
        guild_id = ctx.guild.id

        if member is None: member = ctx.author

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = nextcord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed)
                
        if channel_id == None or 0 and not data:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        else:
            # get user exp
            async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)) as cursor:
                data = await cursor.fetchone()
                exp = data[0]

                # calculate rank
            async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                rank = 1
                async for value in cursor:
                    if exp < value[0]:
                        rank += 1

            lvl = int(math.sqrt(exp)//self.bot.multiplier)

            current_lvl_exp = (self.bot.multiplier*(lvl))**2
            next_lvl_exp = (self.bot.multiplier*((lvl+1)))**2

            lvl_percentage = ((exp-current_lvl_exp) / (next_lvl_exp-current_lvl_exp)) * 100

            embed = nextcord.Embed(title=f"Stats for {member.name}", colour=nextcord.Colour.gold())
            embed.add_field(name="Level", value=str(lvl))
            embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
            embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}")
            embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

            await ctx.send(embed=embed)


    @level.error
    async def level_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    async def lvlboard(self, ctx): 
        guild_id = ctx.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = nextcord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed)
                
        if channel_id == None or 0 and not data:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `$setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        else:
            buttons = {}
            for i in range(1, 6):
                buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i # only show first 5 pages

            previous_page = 0
            current = 1
            index = 1
            entries_per_page = 10

            embed = nextcord.Embed(title=f"Leaderboard Page {current}", description="", colour=nextcord.Colour.gold())
            msg = await ctx.send(embed=embed)

            for button in buttons:
                await msg.add_reaction(button)

            while True:
                if current != previous_page:
                    embed.title = f"Leaderboard Page {current}"
                    embed.description = ""

                    async with self.bot.db.execute(f"SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ", (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                        index = entries_per_page*(current-1)

                        async for entry in cursor:
                            index += 1
                            member_id, exp = entry
                            member = ctx.guild.get_member(member_id)
                            embed.description += f"{index}) {member.mention} : {exp}\n"

                        await msg.edit(embed=embed)

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

                except asyncio.TimeoutError:
                    return await msg.clear_reactions()

                else:
                    previous_page = current
                    await msg.remove_reaction(reaction.emoji, ctx.author)
                    current = buttons[reaction.emoji]


    @lvlboard.error
    async def lvlboard_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(messageCount(bot))