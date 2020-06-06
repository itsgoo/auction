console.log('hi main.js')


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
            // document.getElementById('id_start_auction').min = nextDate
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
			console.log('responce success' + response.acutal_dates_auctions)

		}
	})



})

















