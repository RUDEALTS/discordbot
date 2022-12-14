import asyncio
import discord
from discord.ui import Button, View
from discord.ext import commands
from discord.utils import get


class BoostsCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

        self.GUILD_ID = 938105317781307392
        self.TEAM_ROLE = 1030518060559372318
        self.TICKET_CHANNEL = 1035284564354027613
        self.CATEGORY_ID = 1030518071003201666

        print("Registered boost Cog")

    @commands.command()
    @commands.is_owner()
    async def boosts(self, ctx):
        button1 = Button(label=f"Boosts kaufen!", style=discord.ButtonStyle.green, custom_id="boost_button")
        view = View()
        view.add_item(button1)
        emb = discord.Embed(description=""""
        **Hier findest du günstige Server Boosts**\n
        Um Server Boosts zu kaufen musst du den Button drücken.\n
        \n
        **Preise**\n
        3 Monate:\n
        *Level 2* 6€\n
        *Level 3* 10€        
        """, title=f"**Server Boosts**", colour=discord.Colour.purple())
        emb.set_footer(
            icon_url="https://cdn.discordapp.com/attachments/1030518107388788736/1035695718255579208/1.png",
            text="Server Boosts | Simple Service")
        channel = self.bot.get_channel(self.TICKET_CHANNEL)
        await channel.send(embed=emb, view=view)
        await ctx.send(f"✅ Sent!")

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.channel.id == self.TICKET_CHANNEL:
            if "boost_button" in str(interaction.data):
                guild = self.bot.get_guild(self.GUILD_ID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(
                            description=f"Du kannst keine Kaufanfrage mehrmals senden!\nDu hast bereits eine gestellt: {ticket.mention}")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                category = self.bot.get_channel(self.CATEGORY_ID)
                ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
                ticket_channel = await guild.create_text_channel(f"boost-{ticket_num}", category=category,
                                                                 topic=f"Käufer {interaction.user} \nClient-ID: {interaction.user.id}")

                await ticket_channel.set_permissions(guild.get_role(self.TEAM_ROLE), send_messages=True,
                                                     read_messages=True, add_reactions=False,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                     add_reactions=False,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)
                embed = discord.Embed(description=f"""
                **Warten auf {self.TEAM_ROLE}...**
                *Bitte das Team nicht pingen, wir werden uns bei dir melden.*
                Um das Ticket zu schließen, nutzte `!close`.
                """, color=discord.Colour.blue())
                embed.set_author(name=f'Server Boosts!')
                mess_2 = await ticket_channel.send(embed=embed)
                embed = discord.Embed(title="Anfrage gesendet!",
                                      description=f'Hier findest du deine Anfrage!: {ticket_channel.mention}',
                                      color=discord.colour.Color.green())

                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

async def setup(bot):
    await bot.add_cog(BoostsCog(bot))