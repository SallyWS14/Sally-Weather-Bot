const { SlashCommandBuilder } = require('discord.js');
const uFile = './storage/update.json';
const updateFile = require(uFile);
const fs = require('fs');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('update')
		.setDescription('Updates a json file!')
		.addStringOption(option => option.setName('value').setDescription('Value to update')),
	async execute(interaction) {
		const value = interaction.options.getString('value');
		await interaction.reply({ content: 'hello!' });
		// let hasUser = await checkRecord(interaction.guildId, interaction.user.id);
		// if (value === null || value === '' || value === undefined) {
		// 	if (hasUser) {
		// 		const getUserVal = await getData(interaction.guildId, interaction.user.id);
		// 		await interaction.reply({ content: `-Your value is ${getUserVal}` });
		// 	}
		// 	else {
		// 		await interaction.reply({ content: '--You do not have a value set. Please run the command again using the optional parameter.' });
		// 	}
		// }
		// else {
		// 	if (hasUser) {
		// 		const getUserVal = await getData(interaction.guildId, interaction.user.id);
		// 		await interaction.reply({ content: `---Your updated value is ${getUserVal}` });
		// 	}
		// 	else {
		// 		updateData(interaction.guildId, interaction.user.id, value);
		// 		await interaction.reply({ content: `----Your value is ${value}}` });
		// 	}
		// }
	},
};

const getData = async (guildId, userId) => {
	let val = '';
	if (checkRecord(guildId, userId)) {
		let i = 0;
		for (i = 0; i < updateFile.servers.length; i++) {
			if (updateFile.servers[i].guildId === guildId) {
				if (updateFile.servers[i].userId === userId) {
					val = updateFile.servers[i].value;
				}
			}
		}
	}
	console.log(val);
	return val;
};

const updateData = async (guildId, userId, data) => {
	if (checkRecord(guildId, userId)) {
		let i = 0;
		for (i = 0; i < updateFile.servers.length; i++) {
			if (updateFile.servers[i].guildId === guildId) {
				if (updateFile.servers[i].userId === userId) {
					updateFile.servers[i].value = data;
				}
			}
		}
		fs.writeFileSync(uFile, JSON.stringify(updateFile, null, 4), 'utf-8', err => {
			console.log(err);
		});
	}
};

const checkRecord = async (guildId, userId = null) => {
	let found = false;
	let i = 0;
	if (updateFile.servers.length > 0) {
		for (i = 0; i < updateFile.servers.length; i++) {
			if (updateFile.servers[i].guildId === guildId) {
				if (updateFile.servers[i].userId === userId) {
					found = true;
					break;
				}
			}
		}
	}
	return found;
};
