const availableList=document.querySelector('.availableList')


for(let i=0;i<3;i++){
    const item=document.createElement('div')
    item.classList.add("item")

    const place=document.createElement('div')
    place.innerText = "光復南路巷弄"

    const distance=document.createElement('div')
    distance.innerText="距離 5 km"

    const remain=document.createElement("div")
    remain.innerText="剩餘 1 "

    const fee=document.createElement("div")
    fee.innerText="60 / hr"

    const book=document.createElement("div")
    book.classList.add('book')
    book.innerText=" 預約 "

    item.appendChild(place)
    item.appendChild(distance)
    item.appendChild(remain)
    item.appendChild(fee)
    item.appendChild(book)

    availableList.appendChild(item)

}
