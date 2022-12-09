function welcome() {
	get_user_history()

  
}	

function get_user_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);
            append(messages["name"],messages["wins"])
        }
    };
    request.open("GET", "/score-history1");
    request.send();
}

function append( name, pts){
	const user= document.getElementById("username")
    user.innerHTML = name
    const wins= document.getElementById("wins")
    wins.innerHTML = pts

}
