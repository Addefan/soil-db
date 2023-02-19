// Adding a class for all fields that have errors
$("div .is-invalid").children("input").addClass("is-invalid");
$(document).ready(function() {
    $(".toast").toast('show');
});