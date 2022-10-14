const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('history')
		.setDescription('Get weather history!')
		.addStringOption(
			option => option.setName('location')
				.setDescription('Location to get weather history for').setRequired(true),
		)
		.addStringOption(
			option => option.setName('Date')
				.setDescription('Date to get weather history for').setRequired(true),
		)
		.addStringOption(
			option => option.setName('Time')
				.setDescription('Time to get weather history for').setRequired(true),
		),
	async execute(interaction) {
		const location = interaction.options.getString('location');
		const date = interaction.options.getString('Date');
		const time = interaction.options.getString('Time');
		await interaction.reply({ content: `Your location is ${location}` });
	},
};