const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('ping')
		.setDescription('Replies with Pong!'),
	async execute(interaction) {
		const x = 2 + 2;
		await interaction.reply({ content: `Pong! ${x}`, ephemeral: true });
	},
};
