
const socket = new WebSocket('ws://' + window.location.host + '/websocket');
console.log("connected")

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType
    //add something to front end depending on the result of the game
    switch (messageType) {
        case "rpsChoice":
            console.log("Got back selection: " + ws_message.data);
            break;
        case "rpsResult":
            console.log(message["winner"])
            console.log("Got result: " + ws_message.data);
            if (message["winner"] != "<draw>" && message["winner"] != null) {
                document.getElementById("waiting").style.display = "none";
                document.getElementById("winner").style.display = "block";
                document.getElementById("winner").innerHTML = "The winner is: " + message["winner"];
                socket.send('close')
                console.log("Closed connection")
            }
            else {
                //add gameplay elements back in the case of a tie
                document.getElementById("waiting").innerHTML = "There was a tie! Please choose again."

                setTimeout(endWait,3000)
            }
            break;
        default:
            console.log("Not using that type :(")
            console.log(ws_message.data)
    }
}



function sendMessage(choice) {
    socket.send(JSON.stringify({'messageType': 'rpsChoice', 'messageChoice': choice}));
    var options = document.getElementById("game-modal");
    options.style.display = "none";

    document.getElementById("waiting").style.display = "block";
}

function endWait() {
    document.getElementById("waiting").style.display = "none";
    document.getElementById("waiting").innerHTML = "Waiting..."
    document.getElementById("game-modal").style.display = "block";
}