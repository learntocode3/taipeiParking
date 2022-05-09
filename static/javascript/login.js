const base_url = "http://127.0.0.1:3000"
const userAPI= `${base_url}/api/user`;

const signIn=document.querySelector('.memberSignIn')
signIn.addEventListener('click', memberSignin)

function memberSignin(e){
    e.preventDefault;
    // 從前端拿到input資料換成json格式
    const email = document.querySelector('input[name="email"]')
    const password = document.querySelector('input[name="password"]')
    const data={
        'email': email.value,
        'password': password.value 
    };
    // 把資料裝在body發送request到後端api
    fetch (userAPI,{
        method: "PATCH",
        body: JSON.stringify(data),
        headers: new Headers({
            "content-type":"application/json"
        })
    })
    .then(response => response.json())
    .then(function(data){
        if (data.ok === true){
            location.replace("/");
        } else {
            document.querySelector('.status').innerText='登入失敗，請註冊';
        }
    })

}
