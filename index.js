document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.86.87";   // the IP address of your Raspberry PI

function send_data(data) {
    console.log(data);
    client();
}

function client(){
    const net = require('net');

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        //client.write(`${input}\r\n`);
    });

    //get the data from the server
    client.on('data', (data) => {
        document.getElementById("bluetooth").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
        client.end();
        client.destroy();
    });
}

function updateMetrics(data) {
    var metrics = data.split(",");
    var power = metrics[0].split(":")[1];
    var temp = metrics[1].split(":")[1];
    var speed = metrics[2].split(":")[1];
    document.getElementById("power").innerHTML = power;
    document.getElementById("speed").innerHTML = speed;
    document.getElementById("temperature").innerHTML = temp;
}

function updateCarMetrics(){
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log('connected to server!');
    });

    client.write("data please");
    client.on('data', (data) => {
        //index.js:47 power:7.37,temp:49.17,speed:0.0
        updateMetrics(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
        client.end();
        client.destroy();
    });
}



// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").classList.replace("grey","green");
        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").classList.replace("grey","green");
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").classList.replace("grey","green");
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").classList.replace("grey","green");
        send_data("68");
    }
}

// reset the key to the start state 
function resetKey(e) {
    e = e || window.event;
    document.getElementById("upArrow").classList.replace("green","grey");
    document.getElementById("downArrow").classList.replace("green","grey");
    document.getElementById("leftArrow").classList.replace("green","grey");
    document.getElementById("rightArrow").classList.replace("green","grey");
}


// update data for every 50ms
function update_data(){
    setInterval(function(){
        updateCarMetrics();
    }, 500);
}

update_data();