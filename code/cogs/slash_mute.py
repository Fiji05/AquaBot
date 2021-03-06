import discord
import asyncio
from discord.ext import commands
from datetime import datetime
from discord import app_commands

color = 0xc48aff

class slash_mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(role_name='Name of your servers muted role')
    async def setmute(
        self, 
        interaction: discord.Interaction, 
        role_name: discord.Role
    ):
        "Set the role for users to be given when muted"

        guild_id = interaction.user.guild.id
        role = role_name
        role_id = role.id

        cursor = await self.bot.db.execute("UPDATE mute SET role_id = ? WHERE guild_id = ?", (role_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO mute (role_id, guild_id) VALUES(?, ?)", (role_id, guild_id))
            await self.bot.db.commit()

        embed = discord.Embed(
            title = "Mute Role Changed -",
            description = f"<@&{role_id}> has been assigned as the mute role for {interaction.user.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def delmute(
        self, 
        interaction: discord.Interaction
    ):
        "Delete the role set to be given to muted users"

        guild_id = interaction.user.guild.id
        async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                await self.bot.db.execute(f"DELETE FROM mute WHERE guild_id = ?", (guild_id,))
                await self.bot.db.commit()

                embed = discord.Embed(
                    title = "Mute Role Deleted -",
                    description = f"The mute role for {interaction.user.guild.name} has been deleted.",
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "??? Mute Role Not Set!",
                    description = f"??? The mute role is not set, therefore there is no role I can delete."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def muterole(
        self, 
        interaction: discord.Interaction
    ):
        "See the current role set for when users are muted"

        guild_id = interaction.user.guild.id
        async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                role_id = data[0]
                embed = discord.Embed(
                    title = f"Mute role for {interaction.user.guild.name}",
                    description= f'<@&{role_id}>'
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await interaction.response.send_message(embed=embed)
            
            else:
                embed = discord.Embed(
                    title = f"??? Mute Role Not Set!",
                    description= f'The mute role has not yet been set. Ask an admin to set it up using `/setmute`'
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member='Name of the member you want to temporarily mute')
    @app_commands.describe(time='Amount of time (in hours) to mute the member')
    async def tempmute(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member, 
        time: int
    ): 
        "Mute a user for a specified amount of time"

        try:
            guild_id = interaction.user.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = interaction.user.guild.get_role(role_id)
            role = discord.utils.get(interaction.user.guild.roles, name=f"{role_name}")
            await member.add_roles(role)
            embed = discord.Embed(
                title = f"**User {member} has been muted for {time} hours.**",
                colour = discord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {interaction.user}', value = f'\u200b', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await interaction.response.send_message(embed=embed)

            await asyncio.sleep(time*3600)
            await member.remove_roles(role)
        
        except TypeError:
            embed = discord.Embed(
                colour = color,
                title = "??? No Role Set!",
                description = f"??? It seems you haven't set a muted role yet. Please go do that with `/setmute` before running this command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member='Name of the member you want to mute')
    @app_commands.describe(reason='Reason for muting the member')
    async def mute(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member, 
        reason: str
    ): 
        "Mutes a user for an indefinite amount of time"

        try:
            guild_id = interaction.user.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = interaction.user.guild.get_role(role_id)
            role = discord.utils.get(interaction.user.guild.roles, name=f"{role_name}")
            await member.add_roles(role)
            embed = discord.Embed(
                title = f"**User {member} has been muted for {reason}.**",
                colour = discord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {interaction.user}', value = f'\u200b', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await interaction.response.send_message(embed=embed)

        except TypeError:
            embed = discord.Embed(
                colour = color,
                title = "??? No Role Set!",
                description = f"??? It seems you haven't set a muted role yet. Please go do that with `/setmute` before running this command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member='Name of the member you want to unmute')
    async def unmute(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member
    ):
        "Unmute a specified member"
        
        guild_id = interaction.user.guild.id
        async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            role_id = data[0]
        role_name = interaction.user.guild.get_role(role_id)
        role = discord.utils.get(interaction.user.guild.roles, name=f"{role_name}")
        embed = discord.Embed(
            title = f"**User {member} has been unmuted.**",
            colour = discord.Colour.green()
        )
        embed.add_field(name=f'This command was issued by {interaction.user}', value = f'\u200b', inline=False)
        embed.set_thumbnail(url = member.avatar.url)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        await interaction.response.send_message(embed=embed)
        await member.remove_roles(role)


async def setup(bot):
    await bot.add_cog(slash_mute(bot))