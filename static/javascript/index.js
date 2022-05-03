const findSpace = document.querySelector("#findSpace")
const offerPlace = document.querySelector("#offerSpace")
const longterm = document.querySelector(".longTerm")
const rentNow = document.querySelector(".rentNow")
const rentNowBtn = document.querySelector(".matchRightNow")

rentNowBtn.addEventListener('click', sendSearchPlace)
rentNow.addEventListener('click', changetoRentNow)
longterm.addEventListener('click', changetoLongTerm)
findSpace.addEventListener('click', changeToFind)
offerPlace.addEventListener('click', changeToOffer)

function changeToOffer(){
    document.querySelector(".findSpaceInput").style.display="none";
    document.querySelector(".offerSpaceInput").style.display="flex";
    document.querySelector(".matchLongTerm").style.display="none";
    document.querySelector(".offerSpaceBtn").style.display="inline-block";
}

function changeToFind(){
    document.querySelector(".findSpaceInput").style.display="flex";
    document.querySelector(".offerSpaceInput").style.display="none";
}

function changetoLongTerm(){
    document.querySelector("#offerSpace").style.display="inline-block";
    document.querySelector(".matchRightNow").style.display="none";
    document.querySelector(".matchLongTerm").style.display="inline-block";
    
}

function changetoRentNow(){
    document.querySelector("#offerSpace").style.display="none";
    document.querySelector(".matchLongTerm").style.display="none";
    document.querySelector(".offerSpaceBtn").style.display="none";
    document.querySelector(".matchRightNow").style.display="inline-block";
}

function sendSearchPlace(e){
    e.preventDefault();

    const searchData={"address":document.querySelector('input[name="address"]').value}
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
        })

}