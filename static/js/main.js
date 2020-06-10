
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

























const currentAuctionId = document.getElementById('current_auction_id').textContent
const startTimeVal = document.getElementById('start_time_id_' + currentAuctionId).textContent
console.log('startTimeVal' + startTimeVal)
 


var remain_bv   = 3600;
function parseTime_bv(timestamp){
    if (timestamp < 0) timestamp = 0;
 
    var day = Math.floor( (timestamp/60/60) / 24);
    var hour = Math.floor(timestamp/60/60);
    var mins = Math.floor((timestamp - hour*60*60)/60);
    var secs = Math.floor(timestamp - hour*60*60 - mins*60); 
    var left_hour = Math.floor( (timestamp - day*24*60*60) / 60 / 60 );
 
    $('span.afss_day_bv').text(day);
    $('span.afss_hours_bv').text(left_hour);
 
    if(String(mins).length > 1)
        $('span.afss_mins_bv').text(mins);
    else
        $('span.afss_mins_bv').text("0" + mins);
    if(String(secs).length > 1)
        $('span.afss_secs_bv').text(secs);
    else
        $('span.afss_secs_bv').text("0" + secs);
     
}
 
$(document).ready(function(){
    setInterval(function(){
        remain_bv = remain_bv - 1;
        parseTime_bv(remain_bv);
        if(remain_bv <= 0){
            alert('Hello');
        }
    }, 1000);
});








}