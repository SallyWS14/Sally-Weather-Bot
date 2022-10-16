const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const https = require('node:https');
const { weatherapikey } = require('../config.json');
const fs = require('fs');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('history')
		.setDescription('Get weather history!')
		.addStringOption(option => option.setName('location').setDescription('Location to get weather history for').setRequired(true))
		.addStringOption(option => option.setName('date').setDescription('Date to get weather history for [YYYY-MM-DD]').setRequired(true))
		.addStringOption(option => option.setName('time').setDescription('Time of day')),
	async execute(interaction) {
		const location = interaction.options.getString('location');
		const idate = interaction.options.getString('date');
		const itime = interaction.options.getString('time');
		const history = {
			location: {},
			forecast: {},
		};
		const optionsGet = {
			host: 'api.weatherapi.com',
			port: 0,
			path: encodeURIComponent(`/v1/history.json?key=${weatherapikey}&q=${location}&dt=${idate}${itime == null ? '' : ' ' + itime}`),
			method: 'GET',
		};
		let data = '';
		let fields = [];
		const reqGet = https.request('https://' + optionsGet.host + decodeURIComponent(optionsGet.path), (res) => {
			console.log('===============================');
			console.log(`${res.statusCode} ${res.statusMessage}`);
			console.log('===============================');
			res.on('data', async (d) => {
				data += d;
			});
			res.on('end', async () => {
				const body = JSON.parse(data);
				history.location = (body.location);
				history.forecast = (body.forecast);
				fields = [
					{
						name: `${history.location.name}, ${history.location.region}, ${history.location.country}`,
						value: `Lat: ${history.location.lat}
								Lon: ${history.location.lon}
								Timezone: ${history.location.tz_id}
								Local Time: ${history.location.localtime}`,
					},
					// {
					// 	name: '\u200b',
					// 	value: '\u200b',
					// 	inline: false,
					// },
				];
				// console.log(fields);
				const desc = `Weather for ${location} on ${idate}${itime == null ? '' : ' ' + itime}`;
				const historyEmbed = new EmbedBuilder()
					.setColor(0xFEB548)
					.setTitle('Weather History')
					.setDescription(desc)
					.setThumbnail(interaction.client.user.defaultAvatarURL)
					.setTimestamp(new Date())
					.setFields(fields)
					.setFooter({
						icon_url: interaction.client.user.defaultAvatarURL,
						text: 'Powered by WeatherAPI.com',
					});
				// console.log(historyEmbed);
				await interaction.reply({ content: '', embeds: [historyEmbed] });
			});
		});
		reqGet.on('error', (err) => {
			console.log(err);
		});
		reqGet.end();
	},
};