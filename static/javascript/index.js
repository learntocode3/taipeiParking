const findSpace = document.querySelector("#findSpace")
const offerPlace = document.querySelector("#offerSpace")
const longterm = document.querySelector(".longTerm")
const rentNow = document.querySelector(".rentNow")
const rentNowBtn = document.querySelector(".matchRightNow")
const offerSpaceBtn = document.querySelector(".offerSpaceBtn")

offerSpaceBtn.addEventListener('click', sendOfferPlace)
rentNowBtn.addEventListener('click', sendSearchPlace)
rentNow.addEventListener('click', changetoRentNow)
longterm.addEventListener('click', changetoLongTerm)
findSpace.addEventListener('click', changeToFind)
offerPlace.addEventListener('click', changeToOffer)

function changeToOffer(){
    document.querySelector(".findSpaceInput").style.display="none";
    document.querySelector(".offerSpaceInput").style.display="flex";

    document.querySelector(".offerSpaceBtn").style.display="inline-block";
}

function changeToFind(){
    document.querySelector(".findSpaceInput").style.display="flex";
    document.querySelector(".offerSpaceInput").style.display="none";
}

function changetoLongTerm(){
    document.querySelector("#offerSpace").style.display="inline-block";
    document.querySelector(".matchRightNow").style.display="none";
}

function changetoRentNow(){
    document.querySelector("#offerSpace").style.display="none";
    document.querySelector(".offerSpaceBtn").style.display="none";
    document.querySelector(".matchRightNow").style.display="inline-block";
}

function sendSearchPlace(e){
    e.preventDefault();

    const searchData={"address":document.querySelector('input[name="willingAddress"]').value}
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


function sendOfferPlace(e){
    e.preventDefault();

    const offerData={"address": document.querySelector('input[name="offerAddress"]').value,
                     "price": document.querySelector('input[name="offerPrice"]').value,
                     "time": {
                         "section-1-start": document.getElementById('section-1-start').value,
                         "section-1-end": document.getElementById('section-1-end').value,
                         "section-2-start": document.getElementById('section-2-start').value,
                         "section-2-end": document.getElementById('section-2-end').value,
                         "section-3-start": document.getElementById('section-3-start').value,
                         "section-3-end": document.getElementById('section-3-end').value
                     } 
}
    console.log(offerData)





}