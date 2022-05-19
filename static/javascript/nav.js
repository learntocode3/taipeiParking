// nav bar
const mainPage = document.querySelector(".left")
const rentNow = document.querySelector(".rentNow")
const offerPlace = document.querySelector(".offerNow")
const login = document.querySelector(".signIn")
const signup = document.querySelector(".signUp")
const logOut = document.querySelector(".logOut")
const member = document.querySelector(".member")

mainPage.addEventListener('click', directToMainPage)
rentNow.addEventListener('click', changetoRentNow)
offerPlace.addEventListener('click', directToOfferPage)
login.addEventListener('click', directToLogInPage)
logOut.addEventListener('click', logout)
signup.addEventListener('click', directToSignUpPage)
member.addEventListener('click', directToMemberPage)

function changetoRentNow(){
    window.location.replace('/');
}
function directToMainPage(){
    window.location.replace('/');
}
function directToOfferPage(){
    window.location.replace('/offer');
}
function directToLogInPage(){
    window.location.replace('/login');
}
function directToSignUpPage(){
    window.location.replace('/signup');
}
function directToMemberPage(){
    window.location.replace('/member');
}

function statusCheck(){
    fetch('/api/user')
    .then(res => res.json())
    .then(function(data){
        console.log(data.data)
        console.log(data.orderid)
        if (data.data === null){
            alert('please login or sign up');
            location.replace("/login");
        } else if(data.orderid !== null) {
            location.replace(`/order/${data.orderid}`)
        } else {
            login.style.display='none';
            logOut.style.display='inline-block';
            signup.style.display='none';
            member.style.display='inline-block'
        }
    })
}

// function checkIfExistOrder(){
//     fetch('/api/user')
//     .then(res => res.json())
//     .then(function(data){
//         console.log(data.data)
//         if (data.data === null){
//             alert('please login or sign up');
//             location.replace("/login");
//         } else {
//             login.style.display='none';
//             logOut.style.display='inline-block';
//             signup.style.display='none';
//             member.style.display='inline-block'
//         }
//     })
// }


function logout(){
    fetch ('/api/user', {method:"DELETE"});
    location.replace("/login");
}

// statusCheck();