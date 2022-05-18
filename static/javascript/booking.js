const availableList=document.querySelector('.availableList')
statusCheck();
getLatestUserSearch();

function getLatestUserSearch(){
    fetch('/api/booking')
    .then(res => res.json())
    .then(function(data){
        console.log(data.data)
        console.log(data.data.length)
        for(let i=0;i<data.data.length;i++){
            const item=document.createElement('div')
            item.classList.add("item")
        
            const place=document.createElement('div')
            place.innerText = data.data[i][3]
        
            const distance=document.createElement('div')
            let km=data.data[i][6]
            //console.log(km.toFixed(2))
            distance.innerText="距離 "+ km.toFixed(2) + " km"

        
            const remain=document.createElement("div")
            remain.innerText="可以停到 " + data.data[i][2]
        
            const fee=document.createElement("div")
            fee.innerText= data.data[i][5] + "/hr"
        
            const book=document.createElement("button")
            book.innerText=" 開始預約 ";

            book.addEventListener("click", function(){
                console.log(i)
                orderData={
                    "spaceId":data.data[i][0]
                }
                fetch('/api/start/order',{
                    method:'POST',
                    body:JSON.stringify(orderData),
                    headers: new Headers({
                        "content-type":"application/json"
                    })
                })
                .then(res => res.json())
                .then(function(data){
                    console.log(data.data)
                    if (data.status === "ok"){
                        location.replace(`/order/${data.orderId}`); 
                    }
                })
            })
        
            item.appendChild(place)
            item.appendChild(distance)
            item.appendChild(remain)
            item.appendChild(fee)
            item.appendChild(book)
        
            availableList.appendChild(item)
        
        }

    })
}

// for(let i=0;i<3;i++){
//     const item=document.createElement('div')
//     item.classList.add("item")

//     const place=document.createElement('div')
//     place.innerText = "光復南路巷弄"

//     const distance=document.createElement('div')
//     distance.innerText="距離 5 km"

//     const remain=document.createElement("div")
//     remain.innerText="剩餘 1 "

//     const fee=document.createElement("div")
//     fee.innerText="60 / hr"

//     const book=document.createElement("div")
//     book.classList.add('book')
//     book.innerText=" 預約 "

//     item.appendChild(place)
//     item.appendChild(distance)
//     item.appendChild(remain)
//     item.appendChild(fee)
//     item.appendChild(book)

//     availableList.appendChild(item)

// }
