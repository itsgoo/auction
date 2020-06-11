
// create auction page
const queryString = window.location
if(queryString == 'http://127.0.0.1:8000/create'){




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













// home page
const queryStringMain = window.location
if(queryStringMain == 'http://127.0.0.1:8000/'){



const userStatus = document.getElementById('not_auth')

console.log('userStatus' + userStatus.textContent)

if(userStatus.textContent == 'someoneelse'){
    bidUpfunc()
}



function bidUpfunc(){

    const bidPlusValVal = document.getElementById('bidminus')
    const inputIdMain = bidPlusValVal.parentNode.id.replace('bids_thing_', '')
    
    
    // // load actual price in reload moment
    const inputBidMain = document.getElementById('id_bid_' + inputIdMain)
    
    const actualPriceVal = document.getElementById('actual_price_val_' + inputIdMain).textContent
    
    
    
    inputBidMain.value = actualPriceVal
    
    
    
    const bidUp = bidPlusValVal.value
    
    
    
    
    
    var wrapper = document.querySelector('wr');
    
    var countInput = document.getElementById('id_bid_' + inputIdMain);
    
    
    
    var butM = document.getElementById('bidminus');
    var butP = document.getElementById('bidplus');
    var units = countInput.value.replace(/\d/g, '');
    console.log('units' + units)
    
    butM.onclick = function(){
        if(parseInt(countInput.value) > 1) {
            if(parseInt(countInput.value) == actualPriceVal){
                console.log('its minimum ' + actualPriceVal)
                console.log('parseInt(countInput.value) ' + parseInt(countInput.value))
    
            }
            console.log('bidUp butM ' + typeof Number(bidUp))
            countInput.value = parseInt(countInput.value)-  Number(bidUp) + units;
        }
    };
    butP.onclick = function(){
        if(parseInt(countInput.value) > 1) {
            console.log('bidUp butP ' + typeof Number(bidUp))
            countInput.value = parseInt(countInput.value)+  Number(bidUp) + units;
        }
    };
    
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

    // console.log ( 'startDateSec' +startDateSec )
    // console.log ( 'endDateSec' +endDateSec )

    // console.log ( 'startDate' +startDate )
    // console.log ( 'endDate' +endDate )



    // 7947365000




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

        const timeMsg = 'Auction was over. Winner is: ' + spanCurrentBuyer.textContent
        divTimer.innerHTML = timeMsg

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






}

timer2 = setInterval(updateClock2, 1000);





}