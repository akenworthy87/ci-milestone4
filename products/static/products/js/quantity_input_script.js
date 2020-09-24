// ##### Functions
// Sets max value on quantity selector to variety's availible stock
function handleVarietyChange(itemId) {
    // Only executes this code product details page
    // Checks it is on product details via checking for pressence of the variety selector
    if($("#id_product_variety").length) {
        var stockAvailible = parseInt($('#id_product_variety').find(':selected').data('stockavail'));
        var currentValue = parseInt($(`#id_qty_${itemId}`).val());
        $(`#id_qty_${itemId}`).attr("max", stockAvailible);
        $('#id_qty_avail').text(stockAvailible);
        if(stockAvailible === 0) {
            $(`#id_qty_${itemId}`).prop('disabled', true);
            $('#id_submit_btn').prop('disabled', true);
        } else {
            $(`#id_qty_${itemId}`).prop('disabled', false);
            $('#id_submit_btn').prop('disabled', false);
        }
        if(currentValue > stockAvailible) {
            currentValue = Math.max(stockAvailible, 1);
            $(`#id_qty_${itemId}`).val(currentValue);
        }
        handlePriceDisplays(currentValue);
    }
}

// Disable +/- buttons outside 1-99 range
function handleEnableDisable(itemId) {
    handleVarietyChange(itemId);
    var currentValue = parseInt($(`#id_qty_${itemId}`).val());
    var minValue = parseInt($(`#id_qty_${itemId}`).attr("min"));
    var stockAvailible = parseInt($(`#id_qty_${itemId}`).attr("max"));
    var minusDisabled = currentValue < (minValue + 1);
    var plusDisabled = currentValue >= stockAvailible;
    $(`#decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`#increment-qty_${itemId}`).prop('disabled', plusDisabled);
}

function lightUpdateLink(caller) {
    var closestUpdateLink = caller.closest('.update-form').next('.update-link')[0];
    if(closestUpdateLink) {
        $(closestUpdateLink).addClass("text-primary text-uppercase font-weight-bold font-italic");
    }
}

// Sets displayed price per item and calcs subtotal display
function handlePriceDisplays(currentValue) { 
    var pricePer = parseFloat($('#id_product_variety').find(':selected').data('price'));
    $('#id_price_span').text(pricePer.toFixed(2));
    $('#id_subtotal_span').text((pricePer * currentValue).toFixed(2));
    }


// #### Button Actions
// Increment quantity
$('.increment-qty').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue + 1);
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
    lightUpdateLink($(this));
});

// Decrement quantity
$('.decrement-qty').click(function(e) {
    e.preventDefault();
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    var currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue - 1);
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
    lightUpdateLink($(this));
});


// ##### OnChanges
// Check enable/disable every time the input is changed
$('.qty_input').change(function() {
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
    lightUpdateLink($(this));
});

$('#id_product_variety').change(function() {
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
});


// ##### OnLoads
// Ensure proper enabling/disabling of all inputs on page load
var allQtyInputs = $('.qty_input');
for(var i = 0; i < allQtyInputs.length; i++){
    var itemId = $(allQtyInputs[i]).data('item_id');
    handleEnableDisable(itemId);
}
