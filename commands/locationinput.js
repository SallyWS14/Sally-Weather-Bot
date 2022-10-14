const { SlashCommandBuilder, CommandInteractionOptionResolver } = require('discord.js');
const { callbackify } = require('util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('givelocation')
		.setDescription('Give Location To the Bot')
        .addStringOption(option => option.setName('location').setDescription('Your location?')),
    async execute(interaction) {
        const location = interaction.options.getString('location');
        const user_tag = interaction.user.tag;
        await interaction.reply({ content: 'Your location is: ' + location + '\n' + 'Your id is: ' + user_tag });
        var user = {
            guild: [],
            user: [],
            loc: []
        };
        user.loc.push(location);
        user.user.push(user_tag);
        var jsonString = JSON.stringify(user);
        console.log(jsonString);
        var fs = require('fs');
        fs.writeFile('./commands/userLocation.json', jsonString, 'utf8', err => {
            if (err) {
                console.log('Error writing file', err)
            } else {
                console.log('Successfully wrote file')
            }
        });
    },
};
