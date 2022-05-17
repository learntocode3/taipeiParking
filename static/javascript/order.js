let data;
const orderId = document.URL.split("/").slice(-1)

console.log(orderId[0])


const finishBtn=document.querySelector('#finishBtn')



finishBtn.addEventListener("click", function(){
    orderData={'orderId':orderId[0]}
    fetch('/api/finish/order',{
        method:'POST',
        body:JSON.stringify(orderData),
        headers: new Headers({
            "content-type":"application/json"
        })
    })
    .then(res => res.json())
    .then(function(data){
        console.log(data.data)
        if (data.data === "ok"){
            location.replace(`/thankyou/${data.orderId}`)
        }
    
    })
})

