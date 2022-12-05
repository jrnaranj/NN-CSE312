function welcome() {
	/*get_chat_history()*/
	append("Tommy", "1000")

  
}	

function append( name, pts){
	const user= document.getElementById("username")
    user.innerHTML = name
    const wins= document.getElementById("wins")
    wins.innerHTML = pts

}
