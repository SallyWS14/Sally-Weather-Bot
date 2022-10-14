const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('history')
		.setDescription('Get weather history!'),
	async execute(interaction) {
        await interaction.reply({content: `Something goes here!`});
	},
};