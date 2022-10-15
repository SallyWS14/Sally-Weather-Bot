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
        var data = {
            table: [{
                guild: 'guild id',
                user: 'user id',
                loc: 'location'
            }]
        }
        user.loc.push(location);
        user.user.push(user_tag);
        data.table.push({ guild_id: '807460348361703424', user_tag: user_tag, location: location });
        var jsonString = JSON.stringify(user);
        var json2 = JSON.stringify(data);
        console.log(jsonString);
        console.log(json2);
        var fs = require('fs');
        fs.writeFile('./commands/loctest.json', json2, 'utf8', err => {
            if (err) {
                console.log('Error writing file', err)
            } else {
                console.log('Successfully wrote file')
            }
        });
        fs.readFile('./commands/userLocation.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {
            user = JSON.parse(data); //now it an object
                user.user.push(user_tag); //add some data
                user.loc.push(location);
            json = JSON.stringify(user); //convert it back to json
            fs.writeFile('./commands/userLocation.json', json, 'utf8', err => {
                err ? console.log('Error writing file', err) : console.log('Successfully wrote file');
            }); // write it back
        }});
    },
};
