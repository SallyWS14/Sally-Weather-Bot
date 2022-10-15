const { SlashCommandBuilder } = require('discord.js');
const uFile = './update.json';
const updateFile = require(uFile);
const fs = require('fs');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('update')
		.setDescription('Updates a json file!')
		.addStringOption(option => option.setName('value').setDescription('Value to update')),
	async execute(interaction) {
		const value = interaction.options.getString('value');
        if (!value) {
            if (checkRecord(interaction.guildId, interaction.user.id)) {
                await interaction.reply({content: `Your value is ${getData(interaction.guildId, interaction.user.id)}`});
            } else {
                await interaction.reply({content: `You do not have a value set. Please run the command again using the optional parameter.`});
            }
        } else {
            if (checkRecord(interaction.guildId, interaction.user.id)) {
                await interaction.reply({content: `Your updated value is ${getData(interaction.guildId, interaction.user.id)}`});
            } else {
                updateData(interaction.guildId, interaction.user.id);
                await interaction.reply({content: `Your value is ${getData(interaction.guildId, interaction.user.id)}`});
            }
        }
	},
};

const getData = async (guildId, userId) => {
	let val = '';
	if (checkRecord(guildId, userId)) {
		let i = 0;
		for (i = 0; i < updateFile.length; i++) {
			if (updateFile[i].guildId === guildId) {
				if (updateFile[i].userId === userId) {
					val = updateFile[i].value;
				}
			}
		}
	}
	return val;
};

const updateData = async (guildId, userId, data) => {
	if (checkRecord(guildId, userId)) {
		let i = 0;
		for (i = 0; i < updateFile.length; i++) {
			if (updateFile[i].guildId === guildId) {
				if (updateFile[i].userId === userId) {
					updateFile[i].value = data;
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
	for (i = 0; i < updateFile.length; i++) {
		if (updateFile[i].guildId === guildId) {
			if (updateFile[i].userId === userId) {
				found = true;
				break;
			}
		}
	}
	return found;
};