import discord # install with: pip install discord.py
from discord.ext import commands # to use the commands from discord.ext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from operator import itemgetter

settings = open(r"settings.txt", "r")
settings_str = settings.readlines()
gsk = settings_str[15].replace("Google Sheets Key: ", "")

gc = gspread.service_account(filename=r"credentials.json")
sh = gc.open_by_key(gsk)

players = sh.get_worksheet(0).get("C3:C12") # parse the names of the team members
playerfast = [settings_str[4].replace("Player 1: ", "").replace("\n", ""), settings_str[5].replace("Player 2: ", "").replace("\n", ""), settings_str[6].replace("Player 3: ", "").replace("\n", ""), settings_str[7].replace("Player 4: ", "").replace("\n", ""), settings_str[8].replace("Player 5: ", "").replace("\n", ""), settings_str[9].replace("Player 6: ", "").replace("\n", ""), settings_str[10].replace("Player 7: ", "").replace("\n", ""), settings_str[11].replace("Player 8: ", "").replace("\n", ""), settings_str[12].replace("Player 9: ", "").replace("\n", ""), settings_str[13].replace("Player 10: ", "").replace("\n", "")] # alias of each team member, be sure that the index of every item fits to their position in Google Sheets

agents = ["PX", "JT", "SA", "SV", "BS", "OM", "BR", "CY", "VI", "RZ", "RY", "KJ", "SK", "YO", "AS"] # contractions of all agents
agents_full = ["Phoenix", "Jett", "Sage", "Sova", "Brimstone", "Omen", "Breach", "Cypher", "Viper", "Raze", "Reyna", "Killjoy", "Skye", "Yoru", "Astra"]

maps = ["Bind", "Haven", "Split", "Ascent", "Icebox", "Breeze"]

developerID = int(settings_str[0].replace("DeveloperID: ", "")) # discrod ID of the developer
assistantID = int(settings_str[1].replace("AssistantID: ", "")) # discord ID of the person who can also add games

# set a bot prefix
client = commands.Bot(command_prefix='?', help_command=None)

# import the token from a extern file for security
tokenTxt = open(r"token.txt", "r")
if tokenTxt.mode == "r":
    token = tokenTxt.read()

# bot is online
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("VALORANT"))
    print('We have logged in as {0.user}'.format(client))

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
        await ctx.send("Something went wrong, <@" + str(developerID) + ">.") # mentioned the developer in discord if something go wrong
        print(error)

@client.command()
async def game(ctx, arg1=None):

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
            player_stats_str += getCountry(playerStats[y][1]) + " **" + playerStats[y][0] + "**   Agent: **" + agentFullName(playerStats[y][1]) + "**   |   KDA: **" + str(playerStats[y][2]) + "** / **" + str(playerStats[y][3]) + "** / **" + str(playerStats[y][4]) + "**\n"
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
                    player_stats_str += getCountry(playerStats[y][1]) + " **" + playerStats[y][0] + "**   Agent: **" + agentFullName(playerStats[y][1]) + "**   |   KDA: **" + str(playerStats[y][2]) + "** / **" + str(playerStats[y][3]) + "** / **" + str(playerStats[y][4]) + "**\n"
                for y in range(len(desc_round_list)):
                    desc_round_str += " " + desc_round_list[y]
                await ctx.send("[**" + str(arg1) + "**] Date: **" + str(data[x][0]) + "**   |   Map: **" + data[x][1] + "**\nResult: **" + str(data[x][2]) + "** - **" + str(data[x][3]) + "**\n\n" + desc_round_str + "\n" + your_round_str + "\n" + enemy_round_str + "\n.")
                await ctx.send(player_stats_str)
        

@client.command()
async def map(ctx, arg1=None, arg2=None):
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
    worksheet = sh.get_worksheet(1)
    data = worksheet.get("G2:AT")
    winrate = worksheet.get("C2:D")
    playedmap = worksheet.get("B2:B")

    
    for x in range(len(players)):
        #print(str(type(arg1.lower())) + ": " + str(arg1.lower()) + "  |  " + str(type(players[x][0].lower())) + ": " + str(players[x][0].lower()))
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
        elif arg1.lower() == "-win%":
            playerStats = sorted(playerStats, key= lambda x: x[2]/x[1], reverse=True)

        stats_str = ""
        for x in range(len(playerStats)):
            stats_str += "**" + playerStats[x][0] + "**   KDA: **" + str("%.1f" % (round((playerStats[x][3]/playerStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((playerStats[x][4]/playerStats[x][1]), 1))) + "** / **" + str("%.1f" % (round((playerStats[x][5]/playerStats[x][1]), 1))) + "**   |   K/D: **" + str("%.2f" % (round((playerStats[x][3]/playerStats[x][4]), 2))) + "**   |   Win%: **" + str("%.1f" % (round((playerStats[x][2]/playerStats[x][1]),3)*100)) + "%**   |   Games: **" + str(playerStats[x][1]) + "**\n"
        await ctx.send(stats_str)

@client.command()
async def rounds(ctx, arg1=None):
    worksheet = sh.get_worksheet(1)
    data = worksheet.get("B2:F")

    roundStats = []
    

    for x in range(len(data)):
        attwins = 0
        attrounds = 0
        defwins = 0
        defrounds = 0
        for y in range(len(maps)):
            #try:
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
            #except:
                #pass
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

@client.command()
async def voting(ctx):
    message = await ctx.send("@everyone Könnt ihr heute oder nicht, und wenn ja wann, bitte reagieren:\n:white_check_mark: Ich bin da\n:x: Ich bin nicht da\n\n:clock7: 19.00 Uhr\n:clock730: 19.30 Uhr\n:clock8: 20.00 Uhr\n:clock830: 20.30 Uhr\n:clock9: 21.00 Uhr")
    emoji = ["✅", "❌", "🕖", "🕢", "🕗", "🕣", "🕘"]
    for x in  range(len(emoji)):
        await message.add_reaction(emoji[x])

def getCountry(agent):
    if agent.upper() == "PX" or agent.capitalize() == "Phoenix":
        return ":flag_gb:"
    elif agent.upper() == "JT" or agent.capitalize() == "Jett":
        return ":flag_kr:"
    elif agent.upper() == "SA" or agent.capitalize() == "Sage":
        return ":flag_cn:"
    elif agent.upper() == "SV" or agent.capitalize() == "Sova":
        return ":flag_ru:"
    elif agent.upper() == "BS" or agent.capitalize() == "Brimstone":
        return ":flag_us:"
    elif agent.upper() == "OM" or agent.capitalize() == "Omen":
        return ":grey_question:"
    elif agent.upper() == "BR" or agent.capitalize() == "Breach":
        return ":flag_se:"
    elif agent.upper() == "CY" or agent.capitalize() == "Cypher":
        return ":flag_ma:"
    elif agent.upper() == "VI" or agent.capitalize() == "Viper":
        return ":flag_us:"
    elif agent.upper() == "RZ" or agent.capitalize() == "Raze":
        return ":flag_br:"
    elif agent.upper() == "RY" or agent.capitalize() == "Reyna":
        return ":flag_mx:"
    elif agent.upper() == "KJ" or agent.capitalize() == "Killjoy":
        return ":flag_de:"
    elif agent.upper() == "SK" or agent.capitalize() == "Skye":
        return ":flag_au:"
    elif agent.upper() == "YO" or agent.capitalize() == "Yoru":
        return ":flag_jp:"
    elif agent.upper() == "AS" or agent.capitalize() == "Astra":
        return ":flag_gh:"
    elif agent.lower() == "bind":
        return ":flag_ma:"
    elif agent.lower() == "haven":
        return ":flag_bt:"
    elif agent.lower() == "split":
        return ":flag_jp:"
    elif agent.lower() == "ascent":
        return ":flag_it:"
    elif agent.lower() == "icebox":
        return ":flag_ru:"
    elif agent.lower() == "breeze":
        return ":flag_tt:"

def agentFullName(agent):
    if agent.upper() == "PX":
        return "Phoenix"
    elif agent.upper() == "JT":
        return "Jett"
    elif agent.upper() == "SA":
        return "Sage"
    elif agent.upper() == "SV":
        return "Sova"
    elif agent.upper() == "BS":
        return "Brimstone"
    elif agent.upper() == "OM":
        return "Omen"
    elif agent.upper() == "BR":
        return "Breach"
    elif agent.upper() == "CY":
        return "Cypher"
    elif agent.upper() == "VI":
        return "Viper"
    elif agent.upper() == "RZ":
        return "Raze"
    elif agent.upper() == "RY":
        return "Reyna"
    elif agent.upper() == "KJ":
        return "Killjoy"
    elif agent.upper() == "SK":
        return "skye"
    elif agent.upper() == "YO":
        return "Yoru"
    elif agent.upper() == "AS":
        return "Astra"
    
def getCapsGap(agent):
    if agent.upper() == "PX" or agent.capitalize() == "Phoenix":
        return "         "
    elif agent.upper() == "JT" or agent.capitalize() == "Jett":
        return "                  "
    elif agent.upper() == "SA" or agent.capitalize() == "Sage":
        return "                 "
    elif agent.upper() == "SV" or agent.capitalize() == "Sova":
        return "                "
    elif agent.upper() == "BS" or agent.capitalize() == "Brimstone":
        return "   "
    elif agent.upper() == "OM" or agent.capitalize() == "Omen":
        return "               "
    elif agent.upper() == "BR" or agent.capitalize() == "Breach":
        return "           "
    elif agent.upper() == "CY" or agent.capitalize() == "Cypher":
        return "           "
    elif agent.upper() == "VI" or agent.capitalize() == "Viper":
        return "                "
    elif agent.upper() == "RZ" or agent.capitalize() == "Raze":
        return "                 "
    elif agent.upper() == "RY" or agent.capitalize() == "Reyna":
        return "             "
    elif agent.upper() == "KJ" or agent.capitalize() == "Killjoy":
        return "           "
    elif agent.upper() == "SK" or agent.capitalize() == "Skye":
        return "                 "
    elif agent.upper() == "YO" or agent.capitalize() == "Yoru":
        return "                "
    elif agent.upper() == "AS" or agent.capitalize() == "Astra":
        return "              "
    elif agent.lower() == "bind":
        return "         "
    elif agent.lower() == "haven":
        return "    "
    elif agent.lower() == "split":
        return "        "
    elif agent.lower() == "ascent":
        return "   "
    elif agent.lower() == "icebox":
        return "    "
    elif agent.lower() == "breeze":
        return "    "

client.run(token)