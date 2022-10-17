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
		.addStringOption(option => option.setName('unit').setDescription('Celsius or Farhrerheit').setRequired(true).addChoices(
			{name: 'C', value: 'metric'},
			{name: 'F', value: 'imperial'},
		))
		.addStringOption(option => option.setName('time').setDescription('Time of day [HH:00]')),
	async execute(interaction) {
		const location = interaction.options.getString('location');
		const idate = interaction.options.getString('date');
		const unit = interaction.options.getString('unit');
		const itime = interaction.options.getString('time') == null ? new Date().getHours() : interaction.options.getString('time').split(':')[0];
		const history = {
			location: {},
			forecast: {},
			hours: {},
		};
		const optionsGet = {
			host: 'api.weatherapi.com',
			port: 0,
			path: encodeURIComponent(`/v1/history.json?key=${weatherapikey}&q=${location}&dt=${idate}&hour=${itime}`),
			method: 'GET',
		};
		const embeds = [];
		let data = '';
		const reqGet = https.get(`https://${optionsGet.host}${decodeURIComponent(optionsGet.path)}`, (res) => {
			console.log(`https://${optionsGet.host}${decodeURIComponent(optionsGet.path)}`);
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
				// console.log(history.forecast);
				// console.log(body.forecast.forecastday[0].day);
				// console.log(body.forecast.forecastday[0].hour);
				history.hours = (await deepMagnet(body.forecast.forecastday[0].hour, `${idate} ${itime}:00`));
				console.log(history.hours);
				let fields = [];
				fields = [
					{
						name: `${history.location.name}, ${history.location.region}, ${history.location.country}`,
						value: `Lat: ${history.location.lat}
								Lon: ${history.location.lon}
								Timezone: ${history.location.tz_id}
								Local Time: ${history.location.localtime}`,
					},
					{
						name: 'Average Temperature',
						value: `max: ${unit === 'metric' ? history.hours[0].maxtemp_c : history.hours[0].maxtemp_f}°${unit === 'metric' ? 'C' : 'F'}
								min: ${unit === 'metric' ? history.hours[0].mintemp_c : history.hours[0].mintemp_f}°${unit === 'metric' ? 'C' : 'F'}
								avg: ${unit === 'metric' ? history.hours[0].avgtemp_c : history.hours[0].avgtemp_f}°${unit === 'metric' ? 'C' : 'F'}`,
						inline: true,
					},
					{
						name: `At hour ${itime}:00`,
						value: `${ unit == 'C' ? history.hours.temp_c + '°C' : history.hours.temp_f + '°F'}`,
						inline: true,
					}
				];
				const desc = `Weather for ${location} on ${idate}${itime == null ? '' : ' @' + itime}`;
				const historyEmbed = new EmbedBuilder()
					.setColor(0xFEB548)
					.setTitle('Weather History')
					.setDescription(desc)
					.setThumbnail(history.hours.condition.icon)
					.setTimestamp(new Date())
					.setFields(fields)
					.setFooter({
						icon_url: interaction.client.user.avatarURL(),
						text: 'Powered by WeatherAPI.com',
					});
				await interaction.reply({ content: '', embeds: [historyEmbed] });
			});
		}).on('error', (err) => {
			console.log(err);
		}).end();
	},
};

const magnet = async (haystack, needle) => {
	return (() => {
		return new Promise((resolve, reject) => {
			const res = Object.keys(haystack).find(key => haystack[key].includes(needle));
			return resolve(res);
		});
	})();
};

const hardMagnet = async (haystack, needle) => {
	return (() => {
		return new Promise((resolve, reject) => {
			let res = '';
			for (const element of haystack) {
				if (element.includes(needle)) {
					res = element;
					console.log(res);
				}
			}
			return resolve(res);
		});
	})();
}

const deepMagnet = async (haystack, needle) => {
	return (() => {
		return new Promise((resolve, reject) => {
			let res = haystack.filter(obj => obj.time === needle)
			return resolve(res);
		});
	})();
}