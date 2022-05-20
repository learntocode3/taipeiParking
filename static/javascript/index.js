// send request
statusCheck();
const rentNowBtn = document.querySelector(".matchRightNow")

rentNowBtn.addEventListener('click', sendSearchPlace)

function sendSearchPlace(e){
    e.preventDefault();
    const searchData={
        "address": document.querySelector('input[name="willingAddress"]').value,
        "price": document.querySelector('input[name="willingPrice"]').value,
        "start": document.getElementById('start').value,
        "end": document.getElementById('end').value,
    }
    document.querySelector('.mask').style.display = "block";
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
                document.querySelector('.mask').style.display = "none";
                window.location.replace('/booking')
            }
            
        })

}


