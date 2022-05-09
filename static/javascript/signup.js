const base_url = "http://127.0.0.1:3000"
const userAPI= `${base_url}/api/user`;

const signUp=document.querySelector('.memberSignUp')
signUp.addEventListener('click', memberSignUp)

function memberSignUp(e){
    e.preventDefault;
    // 從前端拿到input資料換成json格式
    const name = document.querySelector('input[name="name"]')
    const email = document.querySelector('input[name="email"]')
    const password = document.querySelector('input[name="password"]')

    const data={
        'name' : name.value,
        'email': email.value,
        'password': password.value 
    };

    // 把資料裝在body發送request到後端api
    fetch (userAPI,{
        method: "POST",
        body: JSON.stringify(data),
        headers: new Headers({
            "content-type":"application/json"
        })
    })
    .then(response => response.json())
    .then(function(data){
        if (data.error === true){
            document.querySelector('.status').innerText=data.message;
        } else {
            document.querySelector('.status').innerText="註冊成功，請點選登入";
        }
    })

}