$("#save").click(function () {
    $.ajax({
        method: "post",
        url: profile_url,
        dataType: "json",
        data: $("#profile_form").serialize(),
        success: function () {
            save_current_input_values();
            let success_toast = new bootstrap.Toast($("#success_toast"));
            success_toast.show();
        },
        error: function (data) {
            displaying_errors(data.responseJSON);
        }
    });
});

function displaying_errors(errors) {
    for (let field_name in errors) {
        let field = $(`#id_${field_name}`);
        field.parent().addClass("is-invalid");
        field.addClass("is-invalid");
        let errors_tag = $(`.${field_name}`).children(".invalid-feedback");
        errors_tag.append($("<ul>"));
        errors_tag = errors_tag.children("ul");
        errors_tag.addClass("errorlist");
        for (let error of errors[field_name]) {
            errors_tag.append($(`<li>${error}</li>`));
        }
    }
}

function save_current_input_values() {
    for (let field of $(".input-group")) {
        if ($(field).hasClass("password")) {
            $(field).children().children("input").val("");
        } else if ($(field).hasClass("email")) {
        } else {
            let input = $(field).children().children("input");
            input.attr("value", input.val());
        }
    }
}