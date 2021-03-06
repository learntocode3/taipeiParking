let data;
const orderId = document.URL.split("/").slice(-1)
const currentAccumulateFee = document.querySelector('.currentAccumulateFee')
statusCheckForOrder();
renderOrderData();
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

function statusCheckForOrder(){
    fetch('/api/user')
    .then(res => res.json())
    .then(function(data){
        console.log(data.data)
        console.log(data.orderid)
        if (data.data === null){
            alert('please login or sign up');
            location.replace("/login");
        } else {
            login.style.display='none';
            logOut.style.display='inline-block';
            signup.style.display='none';
            member.style.display='inline-block'
        }
    })
}

function renderOrderData(){
    orderData={'orderId':orderId[0]}
    fetch('/api/render/order',{
        method:'POST',
        body:JSON.stringify(orderData),
        headers: new Headers({
            "content-type":"application/json"
        })
    })
    .then(res => res.json())
    .then(function(data){
        console.log("current accumulate Price : " + data.finalPrice)
        currentAccumulateFee.innerText = "目前累積費用為 "+ data.finalPrice + " 元"

    })

}