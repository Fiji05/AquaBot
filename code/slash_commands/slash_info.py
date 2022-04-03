import time
import discord
from discord.ext import commands
from datetime import datetime
from discord import app_commands

color = 0xc48aff

class slash_information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command()
    async def ping(
        self, 
        interaction: discord.Interaction
    ):
        "Pong! 🏓"
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(
            title = f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms",
            colour = discord.Colour.yellow()
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def invite(
        self, 
        interaction: discord.Interaction
    ):
        "Get the invite link for the bot and official server"
        embed = discord.Embed(
            title = "Invites",
            description = "Here's the invite for [Aqua Bot](https://discord.com/api/oauth2/authorize?client_id=889027125275922462&permissions=8&scope=bot%20applications.commands) \nHere's the invite for the [Official Support Server](https://discord.gg/fAD3jcexzM)"
        )

        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.describe(member="Member whose information you want to view")
    async def userinfo(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member
    ):
        "Send account information for the given user"

        embed = discord.Embed(
            color=discord.Colour.magenta(),
            title=f"→ User Information For {member}",
            description="— "
                        "\n➤ Shows all information about a user. "
                        "\n➤ The information will be listed below!"
                        "\n —"
        )

        roles = [role for role in member.roles]
        roles = f" ".join([f"{role.mention}, " for role in roles])

        embed.set_thumbnail(url = member.avatar.url)
        embed.add_field(name="• Account name: ", value=str(member))
        embed.add_field(name="• Discord ID: ", value=str(member.id))
        embed.add_field(name="• Nickname: ", value=member.nick or "No nickname!")
        embed.add_field(name="• Account created at: ", value=member.created_at.strftime("%A %d, %B %Y."))
        embed.add_field(name="• Joined server at: ", value=member.joined_at.strftime("%A %d, %B %Y"))

        if member.bot is True:
            embed.add_field(name="• Discord bot? ", value=":robot: = :white_check_mark:")
        else:
            embed.add_field(name="• Discord bot?", value=":robot: = :x:")

        embed.add_field(name="• Top role: ", value=f"{member.top_role.mention}")
        embed.add_field(name="• Roles: ", inline=False, value=roles)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        try:
            await interaction.response.send_message(embed=embed)

        except Exception:
            print("caught")
            embed.remove_field(9)
            await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def botinfo(
        self, 
        interaction: discord.Interaction
    ):
        "Get information about the bot. i.e. creator, creation data, etc."

        embed = discord.Embed(
            color=discord.Colour.magenta(),
            title=f"→ Bot Information",
            description="— "
                        "\n➤ Shows information about the bot. "
                        "\n —"
        )
        before = time.monotonic()
        ping = (time.monotonic() - before) * 1000
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.add_field(name="• Bot Creator: ", value="Fiji#3608"),
        embed.add_field(name="• Servers: ", value = f"{len(self.bot.guilds):,}"),
        embed.add_field(name="• Account name: ", value=str(self.bot.user.name))
        embed.add_field(name="• Discord ID: ", value=str(self.bot.user.id))
        embed.add_field(name="• Bot created at: ", value=self.bot.user.created_at.strftime("%A %d, %B %Y.")),
        embed.add_field(name="• Aqau Bot Code: ", value="[GitHub Link](https://github.com/Fiji05/AquaBot)")
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def vote(
        self, 
        interaction: discord.Interaction
    ):
        "Get link to vote for the bot on top.gg"

        embed = discord.Embed(
            title = "→ Vote for me on top.gg!",
            description = "[Click here to vote](https://top.gg/bot/889027125275922462)",
            colour = discord.Colour.blurple()
        )
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def new(
        self, 
        interaction: discord.Interaction
    ):
        "See all of the new changes in the bot"
        
        embed = discord.Embed(
            title = "Change Log - 4/1/2022",
            description = "***Note - in order to get slash commands working in you server, you must reinvite the bot with the new link provided in the `/invite` command**",
            colour = discord.Colour.og_blurple()
        )

        embed.add_field(name = "Slash Commands", value = "All commands are now restricted to exclusively slash commands. Message commands using the normal bot prefix will no longer work, for any help, please do `/help` and make sure to choose the command from Aqua Bot.", inline=True)
        embed.add_field(name = "Money vs. Profile", value = "The `money` command has been removed in favor of the `profile` command, which will show current monetary balance as well as purchased ranks.", inline=True)
        embed.add_field(name = "Bug Fixes", value = "The errors within the `blackjack` and `slots` slash commands have been fixed, all commands now work under the slash command style.", inline=False)
        embed.add_field(name = "Bugs", value = "As always we've worked hard to make sure all of the bugs have been ironed out, however, if you find any bug please fill out a form using `/bug`.", inline=True)
        embed.add_field(name = "Feedback", value = "Feedback is always welcome and encouraged. A feedback form can be submitted to the bot developer through the `/feedback` command.")
        embed.add_field(name = "\u200b", value = "Thank you all for using Aqua Bot!", inline=False)


        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(slash_information(bot))