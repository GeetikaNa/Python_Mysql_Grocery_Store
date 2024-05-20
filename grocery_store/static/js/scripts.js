$(document).ready(function() {
    // Function to calculate total price
    function calculateTotalPrice() {
        let totalPrice = 0;
        $(".order-item").each(function() {
            const quantity = parseInt($(this).find(".quantity").val());
            const pricePerUnit = parseFloat($(this).find(".price-per-unit").text());
            const total = quantity * pricePerUnit;
            totalPrice += total;
        });
        $("#total-price").text(totalPrice.toFixed(2));
    }

    // Update total price on quantity change
    $(document).on("input", ".quantity", function() {
        calculateTotalPrice();
    });

    // Add product row on add button click
    $("#add-product").click(function() {
        const productRow = `
        <div class="form-row order-item">
            <div class="form-group col-md-4">
                <select class="form-control product" required>
                    <option value="" selected disabled>Select Product</option>
                    <!-- Populate product options dynamically from database -->
                    {% for product in products %}
                    <option value="{{ product.product_id }}" data-price="{{ product.price_per_unit }}" data-uom="{{ product.uom_name }}">{{ product.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group col-md-3">
                <input type="number" class="form-control quantity" value="1" min="1" required>
            </div>
            <div class="form-group col-md-3">
                <span class="price-per-unit">0.00</span>
            </div>
            <div class="form-group col-md-2">
                <span class="total">0.00</span>
            </div>
        </div>`;
        $("#order-items").append(productRow);
    });

    // Submit form
    $("#order-form").submit(function(event) {
        event.preventDefault();
        
        // Collect data from form
        const customerName = $("#customer-name").val();
        const orderDetails = [];
        $(".order-item").each(function() {
            const productId = $(this).find(".product").val();
            const quantity = parseInt($(this).find(".quantity").val());
            orderDetails.push({ productId, quantity });
        });

        // Send data to backend
        $.ajax({
            url: "/insertOrder",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ customerName, orderDetails }),
            success: function(response) {
                alert("Order submitted successfully!");
                // Optionally, redirect to another page or perform any other action
            },
            error: function(xhr, status, error) {
                alert("Error submitting order. Please try again later.");
                console.error(xhr.responseText);
            }
        });
    });
});
