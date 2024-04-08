// static/script.js
document.addEventListener("DOMContentLoaded", function () {
    const productList = document.getElementById("product-list");
    const cartItems = document.getElementById("cart-items");
    const totalAmount = document.getElementById("total");

    // Sample products
    const products = [
        { id: 1, name: "Product 1", price: 20.00 },
        { id: 2, name: "Product 2", price: 15.00 },
        { id: 3, name: "Product 3", price: 30.00 }
    ];

    // Display products
    products.forEach(product => {
        const productElement = document.createElement("div");
        productElement.innerHTML = `
            <p>${product.name} - $${product.price.toFixed(2)}</p>
            <button onclick="addToCart(${product.id})">Add to Cart</button>
        `;
        productList.appendChild(productElement);
    });

    // Shopping cart functionality
    const cart = [];

    window.addToCart = function (productId) {
        fetch(`/add_to_cart/${productId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    location.reload();
                } else {
                    alert(data.message);
                }
            });
    };
});
