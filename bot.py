import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import random
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.members = True

DATA_FILE = os.getenv("DATA_FILE", "diddle_leaderboard.json")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Array of random GIFs
DIDDLE_GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGt2dnllbW0yNnBpYjNzMTBzaTUzZmk2cTh5djk1YWt5ZXdqYXJiZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/UHOnZRVZGZWLL4zCyB/giphy.gif",
    "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzc5eTl1YXJ4anJhN2VvdnU0bzNuYW1lbDhrcmc1enlqaWl6NDg3dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZqmpM7ySeVMBIMrYLY/giphy.gif",
    "https://tenor.com/uLnD0XFaWvZ.gif",
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3JhOTV2NXowanR5cTI3ZnMxMHBrdjFyemhuNDVxNjBuZHRlb3FqcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KS8UYr32V9luw/giphy.gif"
]

ULTIMATE_GIFS = DIDDLE_GIFS + [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHJmZ2x0Z3J4eW5qY3F3Z3Z4eW5qY3F3Z3Z4eW5qY3F3Z3Z4/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHJmZ2x0Z3J4eW5qY3F3Z3Z4eW5qY3F3Z3Z4eW5qY3F3Z3Z4/giphy.gif",
]

# Level thresholds (total diddles needed)
LEVEL_THRESHOLDS = {
    1: 1, 2: 5, 3: 10, 4: 25, 5: 50,
    6: 100, 7: 150, 8: 200, 9: 300, 10: 500,
    11: 750, 12: 1000, 13: 1500, 14: 2000, 15: 3000,
    16: 5000, 17: 7500, 18: 10000, 19: 15000, 20: 20000,
    21: 30000, 22: 50000, 23: 75000, 24: 100000, 25: 150000,
    26: 200000, 27: 300000, 28: 500000, 29: 750000, 30: 1000000,
}

# Level titles and role colors
LEVEL_TITLES = {
    1: "Novice Diddler", 2: "Apprentice Diddler", 3: "Diddle Enthusiast",
    4: "Diddle Adept", 5: "Diddle Veteran", 6: "Diddle Expert",
    7: "Diddle Master", 8: "Grand Diddler", 9: "Diddle Legend",
    10: "Diddle Champion", 11: "Diddle Hero", 12: "Diddle Titan",
    13: "Diddle God", 14: "Diddle Overlord", 15: "Diddle Emperor",
    16: "Diddle Immortal", 17: "Diddle Deity", 18: "Diddle Celestial",
    19: "Diddle Cosmic", 20: "Diddle Universal", 21: "Diddle Multiversal",
    22: "Diddle Omnipotent", 23: "Diddle Transcendent", 24: "Diddle Ascendant",
    25: "DADDY DIDDLER SUPREME", 26: "Diddle Annihilator", 27: "Diddle Destroyer",
    28: "Diddle Devastator", 29: "Diddle Dominator", 30: "ULTIMATE DIDDLER",
}

# Role colors for each level
LEVEL_COLORS = {
    1: discord.Color(0x99AAB5), 2: discord.Color(0x1ABC9C), 3: discord.Color(0x2ECC71),
    4: discord.Color(0x1F8B4C), 5: discord.Color(0x3498DB), 6: discord.Color(0x206694),
    7: discord.Color(0x9B59B6), 8: discord.Color(0x71368A), 9: discord.Color(0xE91E63),
    10: discord.Color(0xAD1457), 11: discord.Color(0xF1C40F), 12: discord.Color(0xC27C0E),
    13: discord.Color(0xE67E22), 14: discord.Color(0xA84300), 15: discord.Color(0xE74C3C),
    16: discord.Color(0x992D22), 17: discord.Color(0xED4245), 18: discord.Color(0x57F287),
    19: discord.Color(0x5865F2), 20: discord.Color(0x5865F2), 21: discord.Color(0xEB459E),
    22: discord.Color(0xFEE75C), 23: discord.Color(0x23272A), 24: discord.Color(0x7289DA),
    25: discord.Color(0xFFD700), 26: discord.Color(0xFF0000), 27: discord.Color(0x00FF00),
    28: discord.Color(0x0000FF), 29: discord.Color(0xFF00FF), 30: discord.Color(0xFFFFFF),
}

ROLE_PREFIX = os.getenv("ROLE_PREFIX", "Diddler ")

# ULTIMATE DIDDLER BOT TOKENS - loaded from .env
ULTIMATE_BOT_TOKENS = [
    os.getenv("ULTIMATE_BOT_TOKEN_1", ""),
    os.getenv("ULTIMATE_BOT_TOKEN_2", ""),
    os.getenv("ULTIMATE_BOT_TOKEN_3", ""),
    os.getenv("ULTIMATE_BOT_TOKEN_4", ""),
    os.getenv("ULTIMATE_BOT_TOKEN_5", ""),
]

ULTIMATE_BOT_NAMES = [
    os.getenv("ULTIMATE_BOT_NAME_1", "Mommy-Diddeler"),
    os.getenv("ULTIMATE_BOT_NAME_2", "Brother-Diddler"),
    os.getenv("ULTIMATE_BOT_NAME_3", "Sister-Diddler"),
    os.getenv("ULTIMATE_BOT_NAME_4", "Dog-Diddler"),
    os.getenv("ULTIMATE_BOT_NAME_5", "Baby-Diddler"),
]

# Cooldown tracking
diddle_cooldowns = {}
infect_daily_uses = {}
ultimate_diddle_cooldowns = {}

# Bypass tracking for admin command
bypassed_users = {}  # {user_id: expiry_timestamp}

# Active ultimate diddle sessions
active_ultimate_sessions = {}  # {target_id: asyncio.Task}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return defaultdict(lambda: {"uses": 0, "targets": {}, "level": 0, "xp": 0}, data)
    return defaultdict(lambda: {"uses": 0, "targets": {}, "level": 0, "xp": 0})

def save_data(data):
    serializable = {k: dict(v) for k, v in data.items()}
    for k in serializable:
        serializable[k]["targets"] = dict(serializable[k]["targets"])
    with open(DATA_FILE, "w") as f:
        json.dump(serializable, f, indent=2)

def get_level_from_uses(uses):
    current_level = 0
    for level, threshold in sorted(LEVEL_THRESHOLDS.items()):
        if uses >= threshold:
            current_level = level
        else:
            break
    return current_level

def get_next_level_info(current_level, uses):
    if current_level >= 30:
        return None, None
    next_level = current_level + 1
    needed = LEVEL_THRESHOLDS[next_level] - uses
    return next_level, needed

def get_role_name(level):
    title = LEVEL_TITLES.get(level, f"Level {level}")
    return f"{ROLE_PREFIX}[Lv.{level}] {title}"

def get_diddle_cooldown_remaining(user_id):
    if user_id not in diddle_cooldowns:
        return 0
    last_used = diddle_cooldowns[user_id]
    cooldown_end = last_used + timedelta(hours=10)
    now = datetime.now()
    if now >= cooldown_end:
        return 0
    remaining = cooldown_end - now
    return int(remaining.total_seconds())

def get_ultimate_diddle_cooldown_remaining(user_id):
    if user_id not in ultimate_diddle_cooldowns:
        return 0
    last_used = ultimate_diddle_cooldowns[user_id]
    cooldown_end = last_used + timedelta(minutes=10)
    now = datetime.now()
    if now >= cooldown_end:
        return 0
    remaining = cooldown_end - now
    return int(remaining.total_seconds())

def get_infect_uses_today(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    if user_id not in infect_daily_uses:
        infect_daily_uses[user_id] = {"date": today, "count": 0}
        return 0
    if infect_daily_uses[user_id]["date"] != today:
        infect_daily_uses[user_id] = {"date": today, "count": 0}
        return 0
    return infect_daily_uses[user_id]["count"]

def use_infect(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    if user_id not in infect_daily_uses or infect_daily_uses[user_id]["date"] != today:
        infect_daily_uses[user_id] = {"date": today, "count": 1}
    else:
        infect_daily_uses[user_id]["count"] += 1

def format_time_remaining(seconds):
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def is_bypassed(user_id):
    """Check if a user has active bypass."""
    if user_id in bypassed_users:
        if datetime.now() < bypassed_users[user_id]:
            return True
        else:
            del bypassed_users[user_id]
    return False

leaderboard_data = load_data()

class UltimateDiddleBot:
    """Individual bot instance for ultimate diddle attacks."""
    def __init__(self, token, name, index):
        self.token = token
        self.name = name
        self.index = index
        self.client = None
        self.ready = False
        self.dm_count = 0
        self.channel_messages = 0
        self.guild_joined = False
    
    async def start(self):
        """Start the bot and connect to Discord."""
        intents_mini = discord.Intents.default()
        intents_mini.members = True
        self.client = discord.Client(intents=intents_mini)
        
        @self.client.event
        async def on_ready():
            print(f"[ULTIMATE] {self.name} ({self.client.user}) is online!")
            self.ready = True
        
        try:
            await self.client.start(self.token)
        except Exception as e:
            print(f"[ULTIMATE] {self.name} failed to start: {e}")
            self.ready = False
    
    async def stop(self):
        """Stop the bot."""
        if self.client:
            await self.client.close()
            self.ready = False
            self.guild_joined = False
    
    async def join_guild(self, invite_link_or_code):
        """Join a guild using an invite link or code."""
        if not self.ready:
            return False
        try:
            invite_code = invite_link_or_code
            if "/" in invite_link_or_code:
                invite_code = invite_link_or_code.split("/")[-1]
            
            invite = await self.client.fetch_invite(invite_code)
            await invite.accept()
            print(f"[ULTIMATE] {self.name} joined guild via invite!")
            self.guild_joined = True
            return True
        except Exception as e:
            print(f"[ULTIMATE] {self.name} failed to join guild: {e}")
            return False
    
    async def ensure_in_guild(self, guild_id):
        """Check if bot is in the guild, try to join if not."""
        if not self.ready:
            return False
        try:
            guild = self.client.get_guild(guild_id)
            if guild:
                self.guild_joined = True
                return True
            
            try:
                guild = await self.client.fetch_guild(guild_id)
                if guild:
                    self.guild_joined = True
                    return True
            except:
                pass
            
            print(f"[ULTIMATE] {self.name} is NOT in guild {guild_id}. DMs will fail without mutual guilds.")
            return False
        except Exception as e:
            print(f"[ULTIMATE] {self.name} error checking guild membership: {e}")
            return False
    
    async def send_dm(self, user_id, embed):
        """Send a DM to target user."""
        if not self.ready:
            return False
        try:
            user = await self.client.fetch_user(user_id)
            if user:
                await user.send(embed=embed)
                self.dm_count += 1
                return True
        except discord.Forbidden as e:
            print(f"[ULTIMATE] {self.name} DM forbidden (no mutual guilds or DMs disabled): {e}")
        except Exception as e:
            print(f"[ULTIMATE] {self.name} DM failed: {e}")
        return False
    
    async def send_channel_message(self, channel_id, content=None, embed=None):
        """Send a message in a channel."""
        if not self.ready:
            return False
        try:
            channel = await self.client.fetch_channel(channel_id)
            if channel:
                await channel.send(content=content, embed=embed)
                self.channel_messages += 1
                return True
        except Exception as e:
            print(f"[ULTIMATE] {self.name} channel msg failed: {e}")
        return False

class UltimateDiddleSquad:
    """Manages all 5 ultimate diddler bots."""
    def __init__(self):
        self.bots = []
        self.active = False
        self._init_bots()
    
    def _init_bots(self):
        for i, token in enumerate(ULTIMATE_BOT_TOKENS):
            if token and not token.startswith("BOT_TOKEN"):
                bot = UltimateDiddleBot(token, ULTIMATE_BOT_NAMES[i], i)
                self.bots.append(bot)
    
    async def deploy(self, guild_id, channel_id, target_id, attacker_name, invite_link=None, duration_minutes=5):
        """Deploy all 5 bots and unleash the ultimate diddling."""
        if self.active:
            return False, "Squad is already active!"
        
        self.active = True
        start_time = asyncio.get_event_loop().time()
        end_time = start_time + (duration_minutes * 60)
        
        bot_tasks = [asyncio.create_task(bot.start()) for bot in self.bots]
        await asyncio.sleep(5)
        
        ready_bots = [b for b in self.bots if b.ready]
        if len(ready_bots) < 3:
            await self._cleanup()
            return False, f"Only {len(ready_bots)}/5 bots connected. Aborting."
        
        for bot in ready_bots:
            in_guild = await bot.ensure_in_guild(guild_id)
            if not in_guild and invite_link:
                print(f"[ULTIMATE] Attempting to join {bot.name} to guild via invite...")
                await bot.join_guild(invite_link)
                await asyncio.sleep(2)
                await bot.ensure_in_guild(guild_id)
        
        ready_bots = [b for b in self.bots if b.ready]
        if len(ready_bots) < 3:
            await self._cleanup()
            return False, f"Only {len(ready_bots)}/5 bots ready after guild join attempts. Aborting."
        
        try:
            while asyncio.get_event_loop().time() < end_time and self.active:
                cycle_start = asyncio.get_event_loop().time()

                dm_embed = discord.Embed(
                    title=f"☠️ ULTIMATE DIDDLING FROM {attacker_name.upper()} ☠️",
                    description="THE DIDDLER LEGION HAS ARRIVED."
                               "You cannot escape."
                               "You cannot hide."
                               "The diddle is eternal. 😈",
                    color=discord.Color(0xFF0000)
                )
                dm_embed.set_image(url=random.choice(ULTIMATE_GIFS))
                dm_embed.set_footer(text=f"Bot Legion Attack | {datetime.now().strftime('%H:%M:%S')}")

                dm_tasks = [bot.send_dm(target_id, dm_embed) for bot in ready_bots]
                await asyncio.gather(*dm_tasks, return_exceptions=True)

                elapsed = asyncio.get_event_loop().time() - cycle_start
                sleep_time = max(0, 5 - elapsed)
                await asyncio.sleep(sleep_time)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[ULTIMATE SQUAD] Error during attack: {e}")
        finally:
            await self._cleanup()

        total_dms = sum(b.dm_count for b in self.bots)
        return True, f"Ultimate diddling complete! {total_dms} DMs delivered."
    
    async def _cleanup(self):
        """Stop all bots and reset state."""
        self.active = False
        for bot in self.bots:
            await bot.stop()
        self.bots = []
        self._init_bots()
    
    def abort(self):
        """Emergency abort."""
        self.active = False

ultimate_squad = UltimateDiddleSquad()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    
    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced!")

    async def on_ready(self):
        print(f"Bot logged in as {self.user}")

bot = MyBot()

async def get_or_create_level_role(guild, level):
    role_name = get_role_name(level)
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if existing_role:
        return existing_role
    
    color = LEVEL_COLORS.get(level, discord.Color.default())
    try:
        new_role = await guild.create_role(
            name=role_name,
            color=color,
            hoist=True,
            mentionable=True,
            reason="Auto-created by Diddle Bot for level progression"
        )
        print(f"Created role: {role_name}")
        return new_role
    except discord.Forbidden:
        print(f"Failed to create role {role_name}: Missing permissions")
        return None
    except Exception as e:
        print(f"Error creating role {role_name}: {e}")
        return None

async def update_user_roles(member, new_level):
    guild = member.guild
    diddler_roles = [role for role in member.roles if role.name.startswith(ROLE_PREFIX)]
    
    roles_to_remove = []
    for role in diddler_roles:
        if not role.name.startswith(f"{ROLE_PREFIX}[Lv.{new_level}]"):
            roles_to_remove.append(role)
    
    if roles_to_remove:
        try:
            await member.remove_roles(*roles_to_remove, reason="Level up - removing old diddler role")
        except Exception as e:
            print(f"Error removing roles: {e}")
    
    new_role = await get_or_create_level_role(guild, new_level)
    if new_role and new_role not in member.roles:
        try:
            await member.add_roles(new_role, reason=f"Level up to {new_level}")
            print(f"Added role {new_role.name} to {member.display_name}")
            return new_role
        except Exception as e:
            print(f"Error adding role: {e}")
            return None
    return new_role

async def check_level_up(interaction, user_id, old_level, new_level):
    if new_level > old_level:
        member = interaction.guild.get_member(int(user_id))
        if not member:
            return
        
        new_role = await update_user_roles(member, new_level)
        title = LEVEL_TITLES.get(new_level, f"Level {new_level}")
        
        embed = discord.Embed(
            title="🎉 LEVEL UP! 🎉",
            description=f"**{member.display_name}** has reached **Level {new_level}**!\n\n**{title}**",
            color=discord.Color.green()
        )
        
        if new_role:
            embed.add_field(
                name="New Role",
                value=f"You've been given the **{new_role.mention}** role!",
                inline=False
            )
        
        embed.set_footer(text=f"Total diddles: {leaderboard_data[user_id]['uses']}")
        await interaction.channel.send(content=member.mention, embed=embed)

@bot.tree.command(name="diddle", description="Diddle someone! (1 per hour cooldown)")
@app_commands.describe(user="The user to diddle")
async def diddle(interaction: discord.Interaction, user: discord.Member):
    user_id = str(interaction.user.id)
    
    if is_bypassed(user_id):
        pass
    else:
        cooldown_remaining = get_diddle_cooldown_remaining(user_id)
        if cooldown_remaining > 0:
            time_str = format_time_remaining(cooldown_remaining)
            await interaction.response.send_message(
                f"⏰ **Cooldown!** You can diddle again in **{time_str}**.\n"
                f"*(Limit: 1 diddle per hour)*",
                ephemeral=True
            )
            return
    
    if user.id == interaction.user.id:
        await interaction.response.send_message("You can't diddle yourself, weirdo!", ephemeral=True)
        return
    if user.bot:
        await interaction.response.send_message("You can't diddle a bot!", ephemeral=True)
        return
    
    target_id = str(user.id)
    old_level = leaderboard_data[user_id].get("level", 0)
    
    leaderboard_data[user_id]["uses"] += 1
    
    if target_id not in leaderboard_data[user_id]["targets"]:
        leaderboard_data[user_id]["targets"][target_id] = 0
    leaderboard_data[user_id]["targets"][target_id] += 1
    
    diddle_count = leaderboard_data[user_id]["targets"][target_id]
    new_level = get_level_from_uses(leaderboard_data[user_id]["uses"])
    leaderboard_data[user_id]["level"] = new_level
    
    if not is_bypassed(user_id):
        diddle_cooldowns[user_id] = datetime.now()
    
    save_data(leaderboard_data)
    await check_level_up(interaction, user_id, old_level, new_level)
    
    random_gif = random.choice(DIDDLE_GIFS)
    user1 = interaction.user.display_name
    user2 = user.display_name
    current_level = leaderboard_data[user_id]["level"]
    level_title = LEVEL_TITLES.get(current_level, f"Level {current_level}")
    
    s = "s" if diddle_count > 1 else ""
    embed = discord.Embed(
        title="Message from DADDY DIDDLER!",
        description=f"**{user1}** has diddled **{user2}** {diddle_count} time{s}!\n\nYO BRO, OIL UP ITS TIME!!",
        color=discord.Color.purple()
    )
    embed.set_image(url=random_gif)
    embed.set_footer(text=f"Total diddles by {user1}: {leaderboard_data[user_id]['uses']} | {level_title} (Lv.{current_level})")
    
    bypass_text = " **[BYPASSED]**" if is_bypassed(user_id) else ""
    await interaction.response.send_message(content=user.mention + bypass_text, embed=embed)

@bot.tree.command(name="leaderboard", description="Show the diddle leaderboard!")
async def leaderboard(interaction: discord.Interaction):
    if not leaderboard_data:
        await interaction.response.send_message("No diddles yet! Be the first to use `/diddle`!", ephemeral=True)
        return
    
    sorted_users = sorted(leaderboard_data.items(), key=lambda x: x[1]["uses"], reverse=True)
    
    embed = discord.Embed(
        title="🏆 DIDDLE LEADERBOARD 🏆",
        description="Who's the biggest diddler of them all?",
        color=discord.Color.gold()
    )
    
    medals = ["🥇", "🥈", "🥉"]
    description_lines = []
    
    for idx, (user_id, data) in enumerate(sorted_users[:10]):
        user = bot.get_user(int(user_id))
        name = user.display_name if user else f"User {user_id[:6]}..."
        level = data.get("level", 0)
        title = LEVEL_TITLES.get(level, f"Lv.{level}")
        medal = medals[idx] if idx < 3 else f"#{idx + 1}"
        s = "s" if data['uses'] != 1 else ""
        description_lines.append(f"{medal} **{name}** — {data['uses']} diddle{s} | *{title}*")
    
    embed.description = "\n".join(description_lines)
    total_diddles = sum(d["uses"] for d in leaderboard_data.values())
    embed.set_footer(text=f"Total diddles across the server: {total_diddles}")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="level", description="Check your diddle level and progress!")
@app_commands.describe(user="Optional: Check another user's level")
async def level(interaction: discord.Interaction, user: discord.Member = None):
    target = user if user else interaction.user
    user_id = str(target.id)
    
    if user_id not in leaderboard_data or leaderboard_data[user_id]["uses"] == 0:
        await interaction.response.send_message(
            f"**{target.display_name}** hasn't diddled anyone yet! Use `/diddle` to start!",
            ephemeral=True
        )
        return
    
    data = leaderboard_data[user_id]
    current_level = data.get("level", 0)
    uses = data["uses"]
    title = LEVEL_TITLES.get(current_level, f"Level {current_level}")
    next_level, needed = get_next_level_info(current_level, uses)
    
    embed = discord.Embed(title=f"📊 {target.display_name}'s Stats", color=discord.Color.blue())
    embed.add_field(name="Level", value=f"**{current_level}**", inline=True)
    embed.add_field(name="Title", value=f"**{title}**", inline=True)
    embed.add_field(name="Total Diddles", value=f"**{uses}**", inline=True)
    
    if next_level:
        s = "s" if needed != 1 else ""
        embed.add_field(name="Next Level", value=f"Level {next_level} — **{needed}** more diddle{s} needed!", inline=False)
    else:
        embed.add_field(name="Status", value="**MAX LEVEL REACHED!** You're the ULTIMATE DIDDLER! 🏆", inline=False)
    
    diddler_role = discord.utils.find(lambda r: r.name.startswith(ROLE_PREFIX), target.roles)
    if diddler_role:
        embed.add_field(name="Current Role", value=diddler_role.mention, inline=False)
    
    targets = data.get("targets", {})
    if targets:
        top_targets = sorted(targets.items(), key=lambda x: x[1], reverse=True)[:3]
        target_text = []
        for tid, count in top_targets:
            tuser = bot.get_user(int(tid))
            tname = tuser.display_name if tuser else f"User {tid[:6]}..."
            s = "s" if count != 1 else ""
            target_text.append(f"• **{tname}**: {count} time{s}")
        embed.add_field(name="Top Targets", value="\n".join(target_text), inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="infect", description="Infect a user with the diddle virus! (Level 25, 3/day limit)")
@app_commands.describe(user="The user to infect")
async def infect(interaction: discord.Interaction, user: discord.Member):
    user_id = str(interaction.user.id)
    current_level = leaderboard_data[user_id].get("level", 0)
    
    bypassed = is_bypassed(user_id)
    
    if not bypassed and current_level < 25:
        await interaction.response.send_message(
            f"You need to be **Level 25** to use `/infect`! You're currently Level {current_level}. Keep diddling! 💪",
            ephemeral=True
        )
        return
    
    if user.id == interaction.user.id:
        await interaction.response.send_message("You can't infect yourself, weirdo!", ephemeral=True)
        return
    if user.bot:
        await interaction.response.send_message("You can't infect a bot!", ephemeral=True)
        return
    
    if not bypassed:
        infect_used_today = get_infect_uses_today(user_id)
        if infect_used_today >= 3:
            now = datetime.now()
            midnight = datetime(now.year, now.month, now.day) + timedelta(days=1)
            time_until_reset = int((midnight - now).total_seconds())
            reset_str = format_time_remaining(time_until_reset)
            
            await interaction.response.send_message(
                f"🚫 **Daily limit reached!** You've used all **3** infects today.\n"
                f"Resets in: **{reset_str}**",
                ephemeral=True
            )
            return
    
    bot_member = interaction.guild.me
    can_manage_nick = bot_member.guild_permissions.manage_nicknames
    
    if not can_manage_nick:
        await interaction.response.send_message(
            "❌ **Error:** I don't have `Manage Nicknames` permission! Ask an admin to give me this permission.",
            ephemeral=True
        )
        return
    
    if user.top_role >= bot_member.top_role:
        await interaction.response.send_message(
            f"❌ **Error:** I can't change **{user.display_name}**'s nickname because their highest role is equal to or higher than mine!\n"
            f"• My top role: {bot_member.top_role.mention}\n"
            f"• Their top role: {user.top_role.mention}\n\n"
            f"**Fix:** Drag my role above {user.top_role.mention} in Server Settings → Roles.",
            ephemeral=True
        )
        return
    
    if not bypassed:
        use_infect(user_id)
        remaining_today = 3 - get_infect_uses_today(user_id)
    else:
        remaining_today = "∞"
    
    bypass_text = " **[BYPASSED]**" if bypassed else ""
    await interaction.response.send_message(
        f"🦠 **{interaction.user.display_name}** has infected **{user.display_name}**!{bypass_text}\n"
        f"({remaining_today}/3 infects remaining today)\n"
        f"The diddle virus is spreading! 🦠"
    )
    
    original_nick = user.nick
    nick_changed = False
    
    try:
        await user.edit(nick="DIDDLER [INFECTED]")
        nick_changed = True
        print(f"[INFECT] Changed {user.display_name}'s nickname to 'DIDDLER [INFECTED]'")
    except discord.Forbidden as e:
        print(f"[INFECT ERROR] Forbidden: {e}")
        await interaction.channel.send(f"⚠️ Couldn't change {user.mention}'s nickname (permission issue). Continuing with DMs...")
    except Exception as e:
        print(f"[INFECT ERROR] {type(e).__name__}: {e}")
        await interaction.channel.send(f"⚠️ Couldn't change {user.mention}'s nickname: {e}. Continuing with DMs...")
    
    dm_count = 0
    start_time = asyncio.get_event_loop().time()
    end_time = start_time + 120
    
    try:
        while asyncio.get_event_loop().time() < end_time:
            random_gif = random.choice(DIDDLE_GIFS)
            embed = discord.Embed(
                title="🦠 YOU'VE BEEN INFECTED! 🦠",
                description=f"**{interaction.user.display_name}** has infected you with the diddle virus!\n\nThere's no escape... 😈",
                color=discord.Color.red()
            )
            embed.set_image(url=random_gif)
            embed.set_footer(text="Infection by Level 25 DADDY DIDDLER SUPREME")
            
            try:
                await user.send(embed=embed)
                dm_count += 1
            except discord.Forbidden:
                await interaction.channel.send(f"⚠️ {user.mention} has DMs disabled. Stopping infection early.")
                break
            
            await asyncio.sleep(10)
        
        elapsed = asyncio.get_event_loop().time() - start_time
        remaining = max(0, 300 - elapsed)
        if remaining > 0:
            await asyncio.sleep(remaining)
        
    except asyncio.CancelledError:
        pass
    
    if nick_changed:
        try:
            if original_nick:
                await user.edit(nick=original_nick)
            else:
                await user.edit(nick=None)
            print(f"[INFECT] Reverted {user.display_name}'s nickname")
        except Exception as e:
            print(f"[INFECT ERROR] Couldn't revert nickname: {e}")
            await interaction.channel.send(f"⚠️ Couldn't revert {user.mention}'s nickname. An admin may need to fix it manually.")
    
    await interaction.channel.send(
        f"✅ **{user.display_name}** has been cured! The diddle infection is over. Total DMs sent: **{dm_count}**"
    )

@bot.tree.command(name="ultimate-diddle", description="UNLEASH THE ULTIMATE DIDDLING! (Level 30, 24h cooldown)")
@app_commands.describe(user="The user to ULTIMATELY diddle")
async def ultimate_diddle(interaction: discord.Interaction, user: discord.Member):
    user_id = str(interaction.user.id)
    current_level = leaderboard_data[user_id].get("level", 0)
    bypassed = is_bypassed(user_id)
    
    if not bypassed and current_level < 30:
        await interaction.response.send_message(
            f"🔒 **LOCKED!** You need to be **Level 30** to use `/ultimate-diddle`!\n"
            f"You're currently Level {current_level}. You're not worthy yet... 💀\n"
            f"Keep diddling, peasant! 💪",
            ephemeral=True
        )
        return
    
    if user.id == interaction.user.id:
        await interaction.response.send_message("You can't ultimate-diddle yourself, weirdo!", ephemeral=True)
        return
    if user.bot:
        await interaction.response.send_message("You can't ultimate-diddle a bot!", ephemeral=True)
        return
    
    if not bypassed:
        cooldown_remaining = get_ultimate_diddle_cooldown_remaining(user_id)
        if cooldown_remaining > 0:
            time_str = format_time_remaining(cooldown_remaining)
            await interaction.response.send_message(
                f"⏰ **ULTIMATE COOLDOWN!** Your power needs to recharge!\n"
                f"Available again in: **{time_str}**\n"
                f"*(Limit: 1 ultimate diddle per 24 hours)*",
                ephemeral=True
            )
            return
    
    if all(not token or token.startswith("BOT_TOKEN") for token in ULTIMATE_BOT_TOKENS):
        await interaction.response.send_message(
            "⚠️ **ULTIMATE DIDDLER bots are not configured yet!**\n"
            f"Add your 5 bot tokens to the `.env` file.\n"
            f"See `.env.example` for the required variables.",
            ephemeral=True
        )
        return
    
    target_id = str(user.id)
    if target_id in active_ultimate_sessions:
        await interaction.response.send_message(
            f"🚫 **{user.display_name}** is already being ULTIMATELY diddled! Wait for the current assault to finish.",
            ephemeral=True
        )
        return
    
    if not bypassed:
        ultimate_diddle_cooldowns[user_id] = datetime.now()
    
    bypass_text = " **[BYPASSED]**" if bypassed else ""
    embed = discord.Embed(
        title="☠️ ULTIMATE DIDDLING INCOMING ☠️",
        description=f"**{interaction.user.display_name}** has summoned the **ULTIMATE DIDDLER LEGION** upon **{user.display_name}**!{bypass_text}\n\n"
                    f"Five bots awaken from the shadows...\n"
                    f"The diddle apocalypse begins... 😈",
        color=discord.Color(0xFFFFFF)
    )
    embed.set_image(url=random.choice(DIDDLE_GIFS))
    embed.set_footer(text="ULTIMATE DIDDLER | Level 30 Power | 24h Cooldown")
    
    await interaction.response.send_message(content=user.mention, embed=embed)
    
    invite_link = None
    try:
        invites = await interaction.guild.invites()
        if invites:
            invite_link = invites[0].url
        else:
            try:
                invite = await interaction.channel.create_invite(max_age=3600, max_uses=10, unique=True)
                invite_link = invite.url
                print(f"[ULTIMATE] Created invite for bots: {invite_link}")
            except Exception as e:
                print(f"[ULTIMATE] Could not create invite: {e}")
    except Exception as e:
        print(f"[ULTIMATE] Error getting invite: {e}")
    
    async def run_ultimate():
        try:
            success, result = await ultimate_squad.deploy(
                guild_id=interaction.guild_id,
                channel_id=interaction.channel_id,
                target_id=user.id,
                attacker_name=interaction.user.display_name,
                invite_link=invite_link,
                duration_minutes=5
            )
            
            if success:
                final_embed = discord.Embed(
                    title="🔥 ULTIMATE DIDDLING COMPLETE 🔥",
                    description=f"**{interaction.user.display_name}**'s ULTIMATE DIDDLING of **{user.display_name}** is complete!{bypass_text}\n\n"
                                f"{result}\n"
                                f"The diddler legion returns to the shadows... for now.",
                    color=discord.Color(0xFFD700)
                )
                final_embed.set_image(url=random.choice(ULTIMATE_GIFS))
                await interaction.channel.send(embed=final_embed)
            else:
                await interaction.channel.send(f"⚠️ **Ultimate Diddle Failed:** {result}")
        except Exception as e:
            print(f"[ULTIMATE ERROR] {e}")
            await interaction.channel.send(f"❌ An error occurred during the ultimate diddling: {e}")
        finally:
            if target_id in active_ultimate_sessions:
                del active_ultimate_sessions[target_id]
    
    task = asyncio.create_task(run_ultimate())
    active_ultimate_sessions[target_id] = task

@bot.tree.command(name="abort-ultimate", description="Emergency abort an active ultimate diddle (Admin/Owner only)")
@app_commands.describe(user="The user being ultimate-diddled to abort")
async def abort_ultimate(interaction: discord.Interaction, user: discord.Member):
    is_admin = interaction.user.guild_permissions.administrator
    is_owner = interaction.user.id == OWNER_ID
    
    if not is_admin and not is_owner:
        await interaction.response.send_message(
            "You don't have permission to use this command! Only **Server Admins** and the **Bot Owner** can abort.", 
            ephemeral=True
        )
        return
    
    target_id = str(user.id)
    if target_id not in active_ultimate_sessions:
        await interaction.response.send_message(
            f"**{user.display_name}** is not currently being ultimate-diddled.",
            ephemeral=True
        )
        return
    
    task = active_ultimate_sessions[target_id]
    task.cancel()
    ultimate_squad.abort()
    del active_ultimate_sessions[target_id]
    
    await interaction.response.send_message(
        f"🚫 **ABORTED!** The ultimate diddling of **{user.display_name}** has been stopped by **{interaction.user.display_name}**.",
        ephemeral=False
    )

@bot.tree.command(name="bypass-restrictions", description="Bypass all cooldowns and level requirements for a user (Admin/Owner only)")
@app_commands.describe(
    user="The user to grant bypass to",
    duration_minutes="How long the bypass lasts (default: 60 minutes, max: 1440)"
)
async def bypass_restrictions(interaction: discord.Interaction, user: discord.Member, duration_minutes: int = 60):
    is_admin = interaction.user.guild_permissions.administrator
    is_owner = interaction.user.id == OWNER_ID
    
    if not is_admin and not is_owner:
        await interaction.response.send_message(
            "🚫 **Access Denied!** Only **Server Admins** and the **Bot Owner** can use `/bypass-restrictions`.", 
            ephemeral=True
        )
        return
    
    if duration_minutes < 1:
        await interaction.response.send_message("Duration must be at least 1 minute!", ephemeral=True)
        return
    if duration_minutes > 1440:
        duration_minutes = 1440
    
    user_id = str(user.id)
    expiry = datetime.now() + timedelta(minutes=duration_minutes)
    bypassed_users[user_id] = expiry
    
    embed = discord.Embed(
        title="⚡ BYPASS ACTIVATED ⚡",
        description=f"**{interaction.user.display_name}** has granted **{user.display_name}** unrestricted diddling powers!\n\n"
                    f"🔓 **All restrictions bypassed:**\n"
                    f"• No diddle cooldowns\n"
                    f"• No level requirements for `/infect`\n"
                    f"• No level requirement for `/ultimate-diddle`\n"
                    f"• No infect daily limits\n"
                    f"• No ultimate diddle cooldown",
        color=discord.Color(0xFF00FF)
    )
    embed.add_field(
        name="⏰ Expires In",
        value=f"**{duration_minutes}** minute{'s' if duration_minutes != 1 else ''}\n"
              f"({expiry.strftime('%H:%M:%S')})",
        inline=False
    )
    embed.set_footer(text="Use wisely... or don't. 😈")
    
    await interaction.response.send_message(content=user.mention, embed=embed)

@bot.tree.command(name="remove-bypass", description="Remove bypass restrictions from a user (Admin/Owner only)")
@app_commands.describe(user="The user to remove bypass from")
async def remove_bypass(interaction: discord.Interaction, user: discord.Member):
    is_admin = interaction.user.guild_permissions.administrator
    is_owner = interaction.user.id == OWNER_ID
    
    if not is_admin and not is_owner:
        await interaction.response.send_message(
            "🚫 **Access Denied!** Only **Server Admins** and the **Bot Owner** can remove bypasses.", 
            ephemeral=True
        )
        return
    
    user_id = str(user.id)
    if user_id in bypassed_users:
        del bypassed_users[user_id]
        await interaction.response.send_message(
            f"🔒 **{user.display_name}**'s bypass has been revoked by **{interaction.user.display_name}**.\n"
            f"Back to the grind, peasant! 💀",
            ephemeral=False
        )
    else:
        await interaction.response.send_message(
            f"**{user.display_name}** doesn't have an active bypass.",
            ephemeral=True
        )

@bot.tree.command(name="list-bypasses", description="List all active bypasses (Admin/Owner only)")
async def list_bypasses(interaction: discord.Interaction):
    is_admin = interaction.user.guild_permissions.administrator
    is_owner = interaction.user.id == OWNER_ID
    
    if not is_admin and not is_owner:
        await interaction.response.send_message(
            "🚫 **Access Denied!** Only **Server Admins** and the **Bot Owner** can view bypasses.", 
            ephemeral=True
        )
        return
    
    if not bypassed_users:
        await interaction.response.send_message("No active bypasses. Everyone's playing fair... for now. 😏", ephemeral=True)
        return
    
    lines = []
    now = datetime.now()
    for uid, expiry in list(bypassed_users.items()):
        if now >= expiry:
            del bypassed_users[uid]
            continue
        remaining = int((expiry - now).total_seconds())
        time_str = format_time_remaining(remaining)
        member = interaction.guild.get_member(int(uid))
        name = member.display_name if member else f"User {uid[:6]}..."
        lines.append(f"• **{name}** — expires in **{time_str}**")
    
    if not lines:
        await interaction.response.send_message("No active bypasses remaining.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🔓 ACTIVE BYPASSES 🔓",
        description="\n".join(lines),
        color=discord.Color(0xFF00FF)
    )
    embed.set_footer(text=f"Total active: {len(lines)}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="level-give", description="Give diddle levels to a user (Admin/Owner only)")
@app_commands.describe(user="The user to give levels to", amount="Amount of levels to add")
async def level_give(interaction: discord.Interaction, user: discord.Member, amount: int):
    is_admin = interaction.user.guild_permissions.administrator
    is_owner = interaction.user.id == OWNER_ID
    
    if not is_admin and not is_owner:
        await interaction.response.send_message(
            "You don't have permission to use this command! Only **Server Admins** and the **Bot Owner** can use it.", 
            ephemeral=True
        )
        return
    
    if amount <= 0:
        await interaction.response.send_message("Amount must be positive!", ephemeral=True)
        return
    if amount > 30:
        await interaction.response.send_message("Maximum level is 30!", ephemeral=True)
        return
    
    user_id = str(user.id)
    if user_id not in leaderboard_data:
        leaderboard_data[user_id] = {"uses": 0, "targets": {}, "level": 0, "xp": 0}
    
    target_level = min(amount, 30)
    required_uses = LEVEL_THRESHOLDS.get(target_level, 0)
    old_level = leaderboard_data[user_id].get("level", 0)
    leaderboard_data[user_id]["uses"] = max(leaderboard_data[user_id]["uses"], required_uses)
    leaderboard_data[user_id]["level"] = target_level
    
    save_data(leaderboard_data)
    new_role = await update_user_roles(user, target_level)
    title = LEVEL_TITLES.get(target_level, f"Level {target_level}")
    
    embed = discord.Embed(
        title="⚡ LEVEL GIVEN! ⚡",
        description=f"**{interaction.user.display_name}** has granted **{user.display_name}** Level **{target_level}**!\n\n**{title}**",
        color=discord.Color.gold()
    )
    
    if new_role:
        embed.add_field(name="Role Assigned", value=new_role.mention, inline=False)
    
    embed.set_footer(text=f"Previous level: {old_level} | New level: {target_level}")
    await interaction.response.send_message(content=user.mention, embed=embed)

@level_give.error
async def level_give_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You need **Administrator** permissions to use this command!", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)

@bot.tree.command(name="sync-roles", description="Sync all diddler roles for users in this server (Admin only)")
@app_commands.checks.has_permissions(administrator=True)
async def sync_roles(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    guild = interaction.guild
    updated = 0
    created = 0
    
    for level in range(1, 31):
        role = await get_or_create_level_role(guild, level)
        if role:
            created += 1
    
    for user_id, data in leaderboard_data.items():
        level = data.get("level", 0)
        if level > 0:
            member = guild.get_member(int(user_id))
            if member:
                await update_user_roles(member, level)
                updated += 1
    
    await interaction.followup.send(
        f"✅ Role sync complete!\n"
        f"• Created/verified **{created}** level roles\n"
        f"• Updated roles for **{updated}** members"
    )

@sync_roles.error
async def sync_roles_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You need **Administrator** permissions to use this command!", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)

# Run the bot using the token from .env
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
