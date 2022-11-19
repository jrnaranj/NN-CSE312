const socket = new WebSocket('ws://' + window.location.host + '/websocket');

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType;
    //const messageResult = message.messageResult

    switch (messageType) {
        case 'rpsResult':
            //add something to front end depending on the result of the game
            console.log("Got result!")
            break;

        default:
            console.log("received an invalid WS messageType");
    }
}



function sendMessage(choice) {
    socket.send(JSON.stringify({'messageType': 'chatMessage', 'messageChoice': choice}));
    var options = document.getElementById("game-modal");
    options.style.display = "none";
}