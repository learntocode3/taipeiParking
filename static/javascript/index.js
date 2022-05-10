const offerPlace = document.querySelector(".offerNow")
const rentNow = document.querySelector(".rentNow")
const rentNowBtn = document.querySelector(".matchRightNow")


offerPlace.addEventListener('click', directToOfferPage)
rentNowBtn.addEventListener('click', sendSearchPlace)
rentNow.addEventListener('click', changetoRentNow)


function directToOfferPage(){
    window.location.replace('/offer');
}

function changetoRentNow(){
    window.location.replace('/');
}

function sendSearchPlace(e){
    e.preventDefault();

    const searchData={
        "address": document.querySelector('input[name="willingAddress"]').value,
        "time": document.querySelector('input[name="willingTime"]').value,
        "price": document.querySelector('input[name="willingPrice"]').value
    }
    console.log(searchData)
    fetch('/api/booking',{
            method:'POST',
            body:JSON.stringify(searchData),
            headers: new Headers({
                "content-type":"application/json"
            })
        })
       
        .then(res => res.json())
        .then(function(data){
            console.log(data.data)
            if (data.data === "ok"){
                window.location.replace('/booking')
            }
            
        })

}


