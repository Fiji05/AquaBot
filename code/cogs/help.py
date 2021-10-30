from typing import List
from urllib.parse import quote_plus

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import context
from utils.helpers import *

color = 0xc48aff

async def get_prefix(self, message):
    async with self.bot.db.execute("SELECT prefix FROM prefix WHERE guild_id = ?", (message.guild.id,)) as cursor:
        data = await cursor.fetchone()
        if data:
            prefix = data[0]
            return prefix
        else:
            prefix = DEFAULT_PREFIX
            return prefix


class HelpDropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(label='Gambling', description='add, blackjack, slots, coinflip, money, leaderboard', emoji="💰"),
            nextcord.SelectOption(label='Moderation', description='mute, tempmute, unmute, kick, ban, softban, purge', emoji="<:moderation:893273273385754686>"),
            nextcord.SelectOption(label='Info', description='contact, covid, invite, track, ping, serverinfo, whois, botinfo, vote', emoji="ℹ️"),
            nextcord.SelectOption(label='Music (BETA)', description='play, skip, queue, remove, stop, clear, repeat, shuffle, nowplaying, pause, remove', emoji='🎵'),
            nextcord.SelectOption(label='Admin', description='setlevel, lvlreset, dellevel, lvlchannel, setmute, muterole, delmute, setjoin, joinchannel, deljoin', emoji="⚙️"),
            nextcord.SelectOption(label='Fun', description='level, lvlboard, calculate, reverse, donald, kanye', emoji='🎉'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Gambling':
            embed = nextcord.Embed(
                title = "💰 - Gambling Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Add**", value = f"**Usage: `{get_prefix}add`**\nGives you $2,500. Can be run every 2 hours", inline=False)
            embed.add_field(name = "**🃏 - Blackjack (bj)**", value = f"**Usage: `$blackjack <bet>`**\nIf no bet is given, the deafult bet of $125 will be placed", inline=False)
            embed.add_field(name = "**🎰 - Slots**", value = f"**Usage: `$slots <bet>`**\nIf no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**🪙 - Coinflip (cf)**", value = f"**Usage: `$coinflip <bet>`**\nHeads means you win, tails means you lose. If no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**💵 - Money**", value = f"**Usage: `$money` **\nThis shows your current dollar balance", inline=False)
            embed.add_field(name = "**🏅 - Leaderboard**", value = f"**Usage: `$leaderboard` **\nShows the top 5 players with the most money. This is a global leaderboard and not per server.", inline=False)
            await interaction.response.edit_message(embed=embed)

        if self.values[0] == 'Moderation':
            embed = nextcord.Embed(
                title = "<:moderation:893273273385754686> - Moderation Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )
            embed.add_field(name = "**Warn**", value = f"**Usage: `$warn <member> <reason>`** \nWarn a member for doing something against the rules.", inline=True)
            embed.add_field(name = "**Delwarn**", value = f"**Usage: `$delwarn <member> <warn ID>`** \nDelete a warning from a member so that it is no longer on their record.", inline=True)
            embed.add_field(name = "**Warnings**", value = f"**Usage: `$warnings <member>`** \nSee all of the warnings for a member. Also includes when they were warned, and who warned them.", inline=True)
            embed.add_field(name = "**Mute**", value = f"**Usage: `$mute <member> <time>`** \nMute a member so they can't send anymore messages.", inline=True)
            embed.add_field(name = "**Tempmute**", value = f"**Usage: `$tempmute <member> <time>` \nExample: `$tempmute @bob 2d 4h 6m 8s`** \nMutes the member temporarily, they will be unmute once the specified time has passed.", inline=True)
            embed.add_field(name = "**Unmute**", value = f"**Usage: `$unmute <member>`** \nUnmute a member so they are able to send messages again.", inline=True)      
            embed.add_field(name = "**Purge**", value = f"**Usage: `$purge <amount>`** \nDelete messages from your server. Max amount that can be deleted at one time is `100` messages.")
            embed.add_field(name = "**Kick**", value = f"**Usage: `$kick <member> <reason>`** \nKick a member from your server. They will be able to join back with a new invite.", inline=True)
            embed.add_field(name = "**Ban**", value = f"**Usage: `$slots <member> <reason>`** \nBan a member from your server. They will not be able to join back until they are unbanned.", inline=True)
            embed.add_field(name = "**Softban**", value = f"**Usage: `$softban <member> (reason)`** \nThis command will ban and then immediately unban the member in order to get rid of their message history.", inline=True)
            await interaction.response.edit_message(embed=embed) 

        if self.values[0] == "Info":
            embed = nextcord.Embed(
                title = "ℹ️ - Info Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Contact**", value = f"**Usage: `$contact`** \nWill DM you and help you get in contact with staff members to resolve your issue, bug.", inline=True)
            embed.add_field(name = "**Covid**", value = f"**Usage: `$covid` **\nSends the current global COVID-19 data.", inline=True)
            embed.add_field(name = "**Invite**", value = f"**Usage: `$invite` **\nSends the invite for the bot.", inline=True)
            embed.add_field(name = "**Track**", value = f"**Usage: `track`** \nSends the amount of servers that the bot is in, as well as the cumulative amount of members.", inline=True)
            embed.add_field(name = "**Ping**", value = f"**Usage: `$ping` **\nGives the current ping of the bot.", inline=True)
            embed.add_field(name = "**Server Info**", value = f"**Usage: `$serverinfo` **\nGives lots of information on your server, inlcuding: region, boosters, roles, etc.", inline=True)
            embed.add_field(name = "**Whois**", value = f"**Usage: `$whois <member>`** \nGives information on a member in your server. Information includes account creation date, when they joined your server, and much more.", inline=True)
            embed.add_field(name = "**Bot Info**", value = f"**Usage: `$botinfo`** \nGives information on the bot.", inline=True)
            embed.add_field(name = "**Vote**", value = f"**Usage: `$vote`** \nSends the link for you to vote for our bot on top.gg", inline=True)
            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == "Music (BETA)":
            embed = nextcord.Embed(
                title = "🎵 - Music Help \n*NOTE - These commands are still in beta. Please report bugs using `$contact`",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Play**", value = f"**Usage: `$play <name of song / URL>` **\nSearches YouTube, and then plays the top song.", inline=True)
            embed.add_field(name = "**Skip**", value = f"**Usage: `$skip` **\nSkips the song that is currently playing.", inline=True)
            embed.add_field(name = "**Queue**", value = f"**Usage: `$queue`** \nSends all of the songs that are in the queue.", inline=True)
            embed.add_field(name = "**Remove**", value = f"**Usage: `$remove <song #>` **\nRemoves the specified song from the queue.", inline=True)
            embed.add_field(name = "**Stop**", value = f"**Usage: `$stop`** \nStops music, clears queue, and leaves VC.", inline=True),            
            embed.add_field(name = "**Clear**", value = f"**Usage: `$clear` **\nRemoves ALL songs in the queue.", inline=True)
            embed.add_field(name = "**Repeat**", value = f"**Usage: `$remove`** \nRepeats the song that is playing. Run the command again to stop repeating.", inline=True)
            embed.add_field(name = "**Shuffle**", value = f"**Usage: `$shuffle`** \nWill play a random song in the queue. Run the command again to stop shuffling.", inline=True)
            embed.add_field(name = "**Nowplaying**", value = f"**Usage: `$nowplaying` **\nSends the song that is currently playing.", inline=True)
            embed.add_field(name = "**Pause**", value = f"**Usage: `$pause`** \nPauses the currently playing song.", inline=True)
            embed.add_field(name = "**Resume**", value = f"**Usage: `$resume` **\nResumes the paused song.", inline=True)

            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == "Admin":
            embed = nextcord.Embed(
                title = "⚙️ - Admin Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Setlevel**", value = f"**Usage: `$setlevel <name of channel>` **\nSets the channel for level up messages to be sent to.", inline=True)
            embed.add_field(name = "**Lvlreset**", value = f"**Usage: `$lvlreset` **\nResets all of the levels for everyone in the server.", inline=True)
            embed.add_field(name = "**Dellevel**", value = f"**Usage: `$dellevel` **\nDeletes the channel from our database, and stops sending new level up messages.", inline=True)
            embed.add_field(name = "**Lvlchannel**", value = f"**Usage: `$lvlchannel` ** \nShows the current channel for leveling messages.", inline=True)
            embed.add_field(name = "**Setmute**", value = f"**Usage: `$setmute <name of role>` **\nSets the role that will be given to users whenever you use the `$mute` command.", inline=False)
            embed.add_field(name = "**Delmute**", value = f"**Usage: `$delmute` **\nDeletes the muted role from our database.", inline=False)
            embed.add_field(name = "**Muterole**", value = f"**Usage: `$muterole`** \nSends the current role that is assigned as the muted role for your server.", inline=False)
            embed.add_field(name = "**Setjoin**", value = f"**Usage: `$setjoin <name of channel>` **\nSets the channel for messages to be sent whenever a new user joins your server.", inline=False)
            embed.add_field(name = "**Deljoin**", value = f"**Usage: `$deljoin`** \nDeletes the channel from our database, and stops sending new user messages.", inline=False),
            embed.add_field(name = "**Joinchannel**", value = f"**Usage: `$joinchannel`** \nSends the current channel that is assigned as the new user messages channel.", inline=False)

            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == 'Fun':
            embed = nextcord.Embed(
                title = "🎉 - Fun Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Level**", value = f"**Usage: `$level`** \nSends your current level in the server.", inline=False)
            embed.add_field(name = "**Lvlboard**", value = f"**Usage: `$lvlboard`** \nSends the current leaderboard for your servers leveling system.", inline=False)
            embed.add_field(name = "**Calculate**", value = f"**Usage: `$calculate`** \nSends a calculator with buttons for you to do math.", inline=False)
            embed.add_field(name = "**Reverse**", value = f"**Usage: `$reverse <text>`** \nReverses whatever text you put in.", inline=False)
            embed.add_field(name = "**Donald**", value = f"**Usage: `$donald` **\nSends a quote from Donald Trump.", inline=False)
            embed.add_field(name = "**Kanye**", value = f"**Usage: `$kanye` **\nSends a quote from Kanye West.", inline=False)
            await interaction.response.edit_message(embed=embed) 

        else:
            return

class HelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(HelpDropdown())
        url = "https://discord.com/api/oauth2/authorize?client_id=889027125275922462&permissions=8&scope=bot"
        self.add_item(nextcord.ui.Button(label="Invite Me", url=url, row=3))
        url = "https://pkmeiner.com"
        self.add_item(nextcord.ui.Button(label="Bot Site", url=url, row=3))

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Help",
            description = "For extended information on commands and categories, please choose and option from the dropdown menu below.",
            colour = nextcord.Colour.random()   
        )

        await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class GuildHelpDropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(label='Gambling', description='add, blackjack, slots, coinflip, money, leaderboard', emoji="💰"),
            nextcord.SelectOption(label='Moderation', description='kick, ban, softban, mute, tempmute, unmute, lock, unlock, purge', emoji="<:moderation:893273273385754686>"),
            nextcord.SelectOption(label='Info', description='contact, covid, invite, track, ping, serverinfo, whois, botinfo, vote', emoji="ℹ️"),
            nextcord.SelectOption(label='Music (BETA)', description='play, skip, queue, remove, stop, clear, repeat, shuffle, nowplaying, pause, remove', emoji='🎵'),
            nextcord.SelectOption(label='Admin', description='setlevel, lvlreset, dellevel, lvlchannel, setmute, muterole, delmute, setjoin, joinchannel, deljoin', emoji="⚙️"),
            nextcord.SelectOption(label='Fun', description='level, lvlboard, calculate, reverse, donald, kanye', emoji='🎉'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Gambling':
            embed = nextcord.Embed(
                title = "💰 - Gambling Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Add**", value = f"**Usage: `$add`**\nGive you $2,500. Can be run every 2 hours", inline=False)
            embed.add_field(name = "**🃏 - Blackjack (bj)**", value = f"**Usage: `$blackjack <bet>`**\nIf no bet is given, the deafult bet of $125 will be placed", inline=False)
            embed.add_field(name = "**🎰 - Slots**", value = f"**Usage: `$slots <bet>`**\nHeads means you win, tails means you lose. If no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**🪙 - Coinflip (cf)**", value = f"**Usage: `$coinflip <bet>`**\nIf no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**💵 - Money**", value = f"**Usage: `$money` **\nThis shows your current dollar balance", inline=False)
            embed.add_field(name = "**🏅 - Leaderboard**", value = f"**Usage: `$leaderboard` **\nShows the top 5 players with the most money. This is a global leaderboard and not per server.", inline=False)
            await interaction.response.edit_message(embed=embed)

        if self.values[0] == 'Moderation':
            embed = nextcord.Embed(
                title = "<:moderation:893273273385754686> - Moderation Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )
            embed.add_field(name = "**Warn**", value = f"**Usage: `$warn <member> <reason>`** \nWarn a member for doing something against the rules.", inline=True)
            embed.add_field(name = "**Delwarn**", value = f"**Usage: `$delwarn <member> <warn ID>`** \nDelete a warning from a member so that it is no longer on their record.", inline=True)
            embed.add_field(name = "**Warnings**", value = f"**Usage: `$warnings <member>`** \nSee all of the warnings for a member. Also includes when they were warned, and who warned them.", inline=True)
            embed.add_field(name = "**Mute**", value = f"**Usage: `$mute <member> <time>` \nExample: `$mute @bob 2d 4h 6m 8s`** \nMute a member so they can't send anymore messages for a specified amount of time.", inline=True)
            embed.add_field(name = "**Tempmute**", value = f"**Usage: `$tempmute <member> <time>` \nExample: `$tempmute @bob 2d 4h 6m 8s`** \nMutes the member temporarily, they will be unmute once the specified time has passed.", inline=False)
            embed.add_field(name = "**Unmute**", value = f"**Usage: `$unmute <member>`** \nUnmute a member so they are able to send messages again.", inline=True)      
            embed.add_field(name = "**Purge**", value = f"**Usage: `$purge <amount>`** \nDelete messages from your server. Max amount that can be deleted at one time is `100` messages.", inline=True)
            embed.add_field(name = "**Kick**", value = f"**Usage: `$kick <member> <reason>`** \nKick a member from your server. They will be able to join back with a new invite.", inline=True)
            embed.add_field(name = "**Ban**", value = f"**Usage: `$slots <member> <reason>`** \nBan a member from your server. They will not be able to join back until they are unbanned.", inline=True)
            embed.add_field(name = "**Softban**", value = f"**Usage: `$softban <member> (reason)`** \nThis command will ban and then immediately unban the member in order to get rid of their message history.", inline=True)
            embed.add_field(name = "**Lock**", value = f"**Usage: `$lock (reason)`** \nThis will lock the channel where the command was sent.", inline=True)
            embed.add_field(name = "**Unlock**", value = f"**Usage: `$unlock (reason)`** \nThis will unlock the channel where the command was sent.", inline=True)
            
            await interaction.response.edit_message(embed=embed) 

        if self.values[0] == "Info":
            embed = nextcord.Embed(
                title = "ℹ️ - Info Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Contact**", value = f"**Usage: `$contact`** \nWill DM you and help you get in contact with staff members to resolve your issue, bug.", inline=True)
            embed.add_field(name = "**Covid**", value = f"**Usage: `$covid` **\nSends the current global COVID-19 data.", inline=True)
            embed.add_field(name = "**Invite**", value = f"**Usage: `$invite` **\nSends the invite for the bot.", inline=True)
            embed.add_field(name = "**Track**", value = f"**Usage: `track`** \nSends the amount of servers that the bot is in, as well as the cumulative amount of members.", inline=True)
            embed.add_field(name = "**Ping**", value = f"**Usage: `$ping` **\nGives the current ping of the bot.", inline=True)
            embed.add_field(name = "**Server Info**", value = f"**Usage: `$serverinfo` **\nGives lots of information on your server, inlcuding: region, boosters, roles, etc.", inline=True)
            embed.add_field(name = "**Whois**", value = f"**Usage: `$whois <member>`** \nGives information on a member in your server. Information includes account creation date, when they joined your server, and much more.", inline=True)
            embed.add_field(name = "**Bot Info**", value = f"**Usage: `$botinfo`** \nGives information on the bot.", inline=True)
            embed.add_field(name = "**Vote**", value = f"**Usage: `$vote`** \nSends the link for you to vote for our bot on top.gg", inline=True)
            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == "Music (BETA)":
            embed = nextcord.Embed(
                title = "🎵 - Music Help \n*NOTE - These commands are still in beta. Please report bugs using `$contact`",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Play**", value = f"**Usage: `$play <name of song / URL>` **\nSearches YouTube, and then plays the top song.", inline=True)
            embed.add_field(name = "**Skip**", value = f"**Usage: `$skip` **\nSkips the song that is currently playing.", inline=True)
            embed.add_field(name = "**Queue**", value = f"**Usage: `$queue`** \nSends all of the songs that are in the queue.", inline=True)
            embed.add_field(name = "**Remove**", value = f"**Usage: `$remove <song #>` **\nRemoves the specified song from the queue.", inline=True)
            embed.add_field(name = "**Stop**", value = f"**Usage: `$stop`** \nStops music, clears queue, and leaves VC.", inline=True),            embed.add_field(name = "**Clear**", value = "**Usage: `$clear` **\nRemoves ALL songs in the queue.", inline=True)
            embed.add_field(name = "**Repeat**", value = f"**Usage: `$remove`** \nRepeats the song that is playing. Run the command again to stop repeating.", inline=True)
            embed.add_field(name = "**Shuffle**", value = f"**Usage: `$shuffle`** \nWill play a random song in the queue. Run the command again to stop shuffling.", inline=True)
            embed.add_field(name = "**Nowplaying**", value = f"**Usage: `$nowplaying` **\nSends the song that is currently playing.", inline=True)
            embed.add_field(name = "**Pause**", value = f"**Usage: `$pause`** \nPauses the currently playing song.", inline=True)
            embed.add_field(name = "**Resume**", value = f"**Usage: `$resume` **\nResumes the paused song.", inline=True)

            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == "Admin":
            embed = nextcord.Embed(
                title = "⚙️ - Admin Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Setlevel**", value = f"**Usage: `$setlevel <name of channel>` **\nSets the channel for level up messages to be sent to.", inline=True)
            embed.add_field(name = "**Lvlreset**", value = f"**Usage: `$lvlreset` **\nResets all of the levels for everyone in the server.", inline=True)
            embed.add_field(name = "**Dellevel**", value = f"**Usage: `$dellevel` **\nDeletes the channel from our database, and stops sending new level up messages.", inline=True)
            embed.add_field(name = "**Lvlchannel**", value = f"**Usage: `$lvlchannel` ** \nShows the current channel for leveling messages.", inline=True)
            embed.add_field(name = "**Setmute**", value = f"**Usage: `$setmute <name of role>` **\nSets the role that will be given to users whenever you use the `$mute` command.", inline=True)
            embed.add_field(name = "**Delmute**", value = f"**Usage: `$delmute` **\nDeletes the muted role from our database.", inline=True)
            embed.add_field(name = "**Muterole**", value = f"**Usage: `$muterole`** \nSends the current role that is assigned as the muted role for your server.", inline=True)
            embed.add_field(name = "**Setjoin**", value = f"**Usage: `$setjoin <name of channel>` **\nSets the channel for messages to be sent whenever a new user joins your server.", inline=True)
            embed.add_field(name = "**Deljoin**", value = f"**Usage: `$deljoin`** \nDeletes the channel from our database, and stops sending new user messages.", inline=True),
            embed.add_field(name = "**Joinchannel**", value = f"**Usage: `$joinchannel`** \nSends the current channel that is assigned as the new user messages channel.", inline=True)

            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == 'Fun':
            embed = nextcord.Embed(
                title = "🎉 - Fun Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Level**", value = f"**Usage: `$level`** \nSends your current level in the server.", inline=False)
            embed.add_field(name = "**Lvlboard**", value = f"**Usage: `$lvlboard`** \nSends the current leaderboard for your servers leveling system.", inline=False)
            embed.add_field(name = "**Calculate**", value = f"**Usage: `$calculate`** \nSends a calculator with buttons for you to do math.", inline=False)
            embed.add_field(name = "**Reverse**", value = f"**Usage: `$reverse <text>`** \nReverses whatever text you put in.", inline=False)
            embed.add_field(name = "**Donald**", value = f"**Usage: `$donald` **\nSends a quote from Donald Trump.", inline=False)
            embed.add_field(name = "**Kanye**", value = f"**Usage: `$kanye` **\nSends a quote from Kanye West.", inline=False)
            await interaction.response.edit_message(embed=embed) 

        else:
            return

class GuildHelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(GuildHelpDropdown())
        url = "https://discord.com/api/oauth2/authorize?client_id=889027125275922462&permissions=8&scope=bot"
        self.add_item(nextcord.ui.Button(label="Invite Me", url=url, row=3))
        url = "https://pkmeiner.com"
        self.add_item(nextcord.ui.Button(label="Bot Site", url=url, row=3))

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Help",
            description = "For extended information on commands and categories, please choose and option from the dropdown menu below.",
            colour = nextcord.Colour.random()   
        )

        await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        if ctx.message.guild.id != 889027208964874240:
            embed = nextcord.Embed(
                title = "Help",
                description = f"**IMPORTANT - Many things have changed in the new update, in order to see all of these changes, please run `{ctx.prefix}new`** \n\nFor extended information on commands and categories, please choose an option from the dropdown menu below.",
                colour = nextcord.Colour.random()    
            )

            view = HelpView()
            await ctx.send(embed=embed, view=view)

        if ctx.message.guild.id == 889027208964874240:
            embed = nextcord.Embed(
                title = "Help",
                description = f"**IMPORTANT - Many things have changed in the new update, in order to see all of these changes, please run `{ctx.prefix}new`** \n\nFor extended information on commands and categories, please choose an option from the dropdown menu below.",
                colour = nextcord.Colour.random()    
            )

            view = GuildHelpView()
            await ctx.send(embed=embed, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))