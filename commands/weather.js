const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('ping')
		.setDescription('Replies with Pong!'),
	async execute(interaction) {
		let x = 2+2
        await interaction.reply({content: `Pong! ${x}`, ephemeral: true});
	},
};
async function getData() {
    const response = await fetch('https://home.openweathermap.org/api_keys')
    const data = await response.json()
  }
 

