const { table } = require('console');
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
        const guildid = interaction.guildId;
        await interaction.reply({ content: 'Your location is: ' + location + '\n' + 'Your id is: ' + user_tag });
        var data = {
            table: [{
                guild_id: 'guild id',
                user_tag: 'user id',
                location: 'location'
            }]
        }

        // var data = {
        //     guildid: {
        //         user_tag: {
        //             "location": location
        //         }
        //     }
        // };
        data.table.push({
            guild_id: guildid,
            user_tag: user_tag,
            location: location
        });
        var json2 = JSON.stringify(data,null,4);
        console.log(json2);
        var fs = require('fs');
        // fs.writeFile('./commands/loctest.json', json2, 'utf8', err => {
        //     if (err) {
        //         console.log('Error writing file', err)
        //     } else {
        //         console.log('Successfully wrote file')
        //     }
        // });
        var file = require('./loctest.json').table;
        fs.readFile('./commands/loctest.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {
                var changed = false;
                for (let i = 0; i < file.length; i++){
                    if (file[i].guild_id == guildid) {
                        if (file[i].user_tag == user_tag) {
                            file[i].location = location;
                            changed = true;
                            json2 = JSON.stringify(file, null, 4); //convert it back to json
                            fs.writeFile('./commands/loctest.json', json2, 'utf8', err => {
                                err ? console.log('Error writing file', err) : console.log('Successfully wrote file');
                            }); // write it back
                        }
                    }
                };
                if (!changed) {
                    data = JSON.parse(data);
                    data.table.push({
                        guild_id: guildid,
                        user_tag: user_tag,
                        location: location
                    });
                    json2 = JSON.stringify(data, null, 4); //convert it back to json
                    fs.writeFile('./commands/loctest.json', json2, 'utf8', err => {
                        err ? console.log('Error writing file', err) : console.log('Successfully wrote file');
                    }); // write it back
                }
            }});
    },
};
