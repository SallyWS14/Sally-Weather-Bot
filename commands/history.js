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
		if (idate > new Date().toISOString().split('T')[0]) {
			const embed = new EmbedBuilder()
			.setColor('#FF0000')
			.setTitle('Error')
			// .setThumbnail(interaction.client.user.avatarURL())
			.setFooter({ text: 'Sally Weather Bot', iconURL: interaction.client.user.avatarURL()})
			.setTimestamp()
			.setDescription('Date cannot be in the future!');
			await interaction.reply({ embeds: [embed] });
			return;
		}
		// else if (idate > new Date().toISOString().split('T')[0] || itime > new Date().getHours() && idate == new Date().toISOString().split('T')[0]) {
		// 	const embed = new EmbedBuilder()
		// 	.setColor('#FF0000')
		// 	.setTitle('Error')
		// 	// .setThumbnail(interaction.client.user.avatarURL())
		// 	.setFooter({ text: 'Sally Weather Bot', iconURL: interaction.client.user.avatarURL()})
		// 	.setTimestamp()
		// 	.setDescription('Date and time cannot be in the future!');
		// 	await interaction.reply({ embeds: [embed] });
		// 	return;
		// }
		const history = {
			location: {},
			forecast: {},
			day: {},
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
				history.day = (body.forecast.forecastday[0].day);
				history.hours = (body.forecast.forecastday[0].hour);
				console.log(history.hours);
				let fields = [];
				const hour = ((itime == '00') || (itime == 0) || (itime == '0') ? '12 AM' : (itime < 12) ? `${itime} AM` : `${itime} PM`);
				fields = [
					{
						name: 'Average Temperature',
						value: `Max Temp: ${unit === 'metric' ? history.day.maxtemp_c : history.day.maxtemp_f}°${unit === 'metric' ? 'C' : 'F'}
								Min Temp: ${unit === 'metric' ? history.day.mintemp_c : history.day.mintemp_f}°${unit === 'metric' ? 'C' : 'F'}
								Avg Temp: ${unit === 'metric' ? history.day.avgtemp_c : history.day.avgtemp_f}°${unit === 'metric' ? 'C' : 'F'}
								Condition: ${history.day.condition.text}`,
						inline: true,
					},
					{
						name: `Weather @ hour ${hour}`,
						value: `Temp: ${unit == 'metric' ? history.hours[0].temp_c : history.hours[0].temp_f}°${unit == 'metric' ? 'C' : 'F'}
								Condition: ${history.hours[0].condition.text}`,
						inline: true,
					},
					{
						name: `${history.location.name}, ${history.location.region}, ${history.location.country}`,
						value: `LatLng: ${history.location.lat}, ${history.location.lon}
								Timezone: ${history.location.tz_id}
								Local Time: ${history.location.localtime}`,
					},
				];
				const desc = `Weather for ${location} on ${idate}${(itime == null) ? '' : ' @ ' + hour}`;
				const historyEmbed = new EmbedBuilder()
					.setColor(0xFEB548)
					.setTitle('Powered by WeatherAPI.com')
					.setURL('https://www.weatherapi.com/')
					.setDescription(desc)
					.setThumbnail(`https:${history.hours[0].condition.icon}`)
					// .setThumbnail(interaction.client.user.avatarURL())
					// .setThumbnail(`https://cdn.weatherapi.com/v4/images/weatherapi_logo.png`)
					.setTimestamp(new Date())
					.setFields(fields)
					.setFooter({
						text: 'Weather History by Sally Weather Bot',
						iconURL: interaction.client.user.avatarURL(),
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
			console.log(res);
			return resolve(res);
		});
	})();
}