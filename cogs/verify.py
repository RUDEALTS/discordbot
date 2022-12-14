import asyncio
import discord
from discord.ui import Button, View
from discord.ext import commands


class RoleButton(discord.ui.Button):
    def __init__(self, role_id):
        self.role_id = role_id

        super().__init__(
            label="\u2705 Verifizieren!",
            style=discord.enums.ButtonStyle.red,
            custom_id="interaction:RoleButton",
        )

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user

        role = interaction.guild.get_role(self.role_id)

        if role is None:
            return

        if role not in user.roles:
            await user.add_roles(role)
            await interaction.response.send_message(f"Erfolgreich verifiziert!", ephemeral=True)

        else:
            await interaction.response.send_message(f"Du hast dich bereits verifiziert!", ephemeral=True)


class VerifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

        self.VERIFY_CHANNEL = 1030518081199546448
        self.role_id = 1034807355583512657
        self.guild_id = 938105317781307392

        print("Registered verify cog")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def verify(self, ctx: commands.Context):  # Command
        view = discord.ui.View(timeout=None)

        view.add_item(RoleButton(self.role_id))
        embed = discord.Embed(description=f"""
        Um Teil unsers Servers zu werden, musst du dich erstmal verifizieren,\n
        um deine Identität nachzuweisen.
        """, title=f"Verifizierung",
                              color=discord.Colour.red())
        embed.set_footer(
            icon_url="https://cdn.discordapp.com/attachments/1030518107388788736/1035695718255579208/1.png",
            text="Verifikation | Simple Service")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1030518107388788736/1035696927997706321/unknown.png?width=565&height=468")
        channel = self.bot.get_channel(self.VERIFY_CHANNEL)
        await channel.send(embed=embed, view=view)
        await ctx.send('Sent')
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(VerifyCog(bot))
