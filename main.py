import discord # install with: pip install discord.py
from discord.ext import commands # to use the commands from discord.ext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from keep_alive import keep_alive

settings = open(r"settings.txt", "r")
settings_str = settings.readlines()

# The ID and range of a sample spreadsheet.
gc = gspread.service_account(filename=r"credentials.json")
gsk = settings_str[15].replace("Google Sheets Key: ", "")
sh = gc.open_by_key(gsk) # key of the Google Sheet

players = sh.get_worksheet(0).get("C3:C12") # parse the names of the team members

# general information
playerfast = [settings_str[4].replace("Player 1: ", ""), settings_str[5].replace("Player 2: ", ""), settings_str[6].replace("Player 3: ", ""), settings_str[7].replace("Player 4: ", ""), settings_str[8].replace("Player 5: ", ""), settings_str[9].replace("Player 6: ", ""), settings_str[10].replace("Player 7: ", ""), settings_str[11].replace("Player 8: ", ""), settings_str[12].replace("Player 9: ", ""), settings_str[13].replace("Player 10: ", "")] # alias of each team member, be sure that the index of every item fits to their position in Google Sheets
agents = ["PX", "JT", "SA", "SV", "BS", "OM", "BR", "CY", "VI", "RZ", "RY", "KJ", "SK", "YO", "AS"] # contractions of all agents
agents_full = ["Phoenix", "Jett", "Sage", "Sova", "Brimstone", "Omen", "Breach", "Cypher", "Viper", "Raze", "Reyna", "Killjoy", "Skye", "Yoru", "Astra"]

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

# command for all map specific information
@client.command()
async def map(ctx, arg1=None):

    # setting some basic variables
    worksheet = sh.get_worksheet(2)
    worksheetstats = sh.get_worksheet(3)
    bindGamesList = worksheet.col_values(2) # default information for map Bind
    bindGames = 0
    bindWins = 0
    bindLosses = 0
    bindDraws = 0
    havenGamesList = worksheet.col_values(3) # default information for map Haven
    havenGames = 0
    havenWins = 0
    havenLosses = 0
    havenDraws = 0
    splitGamesList = worksheet.col_values(4) # default information for map Split
    splitGames = 0
    splitWins = 0
    splitLosses = 0
    splitDraws = 0
    ascentGamesList = worksheet.col_values(5) # default information for map Ascent
    ascentGames = 0
    ascentWins = 0
    ascentLosses = 0
    ascentDraws = 0
    iceboxGamesList = worksheet.col_values(6) # default information for map Icebox
    iceboxGames = 0
    iceboxWins = 0
    iceboxLosses = 0
    iceboxDraws = 0
    breezeGamesList = worksheet.col_values(7) # default information for map Breeze
    breezeGames = 0
    breezeWins = 0
    breezeLosses = 0
    breezeDraws = 0

    if arg1 == None: # when to user want to see the basic informations of all maps
        x = 1
        while x < len(bindGamesList):
            if bindGamesList[x] != "": # checking each game if it has a result in the Bind column
                bindGames += 1
                if int(bindGamesList[x]) > 0: # bindGamesList[x] is the difference between round wins and losses
                    bindWins += 1
                elif int(bindGamesList[x]) < 0:
                    bindLosses += 1
                else:
                    bindDraws += 1
            x += 1
        x = 1
        while x < len(havenGamesList):
            if havenGamesList[x] != "": # checking each game if it has a result in the Haven column
                havenGames += 1
                if int(havenGamesList[x]) > 0: # havenGamesList[x] is the difference between round wins and losses
                    havenWins += 1
                elif int(havenGamesList[x]) < 0:
                    havenLosses += 1
                else:
                    havenDraws += 1
            x += 1
        x = 1
        while x < len(splitGamesList):
            if splitGamesList[x] != "": # checking each game if it has a result in the Split column
                splitGames += 1
                if int(splitGamesList[x]) > 0: # splitGamesList[x] is the difference between round wins and losses
                    splitWins += 1
                elif int(splitGamesList[x]) < 0:
                    splitLosses += 1
                else:
                    splitDraws += 1
            x += 1
        x = 1
        while x < len(ascentGamesList):
            if ascentGamesList[x] != "": # checking each game if it has a result in the Ascent column
                ascentGames += 1
                if int(ascentGamesList[x]) > 0: # ascentGamesList[x] is the difference between round wins and losses
                    ascentWins += 1
                elif int(ascentGamesList[x]) < 0:
                    ascentLosses += 1
                else:
                    ascentDraws += 1
            x += 1
        x = 1
        while x < len(iceboxGamesList):
            if iceboxGamesList[x] != "": # checking each game if it has a result in the Icebox column
                iceboxGames += 1
                if int(iceboxGamesList[x]) > 0: # iceboxGamesList[x] is the difference between round wins and losses
                    iceboxWins += 1
                elif int(iceboxGamesList[x]) < 0:
                    iceboxLosses += 1
                else:
                    iceboxDraws += 1
            x += 1
        x = 1
        while x < len(breezeGamesList):
            if breezeGamesList[x] != "": # checking each game if it has a result in the Breeze column
                breezeGames += 1
                if int(breezeGamesList[x]) > 0: # breezeGamesList[x] is the difference between round wins and losses
                    breezeWins += 1
                elif int(breezeGamesList[x]) < 0:
                    breezeLosses += 1
                else:
                    breezeDraws += 1
            x += 1

        # calculating the winrate of all maps
        try:
            bindWinrate = '%.1f' % (round((bindWins/bindGames), 3)*100)
        except:
            bindWinrate = 0
        try:
            havenWinrate = '%.1f' % (round((havenWins/havenGames), 3)*100)
        except:
            havenWinrate = 0
        try:
            splitWinrate = '%.1f' % (round((splitWins/splitGames), 3)*100)
        except:
            splitWinrate = 0
        try:
            ascentWinrate = '%.1f' % (round((ascentWins/ascentGames), 3)*100)
        except:
            ascentWinrate = 0
        try:
            iceboxWinrate = '%.1f' % (round((iceboxWins/iceboxGames), 3)*100)
        except:
            iceboxWinrate = 0
        try:
            breezeWinrate = '%.1f' % (round((breezeWins/breezeGames), 3)*100)
        except:
            breezeWinrate = 0
        
        # calculating the overall statistics
        try:
            totalWins = bindWins + havenWins + splitWins + ascentWins + iceboxWins + breezeWins
            totalLosses = bindLosses + havenLosses + splitLosses + ascentLosses + iceboxLosses + breezeLosses
            totalDraws = bindDraws + havenDraws + splitDraws + ascentDraws + iceboxDraws + breezeDraws
            totalGames = totalWins + totalLosses + totalDraws
            totalWinrate = '%.1f' % (round((totalWins/totalGames), 3)*100)
        except:
            totalWins = 0
            totalLosses = 0
            totalDraws = 0
            totalGames = 0
            totalWinrate = 0

        # sending the final message in discord
        await ctx.send("Win%: **" + str(totalWinrate) + "%**   |   Wins: **" + str(totalWins) + "**   |   Losses: **" + str(totalLosses) + "**   |   Draws: **" + str(totalDraws) + "**   |   Games: **" + str(totalGames) + "**\n\n:flag_ma: **BIND**         Win%: **" + str(bindWinrate) + "%**   |   Wins: **" + str(bindWins) + "**   |   Losses: **" + str(bindLosses) + "**   |   Draws: **" + str(bindDraws) + "**   |   Games: **" + str(bindGames) + "**\n:flag_bt: **HAVEN**    Win%: **" + str(havenWinrate) + "%**   |   Wins: **" + str(havenWins) + "**   |   Losses: **" + str(havenLosses) + "**   |   Draws: **" + str(havenDraws) + "**   |   Games: **" + str(havenGames) + "**\n:flag_jp: **SPLIT**        Win%: **" + str(splitWinrate) + "%**   |   Wins: **" + str(splitWins) + "**   |   Losses: **" + str(splitLosses) + "**   |   Draws: **" + str(splitDraws) + "**   |   Games: **" + str(splitGames) + "**\n:flag_it: **ASCENT**   Win%: **" + str(ascentWinrate) + "%**   |   Wins: **" + str(ascentWins) + "**   |   Losses: **" + str(ascentLosses) + "**   |   Draws: **" + str(ascentDraws) + "**   |   Games: **" + str(ascentGames) + "**\n:flag_ru: **ICEBOX**    Win%: **" + str(iceboxWinrate) + "%**   |   Wins: **" + str(iceboxWins) + "**   |   Losses: **" + str(iceboxLosses) + "**   |   Draws: **" + str(iceboxDraws) + "**   |   Games: **" + str(iceboxGames) + "**\n:flag_tt: **BREEZE**    Win%: **" + str(breezeWinrate) + "%**   |   Wins: **" + str(breezeWins) + "**   |   Losses: **" + str(breezeLosses) + "**   |   Draws: **" + str(breezeDraws) + "**   |   Games: **" + str(breezeGames) + "**")

    elif arg1.lower() == "bind": # only information of the map Bind
        x = 1
        while x < len(bindGamesList):
            if bindGamesList[x] != "": # checking each game if it has a result in the Bind column
                bindGames += 1
                if int(bindGamesList[x]) > 0: # bindGamesList[x] is the difference between round wins and losses
                    bindWins += 1
                elif int(bindGamesList[x]) < 0:
                    bindLosses += 1
                else:
                    bindDraws += 1
            x += 1
        try:
            bindWinrate = '%.1f' % (round((bindWins/bindGames), 3)*100) # calculating the winrate of the map Bind
        except:
            bindWinrate = 0
        p = worksheetstats.get("Y2:AC11") # parse the player statistics
        playerstats = ""

        for x in range(10): # get the information of each player
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + p[x][0] + "** / **" + p[x][1] + "** / **" + p[x][2] + "**   |   K/D: **" + p[x][3] + "**   |   Win%: **" + p[x][4] + "**\n" # create a string to store all the player statistics
            except:
                pass

        # sending the final message in discord
        await ctx.send(":flag_ma: **__BIND__\nWin%:** " + str(bindWinrate) + "% (**W: **" + str(bindWins) + " | **L: **" + str(bindLosses) + " | **D: **" + str(bindDraws) + " | **[**" + str(bindGames) + "**]**)\n\n" + playerstats) 
    
    elif arg1.lower() == "haven": # only information of the map Haven
        x = 1
        while x < len(havenGamesList):
            if havenGamesList[x] != "": # checking each game if it has a result in the Haven column
                havenGames += 1
                if int(havenGamesList[x]) > 0: # havenGamesList[x] is the difference between round wins and losses
                    havenWins += 1
                elif int(havenGamesList[x]) < 0:
                    havenLosses += 1
                else:
                    havenDraws += 1
            x += 1
        try:
            havenWinrate = '%.1f' % (round((havenWins/havenGames), 3)*100) # calculating the winrate of the map Haven
        except:
            havenWinrate = 0
        p = worksheetstats.get("Y14:AC23") # parse the player statistics
        playerstats = ""

        for x in range(10): # get the information of each player
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + p[x][0] + "** / **" + p[x][1] + "** / **" + p[x][2] + "**   |   K/D: **" + p[x][3] + "**   |   Win%: **" + p[x][4] + "**\n"
            except:
                pass

        # sending the final message in discord
        await ctx.send(":flag_bt: **__Haven__\nWin%:** " + str(havenWinrate) + "% (**W: **" + str(havenWins) + " | **L: **" + str(havenLosses) + " | **D: **" + str(havenDraws) + " | **[**" + str(havenGames) + "**]**)\n\n" + playerstats)

    elif arg1.lower() == "split": # only information of the map Split
        x = 1
        while x < len(splitGamesList):
            if splitGamesList[x] != "": # checking each game if it has a result in the Split column
                splitGames += 1
                if int(splitGamesList[x]) > 0: # splitGamesList[x] is the difference between round wins and losses
                    splitWins += 1
                elif int(splitGamesList[x]) < 0:
                    splitLosses += 1
                else:
                    splitDraws += 1
            x += 1
        try:
            splitWinrate = '%.1f' % (round((splitWins/splitGames), 3)*100) # calculating the winrate of the map Split
        except:
            splitWinrate = 0
        p = worksheetstats.get("Y26:AC35") # parse the player statistics
        playerstats = ""

        for x in range(10): # get the information of each player
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + p[x][0] + "** / **" + p[x][1] + "** / **" + p[x][2] + "**   |   K/D: **" + p[x][3] + "**   |   Win%: **" + p[x][4] + "**\n"
            except:
                pass

        # sending the final message in discord
        await ctx.send(":flag_jp: **__Split__\nWin%:** " + str(splitWinrate) + "% (**W: **" + str(splitWins) + " | **L: **" + str(splitLosses) + " | **D: **" + str(splitDraws) + " | **[**" + str(splitGames) + "**]**)\n\n" + playerstats)

    elif arg1.lower() == "ascent": # only information of the map Ascent
        x = 1
        while x < len(ascentGamesList):
            if ascentGamesList[x] != "": # checking each game if it has a result in the Ascent column
                ascentGames += 1
                if int(ascentGamesList[x]) > 0: # ascentGamesList[x] is the difference between round wins and losses
                    ascentWins += 1
                elif int(ascentGamesList[x]) < 0:
                    ascentLosses += 1
                else:
                    ascentDraws += 1
            x += 1
        try:
            ascentWinrate = '%.1f' % (round((ascentWins/ascentGames), 3)*100) # calculating the winrate of the map Ascent
        except:
            ascentWinrate = 0
        p = worksheetstats.get("Y38:AC47") # parse the player statistics
        playerstats = ""

        for x in range(10): # get the information of each player
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + p[x][0] + "** / **" + p[x][1] + "** / **" + p[x][2] + "**   |   K/D: **" + p[x][3] + "**   |   Win%: **" + p[x][4] + "**\n"
            except:
                pass

        # sending the final message in discord
        await ctx.send(":flag_it: **__Ascent__\nWin%:** " + str(ascentWinrate) + "% (**W: **" + str(ascentWins) + " | **L: **" + str(ascentLosses) + " | **D: **" + str(ascentDraws) + " | **[**" + str(ascentGames) + "**]**)\n\n" + playerstats)

    elif arg1.lower() == "icebox": # only information of the map Icebox
        x = 1
        while x < len(iceboxGamesList):
            if iceboxGamesList[x] != "": # checking each game if it has a result in the Icebox column
                iceboxGames += 1
                if int(iceboxGamesList[x]) > 0: # iceboxGamesList[x] is the difference between round wins and losses
                    iceboxWins += 1
                elif int(iceboxGamesList[x]) < 0:
                    iceboxLosses += 1
                else:
                    iceboxDraws += 1
            x += 1
        try:
            iceboxWinrate = '%.1f' % (round((iceboxWins/iceboxGames), 3)*100) # calculating the winrate of the map Icebox
        except:
            iceboxWinrate = 0
        p = worksheetstats.get("Y50:AC59") # parse the player statistics
        playerstats = ""

        for x in range(10): # get the information of each player
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + p[x][0] + "** / **" + p[x][1] + "** / **" + p[x][2] + "**   |   K/D: **" + p[x][3] + "**   |   Win%: **" + p[x][4] + "**\n"
            except:
                pass

        # sending the final message in discord
        await ctx.send(":flag_ru: **__Icebox__\nWin%:** " + str(iceboxWinrate) + "% (**W: **" + str(iceboxWins) + " | **L: **" + str(iceboxLosses) + " | **D: **" + str(iceboxDraws) + " | **[**" + str(iceboxGames) + "**]**)\n\n" + playerstats)

    elif arg1.lower() == "breeze": # only information of the map Breeze
        x = 1
        while x < len(breezeGamesList):
            if breezeGamesList[x] != "": # checking each game if it has a result in the Breeze column
                breezeGames += 1
                if int(breezeGamesList[x]) > 0: # breezeGamesList[x] is the difference between round wins and losses
                    breezeWins += 1
                elif int(breezeGamesList[x]) < 0:
                    breezeLosses += 1
                else:
                    breezeDraws += 1
            x += 1
        try:
            breezeWinrate = '%.1f' % (round((breezeWins/breezeGames), 3)*100) # calculating the winrate of the map Breeze
        except:
            breezeWinrate = 0
        p = worksheetstats.get("Y62:AC71") # parse the player statistics
        playerstats = ""

        for x in range(10): # get the information of each player
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + p[x][0] + "** / **" + p[x][1] + "** / **" + p[x][2] + "**   |   K/D: **" + p[x][3] + "**   |   Win%: **" + p[x][4] + "**\n"
            except:
                pass
        
        # sending the final message in discord
        await ctx.send(":flag_tt: **__Breeze__\nWin%:** " + str(breezeWinrate) + "% (**W: **" + str(breezeWins) + " | **L: **" + str(breezeLosses) + " | **D: **" + str(breezeDraws) + " | **[**" + str(breezeGames) + "**]**)\n\n" + playerstats)

# command for all round specific information
@client.command()
async def rounds(ctx):
    worksheet = sh.get_worksheet(4)
    data = worksheet.get("AW2:BB")

    bindGames = 0
    havenGames = 0
    splitGames = 0
    ascentGames = 0
    iceboxGames = 0
    breezeGames = 0

    bindARounds = 0
    bindDRounds = 0
    havenARounds = 0
    havenDRounds = 0
    splitARounds = 0
    splitDRounds = 0
    ascentARounds = 0
    ascentDRounds = 0
    iceboxARounds = 0
    iceboxDRounds = 0
    breezeARounds = 0
    breezeDRounds = 0

    bindAWins = 0
    bindDWins = 0
    havenAWins = 0
    havenDWins = 0
    splitAWins = 0
    splitDWins = 0
    ascentAWins = 0
    ascentDWins = 0
    iceboxAWins = 0
    iceboxDWins = 0
    breezeAWins = 0
    breezeDWins = 0

    x = 0
    while x < len(data):
        try:
            if data[x][3] == "Bind": # checking if the game was played on Bind
                bindGames += 1
                if data[x][2] == "D":
                    bindDWins += int(data[x][0])
                    bindAWins += int(data[x][1])
                    bindDRounds += int(data[x][0]) + int(data[x][4])
                    bindARounds += int(data[x][1]) + int(data[x][5])
                elif data[x][2] == "A":
                    bindAWins += int(data[x][0])
                    bindDWins += int(data[x][1])
                    bindARounds += int(data[x][0]) + int(data[x][4])
                    bindDRounds += int(data[x][1]) + int(data[x][5])
            if data[x][3] == "Haven": # checking if the game was played on Haven
                havenGames += 1
                if data[x][2] == "D":
                    havenDWins += int(data[x][0])
                    havenAWins += int(data[x][1])
                    havenDRounds += int(data[x][0]) + int(data[x][4])
                    havenARounds += int(data[x][1]) + int(data[x][5])
                elif data[x][2] == "A":
                    havenAWins += int(data[x][0])
                    havenDWins += int(data[x][1])
                    havenARounds += int(data[x][0]) + int(data[x][4])
                    havenDRounds += int(data[x][1]) + int(data[x][5])
            if data[x][3] == "Split": # checking if the game was played on Split
                splitGames += 1
                if data[x][2] == "D":
                    splitDWins += int(data[x][0])
                    splitAWins += int(data[x][1])
                    splitDRounds += int(data[x][0]) + int(data[x][4])
                    splitARounds += int(data[x][1]) + int(data[x][5])
                elif data[x][2] == "A":
                    splitAWins += int(data[x][0])
                    splitDWins += int(data[x][1])
                    splitARounds += int(data[x][0]) + int(data[x][4])
                    splitDRounds += int(data[x][1]) + int(data[x][5])
            if data[x][3] == "Ascent": # checking if the game was played on Ascent
                ascentGames += 1
                if data[x][2] == "D":
                    ascentDWins += int(data[x][0])
                    ascentAWins += int(data[x][1])
                    ascentDRounds += int(data[x][0]) + int(data[x][4])
                    ascentARounds += int(data[x][1]) + int(data[x][5])
                elif data[x][2] == "A":
                    ascentAWins += int(data[x][0])
                    ascentDWins += int(data[x][1])
                    ascentARounds += int(data[x][0]) + int(data[x][4])
                    ascentDRounds += int(data[x][1]) + int(data[x][5])
            if data[x][3] == "Icebox": # checking if the game was played on Icebox
                iceboxGames += 1
                if data[x][2] == "D":
                    iceboxDWins += int(data[x][0])
                    iceboxAWins += int(data[x][1])
                    iceboxDRounds += int(data[x][0]) + int(data[x][4])
                    iceboxARounds += int(data[x][1]) + int(data[x][5])
                elif data[x][2] == "A":
                    iceboxAWins += int(data[x][0])
                    iceboxDWins += int(data[x][1])
                    iceboxARounds += int(data[x][0]) + int(data[x][4])
                    iceboxDRounds += int(data[x][1]) + int(data[x][5])
            if data[x][3] == "Breeze": # checking if the game was played on Breeze
                breezeGames += 1
                if data[x][2] == "D":
                    breezeDWins += int(data[x][0])
                    breezeAWins += int(data[x][1])
                    breezeDRounds += int(data[x][0]) + int(data[x][4])
                    breezeARounds += int(data[x][1]) + int(data[x][5])
                elif data[x][2] == "A":
                    breezeAWins += int(data[x][0])
                    breezeDWins += int(data[x][1])
                    breezeARounds += int(data[x][0]) + int(data[x][4])
                    breezeDRounds += int(data[x][1]) + int(data[x][5])
        except:
            pass
        x += 1

    try:
        bindAWinrate = "%.1f" % (round(bindAWins/bindARounds,3) * 100)
        bindDWinrate = "%.1f" % (round(bindDWins/bindDRounds,3) * 100)
    except:
        bindAWinrate = "0"
        bindDWinrate = "0"
    try:
        havenAWinrate = "%.1f" % (round(havenAWins/havenARounds,3) * 100)
        havenDWinrate = "%.1f" % (round(havenDWins/havenDRounds,3) * 100)
    except:
        havenAWinrate = "0"
        havenDWinrate = "0"
    try:
        splitAWinrate = "%.1f" % (round(splitAWins/splitARounds,3) * 100)
        splitDWinrate = "%.1f" % (round(splitDWins/splitDRounds,3) * 100)
    except:
        splitAWinrate = "0"
        splitDWinrate = "0"
    try:
        ascentAWinrate = "%.1f" % (round(ascentAWins/ascentARounds,3) * 100)
        ascentDWinrate = "%.1f" % (round(ascentDWins/ascentDRounds,3) * 100)
    except:
        ascentAWinrate = "0"
        ascentDWinrate = "0"
    try:
        iceboxAWinrate = "%.1f" % (round(iceboxAWins/iceboxARounds,3) * 100)
        iceboxDWinrate = "%.1f" % (round(iceboxDWins/iceboxDRounds,3) * 100)
    except:
        iceboxAWinrate = "0"
        iceboxDWinrate = "0"
    try:
        breezeAWinrate = "%.1f" % (round(breezeAWins/breezeARounds,3) * 100)
        breezeDWinrate = "%.1f" % (round(breezeDWins/breezeARounds,3) * 100)
    except:
        breezeAWinrate = "0"
        breezeDWinrate = "0"
    await ctx.send(":flag_ma: **BIND**         ATT Win%: **" + bindAWinrate + "%**   |   DEF Win%: **" + bindDWinrate + "%**   |   Games: **" + str(bindGames) + "**\n:flag_bt: **HAVEN**    ATT Win%: **" + havenAWinrate + "%**   |   DEF Win%: **" + havenDWinrate + "%**   |   Games: **" + str(havenGames) + "**\n:flag_jp: **SPLIT**        ATT Win%: **" + splitAWinrate + "%**   |   DEF Win%: **" + splitDWinrate + "%**   |   Games: **" + str(splitGames) + "**\n:flag_it: **ASCENT**   ATT Win%: **" + ascentAWinrate + "%**   |   DEF Win%: **" + ascentDWinrate + "%**   |   Games: **" + str(ascentGames) + "**\n:flag_ru: **ICEBOX**    ATT Win%: **" + iceboxAWinrate + "%**   |   DEF Win%: **" + iceboxDWinrate + "%**   |   Games: **" + str(iceboxGames) + "**\n:flag_tt: **BREEZE**    ATT Win%: **" + breezeAWinrate + "%**   |   DEF Win%: **" + breezeDWinrate + "%**   |   Games: **" + str(breezeGames) + "**")

# command for all agent specific information
@client.command()
async def agent(ctx, arg1=None):

    playerstats = ""
    worksheet = sh.get_worksheet(3)

    if arg1 == None:
        await ctx.send(":flag_gb: **Phoenix**\n:flag_kr: **Jett**\n:flag_cn: **Sage**\n:flag_ru: **Sova**\n:flag_us: **Brimstone**\n:grey_question: **Omen**\n:flag_se: **Breach**\n:flag_ma: **Cypher**\n:flag_us: **Viper**\n:flag_br: **Raze**\n:flag_mx: **Reyna**\n:flag_de: **Killjoy**\n:flag_au: **Skye**\n:flag_jp: **Yoru**\n:flag_gh: **Astra**\n")

    elif arg1.lower() == "phoenix" or arg1.lower() == "px":
        data = worksheet.get("B16:F25")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_gb: **__Phoenix__**\n" + playerstats)
        
    elif arg1.lower() == "jett" or arg1.lower() == "jt":
        data = worksheet.get("B28:F37")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_kr: **__Jett__**\n" + playerstats)

    elif arg1.lower() == "sage" or arg1.lower() == "sa":
        data = worksheet.get("B40:F49")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_cn: **__Sage__**\n" + playerstats)
    
    elif arg1.lower() == "sova" or arg1.lower() == "sv":
        data = worksheet.get("B52:F61")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_ru: **__Sova__**\n" + playerstats)

    elif arg1.lower() == "brimstone" or arg1.lower() == "bs":
        data = worksheet.get("B64:F73")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_us: **__Brimstone__**\n" + playerstats)

    elif arg1.lower() == "omen" or arg1.lower() == "om":
        data = worksheet.get("B76:F85")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":grey_question: **__Omen__**\n" + playerstats)

    elif arg1.lower() == "breach" or arg1.lower() == "br":
        data = worksheet.get("B88:F97")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_se: **__Breach__**\n" + playerstats)

    elif arg1.lower() == "cypher" or arg1.lower() == "cy":
        data = worksheet.get("B100:F109")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_ma: **__Cypher__**\n" + playerstats)
    
    elif arg1.lower() == "viper" or arg1.lower() == "vi":
        data = worksheet.get("B112:F121")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_us: **__Viper__**\n" + playerstats)

    elif arg1.lower() == "raze" or arg1.lower() == "rz":
        data = worksheet.get("B124:F133")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_br: **__Raze__**\n" + playerstats)

    elif arg1.lower() == "reyna" or arg1.lower() == "ry":
        data = worksheet.get("B136:F145")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_mx: **__Reyna__**\n" + playerstats)

    elif arg1.lower() == "killjoy" or arg1.lower() == "kj":
        data = worksheet.get("B148:F157")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_de: **__Killjoy__**\n" + playerstats)

    elif arg1.lower() == "skye" or arg1.lower() == "sk":
        data = worksheet.get("B160:F169")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_au: **__Skye__**\n" + playerstats)

    elif arg1.lower() == "yoru" or arg1.lower() == "yo":
        data = worksheet.get("B172:F181")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_jp: **__Yoru__**\n" + playerstats)

    elif arg1.lower() == "astra" or arg1.lower() == "as":
        data = worksheet.get("B184:F193")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send(":flag_gh: **__Astra__**\n" + playerstats)

@client.command()
async def player(ctx, arg1=None):
    
    playerstats = ""
    worksheet = sh.get_worksheet(3)
    curAgent = ""
    curAgentPickrate = ""
    maps_stats = ""

    if arg1 == None:
        data = worksheet.get("B2:F11")
        for x in range(10):
            try:
                playerstats += "**" + players[x][0] + ":**   KDA: **" + data[x][0] + "** / **" + data[x][1] + "** / **" + data[x][2] + "**   |   K/D: **" + data[x][3] + "**   |   Win%: **" + data[x][4] + "**\n"
            except:
                pass
        await ctx.send("**__Overall Player Stats:__**\n" + playerstats)
    for y in range(10):
        try:
            if arg1.lower() == players[y][0].lower() or arg1.lower() == playerfast[y].lower():
                data = worksheet.get("A2:F193")
                pickrate = worksheet.get("H2:V11")
                maps = worksheet.get("X2:AC71")
                for x in range(193):
                    try:
                        if data[x][0] == players[y][0]:
                            endBasic = ""
                            if x < 14:
                                endBasic = "\n"
                            elif x >= 14 and x <= 23:
                                curAgent = ":flag_gb: **Phoenix**         "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][0] + "**"
                            elif x >= 26 and x <= 35:
                                curAgent = ":flag_kr: **Jett**                 "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][1] + "**"
                            elif x >= 38 and x <= 47:
                                curAgent = ":flag_cn: **Sage**               "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][2] + "**"
                            elif x >= 50 and x <= 59:
                                curAgent = ":flag_ru: **Sova**               "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][3] + "**"
                            elif x >= 62 and x <= 71:
                                curAgent = ":flag_us: **Brimstone**     "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][4] + "**"
                            elif x >= 74 and x <= 83:
                                curAgent = ":grey_question: **Omen**             "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][5] + "**"
                            elif x >= 86 and x <= 95:
                                curAgent = ":flag_se: **Breach**           "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][6] + "**"
                            elif x >= 98 and x <= 107:
                                curAgent = ":flag_ma: **Cypher**           "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][7] + "**"
                            elif x >= 110 and x <= 119:
                                curAgent = ":flag_us: **Viper**              "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][8] + "**"
                            elif x >= 122 and x <= 131:
                                curAgent = ":flag_br: **Raze**               "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][9] + "**"
                            elif x >= 134 and x <= 143:
                                curAgent = ":flag_mx: **Reyna**            "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][10] + "**"
                            elif x >= 146 and x <= 155:
                                curAgent = ":flag_de: **Killjoy**            "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][11] + "**"
                            elif x >= 158 and x <= 167:
                                curAgent = ":flag_au: **Skye**               "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][12] + "**"
                            elif x >= 170 and x <= 179:
                                curAgent = ":flag_jp: **Yoru**               "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][13] + "**"
                            elif x >= 182 and x <= 191:
                                curAgent = ":flag_gh: **Astra**              "
                                curAgentPickrate = "   |   Pick%: **" + pickrate[y][14] + "**"
                            try:
                                playerstats += curAgent + "KDA: **" + data[x][1] + "** / **" + data[x][2] + "** / **" + data[x][3] + "**   |   K/D: **" + data[x][4] + "**   |   Win%: **" + data[x][5] + "**" + curAgentPickrate + "\n" + endBasic
                            except:
                                pass
                        else:
                            continue
                    except:
                        pass
                for x in range(71):
                    try:
                        if maps[x][0] == players[y][0]:
                            if x <= 9:
                                maps_stats += ":flag_ma: **Bind**          KDA: **" + maps[x][1] + "** / **" + maps[x][2] + "** / **" + maps[x][3] + "**   |   K/D: **" + maps[x][4] +"**   |   Win%: **" + maps[x][5] + "**\n"
                            elif x >= 12 and x <= 21:
                                maps_stats += ":flag_bt: **Haven**      KDA: **" + maps[x][1] + "** / **" + maps[x][2] + "** / **" + maps[x][3] + "**   |   K/D: **" + maps[x][4] +"**   |   Win%: **" + maps[x][5] + "**\n"
                            elif x >= 24 and x <= 33:
                                maps_stats += ":flag_jp: **Split**          KDA: **" + maps[x][1] + "** / **" + maps[x][2] + "** / **" + maps[x][3] + "**   |   K/D: **" + maps[x][4] +"**   |   Win%: **" + maps[x][5] + "**\n"
                            elif x >= 36 and x <= 45:
                                maps_stats += ":flag_it: **Ascent**     KDA: **" + maps[x][1] + "** / **" + maps[x][2] + "** / **" + maps[x][3] + "**   |   K/D: **" + maps[x][4] +"**   |   Win%: **" + maps[x][5] + "**\n"
                            elif x >= 48 and x <= 57:
                                maps_stats += ":flag_ru: **Icebox**      KDA: **" + maps[x][1] + "** / **" + maps[x][2] + "** / **" + maps[x][3] + "**   |   K/D: **" + maps[x][4] +"**   |   Win%: **" + maps[x][5] + "**\n"
                            elif x >= 60 and x <= 69:
                                maps_stats += ":flag_tt: **Brezze**     KDA: **" + maps[x][1] + "** / **" + maps[x][2] + "** / **" + maps[x][3] + "**   |   K/D: **" + maps[x][4] +"**   |   Win%: **" + maps[x][5] + "**\n"
                    except:
                        continue
                await ctx.send("**__" + players[y][0] + "__** aka. **" + playerfast[y] + "**\n" + playerstats + "\n" + maps_stats)
        except:
            pass

@client.command()
async def game(ctx, date, time, rw, rl, map1, firstSide, rounds, p1=None, p2=None, p3=None, p4=None, p5=None):

    userID = ctx.author.id
    allrounds = []
    colorLose = {"backgroundColor": {"red": 52.0, "green": 0.0, "blue": 0.0}}
    colorWin = {"backgroundColor": {"red": 239.0, "green": 171.0, "blue": 52.0}}
    ascii_uppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]
    game_player = [p1, p2, p3, p4, p5]
    player_submit = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]]
    error = False

    rw_manuell = 0
    rl_manuell = 0
    x = 0
    while x < len(rounds):
        if rounds[x] == "W":
            rw_manuell += 1
        elif rounds[x] == "L":
            rl_manuell += 1
        else:
            await ctx.send("Invalid wins and losses. Only use W and L.")
            return
        x += 1

    worksheet = sh.get_worksheet(1)
    if userID != developerID and userID != assistantID:
        await ctx.send("You aren't allowed to submit a new game.")
        return
    if map1 != "Bind" and map1 != "Haven" and map1 != "Split" and map1 != "Ascent" and map1 != "Icebox" and map1 != "Breeze":
        await ctx.send("This map isn't valid or be sure that it is in the right upper and lowercase.")
        return
    if firstSide.upper() == "A":
        firstSide_str = "Attacker"
        secondSide = "D"
        pass
    elif firstSide.upper() == "D":
        firstSide_str = "Defender"
        secondSide = "A"
        pass
    else:
        await ctx.send("The beginning side doesn't exist. Try 'A' or 'D'.")
        return
    if int(rw) < 13 and int(rl) < 13:
        await ctx.send("Something about the Rounds aren't correct.")
        return
    if len(rounds) != int(rw) + int(rl):
        await ctx.send("You would submit to many or to few rounds.")
        return
    if rw_manuell != int(rw) or rl_manuell != int(rl):
        await ctx.send("Incorrect rounds. Check again if they fit to the end result.")
        return
    if int(rw) + int(rl) > 32:
        await ctx.send("The game is too long to submit. (max. 32 Rounds)")
    else:
        for x in range(5):
            try:
                
                game_player[x] = game_player[x].replace("[", "").replace("]", "").split(",")
                game_player[x][0] = str(game_player[x][0])
                game_player[x][1] = str(game_player[x][1]).upper()
                game_player[x][2] = int(game_player[x][2])
                game_player[x][3] = int(game_player[x][3])
                game_player[x][4] = int(game_player[x][4])

                player_str = []
                playerFound = False
                for y in range(10):
                    if game_player[x][0].lower() == players[y][0].lower() or game_player[x][0].lower() == playerfast[y].lower():
                        player_str.append(player[y][0])
                        playerFound = True
                        game_player[x].append(y)
                        if game_player[x][5] == y:
                            player_submit[y] = game_player[x]
                        break
                    else:
                        pass
                agentFound = False
                for y in range(len(agents)):
                    if game_player[x][1].lower() == agents[y].lower():
                        player_str[x].append(agents_full[y])
                        agentFound = True
                        break
                    else:
                        pass
                if agentFound == False:
                    await ctx.send("One agent doesn't exist.")
                    error = True
                    break
                elif playerFound == False:
                    await ctx.send("One player doesn't exist.")
                    error = True
                    break
            except:
                pass
        
        if error == False:
            for x in range(32):
                try:
                    allrounds.append(rounds[x].upper())
                except:
                    pass
            worksheet.append_row([date, time, int(rw), int(rl), map1, firstSide.upper(), "", "", "", "", "", "", "", "", "", "", "", secondSide, "", "", "", "", "", "", "", "", "", "", "", firstSide.upper(), secondSide, firstSide.upper(), secondSide, firstSide.upper(), secondSide, firstSide.upper(), secondSide, player_submit[0][1], player_submit[0][2], player_submit[0][3], player_submit[0][4], player_submit[1][1], player_submit[1][2], player_submit[1][3], player_submit[1][4], player_submit[2][1], player_submit[2][2], player_submit[2][3], player_submit[2][4], player_submit[3][1], player_submit[3][2], player_submit[3][3], player_submit[3][4], player_submit[4][1], player_submit[4][2], player_submit[4][3], player_submit[4][4], player_submit[5][1], player_submit[5][2], player_submit[5][3], player_submit[5][4], player_submit[6][1], player_submit[6][2], player_submit[6][3], player_submit[6][4], player_submit[7][1], player_submit[7][2], player_submit[7][3], player_submit[7][4], player_submit[8][1], player_submit[8][2], player_submit[8][3], player_submit[8][4], player_submit[9][1], player_submit[9][2], player_submit[9][3], player_submit[9][4]])
            row = len(worksheet.get_all_values())
            for x in range(int(rw) + int(rl)):
                if allrounds[x] == "W":
                    worksheet.format(ascii_uppercase[x+5] + str(row), colorWin)
                elif allrounds[x] == "L":
                    worksheet.format(ascii_uppercase[x+5] + str(row), colorLose)
            stats = ""
            for x in range(len(player_str)):
                stats += "**Player:** " + player_str[x][0] + "   |   **Agent:** " + player_str[x][1] + "   |   **KDA:** " + game_player[x][2] + " / " + game_player[x][3] + " / " + game_player[x][4] + "\n"
                print(stats)
            await ctx.send("Created the game with following attributes!\n**Date:** " + date + "   |   **Time:** " + time + "\n**Map:** " + map1 + "   |   **First Round Site:** " + firstSide_str + "\n**Result:** " + rw + " : " + rl + "\n**Player specific stats:**\n" + stats)

@client.command()
async def help(ctx, arg1):

    if arg1.lower() == "map":
        await ctx.send("```?map <map>```__Values for__ `<map>`: **Bind** / **Haven** / **Split** / **Ascent** / **Icebox**\nOnly `?game` to see an overview of all maps.")
    elif arg1.lower() == "agent":
        await ctx.send("```?agent <agent>```__Values for__ `<agent>`: **" + agents[0] + "** / **" + agents[1] + "** / **" + agents[2] + "** / **" + agents[3] + "** / **" + agents[4] + "** / **" + agents[5] + "** / **" + agents[6] + "** / **" + agents[7] + "** / **" + agents[8] + "** / **" + agents[9] + "** / **" + agents[10] + "** / **" + agents[11] + "** / **" + agents[12] + "** / **" + agents[13] + "** / **" + agents[14] + "**\nOnly `?agent` to see all agents.")
    elif arg1.lower() == "player":
        await ctx.send("```?player <player>```__Values for__ `<player>`: **" + players[0][0] + "** / **" + playerfast[0] + "**   |   **" + players[1][0] + "** / **" + playerfast[1] + "**   |   **" + players[2][0] + "** / **" + playerfast[2] + "**   |   **" + players[3][0] + "** / **" + playerfast[3] + "**   |   **" + playerfast[4] + "**   |   **" + players[5][0] + "** / **" + playerfast[5] + "**   |   **" + players[6][0] + "** / **" + playerfast[6] + "**   |   **" + players[7][0] + "** / **" + playerfast[7] + "**\nOnly `?player` to see an overview of all players.")
    elif arg1.lower() == "game":
        await ctx.send("```?game <date> <time> <round-wins> <round-losses> <map> <SideOfFirstRound> <rounds> <p1-stats> <p2-stats> <p3-stats> <p4-stats> <p5-stats>```")
    else:
        await ctx.send("See more info on Github: https://github.com/monkaCode/ValorantStats")

keep_alive()
# bot run with the token
client.run(token)