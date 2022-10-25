import asyncio
import discord
from discord.ui import Button, View
from discord.ext import commands

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

        self.GUILD_ID = 938105317781307392
        self.TEAM_ROLE = 1030518060559372318
        self.TICKET_CHANNEL = 1030518079857369190
        self.CATEGORY_ID = 1030518071003201666

        print("Registered ticket Cog")

    @commands.command()
    @commands.is_owner()
    async def setup(self, ctx):
        button1 = Button(label="Buy Nitro!", style=discord.ButtonStyle.grey, custom_id="nitro_button")
        view = View()
        view.add_item(button1)
        embed = discord.Embed(description=f"Contact the Team.", title=f"Shop & Contact", color="#1414a7")
        embed.add_field(name="Contact for Nitro", value="Open ticket to *buy* cheap Nitro")
        embed.add_field(name="Shop", value="If you want a own Shop.", inline=False)
        embed.set_footer(
            icon_url="https://media.discordapp.net/attachments/1030518107388788736/1034199146736910336/IMG_5300.png?width=580&height=468",
            text="Tickets | Simple Service")
        channel = self.bot.get_channel(self.TICKET_CHANNEL)
        await channel.send(embed=embed, view=view)
        await ctx.reply("Send!")

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.channel.id == self.TICKET_CHANNEL:
            if "nitro_button" in str(interaction.data):
                guild = self.bot.get_guild(self.GUILD_ID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(description=f"You can't open tickets twice.\nYou alredy opend a ticket!: {ticket.mention}")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                category = self.bot.get_channel(self.CATEGORY_ID)
                ticket_num= 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
                ticket_channel = await guild.create_text_channel(f"nitro-{interaction.user}", category=category,
                                                                topic=f"Ticket opend by {interaction.user} \nClient-ID: {interaction.user.id}")

                await ticket_channel.set_permissions(guild.get_role(self.TEAM_ROLE), send_messages=True, read_messages=True, add_reactions=False,
                                                    embed_links=True, attach_files=True, read_message_history=True,
                                                    external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                    embed_links=True, attach_files=True, read_message_history=True,
                                                    external_emojis=True)
                embed = discord.Embed(description=f'Welcome {interaction.user.mention}!\n'
                                                f'Support will be shortly!\n'
                                                f'to close the ticket use`!close`',
                                    color=62719)
                embed.set_author(name=f'New ticket!')
                mess_2 = await ticket_channel.send(embed=embed)
                embed = discord.Embed(title="📬 Opend Ticket!",
                                    description=f'Your Ticket!: {ticket_channel.mention}',
                                    color=discord.colour.Color.green())

                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

    @commands.command()
    async def close(self, ctx):
        if "ticket-" in ctx.channel.name:
            embed = discord.Embed(
                description=f'ticket will be closed in 5 seconds.',
                color=16711680)
        await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(TicketCog(bot))