# pyWoW
Python WoW API Wrapper

## Installation
1. `pip install -U pywow`
2. Get token for WoW Community API [here](https://dev.battle.net/apps/register)
4. Create/add to file config.py in project folder with these values:
```python
blizzard_key = 'Your_WoW_Community_APIKEY_here'
```

## Usage
*!* Only EU region is currently supported. 
```python
import wow
```

## Quick Tutorial

#### Get character
```python
char = wow.Character(name='CharacterName', realm='Character realm')
print('{name} on {realm} ({xplvl}lvl/{ilvl})\nPlaying as {class},{race} at {side}'.format(
	{'name':char.full_name, 'realm':char.realm.name, 'xplvl':char.level['xp']
	'ilvl':char.level['item'], 'class':char.wow_class.name, 'race':char.race.name,
	'side':char.race.side}))
```

