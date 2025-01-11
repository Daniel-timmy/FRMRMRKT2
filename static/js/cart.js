var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		var qty = this.dataset.qty
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)
		console.log('qty:', qty)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, qty, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})	
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, productqty, action){
	console.log('User is not authenticated')
	console.log(productqty)

	if (action == 'add'){
		if (cart[productId] == undefined){
			if (productqty <= 0){
				return
			}
			cart[productId] = {'quantity':1}

		}else{
			if (productqty < (cart[productId]['quantity'] + 1)) {
			return
			}
			cart[productId]['quantity'] += 1
			console.log('Item quantity increased')
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}