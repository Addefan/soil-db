// adding custom attributes
$('#add_button').on('click', function () {
    $.ajax({
        url: path_ajax,
        method: 'post',
        dataType: 'html',
        data: $('#attr_form').serialize(),
        success: function (smt) {
            let new_obj = JSON.parse(smt)
            make_custom_attribute(new_obj.name_attr, new_obj.type_attr, new_obj.slug_name)
        },
    })
})

function make_custom_attribute(name_attribute, type_attribute, slug_name) {
    console.log(name_attribute, type_attribute)
    let field_form_last_div = $('#plant_form div.input-group').last()
    let last_field = document.createElement('div')
    last_field.classList.add('input-group')
    last_field.classList.add('has-validation')
    let div_elem = document.createElement('div')
    div_elem.classList.add('form-floating')
    div_elem.classList.add('mt-3')

    let input_field = document.createElement('input')
    input_field.id = `id_${slug_name}`
    if (type_attribute === 'string') {
        input_field.type = 'text'
    } else if (type_attribute === 'integer') {
        input_field.type = 'number'
    } else if (type_attribute === 'float') {
        input_field.type = 'number'
        input_field.step = 'any'
    } else {
        input_field.type = 'date'
    }
    input_field.name = `${slug_name}`
    input_field.placeholder = 'smt'
    input_field.classList.add('form-control')
    let label = document.createElement('label')
    label.innerHTML = `${name_attribute}`
    label.htmlFor = `${slug_name}`
    label.innerHTML = `${name_attribute}`
    div_elem.append(input_field)
    div_elem.append(label)
    last_field.append(div_elem)
    field_form_last_div.after(last_field)
    $("#attribute_modal_window").modal('hide');
}

$(`#attribute_modal_window`).on('hide.bs.modal', function () {
    console.log('Я тут')
    $("#attribute_modal_window form")[0].reset()
})