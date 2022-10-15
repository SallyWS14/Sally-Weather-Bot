const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const https = require('https');
const histLog = require('./history.json');
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
			// console.log('===============================');
			// console.log(res);
			console.log('===============================');
			console.log(`${res.statusCode} ${res.statusMessage}`);
			console.log('===============================');
			res.on('data', async (d) => {
				// console.log(d);
				data += d;
			});
			res.on('end', async () => {
				const body = JSON.parse(data);
				history.location = (body.location);
				history.forecast = (body.forecast);
				// histLog[interaction.guildId] = {};
				// histLog[interaction.guildId][interaction.user.id] = {
				// 	location: history.location,
				// 	forecast: history.forecast,
				// };
				// histLog[interaction.guildId][interaction.user.id].forecast = history.forecast;
				// if (histLog.servers !== undefined) {
				// 	const servers = {
				// 		servers: [],
				// 	};
				// 	histLog = servers;
				// }
				// console.log(histLog);
				// for (let i = 0; i < histLog.servers.length; i++) {
				// 	if (histLog.servers[i].guildId == interaction.guildId) {
				// 		if (histLog.servers[i].userId == interaction.user.id) {
				// 			histLog.servers[i].location = history.location;
				// 			histLog.servers[i].forecast = history.forecast;
				// 		} else {
				// 			histLog.servers[i].guildId = interaction.guildId;
				// 			histLog.servers[i].userId = interaction.user.id;
				// 			histLog.servers[i].location = history.location;
				// 			histLog.servers[i].forecast = history.forecast;
				// 		}
				// 	}
				// }
				// const histLogJson = JSON.stringify(histLog, null, 4);
				// console.log(histLogJson);
				// fs.writeFileSync('./commands/history.json', histLogJson, function writeJSON(err) {
				// 	if (err) return console.log(err);
				// 	console.log(histLogJson);
				// 	console.log('writing to ' + './commands/history.json');
				// });
				console.log(history);
				fields = [
					{
						name: `${history.location.name}, ${history.location.region}, ${history.location.country}`,
						value: `Lat: ${history.location.lat}
								Lon: ${history.location.lon}
								Timezone: ${history.location.tz_id}
								Local Time: ${history.location.localtime}`,
					},
					{
						name: '\u200b',
						value: '\u200b',
						inline: false,
					},
					{
						name: 'Current Guild',
						value: interaction.guildId,
						inline: true,
					},
					{
						name: 'Inline field title',
						value: 'Some value here',
						inline: true,
					},
					{
						name: 'Inline field title',
						value: 'Some value here',
						inline: true,
					},
				];
				console.log(fields);
				const historyEmbed = new EmbedBuilder()
					.setColor(0xEA4040)
					.setTitle('Weather History')
					.setDescription(`Weather for ${location} on ${idate}${itime == null ? '' : ' ' + itime}`)
					.setThumbnail(interaction.client.user.defaultAvatarURL)
					.setTimestamp(new Date())
					.setFields(fields)
					.setFooter({
						icon_url: interaction.client.user.defaultAvatarURL,
						text: 'Powered by WeatherAPI.com',
					});
				console.log(historyEmbed);
				await interaction.reply({ content: '', embeds: [historyEmbed] });
				// console.log(body);
			});
		});
		reqGet.on('error', (err) => {
			console.log(err);
		});
		reqGet.end();
	},
};