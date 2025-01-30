var updateProductsBtns = document.getElementsByClassName('update-product');
var overlay = document.getElementById('overlay');
var overlayActionButton = document.getElementById('overlay-action-button');

var showBtns = document.getElementsByClassName('show')
var overlayStatus = document.getElementById('overlay-shipping-status');
var overlayShippingBtn = document.getElementById('overlay-shipping-button');



overlayActionButton.addEventListener('click', function() {
    var productId = this.dataset.product;
    productName = document.getElementById('product-name').value
    productDescription = document.getElementById('product-description').value
    productPrice = document.getElementById('product-price').value 
    productQuality = document.getElementById('product-quantity').value
    console.log(productName, productQuality, productPrice, productDescription)
    var productData = {
        name: productName,
        quantity: productQuality,
        price: productPrice,
        description: productDescription
    };
    console.log('Performing action for product ID:', productId);
    updateProduct(productId, 'update', productData);
});

overlayShippingBtn.addEventListener('click', function() {
	var itemId = this.dataset.item;
	var pstatus = document.getElementById('status').value
	var shippingStatus = {
		status: pstatus
	};
	console.log('Performing action for product ID:', itemId);
	console.log(shippingStatus)
	updateOrderItem(itemId, 'update', shippingStatus);
})


function closeOverlay() {
    overlay.style.display = 'none';
	overlayStatus.style.display = 'none';
}

for (var j = 0; j < showBtns.length; j++){
	showBtns[j].addEventListener('click', function(){
		document.getElementById('itemId').innerHTML += this.dataset.id
		document.getElementById('date_added').innerHTML += this.dataset.dateadded
		document.getElementById('transaction_id').innerHTML += this.dataset.transactionid
		document.getElementById('quantity').innerHTML += this.dataset.quantity
		document.getElementById('product_name').innerHTML += this.dataset.name
		document.getElementById('price').innerHTML += this.dataset.price
		document.getElementById('status').innerHTML += this.dataset.status
		console.log(this.dataset.id)
		overlayStatus.style.display = 'block';
		overlayShippingBtn.dataset.item = this.dataset.id;
	})
}

for (var i = 0; i < updateProductsBtns.length; i++) {
    updateProductsBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
		var action = this.dataset.action
        if (action == 'update'){
            var productId = this.dataset.product
            var action = this.dataset.action
            document.getElementById('product-name').value = this.dataset.name;
            document.getElementById('product-description').value = this.dataset.description;
            document.getElementById('product-price').value = this.dataset.price;
            document.getElementById('product-quantity').value = this.dataset.quantity;
            overlay.style.display = 'block';
        
            overlayActionButton.dataset.product = productId;
		}else{
            if (confirm('Are you sure you want to delete this product?')) {
                deleteProduct(productId, action);

            }
		}

    });
}



function deleteProduct(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_product/'

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

function updateProduct(productId, action, datalist){
	console.log('User is authenticated, sending data...')

		var url = '/update_product/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action, 'productData': datalist})	
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function updateOrderItem(Id, action, datalist){
	console.log('User is authenticated, sending data...')

		var url = '/update_order_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'orderItemId':Id, 'action':action, 'OrderItemData': datalist})	
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}