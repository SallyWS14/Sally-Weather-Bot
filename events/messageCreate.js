/* eslint-disable indent */
/* eslint-disable no-trailing-spaces */
const path = require('path');
const triggerFile = path.join(__dirname, '../commands/storage/triggers.json');
let triggerSettings = require(triggerFile);
const fs = require('fs');
let triggers = triggerSettings.triggers;
let enabled = triggerSettings.enabled;

let triggerWords = [];
for (const groups in triggers) {
    for (const words of triggers[groups]) {
        triggerWords.push(words);
    }
}

module.exports = {
 	name: 'messageCreate',
 	execute(message) {
        msg = message.content.toLowerCase();
        if (message.author.bot) return;
        console.log(`${message.author.tag} in #${message.channel.name} sent a message: ${msg}`);
        if (msg.includes("hey sally")) {
            message.reply(`Hello ${message.author.username}!`).then(() => {
                toggleTriggerMode(true);
                console.log(`Replied to ${message.content}`)
            }).catch(console.error);
        }
        if (msg.includes("thank you, sally") || msg.includes("thanks") || msg.includes("thank you") || msg.includes("thx")){
            message.reply(`Happy to help!, ${message.author.username}!`).then(() => {
                toggleTriggerMode(false);
                console.log(`Replied to ${message.content}`)
            }).catch(console.error);
        }
        if (triggerMode) {
            isTriggered(msg, message);
        }
	},
};

const isTriggered = (sentence, msgItem) => {
    Object.entries(triggers).forEach(([g, trigger]) => {
        trigger.forEach(value => {
            const found = sentence.includes(value);
            if (found) {
                console.log(`Trigger found! "${value}" in "${sentence}"`)
                const commands = msgItem.client.commands;
                const command = commands.get(g);
                switch(g) {
                    case 'location':
                        let loc = sentence.split(' ');
                        loc = loc[loc.length-1];
                        const intrc = {
                            // id: msgItem.application,
                            // type: ApplicationCommand,
                            commandName: g,
                            user: msgItem.author,
                        }
                        intrc.user = {...msgItem.author, tag: msgItem.author.tag}
                        let nMsgItem = {...msgItem, interaction: intrc};
                        // const options = {
                        //     name: "location",
                        //     type: String,
                        //     value: loc,
                        //     user: msgItem.author,
                        //     member: msgItem.member,
                        //     channel: msgItem.channel,
                        //     required: commands.get(g).options.required,
                        //     role: msgItem.member.roles[0],
                        // }
                        // const newInteraction = {...msgItem.interaction, options: options};
                        // console.log(newInteraction);
                        // command.execute(newInteraction);
                        
                        console.log(nMsgItem);
                        console.log(nMsgItem.interaction.user.tag);
                        command.execute(nMsgItem, loc);
                        break;
                    case 'history':
                        // commands.get(group)
                        break;
                    case 'weather':
                        command.execute(msgItem);
                        break;
                    case 'wear':
                        command.execute(msgItem);
                        break;
                }
            }
        });
    });
}

const triggerMode = () => {
    return fs.readFileSync(triggerFile, 'utf-8', err => {
        if (err) {
            console.error(err);
            return;
        }
    })["enabled"];
}

const toggleTriggerMode = (toggleVal) => {
    try {
        if (toggleVal) {
            enabled = toggleVal;
        } else {
            enabled = !enabled;
        }
        triggerSettings = {
            enabled: enabled,
            triggers: triggers,
        }
        triggerSettings = JSON.stringify(triggerSettings, null, 4);
        let hasErrors = false;
        fs.writeFileSync(triggerFile, triggerSettings, 'utf-8', err => {
            if (err) {
                console.log(err);
                hasErrors = true;
            }
        });
        if (!hasErrors) {
            console.log(`Updated trigger mode and set enabled to ${toggleVal} `);
        } else {
            console.log(`There was an error updating the trigger mode.`);
        }
    } catch(e) {
        console.error(e);
        return;
    }
};

const findTriggerGroup = (trigger) => {
    for (let i = 0; i < triggers.length; i++) {
        if (triggers[i].includes(trigger)) {
            console.log(i);
            return i;
        }
    }
}