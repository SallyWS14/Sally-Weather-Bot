# Sally-Weather-Bot
![Sally Bot](./images/1x/sally_v1_Asset%201.png)

Provides you with accurate weather data on demand.

## Running
- Add the bot to your server using this authentication link:
	[Sally Authentication](https://discord.com/api/oauth2/authorize?client_id=1021956341872472074&permissions=8&scope=bot)
- Download the `config.json` file to your computer and move it to the same directory as the index.js file
- Run `npm install` to install the required packages
- Run `npm start` to start the bot

## Features

- Weather
  - Returns the current weather data for "today"
- History
  - `Arguments: [Location, Date, Unit, Time (optional)]`
  - This command returns the weather based on the date of the given location and time. It will return either Celsius or Fahrenheit depending  

- DressSense
  - This commands gives the user recommendations on what to wear based on the weather (specifically temperature, precipitation, cloudiness, and windiness) if they ask
  - Uses a synonyms toolkit to reword given recommendation each time. This makes our bot seem more natural in conversation 
  - Uses a sentiment analysis to see if given recommendation indicates good or bad weather, bot adds a message depending on this indication. This feature makes our bot seem more personal 

- StormWatch - _**COMING SOON**_
- Location
  - `Argument: [Location]`
  - This commands let the user provide their location, and we will store the location in name, latitude and longitude
- TriggerMode
  - When enabled this will scan the messages for trigger words and phrases
- AIMode
  - Allows you to have a conversation with Sally

## Triggers
- The following are triggers that will run the individual commands
```json
"location": [
	"i'm currently at",
	"i live in",
	"i've arrived at",
	"i have arrived at",
	"location",
	"new place",
	"place",
	"city",
	"live",
	"arrived at",
	"moved to"
],
"history": [
	"what was the weather like {x} days ago?",
	"did it rain {x} months ago",
	"how was the weather this time last year",
	"ago",
	"last",
	"history",
	"was the weather"
],
"wear": [
	"should i wear jeans today?",
	"what should i wear today?",
	"any recommendations about what i should wear today?",
	"should i grab a coat?",
	"what should i wear?",
	"wear",
	"clothes",
	"cloth",
	"dress",
	"grab",
	"sweater"
],
"weather": [
	"how is the weather today?",
	"is it chilly today?",
	"what is the weather like?",
	"how cold is it today",
	"weather",
	"chilly",
	"cold",
	"hot",
	"today",
	"warm",
	"rain"
],
"time": [
	"time"
]
```
- Trigger for cleverbot and normal triggermode
	- To enable triggermode
		`hey sally`
	- To disable triggermode
		`thank you, sally`, `thanks`, `thank you`, `thx`
	- To enable ai mode
	`talkback`, `talk back`, `think about`
	- To disable ai mode
	`okay`, `stop`, `shut up`, `shut`
