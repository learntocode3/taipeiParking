TPDirect.setupSDK(123973, 'app_LhgynzZTeGWlcousyWdjL85xGDTh2rIMtCkMVdALfdKi3Hk768WvkNTjOTRl', 'sandbox')
let data;
const id = document.URL.split("/").slice(-1)
console.log(id[0])

// Display ccv field
let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
            'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        }
    }
})

const submitButton=document.querySelector('order-btn')

TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        submitButton.removeAttribute('disabled')
    } else {
        // Disable submit Button to get prime.
        submitButton.setAttribute('disabled', true)
        }
    })


const btn=document.querySelector('.order-Btn')
btn.addEventListener('click',onSubmit)    
function onSubmit(event) {
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('can not get prime')
        return
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }
        //alert('get prime 成功，prime: ' + result.card.prime)
        //console.log(result.card.prime)
        const orderData={
            'prime': result.card.prime,
            'id':id[0]
        }
        fetch('/api/user/card',{
            method:'POST',
            body: JSON.stringify(orderData),
            headers: new Headers({
        "content-type":"application/json"
            })
        })
        .then(res => res.json())
        .then(function(data){
            if (data.data === "ok"){
                alert('信用卡註冊成功，請進行登入')
                location.replace('/login');
            }
        })

        
    })
}