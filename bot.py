import traceback
import logging
import os
import discord
from discord import app_commands
import math
import json
import requests
import emoji
from aiohttp import ClientSession
from discord import app_commands
from discord import File, Webhook, SyncWebhook
import sqlite3
import asyncio
import random
import time
from datetime import timedelta
import datetime
import typing
import aiosqlite
from dotenv import load_dotenv
from discord.ui import View, Button
from discord.ext import commands, tasks
from Adventure import *
import uuid

# AdventurersGuild

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']
TOKEN = "" if not TOKEN else TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.reactions = True

# variables
#test variables on test server
#roles = {"guild":1229444878552006708, "silenced":1212840459102064711, "spirit":1224760371915526145, "taunted":1224513474432991324, "enchanted_taunted":1225117686883946563, "enchanted_silenced":1225117688200691936, "trickery":1224519072171954209, "cleric":1222840622214414416, "cleric2":0, "jester":1222840635149778986, "jester2": 1223021547837456394, "magician":1222837868490264636, "magician2":0, "wildshaper":1212840464445743155, "wildshaper2":0, "fae":1212840465100046336, "fae2":0, "mystic":1183898566951981128, "mystic2":0, "pirate":1222255974811701338, "pirate2":0, "bard":1222255705684447303, "bard2":1224521365835747328, "bards_blessing_red":1224521397431435355,"bards_blessing_magenta":1224521391135526912,"bards_blessing_cyan":1224521392817442896, "bards_blessing_green":1224521523793231892, "bards_blessing_blue":1224521395208327259, "bards_blessing_yellow":1224521701208096859, "pig":1224841281843368007, "cat":1224841280387809431, "dog":1224841279113003224, "frog":1224841274478170172, "unicorn":1224841277460316342, "shark":1224858851837218876, "wolf":1224858868027228304, "chick":1221944610545471678, "tiger":1224858866160767116, "sagesgrace":1224863430222282812, "plant-admin":1244657453183008808}
#emojis = {"magician":"<:MAGE:1224412539602079925>","jester":"<:JESTER:1224412538721009715>","bard":"<:BARD:1224412499106070558>","pirate":"<:PIRATE:1224412559550189669>","fae":"<:FAE:1224412501773389987>","mystic":"<:MYSTIC:1224412558287437834>","wildshaper":"<:WILDHSHAPER:1224412540512239678>","cleric":"<:CLERIC:1224412500465025074>"}
#channels = {"spirit":1224756963901177896, "job_change":1058517858507833354, "leveling":1225083241912991766}

roles = {"guild":1233907434284781588, "silenced":1233903289045880872, "spirit":1233902805924970598, "taunted":1233907772370976808, "enchanted_taunted":1234248628487327847, "enchanted_silenced":1233903288454221895, "trickery":1233907671770337343, "cleric":1233907164574384199, "cleric2":1233907163827671071, "jester":1233903291851739166, "jester2": 1233903291390361670, "magician":1233903290278740100, "magician2":1233903290442448896, "wildshaper":1233905939124588564, "wildshaper2":1233907163215171604, "fae":1233905936372862986, "fae2":1233905937081831537, "mystic":1233905938302369906, "mystic2":1233905937375563878, "pirate":1233905935513157662, "pirate2":1233905934816772106, "bard":1233905933822722139, "bard2":1233905932296261633, "elder2": 1257301087686230117, "bards_blessing_red":1233903284230815784,"bards_blessing_magenta":1233903284494794823,"bards_blessing_cyan":1233903287162503168, "bards_blessing_green":1233903286457995344, "bards_blessing_blue":1233903285581385789, "bards_blessing_yellow":1233903287745515540, "pig":1233902817807171634, "cat":1233903159047491654, "dog":1233903278400606320, "rat":1233903279499509820, "unicorn":1233903280556347452, "whale":1233903281651056751, "cockroach":1233903282754420856, "wolf":1234249749071396954, "tiger":1234249750438478025, "giraffe":1245083236451880980, "sagesgrace":1233903283668652042, "tspirit":1234536299545890826, "plant-admin":1234236361645494312}
emojis = {"magician":"<:MAGE:1224412539602079925>","jester":"<:JESTER:1224412538721009715>","bard":"<:BARD:1224412499106070558>","pirate":"<:PIRATE:1224412559550189669>","fae":"<:FAE:1224412501773389987>","mystic":"<:MYSTIC:1224412558287437834>","wildshaper":"<:WILDHSHAPER:1224412540512239678>","cleric":"<:CLERIC:1224412500465025074>", "elder": "<>"}
channels = {"spirit":1234251593700868186, "job_change":1213218513221718096, "leveling":1243857865886924840}
excludedChannels = [1193533785908715600, 1216723387200569437, 1179174879845683221, 1263945044369342506]
excludedCategorys = [1193631336406200420, 1193631336406200420]
doubleChannels = []
levelroles = {"1": 1241664860618752112,
"5": 1241664865802780812,
"10":1241664867232907286,
"15":1241664868327620708,
"20":1241664868759765002,
"30":1241664870324113469,
"40":1241664871712555018,
"50":1241664872983564288,
"60":1241664874254172160,
"70":1241664874350645308,
"80":1241664875709862011,
"90":1241658370449080320,
"100": 1241658571091873872}

closed = False
closedCategorys = []


correctwebhookname = 'ADVENTURES GUILD OFFICIAL WEBHOOK [1]'
expPerCooldown = 45
cooldownInSeconds = 35
levelToClass = 10
levelToEnchant = 50


config = app_commands.Group(name="config", description="To change.")


class StartSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Sign",  custom_id='start_select_view1')
    async def join(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = interaction.guild.get_role(roles['guild'])
        if role in interaction.user.roles:
            await interaction.response.defer()
            return
        else:
            pass
        await interaction.user.add_roles(role)
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT user_id FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                result9 = await cursor.fetchone()
        if result9 is None:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f"INSERT INTO 'exp' (user_id, xp, class, guild_id, valid, cooldown) VALUES ({interaction.user.id}, 0, 0, {interaction.guild.id}, 0, 0)"
                await db.execute(sqlquery)
                await db.commit()
        await interaction.followup.send(content=f"**Congratulations!** You joined the Adventurers Guild! **Reach level 10 to choose a class!**", ephemeral=True)


       
class ClassSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Magician",  custom_id='class_select_view1', row=1)
    async def magician(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 1
        className = 'magician'
        enchantedClassName = 'archmage'
        cemoji = emojis["magician"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and valid[2] != 0 and str(valid[2]) == str(f'{classInt}'):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            role2 = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.remove_roles(role2)
            except:
                pass
            
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={classInt} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            member = interaction.user
            role = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {className.capitalize()} {cemoji}, reach Level {levelToEnchant} to get enchanted! Good luck on your journey and may the winds of fortune be ever in your favor.', ephemeral=True)
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToClass} or already have a class.', ephemeral=True)

       

    @discord.ui.button(label="Jester",  custom_id='class_select_view_2', row=1)
    async def jester(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 2
        className = 'jester'
        enchantedClassName = 'trickster'
        cemoji = emojis["jester"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and valid[2] != 0 and str(valid[2]) == str(f'{classInt}'):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            role2 = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.remove_roles(role2)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={classInt} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            member = interaction.user
            role = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {className.capitalize()} {cemoji}, reach Level {levelToEnchant} to get enchanted! Good luck on your journey and may the winds of fortune be ever in your favor.', ephemeral=True)
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToClass} or already have a class.', ephemeral=True)
        
        
    @discord.ui.button(label="Bard",  custom_id='class_select_view_3', row=1)
    async def bard(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 3
        className = 'bard'
        enchantedClassName = 'enchanter'
        cemoji = emojis["bard"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and valid[2] != 0 and str(valid[2]) == str(f'{classInt}'):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            role2 = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.remove_roles(role2)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={classInt} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            member = interaction.user
            role = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {className.capitalize()} {cemoji}, reach Level {levelToEnchant} to get enchanted! Good luck on your journey and may the winds of fortune be ever in your favor.', ephemeral=True)
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToClass} or already have a class.', ephemeral=True)

    
    @discord.ui.button(label="Pirate",  custom_id='class_select_view_4', row=1)
    async def pirate(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 4
        className = 'pirate'
        enchantedClassName = 'captain'
        cemoji = emojis["pirate"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and valid[2] != 0 and str(valid[2]) == str(f'{classInt}'):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            role2 = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.remove_roles(role2)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={classInt} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            member = interaction.user
            role = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {className.capitalize()} {cemoji}, reach Level {levelToEnchant} to get enchanted! Good luck on your journey and may the winds of fortune be ever in your favor.', ephemeral=True)
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToClass} or already have a class.', ephemeral=True)
    
    
    @discord.ui.button(label="Fae",  custom_id='class_select_view_5', row=2)
    async def fae(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 5
        className = 'fae'
        enchantedClassName = 'feylight'
        cemoji = emojis["fae"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and valid[2] != 0 and str(valid[2]) == str(f'{classInt}'):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            role2 = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.remove_roles(role2)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={classInt} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            member = interaction.user
            role = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {className.capitalize()} {cemoji}, reach Level {levelToEnchant} to get enchanted! Good luck on your journey and may the winds of fortune be ever in your favor.', ephemeral=True)
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToClass} or already have a class.', ephemeral=True)
    
    @discord.ui.button(label="Mystic",  custom_id='class_select_view_6', row=2)
    async def mystic(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 6
        className = 'mystic'
        enchantedClassName = 'celestial'
        cemoji = emojis["mystic"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and valid[2] != 0 and str(valid[2]) == str(f'{classInt}'):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            role2 = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.remove_roles(role2)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={classInt} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            member = interaction.user
            role = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {className.capitalize()} {cemoji}, reach Level {levelToEnchant} to get enchanted! Good luck on your journey and may the winds of fortune be ever in your favor.', ephemeral=True)
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToClass} or already have a class.', ephemeral=True)


    
    @discord.ui.button(label="Wildshaper",  custom_id='class_select_view_7', row=2)
    async def wildshaper(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 7
        className = 'wildshaper'
        enchantedClassName = 'beastmaster'
        cemoji = emojis["wildshaper"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and valid[2] != 0 and str(valid[2]) == str(f'{classInt}'):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            role2 = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.remove_roles(role2)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={classInt} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            member = interaction.user
            role = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {className.capitalize()} {cemoji}, reach Level {levelToEnchant} to get enchanted! Good luck on your journey and may the winds of fortune be ever in your favor.', ephemeral=True)
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToClass} or already have a class.', ephemeral=True)

    @discord.ui.button(label="Cleric",  custom_id='class_select_view_8', row=2)
    async def cleric(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 8
        className = 'cleric'
        enchantedClassName = 'sage'
        cemoji = emojis["cleric"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and valid[2] != 0 and str(valid[2]) == str(f'{classInt}'):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            role2 = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.remove_roles(role2)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={classInt} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            member = interaction.user
            role = interaction.guild.get_role(roles[f'{className.lower()}'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass
            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {className.capitalize()} {cemoji}, reach Level {levelToEnchant} to get enchanted! Good luck on your journey and may the winds of fortune be ever in your favor.', ephemeral=True)
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToClass} or already have a class.', ephemeral=True)

    @discord.ui.button(label="Elder",  custom_id='class_select_view_9', row=3)
    async def elder(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        classInt = 9
        className = 'elder'
        enchantedClassName = 'elder'
        cemoji = emojis["elder"]
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                level = await cursor.fetchone()
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT valid, cooldown, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                valid = await cursor.fetchone()
        if getLevel(level[0])[0] >= levelToEnchant and valid[0] == 1 and len(str(valid[2]))==1 and str(valid[2]) == '0':
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid=0 WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class={int(f"{classInt}{classInt}")} WHERE user_id={interaction.user.id}'''
                await db.execute(sqlquery2)
                await db.commit()
            role = interaction.guild.get_role(roles[f'{className.lower()}2'])
            try:
                await interaction.user.add_roles(role)
            except:
                pass

            # No role removal required since there is no non-enchanted role for this

            await interaction.followup.send(content=f'<@{interaction.user.id}>, **Congratulations!** You are now a {enchantedClassName.capitalize()} {cemoji}! Your dedication has unlocked new abilities for your role.', ephemeral=True)
        elif getLevel(level[0])[0] >= levelToClass and valid[2] == 0 and valid[0] == 1:
            try:
                await interaction.followup.send(content=f'<@{interaction.user.id}>, the elder class is special. You need to be Level {levelToEnchant} and classless to become an elder.', ephemeral=True)
            except:
                pass
        else:
            await interaction.followup.send(content=f'<@{interaction.user.id}>, you either are not Level {levelToEnchant} or already have a class.', ephemeral=True)

    @discord.ui.button(label="Reset",  custom_id='class_select_view_10', row=3)
    async def reset(self, interaction: discord.Interaction, Button2: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        v1 = View(timeout=6)
        b1 = Button(label="Yes")
        b2 = Button(label="No", style=discord.ButtonStyle.red)
        v1.add_item(b1)
        v1.add_item(b2)
        flwup = await interaction.followup.send(content='Are you sure?', view=v1, ephemeral=True)
        flwupid = int(flwup.id)
        async def b1_callback(interaction2: discord.Interaction):
            b1.disabled = True
            b2.disabled = True
            await interaction.followup.edit_message(content='Are you sure?', view=v1, message_id=flwupid)
            await interaction2.response.defer(ephemeral=True)
            async with aiosqlite.connect("exp.sqlite") as db:
                query = f"SELECT xp, cooldown FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
                async with db.execute(query) as cursor:
                    level = await cursor.fetchone()
            if getLevel(level[0])[0] >= 5:
                async with aiosqlite.connect("exp.sqlite") as db:
                    sqlquery = f'''UPDATE exp SET xp={4375+1} WHERE user_id={interaction2.user.id} AND guild_id = {interaction.guild.id}'''
                    await db.execute(sqlquery)
                    sqlquery2 = f'''UPDATE exp SET class={0} WHERE user_id={interaction2.user.id} AND guild_id = {interaction.guild.id}'''
                    await db.execute(sqlquery2)
                    await db.commit()
                    await db.execute(sqlquery)
                member = interaction.user
                for x in CLASSESINORDER:
                    try:
                        role = interaction.guild.get_role(roles[CLASSESINORDER[str(x)].lower()])
                        if role in member.roles:
                            await member.remove_roles(role)
                            break
                    except:
                        pass
                for x in CLASSESINORDER:
                    try:
                        role = interaction.guild.get_role(roles[CLASSESINORDER[str(x)].lower()+"2"])
                        if role in member.roles:
                            await member.remove_roles(role)
                            break
                    except:
                        pass
                for x,y in enumerate(levelroles):
                    try:
                        role = interaction.guild.get_role(levelroles[y])
                        if role in member.roles:
                            await member.remove_roles(role)
                            break
                    except:
                        pass
                role = interaction.guild.get_role(levelroles["5"])
                await member.add_roles(role)
                await flwup.delete()
                await interaction2.followup.send(content="You have been reset to No Class and you are now **Level 5**.", ephemeral=True)
            else:
                await interaction2.followup.send(content="You have to be at least **Level 5** to reset.", ephemeral=True)
                    
        async def b2_callback(interaction2: discord.Interaction):
            await flwup.delete()
                
        b1.callback = b1_callback
        b2.callback = b2_callback

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self) -> None:
       self.add_view(ClassSelectView())
       self.add_view(StartSelectView())

    async def on_ready(self):
        t = time.localtime()
        currenttime = time.strftime("%H:%M:%S", t)
        print("\n\nAdventurers Guild:\n")
        for guild in self.guilds:
            self.tree.clear_commands(guild=guild)
        await self.tree.sync()
        print(f"Ready! @ {currenttime}")

        return await bot.change_presence(activity=discord.Activity(type=4, name = "Start your adventure!"))


    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.author.id in [242681702512721931, 816769793231028244, 270250238420189184] and message.content == "!!rolechangeembed":
            thisChannel = message.channel
            WEBHOOK_URL = 'https://discord.com/api/webhooks/1234262314094559313/BASXhcP4sF1H6hwQ2zqFuL8GtLtcINTNb5BW8MBoaCZw6MHkM8oycgflNOmc_2EZQSWQ'
            level10Message = f'''Congratulations, esteemed adventurer! You've reached level {levelToClass}, a significant milestone indeed.

You are now eligible to select one of the eight distinguished classes offered by the Adventurers Guild.

To choose your class, simply click one of the buttons below corresponding to the class you wish to embark upon. 
**Once you reach Level {levelToEnchant}**, click on the name of your basic class once more **to enchant your class**.


Here's a little paper explaining the classes. Choose wisely, the only way back is to start over.

[Adventurers Guild Classes](https://i.imgur.com/8kwBBAN.jpg)'''
            async with ClientSession() as session:
                    webhook = SyncWebhook.from_url(WEBHOOK_URL) # Initializing webhook
                    webhook.send(content=level10Message, username="[Guild Manager] Ron", avatar_url="https://media.discordapp.net/attachments/1213218623301091369/1221111865166401556/Guild_Master_Ron_mid.png?ex=6611640b&is=65feef0b&hm=4c9d52c57c6f20d6b15b3f8f3571787f3c619cae3f08163c4bf595df893b90f0&=&format=webp&quality=lossless&width=240&height=240") # Executing webhook.
            await asyncio.sleep(1)
            await thisChannel.send("Choose your class.", view=ClassSelectView())
            return
        if message.author.id in [242681702512721931, 816769793231028244] and message.content == "!!rolestartembed":
            thisChannel = message.channel
            WEBHOOK_URL = 'https://discord.com/api/webhooks/1234262232771203143/wkI7T1PU6jFNApytZFFSbY0QKMmttUj7dx8x0RoAsrYOcSxS61jO1n4kAuUD4jGeencF'
            level10Message = f'''Hello there, welcome to the **Adventurers Guild**! My name is Ron, I'm the Guild Manager.
I'm guessing you're here to join the Guild? Great, just sign application below and I will take care of the rest.
Once you joined the Guild you will start gaining experience to unlock exciting classes, all with special perks and abilities! 
Are you ready to start your adventure?
            
See you inside!'''
            async with ClientSession() as session:
                    webhook = SyncWebhook.from_url(WEBHOOK_URL) # Initializing webhook
                    webhook.send(content=level10Message, username="[Guild Manager] Ron", avatar_url="https://media.discordapp.net/attachments/1213218623301091369/1221111865166401556/Guild_Master_Ron_mid.png?ex=6611640b&is=65feef0b&hm=4c9d52c57c6f20d6b15b3f8f3571787f3c619cae3f08163c4bf595df893b90f0&=&format=webp&quality=lossless&width=240&height=240") # Executing webhook.
            await asyncio.sleep(1)
            await thisChannel.send("Adventurers Guild Member Application:", view=StartSelectView())
            return
        
        role = message.guild.get_role(roles[f'guild'])
        roles2 = message.guild.get_role(1229444878552006708)
        if role in message.author.roles or roles2 in message.author.roles:
            pass
        else:
            return
        
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT user_id FROM exp WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}"
            async with db.execute(query) as cursor:
                result9 = await cursor.fetchone()
        if result9 is None:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f"INSERT INTO 'exp' (user_id, xp, class, guild_id, valid, cooldown) VALUES ({message.author.id}, 0, 0, {message.guild.id}, 0, 0)"
                await db.execute(sqlquery)
                await db.commit()
        theChannelCurrently = message.channel.id
        
        if type(message.channel) is discord.Thread:
            
            try:
                theChannelCurrently = message.channel.parent_id
            except:
                theChannelCurrently = message.channel.id
            
        
        if int(theChannelCurrently) in excludedChannels:
            #print(message.channel)
            #print("Channel.")
            #print(int(theChannelCurrently) in excludedChannels)
            return
        if int(message.channel.category.id) in excludedCategorys:
            #print(message.channel)
            #print("Category.")
            return
        # adding xp per message
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, cooldown, class FROM exp WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}"
            async with db.execute(query) as cursor:
                oldLevel = await cursor.fetchone()

        if getLevel(oldLevel[0]) == 10 and oldLevel[2] == 0:
            return

        if int(oldLevel[1])+cooldownInSeconds < timestamproundedf(0):
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f"UPDATE exp SET cooldown = {timestamproundedf(0)} WHERE user_id={message.author.id} AND guild_id = {message.guild.id}"
                await db.execute(sqlquery)
                await db.commit()
            if int(message.channel.id) in doubleChannels or int(message.channel.category.id) in doubleCategory:
                async with aiosqlite.connect("exp.sqlite") as db:
                    sqlquery = f"UPDATE exp SET xp = {oldLevel[0] + (expPerCooldown*2)} WHERE user_id={message.author.id} AND guild_id = {message.guild.id}"
                    await db.execute(sqlquery)
                    await db.commit()
            else:
                async with aiosqlite.connect("exp.sqlite") as db:
                    sqlquery = f"UPDATE exp SET xp = {oldLevel[0] + expPerCooldown} WHERE user_id={message.author.id} AND guild_id = {message.guild.id}"
                    await db.execute(sqlquery)
                    await db.commit()
            

            if getLevel(oldLevel[0]) != getLevel(oldLevel[0] + expPerCooldown):
                newLevel = getLevel(oldLevel[0] + expPerCooldown)[0]
                if str(newLevel) in levelroles:
                    member = message.author
                    for x,y in enumerate(levelroles):
                        try:
                            role = message.guild.get_role(levelroles[y])
                            if role in member.roles:
                                await member.remove_roles(role)
                                break
                        except:
                            pass
                    role2 = message.guild.get_role(levelroles[str(newLevel)])
                    await member.add_roles(role2)
                    if newLevel == levelToClass:
                        async with aiosqlite.connect("exp.sqlite") as db:
                            sqlquery = f'''UPDATE exp SET valid=1 WHERE user_id={message.author.id} AND guild_id = {message.guild.id}'''
                            await db.execute(sqlquery)
                            await db.commit()
                        channel = bot.get_channel(channels["leveling"])
                        await channel.send(f"<@{message.author.id}>, you have reached level {levelToClass}, visit **<#{channels['job_change']}>** to choose your class!")
                    elif newLevel == levelToEnchant:
                            async with aiosqlite.connect("exp.sqlite") as db:
                                sqlquery = f'''UPDATE exp SET valid=1 WHERE user_id={message.author.id} AND guild_id = {message.guild.id}'''
                                await db.execute(sqlquery)
                                await db.commit()
                            channel = bot.get_channel(channels["leveling"])
                            await channel.send(f"**Congratulations!** <@{message.author.id}>, you have reached level {levelToEnchant}, visit **<#{channels['job_change']}>** and **click your class again** to enchant your powers!")
                    else:
                        channel = bot.get_channel(channels["leveling"])
                        await channel.send(f"Hear hear! <@{message.author.id}> has reached another milestone, Level {str(newLevel)}!")



bot = MyClient(intents=intents)

# category: commands

@bot.tree.command(name="magician_silence", description="[MAGICIANS ONLY] Silence someone for sometime.")
@app_commands.describe(member="The member to silence")
@app_commands.rename(member='member')
async def magician_silence(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return

    cooldown = 300
    commandName = 'magician_silence'
    classNamePlural = 'magicians'
    forClass = 1

    role2 = interaction.guild.get_role(roles['sagesgrace'])
    if role2 in member.roles:
        await interaction.followup.send(content=f'<@{interaction.user.id}> has Sages Grace. They are currently immune.', ephemeral=True)
        return

    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        
        # COMMAND
        
        person = member
        role = interaction.guild.get_role(roles['silenced'])
        rolee = interaction.guild.get_role(roles['enchanted_silenced'])
        
        
        try:
            if enchanted == 2:
                await person.add_roles(rolee)
                whichrole = rolee
            else:
                await person.add_roles(role)
                whichrole = role
        except:
            pass
        await interaction.followup.send(content=f'<@{interaction.user.id}>, Silence started on <@{person.id}>!', ephemeral=True)
        
        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = member
        historyEffectedID = member.id
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - on {historyEffected} ({historyEffectedID})")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)

        if enchanted == 1:
            time = 15
        elif enchanted == 2:
            time = 30
        else:
            time = 5

        for x in range(time):
            await asyncio.sleep(1)
        
        role2 = interaction.guild.get_role(roles["trickery"])
        if role2 in member.roles:
            if enchanted == 1:
                await asyncio.sleep(15)
            elif enchanted == 2:
                await asyncio.sleep(30)
            else:
                await asyncio.sleep(5)
        try:
            if enchanted == 2:
                await person.remove_roles(rolee)
            else:
                await person.remove_roles(role)
        except:
            pass

    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return

@bot.tree.command(name="jester_taunt", description="[JESTERS ONLY] Taunt someone for sometime.")
@app_commands.describe(member="The member to taunt")
@app_commands.rename(member='member')
async def jester_taunt(interaction:discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return

    cooldown = 60*5
    commandName = 'jester_taunt'
    classNamePlural = 'jesters'
    forClass = 2

    role2 = interaction.guild.get_role(roles['sagesgrace'])
    if role2 in member.roles:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, has Sages Grace. They are currently immune.', ephemeral=True)
        return

    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        
        
        # COMMAND
        
        animallistog = ["pig", "cat", "dog", "rat", "unicorn", "whale", "cockroach", "wolf","tiger", "giraffe"]
        animallist = [str(x).upper() for x in animallistog]
        person = member
        role = interaction.guild.get_role(roles['taunted'])
        rolee = interaction.guild.get_role(roles['enchanted_taunted'])
        person = member
        ognick = member.global_name if member.nick == None else member.nick

        if ognick in animallist or ognick == " ឵឵ " or ognick == "\u17b5\u17b5":
            pass
        else:
            with open('nicknames.json', 'rb') as f2:
                data = json.load(f2)
            data[str(member.id)] = ognick
            json.dump(data, open("nicknames.json", "w"), indent=4)
        try:
            if enchanted == 2:
                await person.add_roles(rolee)
            else:
                await person.add_roles(role)
        except:
            pass
        try:
            await person.edit(nick=" ឵឵ ")
        except:
            pass
        await interaction.followup.send(content=f'<@{interaction.user.id}>, Taunt started on <@{person.id}>!', ephemeral=True)

        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = member
        historyEffectedID = member.id
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - on {historyEffected} ({historyEffectedID})")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)
        print('flexible')
        if enchanted == 1:
            await asyncio.sleep(60)
        elif enchanted == 2:
            await asyncio.sleep(120)
        else:
            await asyncio.sleep(5)
        
        try:
            if enchanted == 2:
                await person.remove_roles(rolee)
            else:
                await person.remove_roles(role)
        except:
            pass

        try:
            with open('nicknames.json', 'rb') as f2:
                data = json.load(f2)
            await person.edit(nick=f'{data[str(member.id)]}')
            f2.close()
        except:
            pass
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return
    
@bot.tree.command(name="jester_trickery", description="[TRICKSTER ONLY] Trick someone for more time on them.")
@app_commands.describe(member="The member to trick")
@app_commands.rename(member='member')
async def jester_trickery(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return

    cooldown = 60*15
    commandName = 'jester_trickery'
    classNamePlural = 'tricksters'
    forClass = 2

    role2 = interaction.guild.get_role(roles['sagesgrace'])
    if role2 in member.roles:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, has Sages Grace. They are currently immune.', ephemeral=True)
        return

    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    if enchanted == 1:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, you need to be enchanted to do a trick on them!', ephemeral=True)
        return
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        
        # COMMAND
        
        person = member
        role = interaction.guild.get_role(roles['trickery'])
        try:
            await person.add_roles(role)
        except:
            pass
        
        
        await interaction.followup.send(content=f'<@{interaction.user.id}>, Trick started on <@{person.id}>! Their time has been lengthened.', ephemeral=True)

        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = member
        historyEffectedID = member.id
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - on {historyEffected} ({historyEffectedID})")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)

        await asyncio.sleep(140)
        try:
            await person.remove_roles(role)
        except:
            pass
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return



@bot.tree.command(name="bard_blessing", description="[BARDS ONLY] Color someone for sometime.")
@app_commands.describe(member="The member to color")
@app_commands.rename(member='member')
async def bard_blessing(interaction: discord.Interaction, member: discord.Member, color: typing.Literal['Bards Blessing Red', 'Bards Blessing Magenta', 'Bards Blessing Cyan', 'Bards Blessing Green', 'Bards Blessing Blue', 'Bards Blessing Yellow']):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return

    cooldown = 60*5
    commandName = 'bard_blessing'
    classNamePlural = 'bards'
    forClass = 3


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        
        # COMMAND
        
        person = member
        role = interaction.guild.get_role(roles[f'{color.lower().replace(" ", "_")}'])
        try:
            await person.add_roles(role)
        except:
            pass
        await interaction.followup.send(content=f'<@{interaction.user.id}>, Colored <@{person.id}>!', ephemeral=True)

        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = member
        historyEffectedID = member.id
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - on {historyEffected} ({historyEffectedID})")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)

        if enchanted == 1:
            await asyncio.sleep(300)
        elif enchanted == 2:
            await asyncio.sleep(300)
        else:
            await asyncio.sleep(5)

        try:
            await person.remove_roles(role)
        except:
            pass
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return



@bot.tree.command(name="bard_customs", description="[BARDS ONLY] Color someone something custom for sometime.")
@app_commands.describe(member="The member to color")
@app_commands.describe(color="The hex code of the color, example: #FFFFFF")
@app_commands.rename(member='member')
@app_commands.rename(color='color')
async def bard_customs(interaction: discord.Interaction, member: discord.Member, color: str):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return
    
    color = color.replace(" ", '')

    cooldown = 60*5
    commandName = 'bard_customs'
    classNamePlural = 'bards'
    forClass = 3


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    if enchanted == 1:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, You need to be enchanted to choose a color!', ephemeral=True)
        return
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        
        
        # COMMAND
        
        person = member
        try:
            guild = interaction.guild
            try:
                role = await guild.create_role(name=f'Enchanted Blessing', colour=discord.Colour.from_str(color),hoist=True)
            except:
                await interaction.followup.send(content=f'Enter a valid color hex code **with** the #/hashtag! Example: #FFFFFF', ephemeral=True)
                
            all_roles = await guild.fetch_roles()
            num_roles = len(all_roles)
            await role.edit(reason='color position', position=num_roles - 2)
            try:
                await person.add_roles(role)
            except:
                pass
        except:
            await interaction.followup.send(content=f'Something went wrong, let <@816769793231028244> know.', ephemeral=True)
            return
        await interaction.followup.send(content=f'<@{interaction.user.id}>, you blessed <@{person.id}>!', ephemeral=True)

        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = member
        historyEffectedID = member.id
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - on {historyEffected} ({historyEffectedID})")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)

        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        trickeryenabled = False
        if enchanted == 2:
            time = 300
        else:
            time = 5
        
        trickery = interaction.guild.get_role(roles['trickery'])
        for x in range(time):
            if trickery in person.roles:
                trickeryenabled = True
            await asyncio.sleep(1)
        
        if trickeryenabled == True:
            if enchanted == 1:
                await asyncio.sleep(120)
            elif enchanted == 2:
                await asyncio.sleep(300)
            else:
                await asyncio.sleep(5)

        try:
            await person.remove_roles(role)
            await role.delete()
        except:
            pass
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return

@bot.tree.command(name="pirate_parrot", description="[PIRATES ONLY] Make your pirate talk.")
@app_commands.describe(fonts="Which font? (Choose the first 'THIS' if you are not enchanted.)")
@app_commands.rename(fonts='font')
@app_commands.describe(message="What's your message?")
@app_commands.rename(message='message')
@app_commands.describe(parrotName="What's your parrot's name?")
@app_commands.rename(parrotName='parrot-name')
async def pirate_parrot(interaction:discord.Interaction, fonts: typing.Optional[typing.Literal['THIS', '𝔗ℌℑ𝔖', '𝕋ℍ𝕀𝕊', '🆃🅷🅸🆂', '𝐓𝐇𝐈𝐒', 'ＴＨＩＳ']], message: str, parrotName: str):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return

    if fonts is None:
        fonts = 'THIS'
    cooldown = 5
    commandName = 'pirate_parrot'
    classNamePlural = 'pirates'
    forClass = 4


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        webhooks = await interaction.channel.webhooks()
        rightWebhook = 0
        for webhook in webhooks:
            if webhook.name == correctwebhookname:
                rightWebhook = webhook
                break
        if rightWebhook == 0:
            thisWebhook = await interaction.channel.create_webhook(name=correctwebhookname)
            rightWebhook = thisWebhook
        fontList = ['THIS', '𝔗ℌℑ𝔖', '𝕋ℍ𝕀𝕊', '🆃🅷🅸🆂', '𝐓𝐇𝐈𝐒', 'ＴＨＩＳ']
        index = fontList.index(fonts)
        msg = ''
        if enchanted == 1:
            index = 0
        for x in message:
            msg += (font(x, index))
        
        
        # COMMAND
        
        WEBHOOK_URL = rightWebhook.url
        async with ClientSession() as session:
                webhook = SyncWebhook.from_url(WEBHOOK_URL) # Initializing webhook
                webhook.send(content=f'{msg}', username=f"[Parrot] {parrotName}", avatar_url="https://i.imgur.com/VB9J2SC.png") # Executing webhook.
        
        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = None
        historyEffectedID = None
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - with:\n Message:{message}")
        historyembed.set_footer(text=f"{datetime.datetime.now()} | Parrot Name: {parrotName}")
        await historychannel.send(embed=historyembed)

        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        await interaction.followup.send(content='Your parrot just talked!',ephemeral=True)
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return


@bot.tree.command(name="pirate_2choices", description="[PIRATES ONLY] Yes or no?.")
@app_commands.describe(question="Ask a yes or no question!")
@app_commands.rename(question='question')
async def pirate_2choices(interaction: discord.Interaction, question: typing.Optional[str]):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return
    if question is None:
        question = f''
    else:
        question = '> '+question+'\n\n'

    cooldown = 10
    commandName = 'pirate_2choices'
    classNamePlural = 'pirates'
    forClass = 4


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        webhooks = await interaction.channel.webhooks()
        rightWebhook = 0
        for webhook in webhooks:
            if webhook.name == correctwebhookname:
                rightWebhook = webhook
                break
        if rightWebhook == 0:
            thisWebhook = await interaction.channel.create_webhook(name=correctwebhookname)
            rightWebhook = thisWebhook
        choice = random.choice(['Yes', 'No'])
        WEBHOOK_URL = rightWebhook.url
        
        async with ClientSession() as session:
                webhook = SyncWebhook.from_url(WEBHOOK_URL) # Initializing webhook
                
                webhook.send(content=f'{question}I say... **{choice}**!', username=f"Parrot", avatar_url="https://i.imgur.com/VB9J2SC.png") # Executing webhook.
        
        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = None
        historyEffectedID = None
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - with question {question}")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)

        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        await interaction.followup.send(content=f'2 choices sent. You may now dismiss this message.', ephemeral=True)

    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return

@bot.tree.command(name="mystic_spirits", description="[MYSTIC ONLY] Become a spirit.")
async def mystic_spirits(interaction: discord.Interaction, member: typing.Optional[discord.Member]):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            return

    cooldown = 30
    commandName = 'mystic_spirits'
    classNamePlural = 'mystics'
    forClass = 6
    if member is None:
        member = interaction.user

    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        person = member
        role = interaction.guild.get_role(roles['spirit'])
        guiding = False
        town = False
        guiderole = interaction.guild.get_role(1179486841020370974)
        townrole = interaction.guild.get_role(1179174042939445318)
        if guiderole in member.roles:
            guiding = True
        if townrole in member.roles:
            town = True
        try:
            await person.add_roles(role)
        except:
            pass
        
        #finish making sure spirit
        # COMMAND

        await interaction.followup.send(content=f'<@{interaction.user.id}>, Done...', ephemeral=True)

        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = member
        historyEffectedID = member.id
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - on {historyEffected} ({historyEffectedID})")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)

        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return
#spirit_leaverealm 
@bot.tree.command(name="mystic_humans", description="Turn back to human form and leave the Spirit Realm.")
async def mystic_humans(interaction:discord.Interaction, member: typing.Optional[discord.Member]):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return
    if member is None:
        member = interaction.user

    cooldown = 30
    commandName = 'mystic_humans'
    classNamePlural = 'mystics'
    forClass = 6

    

    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    enchanted = int(str(currentclass[0]).count(str(forClass)))

    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        person = member
        role = interaction.guild.get_role(roles['spirit'])

        try:
            await person.remove_roles(role)
        except:
            pass

        
        
        # COMMAND

        await interaction.followup.send(content=f'<@{interaction.user.id}>, Done!', ephemeral=True)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return


@bot.tree.command(name="fae_blossoms", description="[FAE ONLY] Drop a small blossom.")
async def fae_blossoms(interaction : discord.Interaction):
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return
    
    cooldown = 60*60
    commandName = 'fae_blossoms'
    classNamePlural = 'fae'
    forClass = 5


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        await interaction.response.defer()
        person = interaction.user
        cdvar1 = timestamproundedf(60*10)
        v1 = View(timeout=60*10)
        b1 = Button(label='🌸')
        uniqueID = str(uuid.uuid4())
        async def b1_callback(interaction2 : discord.Interaction):
            await interaction2.response.defer(ephemeral=True)
            try:
                
                with open('smallblossom.json', 'rb') as f2:
                    data = json.load(f2)
                
                    
                if uniqueID in data:
                    if str(interaction2.user.id) in list(data[uniqueID]):
                        await interaction2.followup.send(f"You already entered!", ephemeral=True)
                        return
                    else:
                        dataCell = list(data[uniqueID])
                        dataCell.append(str(interaction2.user.id))
                        data[uniqueID] = dataCell
                else:
                    data[uniqueID] = [str(interaction2.user.id)]
                json.dump(data, open("smallblossom.json", "w"), indent=4)
                number = 0
                async with aiosqlite.connect("exp.sqlite") as db:
                    query = f"SELECT xp FROM exp WHERE user_id = {interaction2.user.id} AND guild_id = {interaction2.guild.id}"
                    async with db.execute(query) as cursor:
                        result = await cursor.fetchone()
                if result == None:
                    await interaction2.followup.send(f"Join the guild first!", ephemeral=True)
                    return

                number = 125
                async with aiosqlite.connect("exp.sqlite") as db:
                    sqlquery = f"UPDATE exp SET xp = {result[0] + number} WHERE user_id={interaction2.user.id} AND guild_id = {interaction2.guild.id}"
                    await db.execute(sqlquery)
                    await db.commit()
                await interaction2.followup.send(f"You gained {number} EXP!", ephemeral=True)
            except Exception as e:
                channel = bot.get_channel(1077720777949982783)
                await channel.send(f"An error occured: {str(e)}")
                print(e)
        b1.callback = b1_callback
        v1.add_item(b1)
        with open('smallblossom.json', 'rb') as f2:
            data = json.load(f2)
        data[uniqueID] = []
        json.dump(data, open("smallblossom.json", "w"), indent=4)
        
        lel = await interaction.followup.send(content=f'<@{interaction.user.id}>, dropped a Small Blossom! Click the 🌸 to get 125 experience. (Expires <t:{cdvar1}:R>)', embed=discord.Embed(title='🌸 Small Blossom Drop!', description='Click the 🌸 button to get 125 exp. But, there is a 10 minute time limit, so hurry! (Can only be claimed once)'), view=v1, ephemeral=False)
        historychannel = bot.get_channel(1244686875277398036)
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - in <#{interaction.channel.id}> ({interaction.channel.id})")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)

        messageID = lel.id
        channelID = lel.channel.id
        # COMMAND
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        await asyncio.sleep(60*10)
        getChan = interaction.guild.get_channel(channelID)
        getMes = await getChan.fetch_message(messageID)
        await getMes.delete()
        #await  delete message
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return

@bot.tree.command(name="fae_megablossoms", description="[FAE ONLY] Drop a mega blossom.")
async def fae_megablossoms(interaction : discord.Interaction):
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            return

    cooldown = 60*60
    commandName = 'fae_megablossoms'
    classNamePlural = 'fae'
    forClass = 5


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    if enchanted == 1:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f'<@{interaction.user.id}>, you need to be enchanted to drop a Mega Blossom!', ephemeral=True)
        return
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {0} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({0}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        await interaction.response.defer()
        person = interaction.user
        cdvar1 = timestamproundedf(3)
        v1 = View(timeout=4)
        b1 = Button(label='🌸')
        uniqueID = str(uuid.uuid4())
        async def b1_callback(interaction2:discord.Interaction):
            await interaction2.response.defer(ephemeral=True)
            with open('smallblossom.json', 'rb') as f2:
                data = json.load(f2)
            dataCell = 0
            if uniqueID in data:
                    if str(interaction2.user.id) in list(data[uniqueID]):
                        await interaction2.followup.send(f"You already entered!", ephemeral=True)
                        return
                    else:
                        dataCell = list(data[uniqueID])
                        dataCell.append(str(interaction2.user.id))
                        data[uniqueID] = dataCell
            else:
                    data[uniqueID] = [str(interaction2.user.id)]
            json.dump(data, open("smallblossom.json", "w"), indent=4)
            number = 0
            async with aiosqlite.connect("exp.sqlite") as db:
                query = f"SELECT xp FROM exp WHERE user_id = {interaction2.user.id} AND guild_id = {interaction2.guild.id}"
                async with db.execute(query) as cursor:
                    result = await cursor.fetchone()
            number = 500
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f"UPDATE exp SET xp = {result[0] + number} WHERE user_id={interaction2.user.id}"
                await db.execute(sqlquery)
                await db.commit()
            await interaction2.followup.send(f"You gained {number} EXP!", ephemeral=True)
        b1.callback = b1_callback
        v1.add_item(b1)
        lel = await interaction.followup.send(content=f'<@{interaction.user.id}>, dropped a **__MEGA__** Blossom! Click the 🌸 to get 500 experience. (Expires <t:{cdvar1}:R>)', embed=discord.Embed(title='🍒 Cherry Blossom Small Drop!', description='Click the 🌸 button to get 500 exp. But, there is a **3 SECOND** time limit, so hurry! (Can only be claimed once)'), view=v1, ephemeral=False)
        
        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = None
        historyEffectedID = None
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - in <#{interaction.channel.id}> ({interaction.channel.id})")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)

        # COMMAND
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
        await asyncio.sleep(10)
        await lel.delete()
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return

@app_commands.describe(animal="Only if you are an enchanted Wildshaper!")
@bot.tree.command(name="wildshaper_morph", description="[WILDSHAPERS ONLY] Morph others or yourself into an animal.")
async def wildshaper_morph(interaction : discord.Interaction, member: discord.Member, animal: typing.Optional[typing.Literal['Dog', 'Cat', 'rat', 'Unicorn', 'Pig', 'whale', 'cockroach', 'wolf', 'Tiger', 'Giraffe']]):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return
    if animal is None:
        animal = 'RANDOM'
    role2 = interaction.guild.get_role(roles['sagesgrace'])
    if role2 in member.roles:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, has Sages Grace. They are currently immune.', ephemeral=True)
        return
    cooldown = 60*5
    commandName = 'wildshaper_morph'
    classNamePlural = 'wildshapers'
    forClass = 7


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    if enchanted == 1 and animal != 'RANDOM':
        await interaction.followup.send(content=f'<@{interaction.user.id}>, you need to be enchanted to choose a animal!', ephemeral=True)
        return
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        animallist = ['Dog', 'Cat', 'rat', 'Unicorn', 'Pig', 'whale', 'cockroach', 'wolf', 'Tiger', 'Giraffe']
        animallistup = [str(x).upper() for x in animallist]
        if animal == 'RANDOM':
            animal = random.choice(animallist)
        person = member
        role = interaction.guild.get_role(roles[animal.lower()])
        ognick = person.nick
        if ognick is None:
            ognick = str(person.display_name)
        
        if ognick in animallistup or ognick == " ឵឵ " or ognick == "\u17b5\u17b5":
            pass
        else:
            with open('nicknames.json', 'rb') as f2:
                data = json.load(f2)
            data[str(member.id)] = ognick
            json.dump(data, open("nicknames.json", "w"), indent=4)
        try:
            await person.edit(nick=f'{animal.upper()}')
        except:
            pass

        try:
            await person.add_roles(role)
        except:
            pass
        await interaction.followup.send(content=f'<@{interaction.user.id}>, you morphed <@{person.id}> into {animal}!', ephemeral=True)
        
        historychannel = bot.get_channel(1244686875277398036)
        historyEffected = member
        historyEffectedID = member.id
        historyembed = discord.Embed(title=f"{commandName}", description=f"<@{interaction.user.id}> ({interaction.user.id}) did {commandName} - on {historyEffected} ({historyEffectedID}) into {animal}")
        historyembed.set_footer(text=f"{datetime.datetime.now()}")
        await historychannel.send(embed=historyembed)


        if enchanted == 1:
            await asyncio.sleep(60)
        elif enchanted == 2:
            await asyncio.sleep(120)
        else:
            await asyncio.sleep(5)

        role2 = interaction.guild.get_role(roles["trickery"])
        if role2 in member.roles:
            print("You are being tricked!")
            if enchanted == 1:
                await asyncio.sleep(60)
            elif enchanted == 2:
                await asyncio.sleep(120)
            else:
                await asyncio.sleep(5)

        
        if ognick is None:
            ognick = member.nick
        try:
            with open('nicknames.json', 'rb') as f2:
                data = json.load(f2)
            await person.edit(nick=f'{data[str(member.id)]}')
            f2.close()
        except:
            pass

        try:
            await person.remove_roles(role)
        except:
            pass
        
        
        # COMMAND
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return



@bot.tree.command(name="cleric_healing", description="[CLERICS ONLY] Remove all negative effects")
async def cleric_healing(interaction : discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return
    
    cooldown = 60*5
    commandName = 'cleric_healing'
    classNamePlural = 'clerics'
    forClass = 8


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        with open('nicknames.json', 'rb') as f2:
            data = json.load(f2)
        animals = ["pig", "cat", "dog", "rat", "unicorn", "whale", "cockroach", "wolf","tiger", "giraffe"]
        for x in animals:
            xRole = interaction.guild.get_role(roles[x])
            if xRole in member.roles:
                await member.remove_roles(xRole)
                try:
                    await member.edit(nick=data[str(member.id)])
                except:
                    await member.edit(nick="congrats we cantfind ur old user")
                break
        tauntrole = interaction.guild.get_role(roles['taunted'])
        tauntrole2 = interaction.guild.get_role(roles['enchanted_taunted'])
        if tauntrole in member.roles or tauntrole2 in member.roles:
            try:
                await member.edit(nick=data[str(member.id)])
            except:
                await member.edit(nick="congrats we cantfind ur old user")
                


        try:
            role = interaction.guild.get_role(roles['silenced'])
            await member.remove_roles(role)
        except:
            pass
        try:
            rolee = interaction.guild.get_role(roles['enchanted_silenced'])
            await member.remove_roles(rolee)
        except:
            pass
        try:
            role1 = interaction.guild.get_role(roles['taunted'])
            await member.remove_roles(role1)
        except:
            pass
        try:
            rolee = interaction.guild.get_role(roles['enchanted_taunted'])
            await member.remove_roles(rolee)
        except:
            pass

        await interaction.followup.send(content=f'<@{interaction.user.id}>, you cleansed <@{member.id}> of their negative effects!', ephemeral=True)

        
        # COMMAND
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return

@bot.tree.command(name="cleric_grace", description="[SAGES ONLY] Give sage's grace.")
async def cleric_grace(interaction : discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=True)
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            member = 0
            return
    
    cooldown = 60*10
    commandName = 'cleric_grace'
    classNamePlural = 'clerics'
    forClass = 8


    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            currentclass = await cursor.fetchone()
    if str(forClass) in str(currentclass[0]):
        pass
    else:
        await interaction.followup.send(content=f'<@{interaction.user.id}>, this ability is for {classNamePlural} only!', ephemeral=True)
        return
    enchanted = int(str(currentclass[0]).count(str(forClass)))
    if enchanted == 1:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f'<@{interaction.user.id}>, you need to be enchanted to drop a Mega Blossom!', ephemeral=True)
        return
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE user_id = {interaction.user.id} AND cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        
        role = interaction.guild.get_role(roles['sagesgrace'])

        try:
            await member.add_roles(role)
            await interaction.followup.send(content=f'<@{interaction.user.id}>, Sages Grace has been given to <@{member.id}>!', ephemeral=True)
        except:
            pass
        await asyncio.sleep(60*10)
        try:
            await member.remove_roles(role)
        except:
            pass

        

        # COMMAND
        async with aiosqlite.connect("cooldowns.sqlite") as db:
                sqlquery = f"UPDATE cooldowntb SET unix = {timestamproundedf(cooldown)} WHERE user_id={interaction.user.id} AND cooldown_name='{commandName}'"
                await db.execute(sqlquery)
                await db.commit()
    else:
        await interaction.followup.send(content=f'On cooldown! Try again at <t:{cooldownU}:F>, <t:{cooldownU}:R>.', ephemeral=True)
        return
# category: etc
    
@discord.app_commands.checks.cooldown(1, 15)
@bot.tree.command(name="duels", description="Duel someone!")
async def duels(interaction : discord.Interaction, member : discord.Member):
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            return
    if member.bot:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(content="You can't choose a bot to duel!", ephemeral=True)
            return
    p1 = interaction.user
    p2 = member

    if p1 == p2:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content="You can't choose yourself to duel!", ephemeral=True)
        return

    p1move = None
    p2move = None

    
    rules = {'sword':{'wand':'W','shield':'L'}, 'wand':{'sword':'L','shield':'W'}, 'shield':{'sword':'W','wand':'L'}}

    finalStage = False

    battleView = View(timeout=60*5)
    swordButton = Button(label='Sword 🗡️')
    wandButton = Button(label='Wand 🪄')
    shieldButton = Button(label='Shield 🛡️')

    async def swordButton_callback(interaction2 : discord.Interaction):
            try:
                await interaction2.response.defer()
                nonlocal p1move
                nonlocal p2move
                nonlocal finalStage
                if finalStage == True:
                    return
                if interaction2.user.id == p1.id:
                    if p1move is None:
                        p1move = 'SWORD'
                        
                        await interaction2.followup.send(content="You chose sword!", ephemeral=True)
                        if p1move != None and p2move != None and finalStage != True:
                            finalStage == True
                            winner = None
                            winnerstr = 'NO ONE CAUSE YOU TIED!'
                            if p1move == p2move:
                                winner = None
                            else:
                                if rules[p1move.lower()][p2move.lower()] == 'W':
                                    winner = p1
                                    winnerstr = f'<@{p1.id}>!'
                                    async with aiosqlite.connect("dueling.sqlite") as db:
                                        query = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                        query2 = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                        async with db.execute(query) as cursor:
                                            result = await cursor.fetchone()
                                        async with db.execute(query2) as cursor2:
                                            result2 = await cursor2.fetchone()
                                            
                                    
                                    async with aiosqlite.connect("dueling.sqlite") as db:
                                        if result is None:
                                            sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                            await db.execute(sqlquery3)
                                            result = [0]
                                        if result2 is None:
                                            sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                            await db.execute(sqlquery4)
                                            result2 = [0]
                                        sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                        await db.execute(sqlquery)
                                        sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                        await db.execute(sqlquery2)
                                        await db.commit()
                                else:
                                    winner = p2
                                    winnerstr = f'<@{p2.id}>!'
                                    async with aiosqlite.connect("dueling.sqlite") as db:
                                        query = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                        query2 = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                        async with db.execute(query) as cursor:
                                            result = await cursor.fetchone()
                                        async with db.execute(query2) as cursor2:
                                            result2 = await cursor2.fetchone()
                                            
                                    
                                    async with aiosqlite.connect("dueling.sqlite") as db:
                                        if result is None:
                                            sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                            await db.execute(sqlquery3)
                                            result = [0]
                                        if result2 is None:
                                            sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                            await db.execute(sqlquery4)
                                            result2 = [0]
                                        sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                        await db.execute(sqlquery)
                                        sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                        await db.execute(sqlquery2)
                                        await db.commit()
                                
                            dele = await interaction2.followup.send(content=f"And the winner between <@{p1.id}> ({p1move.upper()}) and <@{p2.id}> ({p2move.upper()}) is...\n\n **{winnerstr}** Congratulations!")
                            await asyncio.sleep(10)
                            await dele.delete()
                    else:
                        await interaction2.followup.send(content="You already made your move!", ephemeral=True)
                elif interaction2.user.id == p2.id:
                    if p2move == None:
                        p2move = 'SWORD'
                        await interaction2.followup.send(content="You chose sword!", ephemeral=True)
                        if p1move != None and p2move != None and finalStage != True:
                            finalStage == True
                            winner = None
                            winnerstr = 'NO ONE CAUSE YOU TIED!'
                            if p1move == p2move:
                                winner = None
                            else:
                                if rules[p1move.lower()][p2move.lower()] == 'W':
                                    winner = p1
                                    winnerstr = f'<@{p1.id}>!'
                                    async with aiosqlite.connect("dueling.sqlite") as db:
                                        query = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                        query2 = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                        async with db.execute(query) as cursor:
                                            result = await cursor.fetchone()
                                        async with db.execute(query2) as cursor2:
                                            result2 = await cursor2.fetchone()
                                            
                                    
                                    async with aiosqlite.connect("dueling.sqlite") as db:
                                        if result is None:
                                            sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                            await db.execute(sqlquery3)
                                            result = [0]
                                        if result2 is None:
                                            sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                            await db.execute(sqlquery4)
                                            result2 = [0]
                                        sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                        await db.execute(sqlquery)
                                        sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                        await db.execute(sqlquery2)
                                        await db.commit()
                                else:
                                    winner = p2
                                    winnerstr = f'<@{p2.id}>!'
                                    async with aiosqlite.connect("dueling.sqlite") as db:
                                        query = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                        query2 = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                        async with db.execute(query) as cursor:
                                            result = await cursor.fetchone()
                                        async with db.execute(query2) as cursor2:
                                            result2 = await cursor2.fetchone()
                                            
                                    
                                    async with aiosqlite.connect("dueling.sqlite") as db:
                                        if result is None:
                                            sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                            await db.execute(sqlquery3)
                                            result = [0]
                                        if result2 is None:
                                            sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                            await db.execute(sqlquery4)
                                            result2 = [0]
                                        sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                        await db.execute(sqlquery)
                                        sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                        await db.execute(sqlquery2)
                                        await db.commit()
                                
                            dele = await interaction2.followup.send(content=f"And the winner between <@{p1.id}> ({p1move.upper()}) and <@{p2.id}> ({p2move.upper()}) is...\n\n **{winnerstr}** Congratulations!")
                            await asyncio.sleep(10)
                            await dele.delete()
                    else:
                        await interaction2.followup.send(content="You already made your move!", ephemeral=True)
            except Exception as error:
                logging.warning(traceback.format_exc()) #logs the error
                channel = bot.get_channel(1077720777949982783)
                await channel.send(f"An error occured: {str(error)}")




    async def wandButton_callback(interaction2 : discord.Interaction):
        await interaction2.response.defer()
        nonlocal p1move
        nonlocal p2move
        nonlocal finalStage
        if finalStage == True:
            return
        if interaction2.user.id == p1.id:
            if p1move == None:
                p1move = 'WAND'
                await interaction2.followup.send(content="You chose wand!", ephemeral=True)
                if p1move != None and p2move != None and finalStage != True:
                    finalStage == True
                    winner = None
                    winnerstr = 'NO ONE CAUSE YOU TIED!'
                    if p1move == p2move:
                        winner = None
                    else:
                        if rules[p1move.lower()][p2move.lower()] == 'W':
                            winner = p1
                            winnerstr = f'<@{p1.id}>!'
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                query = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                query2 = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                async with db.execute(query) as cursor:
                                    result = await cursor.fetchone()
                                async with db.execute(query2) as cursor2:
                                    result2 = await cursor2.fetchone()
                                    
                            
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                if result is None:
                                    sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery3)
                                    result = [0]
                                if result2 is None:
                                    sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery4)
                                    result2 = [0]
                                sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery)
                                sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery2)
                                await db.commit()
                        else:
                            winner = p2
                            winnerstr = f'<@{p2.id}>!'
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                query = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                query2 = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                async with db.execute(query) as cursor:
                                    result = await cursor.fetchone()
                                async with db.execute(query2) as cursor2:
                                    result2 = await cursor2.fetchone()
                                    
                            
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                if result is None:
                                    sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery3)
                                    result = [0]
                                if result2 is None:
                                    sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery4)
                                    result2 = [0]
                                sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery)
                                sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery2)
                                await db.commit()
                        
                    dele = await interaction2.followup.send(content=f"And the winner between <@{p1.id}> ({p1move.upper()}) and <@{p2.id}> ({p2move.upper()}) is...\n\n **{winnerstr}** Congratulations!")
                    await asyncio.sleep(10)
                    await dele.delete()
            else:
                await interaction2.followup.send(content="You already made your move!", ephemeral=True)
        elif interaction2.user.id == p2.id:
            if p2move == None:
                p2move = 'WAND'
                await interaction2.followup.send(content="You chose wand!", ephemeral=True)
                if p1move != None and p2move != None and finalStage != True:
                    finalStage == True
                    winner = None
                    winnerstr = 'NO ONE CAUSE YOU TIED!'
                    if p1move == p2move:
                        winner = None
                    else:
                        if rules[p1move.lower()][p2move.lower()] == 'W':
                            winner = p1
                            winnerstr = f'<@{p1.id}>!'
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                query = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                query2 = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                async with db.execute(query) as cursor:
                                    result = await cursor.fetchone()
                                async with db.execute(query2) as cursor2:
                                    result2 = await cursor2.fetchone()
                                    
                            
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                if result is None:
                                    sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery3)
                                    result = [0]
                                if result2 is None:
                                    sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery4)
                                    result2 = [0]
                                sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery)
                                sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery2)
                                await db.commit()
                        else:
                            winner = p2
                            winnerstr = f'<@{p2.id}>!'
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                query = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                query2 = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                async with db.execute(query) as cursor:
                                    result = await cursor.fetchone()
                                async with db.execute(query2) as cursor2:
                                    result2 = await cursor2.fetchone()
                                    
                            
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                if result is None:
                                    sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery3)
                                    result = [0]
                                if result2 is None:
                                    sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery4)
                                    result2 = [0]
                                sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery)
                                sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery2)
                                await db.commit()

                            
                        
                    dele = await interaction2.followup.send(content=f"And the winner between <@{p1.id}> ({p1move.upper()}) and <@{p2.id}> ({p2move.upper()}) is...\n\n **{winnerstr}** Congratulations!")
                    await asyncio.sleep(10)
                    await dele.delete()
            else:
                await interaction2.followup.send(content="You already made your move!", ephemeral=True)


    async def shieldButton_callback(interaction2:discord.Interaction):
        await interaction2.response.defer()
        nonlocal p1move
        nonlocal p2move
        nonlocal finalStage
        if finalStage == True:
            return
        if interaction2.user.id == p1.id:
            if p1move == None:
                p1move = 'SHIELD'
                await interaction2.followup.send(content="You chose shield!", ephemeral=True)
                if p1move != None and p2move != None and finalStage != True:
                    finalStage == True
                    winner = None
                    winnerstr = 'NO ONE CAUSE YOU TIED!'
                    if p1move == p2move:
                        winner = None
                    else:
                        if rules[p1move.lower()][p2move.lower()] == 'W':
                            winner = p1
                            winnerstr = f'<@{p1.id}>!'
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                query = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                query2 = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                async with db.execute(query) as cursor:
                                    result = await cursor.fetchone()
                                async with db.execute(query2) as cursor2:
                                    result2 = await cursor2.fetchone()
                                    
                            
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                if result is None:
                                    sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery3)
                                    result = [0]
                                if result2 is None:
                                    sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery4)
                                    result2 = [0]
                                sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery)
                                sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery2)
                                await db.commit()
                        else:
                            winner = p2
                            winnerstr = f'<@{p2.id}>!'
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                query = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                query2 = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                async with db.execute(query) as cursor:
                                    result = await cursor.fetchone()
                                async with db.execute(query2) as cursor2:
                                    result2 = await cursor2.fetchone()
                                    
                            
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                if result is None:
                                    sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery3)
                                    result = [0]
                                if result2 is None:
                                    sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery4)
                                    result2 = [0]
                                sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery)
                                sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery2)
                                await db.commit()
                        
                    dele = await interaction2.followup.send(content=f"And the winner between <@{p1.id}> ({p1move.upper()}) and <@{p2.id}> ({p2move.upper()}) is...\n\n **{winnerstr}** Congratulations!")
                    await asyncio.sleep(10)
                    await dele.delete()
            else:
                await interaction.response.defer(ephemeral=True)
                await interaction2.followup.send(content="You already made your move!", ephemeral=True)
        elif interaction2.user.id == p2.id:
            if p2move == None:
                p2move = 'SHIELD'
                await interaction2.followup.send(content="You chose shield!", ephemeral=True)
                if p1move != None and p2move != None and finalStage != True:
                    finalStage == True
                    winner = None
                    winnerstr = 'NO ONE CAUSE YOU TIED!'
                    if p1move == p2move:
                        winner = None
                    else:
                        if rules[p1move.lower()][p2move.lower()] == 'W':
                            winner = p1
                            winnerstr = f'<@{p1.id}>!'
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                query = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                query2 = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                async with db.execute(query) as cursor:
                                    result = await cursor.fetchone()
                                async with db.execute(query2) as cursor2:
                                    result2 = await cursor2.fetchone()
                                    
                            
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                if result is None:
                                    sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery3)
                                    result = [0]
                                if result2 is None:
                                    sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery4)
                                    result2 = [0]
                                sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery)
                                sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery2)
                                await db.commit()
                        else:
                            winner = p2
                            winnerstr = f'<@{p2.id}>!'
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                query = f"SELECT wins FROM winners WHERE user_id = {p2.id} AND guild_id = {interaction.guild_id}"
                                query2 = f"SELECT wins FROM winners WHERE user_id = {p1.id} AND guild_id = {interaction.guild_id}"
                                async with db.execute(query) as cursor:
                                    result = await cursor.fetchone()
                                async with db.execute(query2) as cursor2:
                                    result2 = await cursor2.fetchone()
                                    
                            
                            async with aiosqlite.connect("dueling.sqlite") as db:
                                if result is None:
                                    sqlquery3= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p2.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery3)
                                    result = [0]
                                if result2 is None:
                                    sqlquery4= f"INSERT INTO 'winners' (user_id, wins, guild_id) VALUES ({p1.id}, 0, {interaction.guild_id})"
                                    await db.execute(sqlquery4)
                                    result2 = [0]
                                sqlquery = f'''UPDATE winners SET wins={result[0]+1} WHERE user_id={p2.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery)
                                sqlquery2 = f'''UPDATE winners SET wins={result2[0]-1 if result2[0]-1 >= 0 else 0} WHERE user_id={p1.id} AND guild_id = {interaction.guild_id}'''
                                await db.execute(sqlquery2)
                                await db.commit()
                        

                    dele = await interaction2.followup.send(content=f"And the winner between <@{p1.id}> ({p1move.upper()}) and <@{p2.id}> ({p2move.upper()}) is...\n\n **{winnerstr}** Congratulations!")
                    await asyncio.sleep(10)
                    await dele.delete()
            else:
                await interaction2.followup.send(content="You already made your move!", ephemeral=True)

    swordButton.callback = swordButton_callback
    wandButton.callback = wandButton_callback
    shieldButton.callback = shieldButton_callback
    battleView.add_item(swordButton)
    battleView.add_item(wandButton)
    battleView.add_item(shieldButton)
    msgi = await interaction.response.send_message(content=f'<@{p2.id}>\n\n<@{p1.id}> has challenged you to a duel.\nPick your move! 🗡️ > 🪄 > 🛡️ > 🗡️\n\n**(EXPIRES IN 5 MINUTES)**', view=battleView)
    
    await asyncio.sleep(60*5)
    await interaction.delete_original_response()



@bot.tree.command(name="leaderboard", description="View the level leaderboard.")
async def leaderboard(interaction : discord.Interaction):
    await interaction.response.defer()
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            return
    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT user_id FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            result9 = await cursor.fetchone()
    if result9 is None:
        async with aiosqlite.connect("exp.sqlite") as db:
            sqlquery = f"INSERT INTO 'exp' (user_id, xp, class, guild_id, valid, cooldown) VALUES ({interaction.user.id}, 0, 0, {interaction.guild.id}, 0, 0)"
            await db.execute(sqlquery)
            await db.commit()

    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT xp, user_id FROM exp WHERE guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            result = await cursor.fetchall()
    sortedL = sorted(result, key=lambda y: y[0], reverse=True)
    desc = ''''''
    top = 10
    top10ids = []
    for x in range(top):
        if len(sortedL) < x+1:
            break
        else:
            top10ids.append(sortedL[x][1])
            if interaction.user.id == sortedL[x][1]:
                desc += f'**#{x+1} <@{sortedL[x][1]}> - Level {getLevel(sortedL[x][0])[0]}**\n'
            else:
                desc += f'#{x+1} <@{sortedL[x][1]}> - Level {getLevel(sortedL[x][0])[0]}\n'
    if int(interaction.user.id) in top10ids:
        pass
    else:
        found = [x for x in sortedL if x[1] == interaction.user.id]
        index = sortedL.index(found[0])
        desc += f'\n**#{index+1} <@{sortedL[index][1]}> - Level {getLevel(sortedL[index][0])[0]}**\n'

    await interaction.followup.send(embed=discord.Embed(title='Leaderboard', description=desc))

@bot.tree.command(name="leaderboard_duels", description="View the duel wins leaderboard.")
async def leaderboard_duels(interaction : discord.Interaction):
    await interaction.response.defer()
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            return
    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT user_id FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            result9 = await cursor.fetchone()
    if result9 is None:
        async with aiosqlite.connect("exp.sqlite") as db:
            sqlquery = f"INSERT INTO 'exp' (user_id, xp, class, guild_id, valid, cooldown) VALUES ({interaction.user.id}, 0, 0, {interaction.guild.id}, 0, 0)"
            await db.execute(sqlquery)
            await db.commit()

    async with aiosqlite.connect("dueling.sqlite") as db:
        query = f"SELECT wins, user_id FROM winners WHERE guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            result = await cursor.fetchall()
    sortedL = sorted(result, key=lambda y: y[0], reverse=True)
    desc = ''''''
    top = 10
    top10ids = []
    for x in range(top):
        if len(sortedL) < x+1:
            break
        else:
            top10ids.append(int(sortedL[x][1]))
            if interaction.user.id == sortedL[x][1]:
                word = 'points'
                if getLevel(sortedL[x][0])[0] == 1:
                    word = 'point'
                desc += f'**#{x+1} <@{sortedL[x][1]}> - {sortedL[x][0]} {word}**\n'
            else:
                word = 'points'
                if getLevel(sortedL[x][0])[0] == 1:
                    word = 'point'
                desc += f'#{x+1} <@{sortedL[x][1]}> - {sortedL[x][0]} {word}\n'
    if int(interaction.user.id) in top10ids:
        pass
    else:
        found = [x for x in sortedL if x[1] == interaction.user.id]
        if len(found) == 0:
            pass
        else:
            index = sortedL.index(found[0])
            word = 'wins'
            if getLevel(sortedL[index][0])[0] == 1:
                word = 'win'
            desc += f'\n**#{index+1} <@{sortedL[index][1]}> - {sortedL[index][0]} {word}**\n'
            

    
    await interaction.followup.send(embed=discord.Embed(title='Duels Leaderboard', description=desc))


@bot.tree.command(name="level", description="View your level.")
async def level(interaction : discord.Interaction):
    await interaction.response.defer()
    if int(interaction.channel.category_id) in closedCategorys and closed == True: return
    if interaction.user.bot:
            return
    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT user_id FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            result9 = await cursor.fetchone()
    if result9 is None:
        async with aiosqlite.connect("exp.sqlite") as db:
            sqlquery = f"INSERT INTO 'exp' (user_id, xp, class, guild_id, valid, cooldown) VALUES ({interaction.user.id}, 0, 0, {interaction.guild.id}, 0, 0)"
            await db.execute(sqlquery)
            await db.commit()
    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT xp, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            result = await cursor.fetchone()
    expLeft = getLevel(result[0])[1]-result[0]
    embedSent = discord.Embed(title=f"{interaction.user.display_name}", description=f'''> Class: {getClass(result[1])[0]} {getClass(result[1])[1]} {getClass(result[1])[2]}\n# Level {getLevel(result[0])[0]} ({round(find_percentage(result[0], getLevel(result[0])[2], getLevel(result[0])[1]), 2)}%)\n\nApproximately `{str(math.ceil((expLeft/expPerCooldown)))}` more messages to reach level {getLevel(result[0])[0]+1}.''')
    await interaction.followup.send(embed=embedSent)

@bot.tree.command(name="aga_resetcd", description="[ADMINS ONLY] Reset the cooldown.")
async def reset_cd(interaction: discord.Interaction, member:discord.Member):
    if member is None:
        await interaction.response.defer()
        return
    if member.bot:
        await interaction.response.defer()
        return
    await interaction.response.defer(ephemeral=True)
    admins = [816769793231028244, 242681702512721931]
    plantRole = interaction.guild.get_role(roles["plant-admin"])
            
    if interaction.user.id in admins:
        pass
    elif plantRole in interaction.user.roles:
        pass
    else:
        return
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        sqlquery = f'''UPDATE cooldowntb SET unix=1 WHERE user_id={member.id}'''
        await db.execute(sqlquery)
        await db.commit()

    await interaction.followup.send(f"Did it, reset the cooldowns of <@{member.id}>!", ephemeral=True)

@bot.tree.command(name="aga_resetduels", description="[ADMINS ONLY] Reset duels.")
async def reset(interaction: discord.Interaction):

    await interaction.response.defer(ephemeral=True)

    admins = [816769793231028244, 242681702512721931]
    plantRole = interaction.guild.get_role(roles["plant-admin"])
            
    if interaction.user.id in admins:
        pass
    elif plantRole in interaction.user.roles:
        pass
    else:
        return
    cooldown = int(60*60*24*6.5)
    commandName = "resetDuels"
    async with aiosqlite.connect("cooldowns.sqlite") as db:
        query = f"SELECT unix FROM cooldowntb WHERE cooldown_name='{commandName}'"
        async with db.execute(query) as cursor:
            cooldownRaw = await cursor.fetchone()
    if cooldownRaw is None:
        cdvar = timestamproundedf(cooldown)
        cdvar0 = timestamproundedf(0)
        async with aiosqlite.connect("cooldowns.sqlite") as db:
            sqlquery = f"INSERT INTO 'cooldowntb' (user_id, cooldown_name, unix) VALUES ({interaction.user.id}, '{commandName}', {cdvar})"
            await db.execute(sqlquery)
            await db.commit()
        cooldownU = cdvar0
    else:
        cooldownU = cooldownRaw[0]
    if cooldownU <= timestamproundedf(0):
        pass
    else:
        await interaction.followup.send(f"On cooldown until <t:{cooldownU}:R> (<t:{cooldownU}:F>)", ephemeral=True)

        return
    v1 = View()
    b1 = Button(label="U sure?")

    async def b1callback(interaction2:discord.Interaction):
        b1.disabled = True
        await m1.edit(view=v1)

        async with aiosqlite.connect("dueling.sqlite") as db:
            sqlquery = f'''UPDATE winners SET wins=0 WHERE guild_id={interaction.guild.id}'''
            await db.execute(sqlquery)
            await db.commit()
        await interaction2.response.defer(ephemeral=True)

        await interaction2.followup.send(f"Did it, reset!", ephemeral=True)
            
    b1.callback = b1callback
    v1.add_item(b1)

    m1 = await interaction.followup.send(f"You sure? click u sure", view=v1, ephemeral=True)

@bot.tree.command(name="aga_stageup", description="[ADMINS ONLY] Stage up the user.")
async def stage_up(interaction: discord.Interaction, member:discord.Member):
    if member is None:
        await interaction.response.defer()
        return
    if member.bot:
        await interaction.response.defer()
        return
    await interaction.response.defer(ephemeral=True)
    admins = [816769793231028244, 242681702512721931]
    plantRole = interaction.guild.get_role(roles["plant-admin"])
            
    if interaction.user.id in admins:
        pass
    elif plantRole in interaction.user.roles:
        pass
    else:
        await interaction.response.defer()
        return
    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT xp, class FROM exp WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            result = await cursor.fetchone()
    level = getLevel(result[0])[0]
    limits = getLimits()
    jump = level+30
    async with aiosqlite.connect("exp.sqlite") as db:
        sqlquery = f'''UPDATE exp SET xp={limits[int(jump)][0]+1} WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
        await db.execute(sqlquery)
        sqlquery = f'''UPDATE exp SET valid=1 WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
        await db.execute(sqlquery)
        await db.commit()

    await interaction.followup.send(f"Did it, staged up <@{member.id}>!", ephemeral=True)

@bot.tree.command(name="aga_resetlevel", description="[ADMINS ONLY] Reset level.")
async def reset_level(interaction: discord.Interaction, member:discord.Member):
    await interaction.response.defer(ephemeral=True)
    if member is None:
        await interaction.response.defer()
        return
    if member.bot:
        await interaction.response.defer()
        return
    admins = [816769793231028244, 242681702512721931]
    plantRole = interaction.guild.get_role(roles["plant-admin"])
            
    if interaction.user.id in admins:
        pass
    elif plantRole in interaction.user.roles:
        pass
    else:
        return
    
    async with aiosqlite.connect("exp.sqlite") as db:
        sqlquery = f'''UPDATE exp SET xp=0 WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
        await db.execute(sqlquery)
        sqlquery = f'''UPDATE exp SET class=0 WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
        await db.execute(sqlquery)
        await db.commit()
    CLASSESINORDER = {'1':'Magician','2':'Jester','3':'Bard','4':'Pirate','5':'Fae','6':'Mystic','7':'Wildshaper','8':'Cleric'}

    for x in CLASSESINORDER:
        try:
            role = interaction.guild.get_role(roles[CLASSESINORDER[str(x)].lower()])
            if role in member.roles:
                await member.remove_roles(role)
                break
        except:
            pass
    for x in CLASSESINORDER:
        try:
            role = interaction.guild.get_role(roles[CLASSESINORDER[str(x)].lower()+"2"])
            if role in member.roles:
                await member.remove_roles(role)
                break
        except:
            pass
    for x,y in enumerate(levelroles):
                        try:
                            role = interaction.guild.get_role(levelroles[y])
                            if role in member.roles:
                                await member.remove_roles(role)
                                break
                        except:
                            pass
    await interaction.followup.send("Did it, reset!", ephemeral=True)


@bot.tree.command(name="aga_roles", description="[ADMINS ONLY] Give back roles.")
async def aga_roles(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=True)
    admins = [816769793231028244, 242681702512721931]
    plantRole = interaction.guild.get_role(roles["plant-admin"])
            
    if interaction.user.id in admins:
        pass
    elif plantRole in interaction.user.roles:
        pass
    else:
        return
    
    if member is None:
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, class, user_id FROM exp WHERE guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                result = await cursor.fetchall()
        for x in list(result):
            try:
                mylevel = getLevel(x[0])[0]
                for y in sorted(levelroles, key=lambda z: int(z), reverse=True):
                    if mylevel >= int(y):
                        themem = interaction.guild.get_member(x[2])
                        role1 = interaction.guild.get_role(levelroles[str(y)])
                        for a,b in enumerate(levelroles):
                            try:
                                role = interaction.guild.get_role(levelroles[b])
                                if role in themem.roles:
                                    await themem.remove_roles(role)
                                break
                            except:
                                pass
                        await themem.add_roles(role1)
                        break
            except:
                themem = interaction.guild.get_member(x[2])
                print(f"Didn't do <@{themem.id}>")
    else:
        async with aiosqlite.connect("exp.sqlite") as db:
            query = f"SELECT xp, class, user_id FROM exp WHERE user_id={member.id} AND guild_id = {interaction.guild.id}"
            async with db.execute(query) as cursor:
                result = await cursor.fetchone()
        mylevel = getLevel(result[0])[0]
        for y in sorted(levelroles, key=lambda x: int(x), reverse=True):
            if mylevel >= int(y):
                role1 = interaction.guild.get_role(levelroles[str(y)])
                for a,b in enumerate(levelroles):
                    try:
                        role = interaction.guild.get_role(levelroles[b])
                        if role in member.roles:
                            await member.remove_roles(role)
                        break
                    except:
                        pass
                await member.add_roles(role1)
                break
        

    await interaction.followup.send("Did it, given roles!", ephemeral=True)

                
            
                    
        

@bot.tree.command(name="aga_setlevel", description="[ADMINS ONLY] Set level.")
async def config_level(interaction: discord.Interaction, member:discord.Member, set:int):
    await interaction.response.defer(ephemeral=True)
    if member is None:
        return
    if set is None:
        return
    if member.bot:
        return
    admins = [816769793231028244, 242681702512721931]
    plantRole = interaction.guild.get_role(roles["plant-admin"])
            
    if interaction.user.id in admins:
        pass
    elif plantRole in interaction.user.roles:
        pass
    else:
        await interaction.response.defer()
        return
    limits = getLimits()
    if set > maxLevel() or set < 0:
        await interaction.response.defer()
        return
    async with aiosqlite.connect("exp.sqlite") as db:
        query = f"SELECT xp, class FROM exp WHERE user_id = {member.id} AND guild_id = {interaction.guild.id}"
        async with db.execute(query) as cursor:
            result = await cursor.fetchone()
    pastEXP = result[0]
    async with aiosqlite.connect("exp.sqlite") as db:
        sqlquery = f'''UPDATE exp SET xp={limits[int(set)][0]+1} WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
        await db.execute(sqlquery)
        await db.commit()
    if getLevel(pastEXP)[0] < levelToClass:
        if getLevel(limits[int(set)][0]+1)[0] >= levelToClass:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid={True} WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
                await db.execute(sqlquery)
                await db.commit()

    if getLevel(pastEXP)[0] < levelToEnchant:
        if getLevel(limits[int(set)][0]+1)[0] >= levelToEnchant:
            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid={True} WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
                await db.execute(sqlquery)
                await db.commit()
    if getLevel(pastEXP)[0] > levelToClass:
        if getLevel(limits[int(set)][0]+1)[0] < levelToClass:
            CLASSESINORDER = {'1':'Magician','2':'Jester','3':'Bard','4':'Pirate','5':'Fae','6':'Mystic','7':'Wildshaper','8':'Cleric'}

            for x in CLASSESINORDER:
                try:
                    role = interaction.guild.get_role(roles[CLASSESINORDER[str(x)].lower()])
                    if role in member.roles:
                        await member.remove_roles(role)
                        break
                except:
                    pass


            async with aiosqlite.connect("exp.sqlite") as db:
                sqlquery = f'''UPDATE exp SET valid={False} WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
                await db.execute(sqlquery)
                sqlquery2 = f'''UPDATE exp SET class=0 WHERE user_id={member.id} AND guild_id = {interaction.guild_id}'''
                await db.execute(sqlquery2)
                await db.commit()


    await interaction.followup.send("Did it!", ephemeral=True)


@bot.tree.error
async def on_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    logging.warning(traceback.format_exc()) #logs the error
    channel = bot.get_channel(1077720777949982783)
    await channel.send(f"An error occured: {str(error)}")
    


async def main():
    async with bot:
        #await bot.add_cog(Economy(bot))
        await bot.start(TOKEN)

asyncio.run(main())
