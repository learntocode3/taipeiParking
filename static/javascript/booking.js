const availableList=document.querySelector('.availableList')
statusCheck();
getLatestUserSearch();

function getLatestUserSearch(){
    document.querySelector('.mask').style.display = "block";
    fetch('/api/booking')
    .then(res => res.json())
    .then(function(data){
        console.log(data.data)
        console.log(data.data.length)
        if (data.data.length === 0){
            availableList.innerText = '目前沒有車位';
            document.querySelector('.mask').style.display = "none";
        } else {
            for(let i=0;i<data.data.length;i++){
                const item=document.createElement('div')
                item.classList.add("item")
    
                const image=document.createElement('img')
                if (data.data[i][9] !== null){
                    image.src = data.data[i][9]
                    image.style.width = '310px';
                }
                
                const info=document.createElement('div')
                info.classList = "info";

                const place=document.createElement('div')
                place.innerText = data.data[i][3]
            
                const distance=document.createElement('div')
                let km=data.data[i][6]
                //console.log(km.toFixed(2))
                distance.innerText="距離 "+ km.toFixed(2) + " km"
    
                const remain=document.createElement("div")
                remain.innerText="可以停到 " + data.data[i][2]

                info.appendChild(place)
                info.appendChild(distance)
                info.appendChild(remain)


                const avgTenOrder = document.createElement("div")
                if (data.data[i][10] !== null){
                    avgTenOrder.innerText = "過去10筆訂單平均成交價為" + data.data[i][10];
                }
                
            
                const fee=document.createElement("div")
                const finalPrice = Math.ceil(data.data[i][5])
                console.log(finalPrice)
                fee.innerText= finalPrice + "/hr"
            
                const book=document.createElement("button")
                book.innerText=" 開始保留車位 ";
    
                const commentList = data.data[i][7]
                const starList = data.data[i][8]
                const message=document.createElement('div')
                message.classList = "comment"
                const average = (array) => array.reduce((a, b) => Number(a) + Number(b)) / array.length;
                //console.log(average(starList)); 
                if (commentList.length !== 0){                             
                    message.innerText = commentList.length + '則評價' + '    平均 ' + average(starList).toFixed(2) +' 顆星'
                }
    
                message.addEventListener('click', function(){
                    message.innerText = "";
                    //let fragment = document.createDocumentFragment()
                    for(let j=0; j < commentList.length; j++){
                        let cmt = document.createElement('div')
                        cmt.innerText = `評論${j+1}：` + commentList[j]
                        //fragment.appendChild(commentList[j])
                        message.appendChild(cmt)
                    }
                    
                })
    
    
    
                book.addEventListener("click", function(){
                    //console.log(i)
                    orderData={
                        "spaceId":data.data[i][0],
                        "finalPrice": finalPrice
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
    
                
    
                          
                const checkOut=document.createElement('div')
                checkOut.classList = "checkout"
                checkOut.appendChild(avgTenOrder)
                checkOut.appendChild(fee)
                checkOut.appendChild(book)
                
                item.appendChild(image)
                item.appendChild(info)
                item.appendChild(checkOut)
                ///item.appendChild(message)
                
                const combine=document.createElement('div')
                combine.appendChild(item)
                combine.appendChild(message)
                combine.classList = 'combine'
                
                availableList.appendChild(combine)
                // availableList.appendChild(item)
                // availableList.appendChild(message)
                
            
            }document.querySelector('.mask').style.display = "none";

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
