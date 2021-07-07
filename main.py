import discord # install with: pip install discord.py
from discord.ext import commands # to use the commands from discord.ext
import gspread
import json
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
from operator import itemgetter
from keep_alive import keep_alive

agents = ["PX", "JT", "SA", "SV", "BS", "OM", "BR", "CY", "VI", "RZ", "RY", "KJ", "SK", "YO", "AS", "KO"] # contractions of all agents
agents_full = ["Phoenix", "Jett", "Sage", "Sova", "Brimstone", "Omen", "Breach", "Cypher", "Viper", "Raze", "Reyna", "Killjoy", "Skye", "Yoru", "Astra", "Kay/o"]
agentFlag = [":flag_gb:", ":flag_kr:", ":flag_cn:", ":flag_ru:", ":flag_us:", ":grey_question:", ":flag_se:", ":flag_ma:", ":flag_us:", ":flag_br:", ":flag_mx:", ":flag_de:", ":flag_au:", ":flag_jp:", ":flag_gh:", ":grey_question:"]
agents_role = ["D", "D", "S", "I", "C", "C", "I", "S", "C", "D", "D", "S", "I", "D", "C", "I"]

maps = ["Bind", "Haven", "Split", "Ascent", "Icebox", "Breeze"]
mapFlag = [":flag_ma:", ":flag_bt:", ":flag_jp:", ":flag_it:", ":flag_ru:", ":flag_tt:"]

#get Google Sheet ID
def get_gsk(client, message):
    with open("gsk.json", "r") as f:
        gsk = json.load(f)
    return gsk[str(message.guild.id)]

gc = gspread.service_account(filename=r"credentials.json")

#get developerID
def get_developerID(client, message):
    with open("developerIDs.json", "r") as f:
        developerID = json.load(f)
    return int(developerID[str(message.guild.id)])

# set a bot prefix
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix, help_command=None)

# import the token from a extern file for security
tokenTxt = open(r"token.txt", "r")
if tokenTxt.mode == "r":
    token = tokenTxt.read()

# bot is online
@client.event
async def on_ready():
    with open("prefixes.json", "r") as f:
        serverAmmount = len(json.load(f))
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Stats on {serverAmmount} servers"))
    print('We have logged in as {0.user}'.format(client))

#bot join the first time
@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "?"
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    with open("gsk.json", "r") as f:
        gsk = json.load(f)
    gsk[str(guild.id)] = "0"
    with open("gsk.json", "w") as f:
        json.dump(gsk, f, indent=4)
    with open("developerIDs.json", "r") as f:
        developerID = json.load(f)
    developerID[str(guild.id)] = "0"
    with open("developerIDs.json", "w") as f:
        json.dump(developerID, f, indent=4)
    with open("prefixes.json", "r") as f:
        serverAmmount = len(json.load(f))
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Stats on {serverAmmount} servers"))
    
#bot leave
@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    with open("gsk.json", "r") as f:
        gsk = json.load(f)
    gsk.pop(str(guild.id))
    with open("gsk.json", "w") as f:
        json.dump(gsk, f, indent=4)
    with open("developerIDs.json", "r") as f:
        developerID = json.load(f)
    developerID.pop(str(guild.id))
    with open("developerIDs.json", "w") as f:
        json.dump(developerID, f, indent=4)
    with open("prefixes.json", "r") as f:
        serverAmmount = len(json.load(f))
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Stats on {serverAmmount} servers"))

# output if an error occured
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("This command requires an argument.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Give me a valid argument.")
    else:
        with open("developerIDs.json", "r") as f:
            developerIDs = json.load(f)
        developerID = int(developerIDs[str(ctx.guild.id)])
        await ctx.send("Something went wrong, <@" + str(developerID) + ">.") # mentioned the developer in discord if something go wrong
        print(error)

#set developerID
@client.command()
async def setdeveloperID(ctx, id):
    developerID = get_developerID(client, ctx)
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == developerID:
        with open("developerIDs.json", "r") as f:
            developerID = json.load(f)
        try:
            await client.fetch_user(int(id))
        except:
            await ctx.send(f":x: There is no valid user with the ID: **{id}**")
            return
        developerID[str(ctx.guild.id)] = id
        with open("developerIDs.json", "w") as f:
            json.dump(developerID, f, indent=4)
        await ctx.send(f":white_check_mark: Set the developerID to: **{id}** -> User: **{await client.fetch_user(int(id))}**")
    else:
        await ctx.send(f":warning: Ask **{await client.fetch_user(ctx.guild.owner_id)}** to change the developerID.")

#show developerID
@client.command()
async def showdeveloperID(ctx):
    with open("developerIDs.json", "r") as f:
        developerID = json.load(f)
    id = developerID[str(ctx.guild.id)]
    try:
        await ctx.send(f":information_source: DeveloperID: **{id}** -> User: **{await client.fetch_user(int(id))}**")
    except:
        await ctx.send(f":information_source: DeveloperID: **{id}** -> Set the developerID with **?setdeveloperID <id>**")

#change prefix
@client.command()
async def changeprefix(ctx, prefix):
    developerID = get_developerID(client, ctx)
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == developerID:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f":white_check_mark: Changed prefix to: **{prefix}**")
    else:
        await ctx.send(f"Ask **{await client.fetch_user(ctx.guild.owner_id)}** to change the bot prefix.")

#set gsk
@client.command()
async def setkey(ctx, id):
    developerID = get_developerID(client, ctx)
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == developerID:
        keyList = id.split("/")
        if len(keyList) == 1:
            key = keyList[0]
        else:
            key = keyList[5]
        with open("gsk.json", "r") as f:
            gsk = json.load(f)
        error = 0
        try:
            error = 1
            sh = gc.open_by_key(key)
            print(sh)
            error = 2
            sh.get_worksheet(0).update_cell(1, 1, "")
        except:
            if error == 1:
                await ctx.send(":x: Can't connect the **Google Sheet Document** to **ValorantStats**.\nIs the Document shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access?")
            elif error == 2:
                await ctx.send(f":x: **monkacode@valorantstats.iam.gserviceaccount.com** has no editor access to the Google Sheet Document **{sh.title}**")
            else:
                await ctx.send(":x: Can't connect the **Google Sheet Document** to **ValorantStats**.")
            return
        gsk[str(ctx.guild.id)] = key
        with open("gsk.json", "w") as f:
            json.dump(gsk, f, indent=4)
        await ctx.send(f":white_check_mark: **{sh.title}** x **ValorantStats** connected successfully.")
    else:
        await ctx.send(f":warning: Ask **{await client.fetch_user(ctx.guild.owner_id)}** to set the Google Sheet Key.")

#show gsk
@client.command()
async def showkey(ctx):
    developerID = get_developerID(client, ctx)
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == developerID:
        with open("gsk.json", "r") as f:
            gsk = json.load(f)
        key = gsk[str(ctx.guild.id)]
        await ctx.send(f":information_source: Google Sheet Key: **{key}**")
    else:
        await ctx.send(f":warning: Ask **{await client.fetch_user(ctx.guild.owner_id)}** to see the Google Sheet Key.")

@client.command()
async def addgame(ctx, date=None, played_map=None, rw=None, rl=None, firstSide=None, played_rounds=None, p1=None, p2=None, p3=None, p4=None, p5=None):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return
    developerID = get_developerID(client, ctx)
    players = sh.get_worksheet(0).get("C3:C12") # parse the names of the team members
    playerfast = sh.get_worksheet(0).get("E3:E12")
    info = sh.get_worksheet(0)
    worksheet = sh.get_worksheet(1)
    error = []
    mapExist = False
    game_player = [p1, p2, p3, p4, p5]
    player_str = []
    player_submit = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]]
    player_agent_str = []
    try:
        if ctx.author.id != developerID:
            try:
                error.append("You can't add a game. Contact **" + str(await client.fetch_user(developerID)) + "** for adding a game.")
            except:
                error.append(f"The DeveloperID ({developerID}) isn't a valid user!")
        for x in range(len(maps)):
            if str(played_map.lower()) == str(maps[x].lower()):
                mapExist = True
                break
        if mapExist == False:
            error.append("The map **" + played_map.capitalize() + "** doesn't exist.")
        try:
            int(rw)
            int(rl)
        except:
            error.append("**" + rw + "** and **" + rl + "** aren't integers.")
        if int(rw) < 13 and int(rl) < 13:
            error.append("The result of the game isn't valid.")
        if int(rw) == int(rl) and int(rw) > 12:
            None
        elif int(rw) < int(rl)+2 and int(rl) < int(rw)+2:
            error.append("The result of the game isn't valid.")
        if int(rw) != played_rounds.upper().count("W") or int(rl) != played_rounds.upper().count("L"):
            error.append("The result isn't the same as the rounds.")
        if firstSide.upper() != "A" and firstSide.upper() != "D":
            error.append("The first side must be **A** or **D**.")
        for x in range(5):
            try:
                game_player[x] = game_player[x].replace("[", "").replace("]", "").split(",")
                if len(game_player[x]) != 5:
                    error.append("You missed some stats for the **" + str(x+1) + ".** player.")
                    break
                game_player[x][0] = str(game_player[x][0])
                game_player[x][1] = agentShortName(game_player[x][1])
                try:
                    game_player[x][2] = int(game_player[x][2])
                    game_player[x][3] = int(game_player[x][3])
                    game_player[x][4] = int(game_player[x][4])
                except:
                    error.append("The KDA isn't valid. Use only numbers.")
                playerFound = False
                for y in range(len(players)):
                    if game_player[x][0].lower() == players[y][0].lower() or game_player[x][0].lower() == playerfast[y].lower():
                        player_str.append(players[y][0])
                        game_player[x].append(y)
                        playerFound = True
                        if game_player[x][5] == y:
                            player_submit[y] = game_player[x]
                        break
                    else:
                        error_str = "The player **" + game_player[x][0] + "** isn't in the team."
                
                for y in range(x):
                    try:
                        if player_str[x] == player_str[y]:
                            error_str = "The player **" + game_player[x][0] + "** already exists in this game."
                            playerFound = False
                            break
                    except:
                        pass
                if playerFound == False:
                    error.append(error_str)

                agentFound = False
                for y in range(len(agents)):
                    if game_player[x][1].lower() == agents[y].lower() or game_player[x][1].lower() == agents_full[y].lower():
                        player_agent_str.append(agents_full[y])
                        agentFound = True
                        break
                    else:
                        error_str = "The agent **" + game_player[x][1] + "** doesn't exist."

                for y in range(x):
                    try:
                        if player_agent_str[x] == player_agent_str[y]:
                            error_str = "**" + player_str[y] + "** already plays **" + player_agent_str[x] + "**."
                            agentFound = False
                            break
                    except:
                        pass
                if agentFound == False:
                    error.append(error_str)
            except:
                pass
    except:
        pass
    if len(error) != 0:
        await ctx.send("There are **" + str(len(error)) + "** errors. The first one is:\n" + error[0])
    else:
        worksheet.append_row([date, played_map.capitalize(), int(rw), int(rl), firstSide.upper(), played_rounds.upper(), player_submit[0][1], player_submit[0][2], player_submit[0][3], player_submit[0][4], player_submit[1][1], player_submit[1][2], player_submit[1][3], player_submit[1][4], player_submit[2][1], player_submit[2][2], player_submit[2][3], player_submit[2][4], player_submit[3][1], player_submit[3][2], player_submit[3][3], player_submit[3][4], player_submit[4][1], player_submit[4][2], player_submit[4][3], player_submit[4][4], player_submit[5][1], player_submit[5][2], player_submit[5][3], player_submit[5][4], player_submit[6][1], player_submit[6][2], player_submit[6][3], player_submit[6][4], player_submit[7][1], player_submit[7][2], player_submit[7][3], player_submit[7][4], player_submit[8][1], player_submit[8][2], player_submit[8][3], player_submit[8][4], player_submit[9][1], player_submit[9][2], player_submit[9][3], player_submit[9][4]])
        stats = ""
        for x in range(len(player_str)):
            stats += getCountry(player_agent_str[x]) + " **" + player_agent_str[x].upper() + "**" + getCapsGap(player_agent_str[x]) + "**" + player_str[x] + int(info.get("D3:D12")[game_player[x][5]][0])*" " + "**   |   KDA: **" + str(game_player[x][2]) + "** / **" + str(game_player[x][3]) + "** / **" + str(game_player[x][4]) + "**\n"
        await ctx.send("Created the game with following attributes!\nDate: **" + date + "**\nMap: **" + played_map.capitalize() + "**   |   First Round Site: **" + firstSide.upper() + "**\nResult: **" + rw + "** - **" + rl + "**\n\nPlayer specific stats:\n" + stats)

@client.command()
async def agent(ctx, arg1=None, arg2=None):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return
    players = sh.get_worksheet(0).get("C3:C12") # parse the names of the team members
    worksheet = sh.get_worksheet(1)
    data = worksheet.get("C2:AT")
    map = worksheet.get("B2:B")
    agentStats = []
    allgames = 0

    for x in range(len(maps)):
        if arg1 == None:
            arg1Map = False
            sort_algo = None
            break
        elif arg1.lower() == maps[x].lower():
            arg1Map = True
            if arg2 == None:
                sort_algo = None
            else:
                sort_algo = arg2.lower()
            break
        else:
            arg1Map = False
            sort_algo = arg1.lower()

    if arg1Map == False:
        for x in range(len(data)):
            allgames += 1
            if int(data[x][0]) > int(data[x][1]):  
                win = 1
            else:
                win = 0
            for y in range(len(players)):
                try:
                    if len(agentStats) == 0:
                        agentStats.append([data[x][(y*4)+4], 1, win, int(data[x][(y*4)+5]), int(data[x][(y*4)+6]), int(data[x][(y*4)+7])])
                    else:
                        agentNew = False
                        for z in range(len(agentStats)):
                            if agentStats[z][0] == data[x][(y*4)+4]:
                                agentStats[z][1] += 1
                                agentStats[z][2] += win
                                agentStats[z][3] += int(data[x][(y*4)+5])
                                agentStats[z][4] += int(data[x][(y*4)+6])
                                agentStats[z][5] += int(data[x][(y*4)+7])
                                agentNew = False
                                break
                            else:
                                agentNew = True
                        if agentNew == True:
                            agentStats.append([data[x][(y*4)+4], 1, win, int(data[x][(y*4)+5]), int(data[x][(y*4)+6]), int(data[x][(y*4)+7])])
                except:
                    pass
    else:
        for x in range(len(data)):
            if arg1.lower() == map[x][0].lower():
                allgames += 1
                if int(data[x][0]) > int(data[x][1]):  
                    win = 1
                else:
                    win = 0
                for y in range(len(players)):
                    try:
                        if len(agentStats) == 0:
                            agentStats.append([data[x][(y*4)+4], 1, win, int(data[x][(y*4)+5]), int(data[x][(y*4)+6]), int(data[x][(y*4)+7])])
                        else:
                            agentNew = False
                            for z in range(len(agentStats)):
                                if agentStats[z][0] == data[x][(y*4)+4]:
                                    agentStats[z][1] += 1
                                    agentStats[z][2] += win
                                    agentStats[z][3] += int(data[x][(y*4)+5])
                                    agentStats[z][4] += int(data[x][(y*4)+6])
                                    agentStats[z][5] += int(data[x][(y*4)+7])
                                    agentNew = False
                                    break
                                else:
                                    agentNew = True
                            if agentNew == True:
                                agentStats.append([data[x][(y*4)+4], 1, win, int(data[x][(y*4)+5]), int(data[x][(y*4)+6]), int(data[x][(y*4)+7])])
                    except:
                        pass

    if sort_algo == None:
        agentStats = sorted(agentStats, key= lambda x: x[2]**3/x[1]**2, reverse=True)
    elif sort_algo == "--games" or sort_algo == "--pick%":
        agentStats = sorted(agentStats, key=itemgetter(1), reverse=True)
    elif sort_algo == "--wins":
        agentStats = sorted(agentStats, key=itemgetter(2), reverse=True)
    elif sort_algo == "--kills":
        agentStats = sorted(agentStats, key= lambda x: x[3]/x[1], reverse=True)
    elif sort_algo == "--deaths":
        agentStats = sorted(agentStats, key= lambda x: x[4]/x[1], reverse=True)
    elif sort_algo == "--assists":
        agentStats = sorted(agentStats, key= lambda x: x[5]/x[1], reverse=True)
    elif sort_algo == "--kd":
        agentStats = sorted(agentStats, key= lambda x: x[3]/x[4], reverse=True)
    elif sort_algo == "--kda":
        agentStats = sorted(agentStats, key= lambda x: (x[3]+x[5])/x[4], reverse=True)
    elif sort_algo == "--win%":
        agentStats = sorted(agentStats, key= lambda x: x[2]/x[1], reverse=True)
    
    stats_str = ["", ""]
    for x in range(len(agentStats)):
        if len(stats_str[0]) > 1700:
            stats_str[1] += getCountry(agentStats[x][0]) + " [**" + agentStats[x][0] + "**] **" + agentFullName(agentStats[x][0]).upper() + "**" + getCapsGap(agentFullName(agentStats[x][0])) + "KDA: **" + str("%.1f" % (round((agentStats[x][3]/agentStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((agentStats[x][4]/agentStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((agentStats[x][5]/agentStats[x][1]), 1))) + "**   |   K/D: **" + str("%.2f" % (round((agentStats[x][3]/agentStats[x][4]), 2))) + "**   |   Win%: **" + str("%.1f" % (round((agentStats[x][2]/agentStats[x][1]), 3)*100)) + "%**   |   Pick%: **" + str("%.1f" % (round((agentStats[x][1]/allgames), 3)*100)) + "%**   |   Games: **" + str(agentStats[x][1]) + "**   |   Score: **" + str(round((agentStats[x][2]**3)/(agentStats[x][1]**2)*10)) + "**\n"
        else:
            stats_str[0] += getCountry(agentStats[x][0]) + " [**" + agentStats[x][0] + "**] **" + agentFullName(agentStats[x][0]).upper() + "**" + getCapsGap(agentFullName(agentStats[x][0])) + "KDA: **" + str("%.1f" % (round((agentStats[x][3]/agentStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((agentStats[x][4]/agentStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((agentStats[x][5]/agentStats[x][1]), 1))) + "**   |   K/D: **" + str("%.2f" % (round((agentStats[x][3]/agentStats[x][4]), 2))) + "**   |   Win%: **" + str("%.1f" % (round((agentStats[x][2]/agentStats[x][1]), 3)*100)) + "%**   |   Pick%: **" + str("%.1f" % (round((agentStats[x][1]/allgames), 3)*100)) + "%**   |   Games: **" + str(agentStats[x][1]) + "**   |   Score: **" + str(round((agentStats[x][2]**3)/(agentStats[x][1]**2)*10)) + "**\n"
    await ctx.send(stats_str[0])
    if len(stats_str[1]) != 0:
        await ctx.send(stats_str[1])

@client.command()
async def game(ctx, arg1=None):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return
    players = sh.get_worksheet(0).get("C3:C12") # parse the names of the team members
    playerwidth = sh.get_worksheet(0).get("D3:D12")

    worksheet = sh.get_worksheet(1)
    data = worksheet.get("A2:AT")

    playerStats = []
    player_stats_str = ""

    if arg1 == None:
        x = len(data)-1
        your_round_str = ""
        enemy_round_str = ""
        desc_round_str = ""
        desc_round_list = []
        
        for y in range(len(data[x][5])):
            desc_round_list.append(":black_large_square:")
            if data[x][5][y] == "W":
                your_round_str += " :green_square:"
                enemy_round_str += " :black_large_square:"
                if y == 11 or y == 23:
                    your_round_str += " |"
                    enemy_round_str += " |"
                for n in range(10):
                    if y == 25+(n*2):
                        your_round_str += " |"
                        enemy_round_str += " |"
            elif data[x][5][y] == "L":
                enemy_round_str += " :red_square:"
                your_round_str += " :black_large_square:"
                if y == 11 or y == 23:
                    your_round_str += " |"
                    enemy_round_str += " |"
                for n in range(10):
                    if y == 25+(n*2):
                        your_round_str += " |"
                        enemy_round_str += " |"
        if data[x][4] == "A":
            desc_round_list[0] = ":a:"
            desc_round_list[12] = "| :regional_indicator_d:"
            for n in range(10):
                try:
                    desc_round_list[24+(n*4)] = "| :a:"
                    desc_round_list[26+(n*4)] = "| :regional_indicator_d:"
                except:
                    break
        elif data[x][4] == "D":
            desc_round_list[0] = ":regional_indicator_d:"
            desc_round_list[12] = "| :a:"
            for n in range(10):
                try:
                    desc_round_list[24+(n*4)] = "| :regional_indicator_d:"
                    desc_round_list[26+(n*4)] = "| :a:"
                except:
                    break
        for y in range(len(players)):
            try:
                if data[x][(y*4)+6] != "":
                    playerStats.append([players[y][0], data[x][(y*4)+6], int(data[x][(y*4)+7]), int(data[x][(y*4)+8]), int(data[x][(y*4)+9])])
            except:
                break
        playerStats = sorted(playerStats, key=itemgetter(2), reverse=True)
        for y in range(len(playerStats)):
            for z in range(len(players)):
                if playerStats[z][0] == players[y][0]:
                    playerIndex = z
                    break
            player_stats_str += getCountry(playerStats[y][1]) + " **" +agentFullName(playerStats[y][1]).upper() + "**" + getCapsGap(playerStats[y][1]) + "   **" + playerStats[y][0] + int(playerwidth[playerIndex][0])*" " +"**   |   KDA: **" + str(playerStats[y][2]) + "** / **" + str(playerStats[y][3]) + "** / **" + str(playerStats[y][4]) + "**\n"
        for y in range(len(desc_round_list)):
            desc_round_str += " " + desc_round_list[y]
        await ctx.send("[**" + str(len(data)+1) + "**] Date: **" + str(data[x][0]) + "**   |   Map: **" + data[x][1] + "**\nResult: **" + str(data[x][2]) + "** - **" + str(data[x][3]) + "**\n\n" + desc_round_str + "\n" + your_round_str + "\n" + enemy_round_str + "\n.")
        await ctx.send(player_stats_str)
    else:
        error = False
        try:
            x = int(arg1)-2
        except:
            await ctx.send("This isn't a valid game ID.")
            error = True
        if error == False:
            if x > (len(data)-1):
                await ctx.send("This game don't exists at the moment.")
            else:
                your_round_str = ""
                enemy_round_str = ""
                desc_round_str = ""
                desc_round_list = []
                for y in range(len(data[x][5])):
                    desc_round_list.append(":black_large_square:")
                    if data[x][5][y] == "W":
                        your_round_str += " :green_square:"
                        enemy_round_str += " :black_large_square:"
                        if y == 11 or y == 23:
                            your_round_str += " |"
                            enemy_round_str += " |"
                        for n in range(10):
                            if y == 25+(n*2):
                                your_round_str += " |"
                                enemy_round_str += " |"
                    elif data[x][5][y] == "L":
                        enemy_round_str += " :red_square:"
                        your_round_str += " :black_large_square:"
                        if y == 11 or y == 23:
                            your_round_str += " |"
                            enemy_round_str += " |"
                        for n in range(10):
                            if y == 25+(n*2):
                                your_round_str += " |"
                                enemy_round_str += " |"
                    
                if data[x][4] == "A":
                    desc_round_list[0] = ":a:"
                    desc_round_list[12] = "| :regional_indicator_d:"
                    for n in range(10):
                        try:
                            desc_round_list[24+(n*4)] = "| :a:"
                            desc_round_list[26+(n*4)] = "| :regional_indicator_d:"
                        except:
                            break
                elif data[x][4] == "D":
                    desc_round_list[0] = ":regional_indicator_d:"
                    desc_round_list[12] = "| :a:"
                    for n in range(10):
                        try:
                            desc_round_list[24+(n*4)] = "| :regional_indicator_d:"
                            desc_round_list[26+(n*4)] = "| :a:"
                        except:
                            break
                for y in range(len(players)):
                    try:
                        if data[x][(y*4)+6] != "":
                            playerStats.append([players[y][0], data[x][(y*4)+6], int(data[x][(y*4)+7]), int(data[x][(y*4)+8]), int(data[x][(y*4)+9])])
                    except:
                        break
                playerStats = sorted(playerStats, key=itemgetter(2), reverse=True)
                for y in range(len(playerStats)):
                    for z in range(len(players)):
                        if playerStats[z][0] == players[y][0]:
                            playerIndex = z
                            break
                    player_stats_str += getCountry(playerStats[y][1]) + " **" +agentFullName(playerStats[y][1]).upper() + "**" + getCapsGap(playerStats[y][1]) + "   **" + playerStats[y][0] + int(playerwidth[playerIndex][0])*" " + "**   |   KDA: **" + str(playerStats[y][2]) + "** / **" + str(playerStats[y][3]) + "** / **" + str(playerStats[y][4]) + "**\n"
                for y in range(len(desc_round_list)):
                    desc_round_str += " " + desc_round_list[y]
                await ctx.send("[**" + str(arg1) + "**] Date: **" + str(data[x][0]) + "**   |   Map: **" + data[x][1] + "**\nResult: **" + str(data[x][2]) + "** - **" + str(data[x][3]) + "**\n\n" + desc_round_str + "\n" + your_round_str + "\n" + enemy_round_str + "\n.")
                await ctx.send(player_stats_str)
        
@client.command()
async def map(ctx, arg1=None, arg2=None):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return
    worksheet = sh.get_worksheet(1)
    data = worksheet.get("B2:D")

    allgames = 0
    allwins = 0
    mapStats = []
    if arg2 == None:
        for x in range(len(data)):
            if int(data[x][1]) > int(data[x][2]):  
                win = 1
                draw = 0
                loss = 0
            elif int(data[x][1]) == int(data[x][2]):
                win = 0
                draw = 1
                loss = 0
            else:
                win = 0
                draw = 0
                loss = 1
            for y in range(len(maps)):
                try:
                    if data[x][0] == maps[y]:
                        allgames += 1
                        if win == 1:
                            allwins += 1
                        if len(mapStats) == 0:
                            mapStats.append([maps[y], 1, win, draw, loss])
                        else:
                            mapNew = False
                            for z in range(len(mapStats)):
                                if mapStats[z][0] == maps[y]:
                                    mapStats[z][1] += 1
                                    mapStats[z][2] += win
                                    mapStats[z][3] += draw
                                    mapStats[z][4] += loss
                                    mapNew = False
                                    break
                                else:
                                    mapNew = True
                            if mapNew == True:
                                mapStats.append([maps[y], 1, win, draw, loss])
                except:
                    pass

        if arg1 == None:
            mapStats = sorted(mapStats, key=itemgetter(1), reverse=True)
        elif arg1.lower() == "--wins":
            mapStats = sorted(mapStats, key=itemgetter(2), reverse=True)
        elif arg1.lower() == "--draws":
            mapStats = sorted(mapStats, key=itemgetter(3), reverse=True)
        elif arg1.lower() == "--losses":
            mapStats = sorted(mapStats, key=itemgetter(4), reverse=True)
        elif arg1.lower() == "--win%":
            mapStats = sorted(mapStats, key= lambda x: x[2]/x[1], reverse=True)
        stats_str = ""
        total = [0, 0, 0, 0]
        for x in range(len(mapStats)):
            stats_str += getCountry(mapStats[x][0]) + " **" + mapStats[x][0].upper() + "**" + getCapsGap(mapStats[x][0]) + "Win%: **" + str("%.1f" % (round((mapStats[x][2]/mapStats[x][1]), 3)*100)) +"%**   |   Wins: **" + str(mapStats[x][2]) + "**   |   Losses: **" + str(mapStats[x][4]) + "**   |   Draws: **" + str(mapStats[x][3]) + "**   |   Games: **" + str(mapStats[x][1]) + "**\n"
            for y in range(4):
                total[y] += mapStats[x][y+1]
        await ctx.send("Win%: **" + str("%.1f" % (round((total[1]/total[0]), 3)*100)) + "%**   |   Wins: **" + str(total[1]) + "**   |   Losses: **" + str(total[3]) + "**   |   Draws: **" + str(total[2]) + "**   |   Games: **" + str(total[0]) + "**\n\n" + stats_str)

@client.command()
async def player(ctx, arg1=None, arg2=None):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return
    players = sh.get_worksheet(0).get("C3:C12") # parse the names of the team members
    playerfastold = sh.get_worksheet(0).get("E3:E12")
    playerfast = []
    for x in range(len(playerfastold)):
        playerfast.append(playerfastold[x][0])
    playerwidth = sh.get_worksheet(0).get("D3:D12")
    worksheet = sh.get_worksheet(1)
    data = worksheet.get("G2:AT")
    winrate = worksheet.get("C2:D")
    playedmap = worksheet.get("B2:B")
    
    for x in range(len(players)):
        if arg1 == None:
            break
        elif arg1.lower() == players[x][0].lower() or arg1.lower() == playerfast[x].lower():
            arg1Player = True
            break
        else:
            arg1Player = False

    if arg1 != None and arg1Player == True:
        playerFound = False
        for x in range(len(players)):
            if arg1.lower() == players[x][0].lower() or arg1.lower() == playerfast[x].lower():
                player = x
                playerFound = True
                break
        playergames = 0
        playerwins = 0
        win = 0
        x = 0
        kills = 0
        assists = 0
        deaths = 0
        agentStats = []
        mapStats = []
        if playerFound == True:
            for x in range(len(data)):
                if int(winrate[x][0]) > int(winrate[x][1]):  
                    win = 1
                else:
                    win = 0
                for y in range(len(agents)):
                    try:
                        if data[x][player*4] == agents[y]:
                            playergames += 1
                            if win == 1:
                                playerwins += 1
                            if len(agentStats) == 0:
                                agentStats.append([agents[y], 1, win, int(data[x][(player*4)+1]), int(data[x][(player*4)+2]), int(data[x][(player*4)+3])])
                            else:
                                agentNew = False
                                for z in range(len(agentStats)):
                                    if agentStats[z][0] == agents[y]:
                                        agentStats[z][1] += 1
                                        agentStats[z][2] += win
                                        agentStats[z][3] += int(data[x][(player*4)+1])
                                        agentStats[z][4] += int(data[x][(player*4)+2])
                                        agentStats[z][5] += int(data[x][(player*4)+3])
                                        agentNew = False
                                        break
                                    else:
                                        agentNew = True
                                if agentNew == True:
                                    agentStats.append([agents[y], 1, win, int(data[x][(player*4)+1]), int(data[x][(player*4)+2]), int(data[x][(player*4)+3])])

                    except:
                        pass
                
                try:
                    kills += int(data[x][(player*4)+1])
                    deaths += int(data[x][(player*4)+2])
                    assists += int(data[x][(player*4)+3])
                except:
                    pass
                
                for y in range(len(maps)):
                    try:
                        if playedmap[x][0] == maps[y] and data[x][player*4] != "":
                            if len(mapStats) == 0:
                                mapStats.append([maps[y], 1, win, int(data[x][(player*4)+1]), int(data[x][(player*4)+2]), int(data[x][(player*4)+3])])
                            else:
                                mapNew = False
                                for z in range(len(mapStats)):
                                    if mapStats[z][0] == maps[y]:
                                        mapStats[z][1] += 1
                                        mapStats[z][2] += win
                                        mapStats[z][3] += int(data[x][(player*4)+1])
                                        mapStats[z][4] += int(data[x][(player*4)+2])
                                        mapStats[z][5] += int(data[x][(player*4)+3])
                                        mapNew = False
                                        break
                                    else:
                                        mapNew = True
                                if mapNew == True:
                                    mapStats.append([maps[y], 1, win, int(data[x][(player*4)+1]), int(data[x][(player*4)+2]), int(data[x][(player*4)+3])])
                    except:
                        pass
                
            if arg2 == None:
                agentStats = sorted(agentStats, key=itemgetter(1), reverse=True)
                mapStats = sorted(mapStats, key=itemgetter(1), reverse=True)
            elif arg2.lower() == "--wins":
                agentStats = sorted(agentStats, key=itemgetter(2), reverse=True)
                mapStats = sorted(mapStats, key=itemgetter(2), reverse=True)
            elif arg2.lower() == "--kills":
                agentStats = sorted(agentStats, key= lambda x: x[3]/x[1], reverse=True)
                mapStats = sorted(mapStats, key= lambda x: x[3]/x[1], reverse=True)
            elif arg2.lower() == "--deaths":
                agentStats = sorted(agentStats, key= lambda x: x[4]/x[1], reverse=True)
                mapStats = sorted(mapStats, key= lambda x: x[4]/x[1], reverse=True)
            elif arg2.lower() == "--assists":
                agentStats = sorted(agentStats, key= lambda x: x[5]/x[1], reverse=True)
                mapStats = sorted(mapStats, key= lambda x: x[5]/x[1], reverse=True)
            elif arg2.lower() == "--kd":
                agentStats = sorted(agentStats, key= lambda x: x[3]/x[4], reverse=True)
                mapStats = sorted(mapStats, key= lambda x: x[3]/x[4], reverse=True)
            elif arg2.lower() == "--kda":
                agentStats = sorted(agentStats, key= lambda x: (x[3]+x[5])/x[4], reverse=True)
                mapStats = sorted(mapStats, key= lambda x: (x[3]+x[5])/x[4], reverse=True)
            elif arg2.lower() == "--win%":
                agentStats = sorted(agentStats, key= lambda x: x[2]/x[1], reverse=True)
                mapStats = sorted(mapStats, key= lambda x: x[2]/x[1], reverse=True)

            kills = round((kills/playergames), 1)
            deaths = round((deaths/playergames), 1)
            assists = round((assists/playergames), 1)
            agent_stats_str = ""
            map_stats_str = ""
            for x in range(len(agentStats)):
                agent_stats_str += getCountry(agentStats[x][0]) + " **" + agentFullName(agentStats[x][0]).upper() + "**" + getCapsGap(agentStats[x][0]) + "KDA: **" + str("%.1f" % (round((agentStats[x][3]/agentStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((agentStats[x][4]/agentStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((agentStats[x][5]/agentStats[x][1]), 1))) + "**   |   K/D: **" + str("%.2f" % (round((agentStats[x][3]/agentStats[x][4]), 2))) + "**   |   Win%: **" + str("%.1f" % (round((agentStats[x][2]/agentStats[x][1]), 3)*100)) + "%**   |   Pick%: **" + str("%.1f" % (round((agentStats[x][1]/playergames), 3)*100)) + "%**   |   Games: **" + str(agentStats[x][1]) + "**\n"
            for x in range(len(mapStats)):
                map_stats_str += getCountry(mapStats[x][0]) + " **" + mapStats[x][0].upper() + "**" + getCapsGap(mapStats[x][0]) + "KDA: **" + str("%.1f" % (round((mapStats[x][3]/mapStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((mapStats[x][4]/mapStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((mapStats[x][5]/mapStats[x][1]), 1))) + "**   |   K/D: **" + str("%.2f" % (round((mapStats[x][3]/mapStats[x][4]), 2))) + "**   |   Win%: **" + str("%.1f" % (round((mapStats[x][2]/mapStats[x][1]), 3)*100)) + "%**   |   Play%: **" + str("%.1f" % (round((mapStats[x][1]/playergames), 3)*100)) + "%**   |   Games: **" + str(mapStats[x][1]) + "**\n"
            
            await ctx.send("**__" + players[player][0] + "__** aka. **" + playerfast[player] + "**\nKDA: **" + str(kills) + "** / **" + str(deaths) + "** / **" + str(assists) + "**   |   K/D: **" + str("%.2f" % (round((kills/deaths), 2))) + "**   |   Win%: **" + str("%.1f" % (round((playerwins/playergames), 3)*100)) + "%**   |   Games: **" + str(playergames) + "**\n\n" + agent_stats_str + ".")
            await ctx.send(map_stats_str)
        else:
            await ctx.send("This player doesn't exist.")

    else:
        playerStats = []
        for x in range(len(data)):
            if int(winrate[x][0]) > int(winrate[x][1]):  
                win = 1
            else:
                win = 0
            for y in range(len(players)):
                try:
                    if len(playerStats) == 0:
                        playerStats.append([players[y][0], 1, win, int(data[x][(y*4)+1]), int(data[x][(y*4)+2]), int(data[x][(y*4)+3])])
                    else:
                        playerNew = False
                        for z in range(len(playerStats)):
                            if playerStats[z][0] == players[y][0] and data[x][(y*4)] != "":
                                playerStats[z][1] += 1
                                playerStats[z][2] += win
                                playerStats[z][3] += int(data[x][(y*4)+1])
                                playerStats[z][4] += int(data[x][(y*4)+2])
                                playerStats[z][5] += int(data[x][(y*4)+3])
                                playerNew = False
                                break
                            else:
                                playerNew = True
                        if playerNew == True:
                            playerStats.append([players[y][0], 1, win, int(data[x][(y*4)+1]), int(data[x][(y*4)+2]), int(data[x][(y*4)+3])])
                except:
                    pass

        if arg1 == None:
            playerStats = sorted(playerStats, key=itemgetter(1), reverse=True)
        elif arg1.lower() == "--wins":
            playerStats = sorted(playerStats, key=itemgetter(2), reverse=True)
        elif arg1.lower() == "--kills":
            playerStats = sorted(playerStats, key= lambda x: x[3]/x[1], reverse=True)
        elif arg1.lower() == "--deaths":
            playerStats = sorted(playerStats, key= lambda x: x[4]/x[1], reverse=True)
        elif arg1.lower() == "--assists":
            playerStats = sorted(playerStats, key= lambda x: x[5]/x[1], reverse=True)
        elif arg1.lower() == "--kd":
            playerStats = sorted(playerStats, key= lambda x: x[3]/x[4], reverse=True)
        elif arg1.lower() == "--kda":
            playerStats = sorted(playerStats, key= lambda x: (x[3]+x[5])/x[4], reverse=True)
        elif arg1.lower() == "--win%":
            playerStats = sorted(playerStats, key= lambda x: x[2]/x[1], reverse=True)

        stats_str = ""
        for x in range(len(playerStats)):
            for y in range(len(players)):
                if playerStats[x][0] == players[y][0]:
                    playerIndex = y
                    break
            stats_str += "**" + playerStats[x][0] + int(playerwidth[playerIndex][0])*" " + "**   KDA: **" + str("%.1f" % (round((playerStats[x][3]/playerStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((playerStats[x][4]/playerStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((playerStats[x][5]/playerStats[x][1]), 1))) + "**   |   K/D: **" + str("%.2f" % (round((playerStats[x][3]/playerStats[x][4]), 2))) + "**   |   Win%: **" + str("%.1f" % (round((playerStats[x][2]/playerStats[x][1]),3)*100)) + "%**   |   Games: **" + str(playerStats[x][1]) + "**\n"
        await ctx.send(stats_str)

@client.command()
async def role(ctx):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return

@client.command()
async def rolecomb(ctx, arg1=None):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return
    players = sh.get_worksheet(0).get("C3:C12") # parse the names of the team members

    worksheet = sh.get_worksheet(1)
    data = worksheet.get("C2:AT")
    map = worksheet.get("B2:B")
    agentsCompStats = []
    allgames = 0
    passGame = False
    for x in range(len(data)):
        if arg1 == None:
            None
        else:
            if arg1.lower() != map[x][0].lower():
                passGame = True
                continue
            else:
                passGame = False
        if passGame == True:
            continue
        agentsComp = []
        allgames += 1
        duelist = 0
        initiator = 0
        controller = 0
        sentinel = 0
        if int(data[x][0]) > int(data[x][1]):
            win = 1
        else:
            win = 0
        for y in range(len(players)):
            try:
                if data[x][4+y*4] != "":
                    agentsComp.append(data[x][4+y*4])
            except:
                pass
        for y in range(len(agentsComp)):
            if getAgentRole(agentsComp[y]) == "D":
                duelist += 1
            elif getAgentRole(agentsComp[y]) == "I":
                initiator += 1
            elif getAgentRole(agentsComp[y]) == "C":
                controller += 1
            elif getAgentRole(agentsComp[y]) == "S":
                sentinel += 1
        if duelist+initiator+controller+sentinel != 5:
            allgames -= 1
            continue
        agentsCompSTR = str(duelist) + str(initiator) + str(controller) + str(sentinel)
        if len(agentsCompStats) == 0:
            agentsCompStats.append([agentsCompSTR, 1, win])
        else:
            agentFound = False
            for y in range(len(agentsCompStats)):
                if agentsCompSTR == agentsCompStats[y][0]:
                    agentsCompStats[y][1] += 1
                    agentsCompStats[y][2] += win
                    agentFound = True
                    break
                else:
                    agentFound = False
            if agentFound == False:
                agentsCompStats.append([agentsCompSTR, 1, win])

    agentsCompStats = sorted(agentsCompStats, key=itemgetter(1), reverse=True)
    stats_str = ""
    for x in range(len(agentsCompStats)):
        if x < 10:
            stats_str += "**" + agentsCompStats[x][0][0] + "x** Duelist | **" + agentsCompStats[x][0][1] + "x** Initiator | **" + agentsCompStats[x][0][2] + "x** Controller | **" + agentsCompStats[x][0][3] + "x** Sentinel   |   Win%: **" + str("%.1f" % (round((agentsCompStats[x][2]/agentsCompStats[x][1]), 3)*100)) + "%**   |   Games: **" + str(agentsCompStats[x][1]) + "**\n"
    await ctx.send(stats_str)

@client.command()
async def rounds(ctx, arg1=None):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return

    worksheet = sh.get_worksheet(1)
    data = worksheet.get("B2:F")

    roundStats = []
    

    for x in range(len(data)):
        attwins = 0
        attrounds = 0
        defwins = 0
        defrounds = 0
        for y in range(len(maps)):
            try:
                if data[x][0] == maps[y]:
                    if len(roundStats) == 0:
                        if len(data[x][4]) > 24:
                            value = [data[x][4][i:i+12] for i in range(0, len(data[x][4]), 12)]
                            for z in range(len(value[2])):
                                if data[x][3] == "A":
                                    try:
                                        if value[2][2*z] == "W":
                                            attwins += 1
                                            attrounds += 1
                                        else:
                                            attrounds += 1
                                    except:
                                        break
                                    try:
                                        if value[2][(2*z)+1] == "W":
                                            defwins += 1
                                            defrounds += 1
                                        else:
                                            defrounds += 1
                                    except:
                                        break
                                elif data[x][3] == "D":
                                    try:
                                        if value[2][2*z] == "W":
                                            defwins += 1
                                            defrounds += 1
                                        else:
                                            defrounds += 1
                                    except:
                                        break
                                    try:
                                        if value[2][(2*z)+1] == "W":
                                            attwins += 1
                                            attrounds += 1
                                        else:
                                            attrounds += 1
                                    except:
                                        break
                            if data[x][3] == "A":
                                roundStats.append([maps[y], len(value[0])+attrounds, value[0].count("W")+attwins, len(value[1])+defrounds, value[1].count("W")+defwins, 1])
                            elif data[x][3] == "D":
                                roundStats.append([maps[y], len(value[1])+attrounds, value[1].count("W")+attwins, len(value[0])+defrounds, value[0].count("W")+defwins, 1])
                        else:
                            value = [data[x][4][i:i+12] for i in range(0, len(data[x][4]), 12)]
                            if data[x][3] == "A":
                                print(type(str({})) + " | " + str({}) + "\n" + type(str({})) + " | " + str({}) + "\n" + type(str({})) + " | " + str({}) + "\n" + type(str({})) + " | " + str({}) + "\n", format(maps[y], len(value[0]), value[0].count("W"), len(value[1]), value[1].count("W")))
                                roundStats.append([maps[y], len(value[0]), value[0].count("W"), len(value[1]), value[1].count("W"), 1])
                            elif data[x][3] == "D":
                                roundStats.append([maps[y], len(value[1]), value[1].count("W"), len(value[0]), value[0].count("W"), 1])

                    else:
                        mapNew = False
                        for z in range(len(roundStats)):
                            if roundStats[z][0] == maps[y]:
                                if len(data[x][4]) > 24:
                                    value = [data[x][4][i:i+12] for i in range(0, len(data[x][4]), 12)]
                                    for xx in range(len(value[2])):
                                        if data[x][3] == "A":
                                            try:
                                                if value[2][2*xx] == "W":
                                                    attwins += 1
                                                    attrounds += 1
                                                else:
                                                    attrounds += 1
                                            except:
                                                break
                                            try:
                                                if value[2][(2*xx)+1] == "W":
                                                    defwins += 1
                                                    defrounds += 1
                                                else:
                                                    defrounds += 1
                                            except:
                                                break
                                        elif data[x][3] == "D":
                                            try:
                                                if value[2][2*xx] == "W":
                                                    defwins += 1
                                                    defrounds += 1
                                                else:
                                                    defrounds += 1
                                            except:
                                                break
                                            try:
                                                if value[2][(2*xx)+1] == "W":
                                                    attwins += 1
                                                    attrounds += 1
                                                else:
                                                    attrounds += 1
                                            except:
                                                break
                                else:
                                    value = [data[x][4][i:i+12] for i in range(0, len(data[x][4]), 12)]
                                roundStats[z][1] += len(value[0])+attrounds
                                roundStats[z][2] += value[0].count("W")+attwins
                                roundStats[z][3] += len(value[1])+defrounds
                                roundStats[z][4] += value[1].count("W")+defwins
                                roundStats[z][5] += 1
                                mapNew = False
                                break
                            else:
                                mapNew = True
                        if mapNew == True:
                            if len(data[x][4]) > 24:
                                value = [data[x][4][i:i+12] for i in range(0, len(data[x][4]), 12)]
                                for z in range(len(value[2])):
                                    if data[x][3] == "A":
                                        try:
                                            if value[2][2*z] == "W":
                                                attwins += 1
                                                attrounds += 1
                                            else:
                                                attrounds += 1
                                        except:
                                            break
                                        try:
                                            if value[2][(2*z)+1] == "W":
                                                defwins += 1
                                                defrounds += 1
                                            else:
                                                defrounds += 1
                                        except:
                                            break
                                    elif data[x][3] == "D":
                                        try:
                                            if value[2][2*z] == "W":
                                                defwins += 1
                                                defrounds += 1
                                            else:
                                                defrounds += 1
                                        except:
                                            break
                                        try:
                                            if value[2][(2*z)+1] == "W":
                                                attwins += 1
                                                attrounds += 1
                                            else:
                                                attrounds += 1
                                        except:
                                            break
                                if data[x][3] == "A":
                                    roundStats.append([maps[y], len(value[0])+attrounds, value[0].count("W")+attwins, len(value[1])+defrounds, value[1].count("W")+defwins, 1])
                                elif data[x][3] == "D":
                                    roundStats.append([maps[y], len(value[1])+attrounds, value[1].count("W")+attwins, len(value[0])+defrounds, value[0].count("W")+defwins, 1])
                            else:
                                value = [data[x][4][i:i+12] for i in range(0, len(data[x][4]), 12)]
                                if data[x][3] == "A":
                                    roundStats.append([maps[y], len(value[0]), value[0].count("W"), len(value[1]), value[1].count("W"), 1])
                                elif data[x][3] == "D":
                                    roundStats.append([maps[y], len(value[1]), value[1].count("W"), len(value[0]), value[0].count("W"), 1])
            except:
                pass
    if arg1 == None:
        roundStats = sorted(roundStats, key=itemgetter(5), reverse=True)
    elif arg1.lower() == "--attwin%":
        roundStats = sorted(roundStats, key= lambda x: x[2]/x[1], reverse=True)
    elif arg1.lower() == "--defwin%":
        roundStats = sorted(roundStats, key= lambda x: x[4]/x[3], reverse=True)

    stats_str = ""
    for x in range(len(roundStats)):
        stats_str += getCountry(roundStats[x][0]) + " **" + roundStats[x][0].upper() + "**" + getCapsGap(roundStats[x][0]) + "ATT Win%: **" + str("%.1f" % (round((roundStats[x][2]/roundStats[x][1]), 3)*100)) + "%**   |   DEF Win%: **" + str("%.1f" % (round((roundStats[x][4]/roundStats[x][3]), 3)*100)) + "%**   |   Games: **" + str(roundStats[x][5]) + "**\n"
    await ctx.send(stats_str)

@client.command()
async def verify(ctx):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return
    players = sh.get_worksheet(0).get("C3:C12") # parse the names of the team members

    info = sh.get_worksheet(0)

    worksheet = sh.get_worksheet(1)
    data = worksheet.get("C2:F")
    

    allFine = True
    wrongGames = []
    for x in range(len(data)):
        rw = data[x][3].count("W")
        rl = data[x][3].count("L")
        if rw != int(data[x][0]) or rl != int(data[x][1]):
            allFine = False
            wrongGames.append(x+2)
    if allFine == True:
        await ctx.send("All games are fine.")
    else:
        await ctx.send("These rows of games aren't correct: " + str(wrongGames))
    biggest_player_width = 0
    for x in range(len(players)):
        if getCustomWidth(players[x][0]) > biggest_player_width:
            biggest_player_width = getCustomWidth(players[x][0])
    for x in range(len(players)):
        info.update_cell(3+x, 4, ("%.0f" % (round((biggest_player_width-getCustomWidth(players[x][0])) / 3, 0))))
"""
@client.command()
async def voting(ctx):
    try:
        sh = gc.open_by_key(get_gsk(client, ctx))
        print(sh)
    except:
        await ctx.send("The Google Sheet Key is invalid. Be sure the sheet is shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.")
        return

    voting_msg = settings_str[19].replace("Voting command message: ", "").replace("\n", "").replace('"', "")
    voting_clock = settings_str[20].replace("Voting clock reactions: ", "").replace("\n", "").split(",")
    clocks = [["🕐", "clock1"], ["🕑", "clock2"], ["🕒", "clock3"], ["🕓", "clock4"], ["🕔", "clock5"], ["🕕", "clock6"], ["🕖", "clock7"], ["🕗", "clock8"], ["🕘", "clock9"], ["🕙", "clock10"], ["🕚", "clock11"], ["🕛", "clock12"], ["🕜", "clock130"], ["🕝", "clock230"], ["🕞", "clock330"], ["🕟", "clock430"], ["🕠", "clock530"], ["🕡", "clock630"], ["🕢", "clock730"], ["🕣", "clock830"], ["🕤", "clock930"], ["🕥", "clock1030"], ["🕦", "clock1130"], ["🕧", "clock1230"]]
    message = await ctx.send(voting_msg)
    emoji = ["✅", "❌"]
    for x in range(len(voting_clock)):
        for y in range(len(clocks)):
            if voting_clock[x] == clocks[y][1]:
                emoji.append(clocks[y][0])
    for x in  range(len(emoji)):
        await message.add_reaction(emoji[x])
"""
@client.command()
async def setup(ctx):
    developerID = get_developerID(client, ctx)
    prefix = get_prefix(client, ctx)
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == developerID:
        await ctx.send(":one: Make an copy of this Google Sheet Document: <https://docs.google.com/spreadsheets/d/1vpNyLf-vzPHh88zD2xacgQFGOTUvunAH3pKrY9RcR6Y/edit?usp=sharing>\n:two: Share this Google Sheet Document to this email address: **monkacode@valorantstats.iam.gserviceaccount.com**\n:three: Type in the URL of your copy or the key of the Document:")
        channel = ctx.channel
        author = ctx.author.id
        def check(m):
            return m.channel == channel and m.author.id == author
        msg = await client.wait_for("message", check=check)
        keyList = msg.content.split("/")
        if len(keyList) == 1:
            key = keyList[0]
        else:
            key = keyList[5]
        with open("gsk.json", "r") as f:
            gsk = json.load(f)
        try:
            sh = gc.open_by_key(key)
            print(sh)
            sh.get_worksheet(0).update_cell(1, 1, "")
        except:
            await ctx.send(f":x: The Google Sheet Document isn't shared to **monkacode@valorantstats.iam.gserviceaccount.com** with editor access.\nRun the **{prefix}setup** command again.")
            return
        gsk[str(ctx.guild.id)] = key
        with open("gsk.json", "w") as f:
            json.dump(gsk, f, indent=4)
        await ctx.send(f":white_check_mark: **{sh.title}** x **ValorantStats** connected successfully.\n:four: Type in the Discord User ID of this person who uses the bot to add new games and stuff liked that.")
        msg = await client.wait_for("message", check=check)
        with open("developerIDs.json", "r") as f:
            developerID = json.load(f)
        try:
            await client.fetch_user(int(msg.content))
        except:
            await ctx.send(f":x: **Can't set the developerID to:** {msg.content} -> **No valid user!**\nTry to change again the developerID with: **{prefix}setdeveloperID <id>**")
            return
        developerID[str(ctx.guild.id)] = msg.content
        with open("developerIDs.json", "w") as f:
            json.dump(developerID, f, indent=4)
        await ctx.send(f":white_check_mark: **Set the developerID to:** {msg.content} -> **User:** {await client.fetch_user(int(msg.content))}\n:checkered_flag: **__The setup was finished successfully!__** :checkered_flag:")
    else:
        try:
            if developerID != ctx.guild.owner_id:
                await ctx.send(f":warning: Ask **{await client.fetch_user(ctx.guild.owner_id)}** or **{await client.fetch_user(developerID)}** to set up the bot.")
        except:
            await ctx.send(f":warning: Ask **{await client.fetch_user(ctx.guild.owner_id)}** to set up the bot.")

@client.command()
async def help(ctx, arg1=None):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    if arg1 == "addgame":
        embedVar = discord.Embed(title=f"Help for {prefix}addgame command", description="More information for the addgame command.", color=0xFF0000)
        embedVar.add_field(name=f"{prefix}addgame <date> <map> <round-wins> <round-losses> <firstSide> <rounds> <player1> <player2> <player3> <player4> <player5>", value=f"Add a new played game.\n<date> -> The date of the game\n<map> -> The map on which the game was played on\n<round-wins> -> The ammount of rounds that your team wins\n<round-losses> -> The ammount of rounds that your team lose\n<firstSide> -> The Side on which your team started. Attacker (A) or Defender (D)\n<rounds> -> W for win and L for lose. Example (13-8): LWWWWWWLWWWLWWLWLLLLW\n<player1-5> -> Stats for players. Format: [name,agent,kills,deaths,assists] Example: [ScreaM,Sage,23,12,8] You can also use the abbreviation of the agents.", inline=False)
    elif arg1 == "player":
        embedVar = discord.Embed(title=f"Help for {prefix}player command", description="More information for the player command.", color=0xFF0000)
        embedVar.add_field(name=f"{prefix}player <sorting>", value="Show statistics for all player. For <sorting> you can use: --wins, --kills, --deaths, --assists, --kd, --kda, --win%. Without sorting it is sorted by played games.", inline=False)
        embedVar.add_field(name=f"{prefix}player <player> <sorting>", value="Show statistics for <player>. For <sorting> you can use: --wins, --kills, --deaths, --assists, --kd, --kda, --win%. Without sorting it is sorted by played games.", inline=False)
    elif arg1 == "map":
        embedVar = discord.Embed(title=f"Help for {prefix}map command", description="More information for the map command.", color=0xFF0000)
        embedVar.add_field(name=f"{prefix}map <sorting>", value=f"Show statistics for maps. For <sorting> you can use: --wins, --losses, --draws, --win%. Without sorting it is sorted by played games.", inline=False)
    elif arg1 == "rounds":
        embedVar = discord.Embed(title=f"Help for {prefix}rounds command", description="More information for the rounds command.", color=0xFF0000)
    elif arg1 == None:
        embedVar = discord.Embed(title="Help Command", description="Short description for all commands.", color=0xFF0000)
        embedVar.add_field(name=f"{prefix}changeprefix <prefix>", value="Changes the Bot Prefix to <prefix>", inline=False)
        embedVar.add_field(name=f"{prefix}setdeveloperID <id>", value="Set the developerID to the user with this Discord ID: <id> ", inline=False)
        embedVar.add_field(name=f"{prefix}showdeveloperID", value="Show the developerID and the user with this id.", inline=False)
        embedVar.add_field(name=f"{prefix}setkey <key>", value="Set the Key from the Google Sheet Document. <key> can be the key or the whole URL.", inline=False)
        embedVar.add_field(name=f"{prefix}showkey", value="Show the Key from the Google Sheet Document.", inline=False)
        embedVar.add_field(name=f"{prefix}verify", value="Verify all matches and improves the clarity.", inline=False)
        embedVar.add_field(name=f"{prefix}addgame", value=f"Add a new played game. More information with: **{prefix}help addgame**", inline=False)
        embedVar.add_field(name=f"{prefix}player", value=f"Show statistics for players. More information with: **{prefix}help player**", inline=False)
        embedVar.add_field(name=f"{prefix}map", value=f"Show statistics for maps. More information with: **{prefix}help map**", inline=False)
        embedVar.add_field(name=f"{prefix}rounds", value=f"Show statistics for rounds. More information with: **{prefix}help rounds**", inline=False)
        embedVar.add_field(name=f"{prefix}agent", value="Show statistics for all agents.", inline=False)
        embedVar.add_field(name=f"{prefix}game <id>", value="Show statistics for the played game with this ID: <id>. The id you can see on the row of the Google Sheet Document. Without the <id> attribute, the last played game get showed.", inline=False)
        embedVar.add_field(name=f"{prefix}rolecomb <map>", value="Show statistics for the combination of agents roles on this <map> Map. For all maps ignore <map>.", inline=False)
    await ctx.channel.send(embed=embedVar)

def getCountry(item):
    for x in range(len(agents)):
        if item.upper() == agents[x] or item.capitalize() == agents_full[x]:
            return agentFlag[x]
    for x in range(len(maps)):
        if item.capitalize() == maps[x]:
            return mapFlag[x]

def agentFullName(agent):
    for x in range(len(agents)):
        if agent.upper() == agents[x]:
            return agents_full[x]
    
def agentShortName(agent):
    for x in range(len(agents)):
        if agent.upper() == agents[x] or agent.capitalize() == agents_full[x]:
            return agents[x]

def getCapsGap(item):
    if item.upper() == "PX" or item.capitalize() == "Phoenix" or item.lower() == "bind":
        return "         "
    elif item.upper() == "JT" or item.capitalize() == "Jett":
        return "                  "
    elif item.upper() == "SA" or item.capitalize() == "Sage" or item.upper() == "RZ" or item.capitalize() == "Raze" or item.upper() == "SK" or item.capitalize() == "Skye":
        return "                 "
    elif item.upper() == "SV" or item.capitalize() == "Sova" or item.upper() == "VI" or item.capitalize() == "Viper" or item.upper() == "YO" or item.capitalize() == "Yoru":
        return "                "
    elif item.upper() == "BS" or item.capitalize() == "Brimstone" or item.lower() == "ascent":
        return "   "
    elif item.upper() == "OM" or item.capitalize() == "Omen":
        return "               "
    elif item.upper() == "BR" or item.capitalize() == "Breach" or item.upper() == "CY" or item.capitalize() == "Cypher" or item.upper() == "KJ" or item.capitalize() == "Killjoy":
        return "           "
    elif item.upper() == "RY" or item.capitalize() == "Reyna":
        return "             "
    elif item.upper() == "AS" or item.capitalize() == "Astra":
        return "              "
    elif item.lower() == "haven" or item.lower() == "icebox" or item.lower() == "breeze":
        return "    "
    elif item.lower() == "split":
        return "        "

def getCustomWidth(item):

    width = 0
    widthletter = [[3, "l", " "], [4, "i", "I", "j"], [5, "r"], [6, "f", "J", "s", "t", "1"], [7, "c", "e", "L", "z", "ä"], [8, "a", "b", "B", "d", "E", "F", "h", "k", "n", "o", "p", "q", "S", "u", "v", "x", "y", "ö", "ü", "2", "3", "5", "6", "7", "9"], [9, "C", "g", "K", "P", "R", "Z", "4", "8", "0", "ß"], [10, "D", "G", "H", "N", "T", "U", "V", "X"], [11, "A", "O", "Q", "w", "Y", "Ä", "Ö", "Ü"], [12, "m"], [13, "M"], [15, "W"]]

    for x in range(len(item)):
        for y in range(len(widthletter)):
            for z in range(len(widthletter[y])):
                try:
                    if item[x] == widthletter[y][z+1]:
                        width += widthletter[y][0]
                except:
                    pass
    return width

def getAgentRole(agent):
    for x in range(len(agents)):
        if agent.upper() == agents[x] or agent.capitalize() == agents_full[x]:
            return agents_role[x]


keep_alive()
#run the bot
client.run(token)
