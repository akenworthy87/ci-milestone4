$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    // Value from selector is in format: sort_direction
    var selectedVal = selector.val();
    if(selectedVal != "reset"){
        // Splits value into it's two subcomponents
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];

        // Sets the URL parameters 
        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.replace(currentUrl);
    }
});
