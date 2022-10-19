//at the top of your file
const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const https = require('https');
const { API_KEY } = require('../config.json');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('weather')
		.setDescription('Get current weather!'),
	async execute(interaction) {
        https.get(`https://api.openweathermap.org/data/2.5/weather?lat=49.9&lon=-119.9&appid=2de35d4c586e85adf3afcbd482bd52dd&units=metric`);
        //https://api.openweathermap.org/data/2.5/weather?lat=57&lon=-2.15&appid={API key}&units=imperial
        let data = '';
        let weather = '';
        https.get(`https://api.openweathermap.org/data/2.5/weather?lat=49.9&lon=-119.9&appid=2de35d4c586e85adf3afcbd482bd52dd&units=metric`,(res) => {
            res.on('data',async (d) => {
                // process.stdout.write(d);
                data += d;;
            })
            res.on('end', async () => {
                const body = JSON.parse(data);
                console.log(body);
                weather = body.main.temp;
                // process.stdout.write(body.weather);
                // body.weather[0].main
                // body.weather[0].description\
                const weatherEmbed = new EmbedBuilder()
                    .setColor(0xFEB548)
                    .setThumbnail(`http://openweathermap.org/img/wn/${body.weather[0].icon}@2x.png`)
                    .setTitle('Powered by OpenWeatherMap.org')
                    .setURL('https://openweathermap.org/api')
                    .setDescription(body.weather[0].description.toUpperCase())
                    .setTimestamp()
                    .addFields(
                    	{ name: 'Maximum Temperature: ', value: body.main.temp_max+' C' },
                        { name: 'Minimum Temperature: ', value: body.main.temp_min + ' C' },
                        { name: 'Humidity: ', value: body.main.humidity +' '}
                    )
                    .setFooter({
                        text: "Weather by Sally Weather Bot",
                        iconURL: interaction.client.user.avatarURL()
                    });
                console.log(weatherEmbed)
                await interaction.reply({content: ``, embeds: [weatherEmbed]});
                //await interaction.reply({content: `The current weather ${body.weather}`, ephemeral: true})
            });
        }).on('error',(e) => {
            console.error(e);
        }).end();
        //await interaction.reply({content: `The current weather ${weather}`, ephemeral: true});
    },
};
