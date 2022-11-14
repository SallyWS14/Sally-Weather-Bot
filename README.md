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

* Get_Context
  * Getting the context of the sentence (weather, history, location, dress sense)
* Get_Tense
  * Getting the tense of the sentence and store it then pass the sentense along with the tense to Get_Context

- Weather

  - Returns the current weather data for "today"
  - Synonyms and Spell Check to make sure we get the correct sentence from the user
- History

  - `Arguments: [Location, Date, Unit, Time (optional)]`
  - This command returns the weather based on the date of the given location and time. It will return either Celsius or Fahrenheit depending
  - Using the Get_Tense function to decide whether to give out history or forcast
- DressSense

  - This commands gives the user recommendations on what to wear based on the weather (specifically temperature, precipitation, cloudiness, and windiness) if they ask
  - Synonym and Sentiment Analysis to know whether the sentence is positive or negative
- StormWatch - _**COMING SOON**_
- Location

  - `Argument: [Location]`
  - This commands let the user provide their location, and we will store the location in name, latitude and longitude
  - This command takes in the user sentence and extract the locations out of the sentence, for now this uses the first location in the sentence to convert to a geocode to be stored
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
