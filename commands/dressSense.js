const { SlashCommandBuilder } = require('discord.js');
const https = require('https');
const { API_KEY } = require('../config.json');
const lat = 24.77;
const lon = 46.73;



module.exports = {
	data: new SlashCommandBuilder()
		.setName('wear')
		.setDescription('Replies with what you should wear based on current weather'),
	async execute(interaction) {
        https.get(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=lat=${lon}&appid=${API_KEY}&units=metric`);
        let data = '';
        let weather = '';
        https.get(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`, (res) => {
        
            res.on('data', (d) => {
                data += d;
              //process.stdout.write(d);
              //process.stdout.write(d);
              
            });

            res.on('end', async() => {
                const body = JSON.parse(data);
                let wear = "I recommend you wear:\n";

                console.log(body);
              
                
                if (body.main.temp >= 22) {
                  wear = wear + ("- a short sleeved shirt \n") + ("- shorts \n");

                    //Check if it is cloudy/sunny 
                    if (body.clouds.all<40) {
                      wear = wear + ('- a hat \n') + ('- sunglasses \n');
                    }
                }

                if (body.main.temp >= 15 & body.main.temp <= 21) {
                  wear = wear + ('- a T-shirt \n');
                    checkIfWindy();
                }

                if (body.main.temp >= 7 & body.main.temp <= 14) {
                  wear = wear + ('- a hoodie or a sweater \n')
                    checkIfWindy();
                }
                
                if (body.main.temp >= -13 & body.main.temp <= 6) {
                  wear = wear + ('- a light or medium jacket \n');
                
                  if (body.wind.speed >= 40) {
                    wear = wear + ('- a hat\n');
                  }
                  
                }
                
                if (body.main.temp <= -14) {
                  wear = wear + ('- a winter jacket \n' ) + ('- a scarf \n') + ('- gloves \n') + ('- a hat \n ');
                }
                

                //Checks if it is raining
                if (body.weather[0].main.includes("rain") || body.weather[0].main.includes("Rain")) {
                  wear = wear + ('- a raincoat \n') + ('- rain boots \n') + ('- an umbrella \n');
              
                }

                console.log('wear:');
                console.log(wear);
                console.log(body.clouds.all);
                
                //Reply
                await interaction.reply({content: wear, ephemeral: true});

              //Check if it is windy
              function checkIfWindy() {
                if (body.wind.speed >= 40) {
                  wear = wear + ('- a windbreaker \n') + ('- a hat\n');
                }
              }


            });
          }).on('error', (e) => {
            console.error(e);
          });
    
	},
};