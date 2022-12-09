
function get_score_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);
            console.log(messages)
			c=1
			datalist=[]
			for (const [key, value] of Object.entries(messages)) {
				console.log(`${key}: ${value},`);
				datalist.push({"name":key,"val":value})
				

			}
			datalist.sort((a, b) => (a.val < b.val) ? 1 : -1)
			console.log(datalist)
			standard=0
			if(datalist[0].val>100){
				standard= datalist[0].val
				datalist[0].perc=100
			}
			for (const x of datalist){
				console.log(x)
				if(x.val>100){
					x.perc=(100/standard)*x.val
				}
				else{
					x.perc=(100/standard)*x.val


				}
				append(c.toString(),x.name,x.val.toString(),x.perc)
				c++
			}
        }
    };
    request.open("GET", "/score");
    request.send();
}
function welcome() {
	get_score_history()
	
  
}	


function append(pl, name, pts,perc){
	width1 = parseInt(perc)+"%"
	console.log(width1)
	const box = document.getElementsByClassName('lboard_mem');
    	box2= box[0]
	const lboard_mem= document.createElement("div")
	lboard_mem.classList.add("lboard_mem")
	const img = document.createElement("div")
	img.classList.add('img')
	const par = document.createElement("div")
	par.classList.add('name_bar')
	par.innerHTML="<p><span>"+pl+".</span> "+name+" </p>"
	const bar_wrap = document.createElement("div")
	bar_wrap.classList.add('w3-light-grey', 'w3-round')
	const inner_bar = document.createElement("div")
	inner_bar.classList.add('w3-container', 'w3-blue', 'w3-round')
	inner_bar.innerHTML = width1
	console.log(inner_bar)
	inner_bar.style.width= width1

	inner_bar.style.height = "17px"

	bar_wrap.appendChild(inner_bar)
	const points = document.createElement("div")
	points.classList.add('points')
	points.textContent = " "+pts +"points"
	console.log(par)
	console.log(bar_wrap)
	console.log(points)
	console.log(lboard_mem)
    	box2.classList.add('bar');
    	console.log(box2.classList)

    	console.log(box[0])
    	console.log(box2[0])

	
	lboard_mem.appendChild(img)
	par.appendChild(bar_wrap)
	lboard_mem.appendChild(par)
	lboard_mem.appendChild(points)
	console.log(lboard_mem)
	const box3 = document.getElementsByClassName('lboard_item month');
	console.log(box3.innerHTML)
	box3[0].appendChild(lboard_mem)
	box3[0].appendChild(lboard_mem)
	box3[0].appendChild(lboard_mem)
	box3[0].appendChild(lboard_mem)
	box3[0].appendChild(lboard_mem)
	box3[0].appendChild(lboard_mem)

}
