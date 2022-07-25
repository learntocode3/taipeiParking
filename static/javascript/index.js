// send request
statusCheck();
const mapTest = document.querySelector('.mapTest')
const rentNowBtn = document.querySelector(".matchRightNow")
const userInputAddress=document.querySelector('input[name="willingAddress"]')

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
    if(searchData.start > searchData.end){
      alert('Please enter valid time')
      window.location.replace('/')
    }
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

// get User current location
const getCurrentLocation = document.querySelector('.getCurrentLocation');
getCurrentLocation.addEventListener('click', getLocation)
//getLocation();

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else { 
    console.log("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  //console.log("Latitude: " + position.coords.latitude + 
  //"Longitude: " + position.coords.longitude);
  let loca = {'latitude':position.coords.latitude, 'longtitude':position.coords.longitude}
  fetch('/api/getUserLocation',{
    method:'POST',
    body:JSON.stringify(loca),
    headers: new Headers({
        "content-type":"application/json"
    })
})
  .then(res => res.json())
  .then(function(data){
      //console.log(data.data)
      userInputAddress.defaultValue=data.data;
      //mapTest.setAttribute('src',`https://www.google.com/maps/embed/v1/place?q=${data.data}`);
  })


}

function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
        console.log("User denied the request for Geolocation.")
      break;
    case error.POSITION_UNAVAILABLE:
        console.log("Location information is unavailable.")
      break;
    case error.TIMEOUT:
        console.log("The request to get user location timed out.")
      break;
    case error.UNKNOWN_ERROR:
        console.log("An unknown error occurred.")
      break;
  }
}
