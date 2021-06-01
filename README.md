# ValorantStats
A Google Sheets based tracking system, to store much of information from your VALORANT team. You can also host a Discord Bot to have access to this data in Discord or to update your match history.

<p align="center">
  </a>
  <a href="https://twitter.com/liiquidsilver"><img src="https://img.shields.io/badge/Twitter-@LiiquidSilver-1da1f2.svg?logo=twitter?style=for-the-badge&logo=appveyor"></a>
  <a href="https://www.twitch.tv/monkaaaaaaa"><img src="https://img.shields.io/badge/Twitch-monkaaaaaaa-blueviolet"></a>
  
</p>

## How to install the Discord Bot
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/mYsGgcFFwgA/0.jpg)](http://www.youtube.com/watch?v=mYsGgcFFwgA)<br/>
Watch [this video](http://www.youtube.com/watch?v=mYsGgcFFwgA "ValorantStats - Discord Bot Setup") above.


## All commands

### ?player
```
?player                          -> Overall player stats for all players in your team sorted descending by the amount of games
?player <sort-algorithm>         -> Overall player stats for all players in your team sorted by a sort-algorithm
?player <name> <sort-algorithm>  -> Specific player stats about the <name>
```
Example: 
```
?player ScreaM --kd
```
All sort values:

| Sort value    | Description                                               |
| ------------- | --------------------------------------------------------- |
| --kd          | sort descending to the K/D                                |
| --kda         | sort descending to the K+A/D                              |
| --win%        | sort descending to the winrate on agents and maps         |
| --kills       | sort descending to the average kills                      |
| --deaths      | sort descending to the average deaths                     |
| --assists     | sort descending to the average assists                    |

If you don't use a sort-algorith then the default is sorted descending to the amount of games.<br/>

### ?map
```
?map                                    -> Map stats for all maps sorted descending to the amount of games
?map <sort-algorithm>                   -> Map stats for all maps sorted to the sort-algorithm
```
Example:
```
?map --win%
```
All sort values:

| Sort value  | Description                                |
| ----------- | ------------------------------------------ |
| --win%      | sort descending to the winrate             |
| --wins      | sort descending to the amount of wins      |
| --losses    | sort descending to the amount of losses    |
| --draws     | sort descending to the amount of draws     |

If you don't use a sort-algorithm then the default is sorted descending to the amount of games.<br/>

### ?rounds
```
?rounds                         -> Attacker and Defender winrate sorted descending to the amount of games
?rounds <sort-algorithm>        -> Attacker and Defender winrate sorted to the sort-algorithm
```
Example: 
```
?rounds --attwin%
```
All sort values:

| Sort value | Description                                |
| ---------- | ------------------------------------------ |
| --attwin%  | sort descending to the Attacker winrate    |
| --defwin%  | sort descending to the Defender winrate    |

If you don't use a sort-algorithm then the default is sorted descending to the ammount of games.<br/>

### ?game
```
?game                   -> Show all information about the last submitted game
?game <game-id>         -> Show all information about an specific game with the ID (ID = Row in Google Sheets)
```
### ?addgame
```
?addgame <date> <map> <round-wins> <round-losses> <first-side> <rounds> {player1} {player2} {player3} {player4} {player5}
```

| Value           | Description                                                                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| date            | Whatever you want but i prefer your date format e.g. 01.06.2021 or 06/01/2021                                                                    |
| map             | The played map e.g. Icebox or Haven                                                                                                              |
| round-wins      | The amount of rounds you've won                                                                                                                  |
| round-losses    | The amount of rounds you've loss                                                                                                                 |
| first-side      | The side you started from e.g. A for Attacker or D for Defender                                                                                  |
| rounds          | If you win 13 - 1 and loss the third round then you type in WWLWWWWWWWWWWW (each letter is a round, if you won this round you type W and when you loss you type L) |
| player1-5       | You don't need this option but it's very recommended at least to add 3 or more player to a game. The format for this option are [`<name>`,`<agent>`,`<kills>`,`<deaths>`,`<assists>`] you can also don't use these [ ] but it's more clear Be sure that there is no space between the commas. For the name type in the ingame name or the shortcut you set in the settings.txt file. For the agent you type in the whole name of the agent or use the shortcut (all shortcut for agents you can see with the "?agent" command) |

All agents shortcut:

| Shortcut | Agent name       |
| -------- | ---------------- |
| PX       | Pheonix          |
| JT       | Jett             |
| SA       | Sage             |
| SV       | Sova             |
| BS       | Brimstone        |
| OM       | Omen             |
| BR       | Breach           |
| CY       | Cypher           |
| VI       | Viper            |
| RZ       | Raze             |
| RY       | Reyna            |
| KJ       | Killjoy          |
| SK       | Skye             |
| YO       | Yoru             |
| AS       | Astra            |

### ?voting
```
?voting        -> Create a voting on that your team can vote when your team is ready to play
```

## General information
In general you can use for `<name>` the ingame name or the shortcut you set in settings.txt
