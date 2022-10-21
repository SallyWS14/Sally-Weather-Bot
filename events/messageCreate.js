/* eslint-disable indent */
/* eslint-disable no-trailing-spaces */
const path = require('path');
const https = require('node:https');
const triggerFile = path.join(__dirname, '../commands/storage/triggers.json');
let triggerSettings = require(triggerFile);
const { cleverbot } = require('../config.json');
const fs = require('fs');
let triggers = triggerSettings.triggers;
let enabled = triggerSettings.enabled;
let aimode = triggerSettings.aimode;

let triggerWords = [];
for (const groups in triggers) {
    for (const words of triggers[groups]) {
        triggerWords.push(words);
    }
}
let cs;

const ai = require('clever-bot-api')
let cb = {
    url: 'https://www.cleverbot.com/getreply',
    key: cleverbot
}

module.exports = {
 	name: 'messageCreate',
 	execute(message) {
        let msg = message.content.toLowerCase();
        if (message.author.bot) return;
        console.log(`${message.author.tag} in #${message.channel.name} sent a message: ${msg}`);
        if (msg.includes("hey sally")) {
            message.reply(`Hello ${message.author.username}!`).then(() => {
                toggleTriggerMode(true);
                console.log(`Replied to ${message.content}`)
            }).catch(console.error);
        }
        if (msg.includes("thank you, sally") || msg.includes("thanks") || msg.includes("thank you") || msg.includes("thx")){
            toggleAIMode(false);
            toggleTriggerMode(false);
            message.reply(`Happy to help!, ${message.author.username}!`).then(() => {
                console.log(`Replied to ${message.content}`)
            }).catch(console.error);
        }
        if (msg.includes("talkback") || msg.includes("talk back") || msg.includes("think about")) {
            toggleAIMode(true);
        }
        if (msg.includes("okay") || msg.includes("stop") || msg.includes("shut up") || msg.includes("shut")) {
            toggleAIMode(false);
        }
        // console.log(triggerMode());
        if (triggerMode()) {
            isTriggered(msg, message);
            // const history = [msgs] for context;
            // ai(msg, message.channel.name).then((resp) => {
            //     message.reply(`${resp}`);
            //     console.log(resp);
            // });
            
        }
        if (aiMode()) {
            talkToSally(msg, message, cs);
        }
	},
};


// 
const talkToSally = (msg, message, cs) => {
    let options = {
        hostname: 'https://www.cleverbot.com/getreply',
        port: 443,
        path: `?key=${cleverbot}&input=${msg}&cs=${cs}`,
        method: 'POST',
    };
    let link = `${cb.url}?key=${cb.key}&input=${msg}${cs !== undefined || cs != null ? '&cs=' + cs : ''}`;
    https.request(link, (resp) => {
        resp.setEncoding('utf8');
        let data = '';
        resp.on('data', (chunk) => {
            data+=chunk;
        });
        resp.on('end', () => {
            data = JSON.parse(data);
            // console.log(data);
            cb.cs = data.cs;
            message.reply(data.output);
        });
    }).on('error', err => {
        console.error(err);
    })
    .end();
};

const isTriggered = (sentence, msgItem) => {
    let triggerGroup = [];
    let triValues = [];
    Object.entries(triggers).forEach(([g, trigger]) => {
        trigger.forEach(value => {
            const found = sentence.includes(value);
            if (found) {
                console.log(`Trigger found! "${value}" in "${sentence}"`)
                triggerGroup.push(g);
                triValues.push(value);
                return true;
            }
        });
    });
    if (triggerGroup.length > 0) {
        triggerGroup = [...new Set(triggerGroup)];
        for (const element of triggerGroup) {
            const g = element;
            const commands = msgItem.client.commands;
            let command;
            switch(g) {
                case 'location':
                    command = commands.get(g);
                    msgItem.reply(`I am unable to unable your location. Please run /${g} to change your location`);
                    break;
                case 'history':
                    command = commands.get(g);
                    msgItem.reply(`I am unable to process that, please run the /${g} to get the historical weather data`);
                    // commands.get(group)
                    break;
                case 'weather':
                    command = commands.get(g);
                    command.execute(msgItem);
                    break;
                case 'wear':
                    command = commands.get(g);
                    command.execute(msgItem);
                    break;
                default:
                    if (g == 'time') {
                        const curTime = new Date();
                        msgItem.reply(`The curernt time is ${curTime.toLocaleTimeString()}`);
                    }
                    break;
            }
        }
    }
}

const triggerMode = () => {
    let res = fs.readFileSync(triggerFile, 'utf-8');
    res = JSON.parse(res).enabled;
    return res;
}

const aiMode = () => {
    let res = fs.readFileSync(triggerFile, 'utf-8');
    res = JSON.parse(res).aimode;
    return res;
}

const toggleAIMode = (val) => {
    try {
        if (val) {
            aimode = val;
        } else {
            aimode = !aimode;
        }
        triggerSettings = {
            aimode: aimode,
            triggers: triggers,
            enabled: enabled
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
            console.log(`Updated ai mode and set to ${val} `);
        } else {
            console.log(`There was an error updating the ai mode.`);
        }
    } catch(e) {
        console.error(e);
        return;
    }
}

const toggleTriggerMode = (toggleVal) => {
    try {
        if (toggleVal) {
            enabled = toggleVal;
        } else {
            enabled = !enabled;
        }
        triggerSettings = {
            aimode: aimode,
            triggers: triggers,
            enabled: enabled,
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