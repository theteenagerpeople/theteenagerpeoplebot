import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ Kick command
    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member.mention} was kicked. Reason: {reason}")

    # ✅ Ban command
    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member.mention} was banned. Reason: {reason}")

    # ✅ Unban command
    @app_commands.command(name="unban", description="Unban a previously banned user.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"♻️ {user.name} has been unbanned.")

    # ✅ Timeout command
    @app_commands.command(name="timeout", description="Timeout (mute temporarily) a member for given minutes.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided"):
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await interaction.response.send_message(f"⏳ {member.mention} has been timed out for {minutes} minutes. Reason: {reason}")

    # ✅ Mute command (using roles)
    @app_commands.command(name="mute", description="Mute a member by assigning a 'Muted' role.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not role:
            role = await interaction.guild.create_role(name="Muted")
            for channel in interaction.guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        await member.add_roles(role)
        await interaction.response.send_message(f"🔇 {member.mention} has been muted.")

    # ✅ Unmute command
    @app_commands.command(name="unmute", description="Remove the 'Muted' role from a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"🔊 {member.mention} has been unmuted.")
        else:
            await interaction.response.send_message("⚠️ That user isn’t muted.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
