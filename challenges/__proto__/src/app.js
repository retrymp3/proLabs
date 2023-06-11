const express = require('express')
const bodyParser = require('body-parser');
const session = require('express-session');
const { execSync, fork } = require('child_process');
const { v4: uuidv4 } = require('uuid');
const app = express();
app.set('view engine', 'ejs');
const port = 9000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(session({secret: uuidv4(),saveUninitialized: true,resave: true,cookie: {expires: 2678400000}}));

// utils
function isObject(obj) {
    return typeof obj === 'function' || typeof obj === 'object';
}

function merge(target, source) {
    for (let key in source) {
        if (isObject(target[key]) && isObject(source[key])) {
            merge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

function clone(target) {
    return merge({}, target);
}

// api's
app.get('/', (req, res) => {
    send = req.query.send;
    if(send){
        try{
            send = JSON.parse(send);
        }catch(e){
            return res.send(`${send} is not Valid JSON`)
        }
    }
    data = clone(send);
    fork('add.js');
    return res.render('index',{data: data});
});

app.get('/time', (req, res) => {
    fork('add.js');
    return res.send(`the time is time`);
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
    }
);