# Sally-Weather-Bot
![Sally Bot](./images/1x/sally_v1_Asset%201.png)

Provides you with accurate weather data on demand.

## Features

- Weather
  - Returns the current weather data for "today"
- History
  - `Arguments: [Location, Date, Unit, Time (optional)]`
  - This command returns the weather based on the date of the given location and time. It will return either Celsius or Fahrenheit depending  

- DressSense
  - This commands gives the user recommendations on what to wear based on the weather (specifically temperature, precipitation, cloudiness, and windiness) if they ask
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