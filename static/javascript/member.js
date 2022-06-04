statusCheck();

const offerList=document.querySelector('.spaceList');
const orderList=document.querySelector('.orderList');

const unfinishedList=document.querySelector('.unfinished-list');
const finishedList=document.querySelector('.finished-list');
const changeCredit=document.querySelector('.changeCredit');

const memberInfo=document.querySelector('.memberInfo');
const memberInfoList=document.querySelector('.memberInfoList');

let orderOffset = 0;

const updateSpace=document.querySelector('.updateSpace')
const allOrder=document.querySelector('.allOrder')

updateSpace.addEventListener('click', getOfferList)
allOrder.addEventListener('click', getAllOrder)
changeCredit.addEventListener('click', directToChangeCredit)
memberInfo.addEventListener('click', getMemberInfo)

function directToChangeCredit(){
    fetch('/api/user')
    .then(res => res.json())
    .then(function(data){
        location.replace(`/card/${data.memberId}`);
    })
    
}

function getMemberInfo(){
    document.querySelector('.spaceList').style.display = "none";
    document.querySelector('.orderList').style.display = "none";
    document.querySelector('.memberInfoList').style.display = "flex";
    fetch('/get/revenue')
    .then(res => res.json())
    .then(function(data){
        console.log(data.data)
        let totalRev=0;
        for(let i=0; i<data.data.length; i++){
            totalRev = totalRev + data.data[i][3]
        }
        const revenue=document.createElement('div');
        
        if (data.data.length === 0){
            revenue.innerText = '會員' + data.data[0][0] + '您好，您的帳戶目前還沒有收益';
        } else {
            revenue.innerText = '會員' + data.data[0][0] + `您好，您的帳戶目前有${data.data.length}比成立的訂單，總共累積的收益為` + `${totalRev}` + '元';
            const withDraw=document.createElement('button');
            withDraw.classList = 'withDraw'
            withDraw.innerText = '點擊提取'
            withDraw.addEventListener('click', function(){
                alert('客服將與您聯繫確認')
            })
            revenue.appendChild(withDraw)
        }
        memberInfoList.appendChild(revenue)
    })
}


function getOfferList(){
    document.querySelector('.orderList').style.display = "none";
    document.querySelector('.memberInfoList').style.display = "none";
    document.querySelector('.spaceList').innerHTML = "";
    document.querySelector('.spaceList').style.display = "flex";
    fetch('/get/supply')
    .then(res => res.json())
    .then(function(data){
        console.log(data.data)
        for (let i=0; i<data.data.length; i++){
            const item=document.createElement('div')
            item.classList.add("item")
        
            const place=document.createElement('div')
            place.innerText = data.data[i][2]
        
            const address=document.createElement('div')
            address.innerText=data.data[i][3]

            const number=document.createElement("div")
            number.innerText= "車位號碼" + data.data[i][4]
        
            const fee=document.createElement("div")
            fee.innerText= data.data[i][7] + "/hr"
        
            const alter=document.createElement("button")
            alter.innerText= " 修改資料 ";

            alter.addEventListener('click', function(){
                location.replace(`/alter/${data.data[i][1]}`);
            })

            item.appendChild(place);
            item.appendChild(address);
            item.appendChild(number);
            item.appendChild(fee);
            item.appendChild(alter);
            offerList.appendChild(item)

        }
        
    })
}


function getAllOrder(){
    document.querySelector('.spaceList').style.display = "none";
    document.querySelector('.memberInfoList').style.display = "none";
    fetch('/api/allOrder'+'?orderOffset='+orderOffset)
    .then(res => res.json())
    .then(function(data){
        console.log(data.unfinish)
        console.log(data.finish)
        //document.querySelector('.orderList').innerHTML = "";
        document.querySelector('.orderList').style.display = "flex";
        if (data.unfinish.length !== 0){
            for(let i=0; i < data.unfinish.length; i++ ){
            
            const unfin=document.createElement('div')
            unfin.classList.add('unfin')

            const orderId = document.createElement('div')
            orderId.innerText = '訂單號碼：' + data.unfinish[i][0]

            const address = document.createElement('div')
            address.innerText = '停車地址：' + data.unfinish[i][1]

            const start = document.createElement('div')
            start.innerText = '開始時間：' + data.unfinish[i][2]

            const toOrderPage = document.createElement('a')
            toOrderPage.href = `/order/${data.unfinish[i][0]}`;
            toOrderPage.innerText = '前往訂單'


            unfin.appendChild(orderId)
            unfin.appendChild(address)
            unfin.appendChild(start)
            unfin.appendChild(toOrderPage)

            unfinishedList.appendChild(unfin)
            }

        }


        for(let i=0; i < data.finish.length; i++ ){
            
            const fin=document.createElement('div')
            fin.classList.add('fin')

            const orderId = document.createElement('div')
            orderId.innerText = '訂單號碼：' + data.finish[i][0]

            const address = document.createElement('div')
            address.innerText = '停車地址：' + data.finish[i][1]

            const start = document.createElement('div')
            start.innerText = '開始時間：' + data.finish[i][2]

            const end = document.createElement('div')
            end.innerText = '結束時間：' + data.finish[i][3]

            const fee = document.createElement('div')
            fee.innerText = '總共花費：' + data.finish[i][4]

            fin.appendChild(orderId)
            fin.appendChild(address)
            fin.appendChild(start)
            fin.appendChild(end)
            fin.appendChild(fee)
            finishedList.appendChild(fin)
        }
        
        

    })
    orderOffset++;
}
