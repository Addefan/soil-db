// Adding a class for all fields that have errors
$("div .is-invalid").children("input").addClass("is-invalid");

$('button[data-usage="xlsx-submit"]').on("click", event => {
    let xlsxForm = document.forms.xlsx_form;
    xlsxForm.submit();
})

$(document).ready(() => {
    $(".toast.messages").toast('show');
});

$('form[role="search"]').submit(event => {
    if (!this.search.value) {
        event.preventDefault();
    }
});
