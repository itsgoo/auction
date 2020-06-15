

function btnBidEvent(event){

	const bidBtnId = event.target.id

	bidId = bidBtnId.replace('add_form_btn_','');
	const bidValueDirty = 'id_bid_' + bidId
	console.log('bidValueDirty ' + bidValueDirty)

	const bidValue = document.getElementById(bidValueDirty).value
	console.log('bidValue ' + bidValue)
	


	const confirmBid = 'form_send_bid_' + bidId
	const confirmBidInput = 'id_send_bid_' + bidId
	const confirmBidBtn = 'id_send_btn_' + bidId

	return new Promise((resolve, reject) =>{
		const confirmationPopUp = document.getElementById('exampleModal')
		console.log('confirmationPopUp'+confirmationPopUp)
		
		const formPopUp = confirmationPopUp.getElementsByTagName('form')[0].setAttribute('id', confirmBid)


		const ok = confirmationPopUp.getElementsByTagName('button')[1].setAttribute('id', confirmBidBtn)
		console.log('ok' + ok )


		console.log('formPopUp'+formPopUp)


		resolve(bidId)


		confirmationPopUp.getElementsByTagName('input')[1].setAttribute('id', confirmBidInput)

		confirmationPopUp.getElementsByTagName('option')[0].value = bidId
		


		document.getElementById(confirmBidInput).value= bidValue

		


		
	})
	.then((event) =>{

		addToBd(event)
		
	})
	.then(() => {


		const confirmationPopUp2 = document.getElementById('exampleModal')
		console.log('confirmationPopUp2' + confirmationPopUp2)
		confirmationPopUp2.classList.remove('show')
		confirmationPopUp2.style.display = "none"
		confirmationPopUp2.style.paddingRight = 0
		

	})
}

// function confirmation(event){
// 	closeBtnToPopUp(event){
		
// 	}
// }

function addToBd (event){

console.log('hi' + event)

$('.modal').on('click', '#id_send_btn_' + event, function() {



	var elementId = event
	console.log('elementId ' + event)

	var serializedData = $("#form_send_bid_" + elementId).serialize();
	console.log(serializedData)

	$.ajax({
		url: $("#form_send_bid_" + elementId).data('url'),
		data: serializedData,
		type: 'post',
		success: function(response){
			console.log('response.bid_data.new_bid ' + response.bid_data.new_bid)
			$('#bid_list_'  + elementId).append('<small>bid: ' + response.bid_data.bid + ' | </small>');
			
			if (response.bid_data.new_bid != undefined) {
				console.log('$(this)' + $(this))
				console.log('elementId' + elementId)
				console.log('response.bid_data.current_buyer' + response.bid_data.current_buyer)
				

				$('#actual_price_val_'  + elementId).replaceWith($('#actual_price_val_'  + elementId).text(response.bid_data.new_bid))

				$('#current_buyer_'  + elementId).replaceWith($('#current_buyer_'  + elementId).text(response.bid_data.current_buyer))

				$('#id_bid_' + elementId).val(response.bid_data.new_bid);


			};

		}
	})

	$('#form_send_bid_' + elementId)[0].reset();
	$('#add_form_' + elementId)[0].reset();


	const confirmationPopUp2 = document.getElementById('exampleModal')
	const confirmationPopUp3 = document.getElementsByClassName('modal-backdrop')[0]
	console.log('confirmationPopUp2' + confirmationPopUp2)
	confirmationPopUp2.classList.remove('show')
	confirmationPopUp2.style.display = "none"

	confirmationPopUp3.classList.remove('show')
	confirmationPopUp3.style.display = "none"
	

	const bodyTag = document.getElementsByTagName('body')[0]
	bodyTag.classList.remove('modal-open')
	bodyTag.style.paddingRight = 0
	showNotification(event)

});

}


function showNotification(event){



	return new Promise((resolve, reject) => {
		console.log('event ' + event)
		const toastEl = document.getElementById('toast-notification')
		console.log('toastEl' + toastEl)
		toastEl.classList.add('show')
		
		resolve(toastEl)
		const toastElClose = document.getElementById('close-notification').addEventListener('click', () => {
			toastEl.classList.remove('show')
	
	
		})
		
	})
	.then((elem) => {

		setTimeout((elem) => {
			const toastEl = document.getElementById('toast-notification')
			toastEl.classList.remove('show')
	
		}, 5000);
	
	})



}









// $('.main_cards').on('click', '.btn_confirm', function() {



// 	var elementId = $(this).data('id');
// 	console.log(elementId)

// 	var serializedData = $("#add_form_" + elementId).serialize();
// 	console.log(serializedData)

// 	$.ajax({
// 		url: $("#add_form_" + elementId).data('url'),
// 		data: serializedData,
// 		type: 'post',
// 		success: function(response){
// 			console.log(response.bid_data.new_bid)
// 			$('#bid_list_'  + elementId).append('<small>bid: ' + response.bid_data.bid + ' | </small>');
// 			if (response.bid_data.new_bid != undefined) {
// 				console.log($(this))
// 				$('#actual_price_val_'  + elementId).replaceWith($('#actual_price_val_'  + elementId).text('actual price: ' + response.bid_data.new_bid))
// 			};

// 		}
// 	})

// 	$('#add_form_' + elementId)[0].reset();
	
// });

































// var csrfJqToken = $('input[name=csrfmiddlewaretoken]').val();


//     console.log('csrfJqToken', csrfJqToken)

// function BidButtonClickHandler(event){

// 	event.preventDefault()

//     const form = event.target.form

//     const token = form.querySelector('input').value
//     const bid = form.querySelector('#id_bid').value
//     const auctionId = form.querySelector('#id_auction').value
//     const buyerId = form.querySelector('#id_buyer_id').value
//     // // const getPath = form.querySelector('#id_buyer_id').value
//     // const csrfToken = form.getELementsByName('csrfmiddlewaretoken')

//     // console.log('csrfToken', csrfToken)
//     console.log(form)
//     console.log(token)

//     const path = "/"


// // csrfmiddlewaretoken=DlhBFzzzEHMBXl6wugLhptiCIsBLiRM6zvNF80d8S4CELSM466j66xbZlXJ04leR&bid=145&auction=17&buyer_id=9

// 	const jsonStr = 'csrfmiddlewaretoken=' + csrfJqToken + '&bid=' + bid + '&auction=' + auctionId + '&buyer_id=' + buyerId

//     console.log('jsonStr', jsonStr)

//     const auction = {
//     	csrfmiddlewaretoken: csrfJqToken,
//     	bid: bid,
//     	auction: auctionId,
//     	buyer_id: buyerId,
//     }


//     const xhr = new XMLHttpRequest()

//     const json = JSON.stringify({

//     	csrfmiddlewaretoken: csrfJqToken,
//     	bid: bid,
//     	auction: auctionId,
//     	buyer_id: buyerId,
//     	})

//     console.log('json', json)
//     xhr.open('POST', path)
//     xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');

//     xhr.send(jsonStr)

// }
