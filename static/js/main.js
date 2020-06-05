console.log('hi main.js')


const rad = document.createAuctionForm.myRadios
const prev = null
for( i = 0; i < rad.length; i++) {
    rad[i].addEventListener('change', function() {
        console.log('prev.value ' + this.value)

        if (prev != null){
            console.log(prev)
        }

        if(this.value != prev) {
            console.log('prev' + prev)
            console.log('this' + this)
            prev = this.value
        }
        console.log('this.value' + this.value)
        console.log('prev' + prev)
    });
}
