
const socket = new WebSocket('ws://' + window.location.host + '/websocket');
console.log("connected")

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType
     //add something to front end depending on the result of the game
    console.log("Got result! " + ws_message.data)
}



function sendMessage(choice) {
    socket.send(JSON.stringify({'messageType': 'rpsChoice', 'messageChoice': choice}));
    var options = document.getElementById("game-modal");
    options.style.display = "none";
}