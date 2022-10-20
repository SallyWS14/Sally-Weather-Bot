/* eslint-disable indent */
/* eslint-disable no-trailing-spaces */
 const { triggers } = require('../storage/triggers.json');
 let triggerWords = [];

 for (let i = 0; i < triggers.length; i++) {
     for (let j = 0; j < triggers[i].length; j++) {
         triggerWords.push(triggers[i][j]);
     }
 }

 module.exports = {
 	name: 'messageCreate',
 	execute(message) {
 		console.log(`${interaction.user.tag} in #${interaction.channel.name} triggered an interaction.`);
       if (message.author.bot) return;
       if (message.content.contains())
	},
};
