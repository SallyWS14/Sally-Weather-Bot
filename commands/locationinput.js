const { table } = require('console');
const { SlashCommandBuilder, CommandInteractionOptionResolver } = require('discord.js');
const { callbackify } = require('util');
const { EmbedBuilder } = require('discord.js');
const {Client} = require("@googlemaps/google-maps-services-js");


module.exports = {
	data: new SlashCommandBuilder()
		.setName('location')
		.setDescription('Give Location To the Bot')
        .addStringOption(option => option.setName('location').setDescription('Your location?')
        .setRequired(true)),

    async execute(interaction) {
        var fs = require('fs');
        var file = require('./loctest.json');
        const location = interaction.options.getString('location');
        const user_tag = interaction.user.tag;
        const guildid = interaction.guildId;
        let lat = 'latitude';
        let lng = 'longitude';
        const client = new Client({});

        client.geocode({
            params: {
                key: 'AIzaSyD1Ae_641pTLg2f_X2ElsRq21a5BYKNBlw',
                address: location
            }
        }).then((r) => {
            console.log(r.data.results[0].geometry.location.lat);
            console.log(r.data.results[0].geometry.location.lng);
            lat = (r.data.results[0].geometry.location.lat);
            lng = (r.data.results[0].geometry.location.lng);
        });

        const currLoc = new EmbedBuilder()
        .setColor(0xFEB548)
        .setTitle('Current Location')
        .setDescription('This is your current location')
        .setTimestamp()
        .addFields(
        	{ name: 'Your Name: ', value: user_tag },
            { name: 'Your Current Location: ', value: location }
        )
        .setThumbnail(interaction.client.user.avatarURL())
        await interaction.reply({content: '', embeds:[currLoc]})
        fs.readFile('./commands/loctest.json', 'utf8', function readFileCallback(err, data){
        if (err){
            console.log(err);
        } else {
            var changed = false;
            for (let i = 0; i < file.length; i++){
                if (file[i].guild_id == guildid) {
                    if (file[i].user_tag == user_tag) {
                        file[i].location = location;
                        file[i].latitude = lat;
                        file[i].longitude = lng;
                        changed = true;
                    }
                }
            };
            if (!changed) {
                data = JSON.parse(data);
                data.push({
                    guild_id: guildid,
                    user_tag: user_tag,
                    location: location,
                    latitude: lat,
                    longitude: lng
                });
                json2 = JSON.stringify(data, null, 4); //convert it back to json
                console.log(json2);
                fs.writeFile('./commands/loctest.json', json2, 'utf8', err => {
                    err ? console.log('Error writing file', err) : console.log('Successfully wrote file');
                }); // write it back
            } else {
                json2 = JSON.stringify(file, null, 4); //convert it back to json
                        console.log(json2);
                        fs.writeFile('./commands/loctest.json', json2, 'utf8', err => {
                            err ? console.log('Error writing file', err) : console.log('Successfully wrote file');
                        }); // write it back
            }
        }});
    },
};
