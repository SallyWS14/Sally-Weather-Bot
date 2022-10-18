const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const fs = require('fs');
const cbFile = './storage/cleverbot.json';
const logFolder = './logs/conversations/';
const cbStorage = require(cbFile);

module.exports = {
	data: new SlashCommandBuilder()
		.setName('chatmode')
		.setDescription('Conversation with Sally')
        .addBooleanOption(options => options.setName('toggle').setDescription('Toggle chat with bot').setRequired(true))
        .addStringOption(options => options.setName('mode').setDescription('Set mode [active for whole server or user]').setRequired(true).addChoices(
            {name: 'User', value: 'user'},
            {name: 'Global', value: 'global'},
        )),
	async execute(interaction) {
        const toggle = interaction.options.get('toggle');
        const mode = interaction.options.get('mode');
        const entry = {
            severId: interaction.guildId,
            active: mode === 'global' ? true : false,
            channelId: interaction.channelId,
            users: [
                {
                    userId: interaction.user.Id,
                    channelId: interaction.channelId,
                    active: mode === 'user' ? true : false,
                    firstInitiated: 
                }
            ]
        }
        const server = getServerIfExistsInJSONObject(interaction.guildId);
        // if serverId is in cleverbot.json and toggle is true then set channelId to current channelId
        // if serverId is in cleverbot.json, then set active to toggle
        // if serverId is in cleverbot.json and mode is individual then set servers[index].ser.users.userId to current userId and set servers.users[userId]
		await interaction.reply({ content: `${ server == null ? 'Not found' : 'Found'}`, ephemeral: mode });
	},
};

const getServerIfExistsInJSONObject = async function(serverId) {
    let server = null;
    try {
        server = await cbStorage.get(servers).get(serverId);
        console.log(server);
    } catch {
        server = null;
    }
};

const getUsersFromServerObject = async function(serverId) {
    let users = [];
    try {
        users = await cbStorage.get(servers).get(userId);
        console.log(users);
    } catch {
        users = [];
    }
};