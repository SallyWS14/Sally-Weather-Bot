const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const https = require('https');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('history')
		.setDescription('Get weather history!')
		.addStringOption(option => option.setName('location').setDescription('Location to get weather history for').setRequired(true))
		.addStringOption(option => option.setName('date').setDescription('Date to get weather history for [YYYY-MM-DD]').setRequired(true))
		.addStringOption(option => option.setName('time').setDescription('Time of day')),
	async execute(interaction) {
		const location = interaction.options.getString('location');
		const idate = interaction.options.getString('Date');
		const itime = interaction.options.getString('Time');
		const history = [];
		const optionsGet = {
			host: 'api.weatherapi.com',
			port: 0,
			path: encodeURIComponent(`/v1/history.json?key=${process.env.CLEMENT_WAPIKEY}&q=${location}&dt=${idate} ${itime}`),
			method: 'GET',
		};
		const reqGet = https.request(optionsGet, (res) => {
			res.on('data', async (d) => {
				console.log(d);
			});
		});
		reqGet.end();
		reqGet.on('error', (err) => {
			console.error(err);
		});
		const historyEmbed = new EmbedBuilder()
			.setColor(0xEA4040)
			.setTitle('Weather History')
			.setDescription(`Weather for ${location} on ${idate} ${itime}`)
			.setThumbnail(interaction.client.user.defaultAvatarURL)
			.setTimestamp(new Date());
			// .setFooter({
			// 	icon_url: interaction.client.user.defaultAvatarURL,
			// 	text: 'Powered by WeatherAPI.com'
			// });
		console.log(historyEmbed);
		await interaction.reply({content: 'test', embeds: [historyEmbed] });
	},
};