document.querySelectorAll('.quantity-input').forEach(function(quantityInput) {
    const quantityField = quantityInput.querySelector('.quantity-field');
    const plusBtn = quantityInput.querySelector('.plus-btn');
    const minusBtn = quantityInput.querySelector('.minus-btn');

    plusBtn.addEventListener('click', function() {
        quantityField.value = parseInt(quantityField.value) + 1;
    });

    minusBtn.addEventListener('click', function() {
        if (parseInt(quantityField.value) > 1) {
            quantityField.value = parseInt(quantityField.value) - 1;
        }
    });
});