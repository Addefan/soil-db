$(document).ready(function () {
    // Setting attributes for the tooltip on the email's input
    let div_with_email = $("#id_email").parent();
    div_with_email.attr("data-bs-toggle", "tooltip");
    div_with_email.attr("data-bs-title", "Почту изменить нельзя");
    div_with_email.attr("tabindex", 0);

    // Activation all tooltips (code from Bootstrap documentation)
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});