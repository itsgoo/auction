

const queryString = window.location
if(queryString == 'http://127.0.0.1:8000/create'){




const rad = document.createAuctionForm.myRadios

let prev = null
for( i = 0; i < rad.length; i++) {
    rad[i].addEventListener('change', function() {
    const now = new Date();
    console.log( now )
    const nextDay = now.getDate() + 1
    const actualMonth = now.getMonth() + 1
    const nextDate =  now.getFullYear() + '-0' + actualMonth + '-0' + nextDay

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



const bidMinusVal = document.getElementById('bidminus')
const bidPlusVal = document.getElementById('bidplus')



const bidPlusValVal = document.getElementById('bidminus')

const inputIdMain = bidPlusValVal.parentNode.id.replace('bids_thing_', '')

const inputBidMain = document.getElementById('id_bid_' + inputIdMain)

const actualPriceVal = document.getElementById('actual_price_val_' + inputIdMain).textContent

inputBidMain.value = actualPriceVal






bidMinusVal.addEventListener('click', (event) => {
    console.log(event.target.value)
    

    const inputId = event.target.parentNode.id.replace('bids_thing_', '')
    console.log(inputId)

    const inputBid = document.getElementById('id_bid_' + inputId)


})








