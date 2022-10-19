const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('cleverbot')
		.setDescription('Conversation with Sally')
        .addStringOption(options => options.setName('toggle').setDescription('Toggle chat with bot').setRequired(true)),
	async execute(interaction) {
		const x = 2 + 2;
		await interaction.reply({ content: `Pong! ${x}`, ephemeral: true });
	},
};
