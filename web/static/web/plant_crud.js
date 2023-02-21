$('#add_button').on('click', function () {
    $.ajax({
        url: path_ajax,
        method: 'post',
        dataType: 'html',
        data: $('#attr_form').serialize(),
        success: function (smt) {
            window.location.reload()
        },
    })
})