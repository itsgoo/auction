
// create auction page
const queryString = window.location
if(queryString == 'http://127.0.0.1:8000/create' || queryString == 'http://127.0.0.1:8000/en/create'){




const rad = document.createAuctionForm.myRadios

let prev = null
for( i = 0; i < rad.length; i++) {
    rad[i].addEventListener('change', function() {
    const now = new Date();
    console.log( now )



    let actualMonth = String(now.getMonth() + 1);
    let nextDay = String(now.getDate() + 1);
    const year = String(now.getFullYear());
  
    if (actualMonth.length < 2) actualMonth = '0' + actualMonth;
    if (nextDay.length < 2) nextDay = '0' + nextDay;






  
    const nextDate =  now.getFullYear() + '-' + actualMonth + '-' + nextDay

    console.log('nextDate ' + nextDate)
    console.log('now.getMonth() ' + now.getUTCMonth())
    console.log('now.getDate() ' + now.getDate())
    
    const formStartAuction = document.getElementById('idStartAuction')

        if(this.value != prev) {
            prev = this.value
        }
        console.log('prev ' + this.id)
        

        if (prev == 'automatic'){
            console.log('prev == automatic ' + prev)
            formStartAuction.classList.remove('show_start_auction')
            document.getElementById('id_start_auction').value = '0001-01-01'

        }else if(prev == 'manual'){
            console.log('prev == manual ' + prev)
            formStartAuction.classList.add('show_start_auction')
            document.getElementById('id_start_auction').value =  nextDate
            document.getElementById('id_start_auction').min = nextDate


            const selectDivErase = document.getElementById('id_start_auction_time')

            selectDivErase.innerHTML = ``


        }




        

    })
}



const btnDateField = document.getElementById('choose_free_time')


btnDateField.addEventListener('click', (event) => {

    var serializedData = $("#id_start_auction").serialize();
	console.log(serializedData)

	$.ajax({
		url: "/create/",
		data: serializedData,
		type: 'get',
		success: function(response){



            const fieldTime = document.getElementById('field_shoise_time_id')
            fieldTime.classList.add('show_start_auction')


            const responseData = response.acutal_dates_auctions
			console.log('response success' + responseData)
            const selectDiv = document.getElementById('id_start_auction_time')

            selectDiv.innerHTML = ``
            const obj = JSON.parse(responseData)






            let busyDates = new Array
            let currentFreeDates = new Array

            obj.forEach(element => {
                console.log('obj success element ' + element.fields.active_date_time)
                const valueTime = element.fields.active_date_time

                busyDates.push(valueTime)

            })






            Array.from(new Array(24), (x,i) => {

                currentFreeDates.push(i)

            })

            
            busyDates.forEach(busyElement => {
                // console.log('busyElement ' + busyElement)
                
                currentFreeDates.forEach(freeElement => {

                    if(freeElement == busyElement ){

                        delete currentFreeDates[busyElement]
                    }

                })
            })


            currentFreeDates.forEach(freeElement => {

                    
            selectDiv.innerHTML = selectDiv.innerHTML + `<option value="` + freeElement + `" >` + freeElement + `</option>`


            })

		}
	})

})

}











function t(){
    if (location.pathname.split('/')[1] == 'en'){
        return 'En'
    }else{
        return ''
    }
}

window.scrollTo( 0, 1 );

// home page
const queryStringMain = window.location
if(queryStringMain == 'http://127.0.0.1:8000/' || queryStringMain == 'http://127.0.0.1:8000/en/'){






const userStatus = document.getElementById('not_auth')



// check user status
console.log('userStatus' + userStatus.textContent)

if(userStatus.textContent == 'someoneelse'){
    bidUpfunc()
}



function bidUpfunc(){

    const bidPlusValVal = document.getElementById('bidminus')
    const inputIdMain = bidPlusValVal.parentNode.id.replace('bids_thing_', '')
    
    // load actual price in reload moment
    const inputBidMain = document.getElementById('id_bid_' + inputIdMain)
    
    const actualPriceVal = document.getElementById('actual_price_val_' + inputIdMain).textContent
    
    inputBidMain.value = actualPriceVal
    
    const bidUp = bidPlusValVal.value
    
    
    var countInput = document.getElementById('id_bid_' + inputIdMain);
    
    var butM = document.getElementById('bidminus');
    var butP = document.getElementById('bidplus');
    var units = countInput.value.replace(/\d/g, '');
    console.log('units' + units)
    
    const bidFirstBtn = document.getElementById('add_form_btn_' + inputIdMain)
    bidFirstBtn.classList.add('disabled')
    bidFirstBtn.setAttribute("disabled", "true")

    const minimumBid = Number(actualPriceVal) + Number(bidUp)
    console.log('minimumBid ' + minimumBid)


    butM.onclick = function(){
        if(parseInt(countInput.value) > actualPriceVal) {
            


            console.log('bidUp butM typeof' + typeof Number(bidUp))
            console.log('bidUp butM ' + bidUp)
            countInput.value = parseInt(countInput.value)-  Number(bidUp) + units;

            activeBidButton()



        }
    };




    butP.onclick = function(){
        if(parseInt(countInput.value) > 1) {
            console.log('bidUp butP ' + typeof Number(bidUp))
            countInput.value = parseInt(countInput.value)+  Number(bidUp) + units;
            activeBidButton()
        }
    };
    


    function activeBidButton() {

        if(parseInt(countInput.value) < minimumBid){
            console.log('its minimum ' + minimumBid)
            console.log('parseInt(countInput.value) ' + parseInt(countInput.value))
            bidFirstBtn.classList.add('disabled')
            bidFirstBtn.setAttribute("disabled", "true")
            

        }else if(parseInt(countInput.value) >= minimumBid){
            console.log('its ok ' + minimumBid)
            bidFirstBtn.classList.remove('disabled')
            bidFirstBtn.removeAttribute('disabled')
        }
    }







}






























function updateClock2() {

    const currentAuctionId = document.getElementById('current_auction_id').textContent
    let startTimeVal = document.getElementById('start_time_id_' + currentAuctionId).textContent
    let clearHourVal = startTimeVal.replace(':00', '')
    clearHourVal = Number(clearHourVal) + 1
    
    // console.log('clearHourVal' + clearHourVal)
    
    // текущая дата
    const date = new Date()

    // час в текущей временной зоне
    // console.log('time' + date.getTime())
    // console.log('date' + date.getDate())
    // console.log( date.getHours() )
    // console.log ( date.getMinutes() )
    // console.log ( date.getSeconds() )



    let actualMonth1 = String(date.getMonth())
    let nextDay1 = String(date.getDate())
    let nextDay2 = String(date.getDate() + 1)
    const year = String(date.getFullYear())

    const startDate = new Date(year, actualMonth1, nextDay1 , date.getHours(), date.getMinutes(), date.getSeconds())
    let startDateSec = Math.round(startDate.getMinutes())






    const endDate = new Date(year, actualMonth1, nextDay1, clearHourVal, 00, 00)

    let endDateSec = Math.round(endDate.getMinutes())





    delta = (endDate - startDate)/1000
    // console.log ( 'delta ' +delta )
    const day1 = Math.floor( (delta/60/60) / 24)


    let minLeft = Math.floor(delta/60)
    let secLeft = Math.floor(delta- (minLeft*60))

    minLeft = String(minLeft)
    secLeft = String(secLeft)

    if (secLeft.length < 2){
        secLeft = '0' + secLeft
    }
    if (minLeft.length < 2){
        minLeft = '0' + minLeft
    }

    if (minLeft == '00' && secLeft == '00' ){

        const divTimer = document.getElementById('timer_' + currentAuctionId)
        const spanCurrentBuyer = document.getElementById('current_buyer_' + currentAuctionId)




        this['leader' + t()] = 'Leader'

        const leader = 'מַנהִיג'

        const leaderT = t() == 'En' ? leaderEn : leader




        this['timeMsg' + t()] = 'Auction was over'

        const timeMsg = 'המכרז הסתיים'

        const timeMsgT = t() == 'En' ? timeMsgEn : timeMsg

        divTimer.innerHTML = timeMsgT

        const bidForm = document.getElementById('add_form_' + currentAuctionId)
        bidForm.innerHTML = 'Auction was closed'

        const divCurrentBuyer = document.getElementById('current_buyer_div_' + currentAuctionId)
        divCurrentBuyer.innerHTML = ''

    }else{

        // console.log ( 'day1 ' +day1 )
        // console.log ( 'minLeft ' +minLeft )
        // console.log ( 'secLeft ' +secLeft )
    
        const divMin = document.getElementById('timer_min_' + currentAuctionId)
        const divSec = document.getElementById('timer_sec_' + currentAuctionId)
    
        divMin.innerHTML = minLeft
        divSec.innerHTML = secLeft
    }


    setProgressSec(secLeft)
    setProgresMin(minLeft)



}

timer2 = setInterval(updateClock2, 1000);




const circleSec = document.querySelector('.progress_ring_circle_sec')
const radiusSec = circleSec.r.baseVal.value
const curcumferenceSec = 2 * Math.PI * radiusSec

circleSec.style.strokeDasharray = `$(curcumferenceSec) $(curcumferenceSec)`
circleSec.style.strokeDasharray = curcumferenceSec

function setProgressSec(percent){
    const offset = curcumferenceSec - percent / -60 * curcumferenceSec
    circleSec.style.strokeDashoffset = offset
}



const circleMin = document.querySelector('.progress_ring_circle_min')
const radiusMin = circleMin.r.baseVal.value
const curcumferenceMin = 2 * Math.PI * radiusMin

circleMin.style.strokeDasharray = `$(curcumferenceMin) $(curcumferenceMin)`
circleMin.style.strokeDasharray = curcumferenceMin

function setProgresMin(percent){
    const offset = curcumferenceMin - percent / -60 * curcumferenceMin
    circleMin.style.strokeDashoffset = offset
}












// get notification about next acutions

console.log('document.notif_form' + document.notif_form.auction.textContent)

function getNotification(event, id){
    console.log('getNotification')
    return new Promise ((reslove, reject) => {
        console.log('Promise')
        const notifModalDiv = document.getElementById('get_notification')
        const notifForm = notifModalDiv.getElementsByTagName('form')[0]
        notifForm.setAttribute('id', 'form_notif_' + id)
        let selectAuction = notifForm.getElementsByTagName('select')[0]
        let selectOption = selectAuction.getElementsByTagName('option')[0].setAttribute('value', id)
    

        document.getElementById('close').id = 'close_' + id
        document.getElementById('btn_notif').id = 'btn_notif_' + id



        reslove(id)

    })
    .then((id) =>{





        const btnNotifId = document.getElementById('btn_notif_' + id)
        console.log('btnNotifId' + btnNotifId.id)
        let count = 0

        
        btnNotifId.addEventListener('click', (event) => {
            count ++
            console.log('count' + count)
            console.log('event' + event)



            console.log('document.notif_form reset_ ' + document.notif_form.auction.value)
            console.log('document.notif_form reset_ ' + document.notif_form.subscriber.value)

            serializedData = $("#form_notif_" + id).serialize();



            console.log('data form')

            console.log('serializedData' + serializedData)
            
            $.ajax({
                url: $("#form_notif_" + id).data('url'),
                data: serializedData,
                type: 'post',
                success: function(response){
                    console.log('success send')
                    const btnNotifId = document.getElementById('call_notif_' + id).setAttribute('disabled', 'disabled')

        
                }
            })


            removePopUp('get_notification')

            let textForNote = 'we will notify you about the beginning of the auction'
            showNotification(textForNote)

        })



        const btnNotifCLose = document.getElementById('close_' + id)
        btnNotifCLose.addEventListener('click', (event) => {

            
            btnNotifCLose.id = 'close'
            btnNotifId.id = 'btn_notif'

            document.notif_form.reset()
            console.log('document.notif_form_ ' + document.notif_form.auction.value)


        })






        return id

    })
    .then((id) => {
        
        let btnNotifIdDel = document.getElementById('btn_notif_' + id).id = 'btn_notif'
        document.notif_form.reset();

    })

}





















}








// reports page
if(queryStringMain == 'http://127.0.0.1:8000/reports' || queryStringMain == 'http://127.0.0.1:8000/en/reports'){

const tableItems = document.getElementById('table_items')
let colIndex = -1


const sortTable = function(elIndex, dataType, isSorted){

    console.log('el TH elIndex' + elIndex)
    const tbody = tableItems.querySelector('tbody')

    const compare = function(rowPrev, rowNext) {


        const rowDataPrev =  rowPrev.cells[elIndex].innerHTML
        const rowDataNext =  rowNext.cells[elIndex].innerHTML


        switch (dataType){
            case 'integer':
                // console.log(rowDataPrev - rowDataNext)
                return rowDataPrev - rowDataNext
                break
            case 'text':
                if(rowDataPrev < rowDataNext) return -1
                else if(rowDataPrev > rowDataNext) return 1
                return 0
                break
        }


        
    }

    let rows = [].slice.call(tbody.rows)

    // console.log('rows' + rows)
    rows.sort(compare)

    if (isSorted) rows.reverse()

    tableItems.removeChild(tbody)

    for (i = 0; i < rows.length; i++){
        tbody.appendChild(rows[i])
    }

    tableItems.appendChild(tbody)

}

tableItems.addEventListener('click', (event) => {
    
    const el = event.target
    // const el = event.target.textContent


    if (el.nodeName != 'TH') return;

    const elIndex = el.cellIndex

    // let sorted = [...winnerSortEl].sort()
    // console.log('items' + sorted)
    const dataType = el.getAttribute('data-type')

    sortTable(elIndex, dataType, colIndex == elIndex)
    colIndex = (colIndex == elIndex) ? -1 : elIndex

})

















}







