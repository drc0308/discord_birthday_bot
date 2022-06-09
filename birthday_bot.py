# /bin/python3

from collections import deque
import datetime
import logging
import re
import sqlite3
import pytz
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

import discord
from discord.ext import commands, tasks

# Globals
TOKEN = Path('secret_token.txt').read_text()
db_con = sqlite3.connect('birthdays.db')
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
DEFAULT_VAL_NON_USER = -1

# Helper functions and data types
@dataclass
class BirthdayEntry:
    """ Data submitted by a user to store in leaderboard
    """
    userid: str = ""
    date: str = ""
    username: str = ""

# Discord Bot Tasks
# TODO (really should capture everything in this class :shrug:)
class BdayReminder(commands.Cog):
    def __init__(self):
        print("created")
        self.check_for_birthdays.start()
        
    @staticmethod
    def get_announcements_chan_id() -> id:
        for chan in bot.get_all_channels():
            if chan.name == 'announcements':
                return chan

    @tasks.loop(hours=24.0)
    async def check_for_birthdays(self):
        chan = self.get_announcements_chan_id()
        bdays = check_for_bdays_today()
        if bdays:
            bday_string = ''
            for bday in bdays:
                if int(bday[0]) != -1:
                    bday_string += f"Happy birthday <@{bday[0]}> :birthday: :partying_face: \n" 
                else:
                    bday_string += f"Happy birthday {bday[2]} :birthday: :partying_face: \n" 
            await chan.send(bday_string)
    
    @check_for_birthdays.before_loop
    async def before_printer(self):
        await bot.wait_until_ready()


def parse_message(msg : str, command_key : str, userid : str, username: str) -> Optional[BirthdayEntry]:
    logging.debug(msg)
    m = re.search(command_key+'\s([0-9][0-9][/,-,|][0-9][0-9])', msg)
    if m is None:
        return None
    else:
        result = BirthdayEntry()
        date_string = m.group(1)
        try:
            date = datetime.datetime.strptime(date_string, '%m-%d')
        except ValueError:
            try:
                date = datetime.datetime.strptime(date_string, '%m/%d')
            except ValueError:
                return None
        result.userid = userid
        result.username = username
        result.date = date.strftime("%m/%d")
        return result

def parse_message_bday_other(msg : str, userid : str, username : str) -> Optional[BirthdayEntry]:
    print(msg)
    m = re.search('\\$bday-add-other\s([A-z]+)\s([0-9][0-9][/,-,|][0-9][0-9])', msg)
    if m is None:
        return None
    else:
        result = BirthdayEntry()
        date_string = m.group(2)
        try:
            date = datetime.datetime.strptime(date_string, '%m/%d')
        except ValueError:
            return None
        result.userid = DEFAULT_VAL_NON_USER
        result.username = str(m.group(1))
        result.date = date.strftime("%m/%d")
        return result

def check_for_bdays_today() -> List[str]:
    cur = db_con.cursor()
    date = datetime.datetime.now().strftime("%m/%d")
    check_cmd = 'SELECT * from birthday WHERE date = ?'
    cur.execute(check_cmd, [date])
    return cur.fetchall()

def get_all_bdays() -> List[str]:
    cur = db_con.cursor()
    check_cmd = 'SELECT * from birthday ORDER BY date ASC'
    cur.execute(check_cmd)
    return cur.fetchall()

def insert_bday(bday : BirthdayEntry):
    cur = db_con.cursor()
    insert_cmd = 'INSERT into birthday values (?, ?, ?)'
    cur.execute(insert_cmd,[str(bday.userid), str(bday.date), str(bday.username)])
    db_con.commit()

def delete_bday(bday : BirthdayEntry):
    cur = db_con.cursor()
    delete_cmd = 'DELETE from birthday WHERE user = ?'
    cur.execute(delete_cmd,[bday.userid])
    db_con.commit()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="to $help"))

@bot.command(name='bday-add', help="Allows you to add your bday in format MM/DD")
async def handle_bday_add(ctx):
    # Note $ is a special character in python regex so it needs to be escaped
    res = parse_message(ctx.message.content, '\\$bday-add', ctx.message.author.id, ctx.message.author)
    if res is None:
        logging.info(f"Invalid message format: {ctx.message.content}")
        await ctx.send("Error with bday message try again, must be `MM/DD` format and a valid date")
        return
    else:
        insert_bday(res)
        await ctx.send(f"Bday recorded for {res.username} as {res.date}")

@bot.command(name='bday-add-other', help="Allows you to add a non draper gang bday in format NAME MM/DD")
async def handle_bday_add_other(ctx):
    res = parse_message_bday_other(ctx.message.content, ctx.message.author.id, ctx.message.author)
    if res is None:
        logging.info(f"Invalid message format: {ctx.message.content}")
        await ctx.send("Error with bday message try again, must be `NAME MM/DD` format and a valid date")
        return
    else:
        insert_bday(res)
        await ctx.send(f"Bday recorded for {res.username} as {res.date}")

@bot.command(name='bday-delete', help='Delete your submitted birthday')
async def handle_bday_delete(ctx):
    bday = BirthdayEntry()
    bday.userid = str(ctx.message.author.id)
    delete_bday(bday)
    await ctx.send(f"Birthday deleted for {bday.user} on {bday.date}")

@bot.command(name='bday-list', help='See all channel birthdays')
async def handle_bday_list(ctx):
    bdays = get_all_bdays()
    cur_day = datetime.date.today()
    past_list = []
    up_list = []

    for bday in bdays:
        bday_date = datetime.datetime.strptime(f"{bday[1]}/{datetime.date.today().year}",'%m/%d/%Y');
        
        guild = bot.get_guild(ctx.guild.id)
        guild.fetch_members()
        if(int(bday[0]) == -1):
            display_name = bday[2]
        else:
            display_name = guild.get_member(int(bday[0])).nick
            if display_name is None:
                display_name = guild.get_member(int(bday[0])).name
        if bday_date.date() < cur_day:
            past_list.append(f"{display_name} : {bday[1]} \n")
        else:
            up_list.append(f"{display_name} : {bday[1]} \n")
    bday_list = up_list + past_list

    bday_list_string = ":birthday: Upcoming birthdays :birthday: \n" + "".join(bday_list)

    await ctx.send(bday_list_string)
    return

def main():
    # logging.basicConfig(filename='birthday_bot.log', level=logging.DEBUG)
    logging.basicConfig(level=logging.WARN)
    logging.info('Starting the birthday bot')
    BdayReminder()
    bot.run(TOKEN)
    
if __name__ == '__main__':
    main() 