var keypress = require('keypress');

// make `process.stdin` begin emitting "keypress" events
keypress(process.stdin);

function handle_keypress(ch, key) {
    if (key && key.ctrl && key.name == 'c') {
        process.stdin.pause();
        process.exit();
    } else if (key && key.name == 'return') {
        process.stdout.write('\r\n');
    } else if (key && key.name == 'backspace') {
        process.stdout.write('\033[1D \033[1D');
    } else {
        if (typeof ch != 'undefined') {
            process.stdout.write(ch);
        }
    }
}

// listen for the "keypress" event
process.stdin.on('keypress', function (ch, key) {
//  console.log('got "keypress"', key);

    handle_keypress(ch, key);
    msghub.publish('keypress', {ch: ch, key: key}, true);
});

process.stdin.setRawMode(true);
process.stdin.resume();


MsgHub = require('pubsub-client.js')
//MsgHub = require('/root/pubsub/pubsub-client.js')
//MsgHub = require('./pubsub/pubsub-client.js')
//msghub = new MsgHub('http://pubsub.msghub.io:58080')
msghub = new MsgHub('https://pubsub.msghub.io')
//msghub = new MsgHub('http://198.199.97.15:12345')

function cb(ch, msg) {
    handle_keypress(msg.ch, msg.key);
//    console.log('receive msg', msg, 'from channel', ch, (new Date()).toISOString());
}

msghub.subscribe('keypress', cb);
//msghub.publish('log', 'hello!!', false);

