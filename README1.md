# Sally-Weather-Bot

![Sally Bot](./images/1x/sally_v1_Asset%201.png)

Provides you with accurate weather data on demand.

## Running

- Clone the git repo
- Switch to web branch
- Run ``pip install -r requirements.txt``
- Load the config file

* **Activate the python environment**
  - `python3 -m venv venv`
  - `. venv/Scripts/activate` or `. venv/bin/activate` for mac users
  - **Install requirements**
  - `pip install -r requirements.txt`
  - `pip install wikipedia`
  - `pip install googletrans==3.1.0a0`
  - **Start the program**
  - `flask run` **(edited)**

- Go to localhost:5000


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
<<<<<<< HEAD
  - Synonym and Sentiment Analysis to know whether the sentence is positive or negative
=======
  - Uses a synonyms toolkit to reword given recommendation each time. This makes our bot seem more natural in conversation 
  - Uses a sentiment analysis to see if given recommendation indicates good or bad weather, bot adds a message depending on this indication. This feature makes our bot seem more personal 

>>>>>>> 35521535fcbf80df36632b98ba9d8682eca92e51
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
