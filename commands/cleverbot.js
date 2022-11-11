const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const path = require('path');
const fs = require('fs');
const update = require('./update');
const cbFile = './storage/cleverbot.json';
const logFolder = '../logs/conversations';
let cbStorage = require(cbFile);

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
        const today = new Date().toISOString().split('T')[0];
        let entry = {};
        let server = await getServerIfExistsInJSONObject(interaction.guildId);
        if (!server) {
            entry = {
                severId: interaction.guildId,
                active: mode === 'global' ? true : false,
                channelId: interaction.channelId,
                logs: `${logFolder}/servers/${interaction.guildId}/global/${today}_conversations.log`,
                users: [
                    {
                        userId: interaction.user.id,
                        channelId: interaction.channelId,
                        active: mode === 'user' ? true : false,
                        lastInitiated: new Date(),
                        firstContact: getUserFromServerObject(interaction.guildId, interaction.user.id).firstContact || new Date(),
                        conversationLogs: `${logFolder}/servers/${interaction.guildId}/users/${interaction.user.id}/${today}_conversations.log`
                    }
                ]
            }
        } else {
            const user = await getUserFromServerObject(interaction.guildId, interaction.user.id);
            let userEntry = {};
            if (!user) {
                userEntry = {
                    userId: interaction.user.id,
                    channelId: interaction.channelId,
                    active: mode === 'user'? true : false,
                    lastInitiated: new Date(),
                    firstContact: getUserFromServerObject(interaction.guildId, interaction.user.id).firstContact || new Date(),
                    conversationLogs: `${logFolder}/servers/${interaction.guildId}/users/${interaction.user.id}/${today}_conversations.log`
                }
            } else {
                await updateUserValue(userId, "active", mode === 'user' ? true : false);
                await updateUserValue(userId, "lastInitiated", new Date());
                await updateUserValue(userId, "channelId", interaction.channelId);
            }
        }
        // console.log(entry);
        // const user = await getUserFromServerObject(interaction.guildId, interaction.user.id);
        // if (server === null) {
        //     await setServer(interaction.guildId, entry);
        //     server = await getServerIfExistsInJSONObject(interaction.guildId);
        // }
        // console.log(server);
        // console.log(user);
        // if serverId is in cleverbot.json and toggle is true then set channelId to current channelId
        // if serverId is in cleverbot.json, then set active to toggle
        // if serverId is in cleverbot.json and mode is individual then set servers[index].ser.users.userId to current userId and set servers.users[userId]
		await interaction.reply({ content: `${ server === null ? 'Not found' : 'Found'}`, ephemeral: mode });
	},
};

const getServerIfExistsInJSONObject = async function(serverId) {
    let server = null;
    let servers = fs.readFileSync(path.join(__dirname, cbFile), 'utf8');
    // console.log(servers);
    for (let i = 0; i < servers.length; i++) {
        if (servers[i].serverId === serverId) {
            server = servers[i];
            // console.log(server);
            break;
        }
    }
    return server;
};

const setSeverValue = async function(serverId, key, value) {
    let server = null;
    try {
        server = await getServerIfExistsInJSONObject(serverId);
        server[key] = value;
        await server.set(key, value);
        console.log(`Successfully updated ${serverId} with ${key}: ${value}`);
    } catch {
        console.log(`Failed to set ${key}: ${value} for ${serverId}`);
        await interaction.reply({ content: 'Operation failed please try again', ephemeral: true });
    }
};

const setServer = async function(serverId, values = {}) {
    cbStorage.servers.push(values);
    cbStorage = JSON.stringify(cbStorage, null, 4);
    fs.writeFileSync(`${ path.join(__dirname, cbFile) }`, cbStorage, 'utf8', (err, data) => {
        if (err) {
            console.log(err);
            return interaction.reply({ content: 'Something went wrong', ephemeral: true });
        }
        interaction.reply({ content: 'Successfully updated', ephemeral: true });
        console.log(`Updated ${serverId} with ${values}`);
        console.log(data);
    });
}

const getUserFromServerObject = async function(serverId, userId) {
    let users = [];
    try {
        users = await getServerIfExistsInJSONObject(serverId).users.get(userId);
        console.log(users);
    } catch {
        users = [];
        // await interaction.reply({ content: 'No Value Found', ephemeral: true });
        console.log(`Operation failed: no users found for ${serverId}`);
    }
};