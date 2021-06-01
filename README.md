# ValorantStats
A Google Sheets based tracking system, to store much of information from your VALORANT team. You can also host a Discord Bot to have access to this data in Discord or to update your match history.

<p align="center">
  </a>
  <a href="https://twitter.com/liiquidsilver"><img src="https://img.shields.io/badge/Twitter-@LiiquidSilver-1da1f2.svg?logo=twitter?style=for-the-badge&logo=appveyor"></a>
  <a href="https://www.twitch.tv/monkaaaaaaa"><img src="https://img.shields.io/badge/Twitch-monkaaaaaaa-blueviolet"></a>
  
</p>

## How to install the Discord Bot
Watch <a href="https://youtu.be/mYsGgcFFwgA">this video</a>.

## All commands

### ?player
?player                                   -> Overall player stats for all players in your team sorted descending by the amount of games<br/>
?player (sort-algorithm)                  -> Overall player stats for all players in your team sorted by a sort-algorithm<br/>
?player (name) (sort-algorithm)           -> Specific player stats about the (name)<br/>
 <br/>
Example: ?player ScreaM --kd<br/>
<br/>
All sort values:  --kd            -> sort descending to the K/D<br/>
                  --kda           -> sort descending to the K+A/D<br/>
                  --win%          -> sort descending to the winrate on agents and maps<br/>
                  --kills         -> sort descending to the average kills<br/>
                  --deaths        -> sort descending to the average deaths<br/>
                  --assists       -> sort descending to the average assists<br/>
<br/>
If you don't use a sort-algorith then the default is sorted descending to the amount of games.<br/>
  <br/>
### ?map
?map                                    -> Map stats for all maps sorted descending to the amount of games<br/>
?map (sort-algorithm)                   -> Map stats for all maps sorted to the sort-algorithm<br/>
<br/>
Example: ?map --win%<br/>
 <br/>
All sort values:  --win%        -> sort descending to the winrate<br/>
                  --wins        -> sort descending to the amount of wins<br/>
                  --losses      -> sort descending to the amount of losses<br/>
                  --draws       -> sort descending to the amount of draws<br/>
  <br/>
If you don't use a sort-algorithm then the default is sorted descending to the amount of games.<br/>
  <br/>
### ?rounds
?rounds                         -> Attacker and Defender winrate sorted descending to the amount of games<br/>
?rounds (sort-algorithm)        -> Attacker and Defender winrate sorted to the sort-algorithm<br/>
<br/>
Example: ?rounds --attwin%<br/>
<br/>
All sort values:  --attwin%     -> sort descending to the Attacker winrate<br/>
                  --defwin%     -> sort descending to the Defender winrate<br/>
<br/>
If you don't use a sort-algorithm then the default is sorted descending to the ammount of games.<br/>
<br/>
### ?game
?game                   -> Show all information about the last submitted game<br/>
?game (game-id)         -> Show all information about an specific game with the ID (ID = Row in Google Sheets)<br/>

### ?addgame
?addgame <date> <map> <round-wins> <round-losses> <first-side> <rounds> {player1} {player2} {player3} {player4} {player5}<br/>
<br/>
(date)          -> Whatever you want but i prefer your date format e.g. 01.06.2021 or 06/01/2021<br/>
(map)           -> The played map e.g. Icebox or Haven<br/>
(round-wins)    -> The amount of rounds you've won<br/>
(round-losses)  -> The amount of rounds you've loss<br/>
(first-side)    -> The side you started from e.g. A for Attacker or D for Defender<br/>
(rounds)        -> If you win 13 - 1 and loss the third round then you type in WWLWWWWWWWWWWW (each letter is a round, if you won this round you type W and when you loss you type L)<br/>
{player1-5}     -> You don't need this option but it's very recommended at least to add 3 or more player to a game. The format for this option are [<name>,<agent>,<kills>,<deaths>,<assists>] you can also don't use these [ ] but it's more clear. For the name type in the ingame name or the shortcut you set in the settings.txt file. For the agent you type in the whole name of the agent or use the shortcut (all shortcut for agents you can see with the "?agents" command)<br/>
<br/>
All agents shortcut: PX -> Phoenix<br/>
                     JT -> Jett<br/>
                     SA -> Sage<br/>
                     SV -> Sova<br/>
                     BS -> Brimstone<br/>
                     OM -> Omen<br/>
                     BR -> Breach<br/>
                     CY -> Cypher<br/>
                     VI -> Viper<br/>
                     RZ -> Raze<br/>
                     RY -> Reyna<br/>
                     KJ -> Killjoy<br/>
                     SK -> Skye<br/>
                     YO -> Yoru<br/>
                     AS -> Astra<br/>

## General information
In general you can use for <name> the ingame name or the shortcut you set in settings.txt
