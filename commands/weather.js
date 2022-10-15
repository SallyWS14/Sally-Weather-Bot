const { SlashCommandBuilder } = require('discord.js');
const https = require('node:https');
const { API_KEY } = require('../config.json');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('weather')
		.setDescription('Get current weather!'),
	async execute(interaction) {
        https.get('https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={2de35d4c586e85adf3afcbd482bd52dd}')
        , (res) => {
            let data = '';
                res.on('data', (chunk) => {
                    data += chunk;
                    
                });
                res.on('end', async () => {
                    const body = JSON.parse(data);
                    console.log(body); // print result;
                    await interaction.reply({content: `The current weather ${body}`, ephemeral: true});
                });
        }
    }
}