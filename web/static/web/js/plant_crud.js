// adding custom attributes
$('#add_button').on('click', function () {
    $.ajax({
        url: path_ajax,
        method: 'post',
        dataType: 'json',
        data: $('#attr_form').serialize(),
        success: function (new_obj) {
            make_custom_attribute(new_obj.name_attr, new_obj.type_attr, new_obj.slug_name)
        },
    })
})
// TODO переписать на vue
function make_custom_attribute(name_attribute, type_attr, slug_name) {
    const type_attributes = {
        int: 'number',
        float: 'number',
        text: 'text'
    }

    let field_form_last_div = $('#plant_form div.input-group').last()
    let last_field = $('<div>', {
        class: 'input-group has-validation'
    })
    let div_elem = $('<div>', {
        class: 'form-floating mt-3'
    })

    let input_field = $('<input>', {
        id: `id_${slug_name}`,
        type: () => {
            return type_attributes[type_attr] ?? 'date'
        },
        name: `${slug_name}`,
        placeholder: 'smt',
        class: 'form-control',
        step: () => {
            if (type_attr === 'float'){
                return 'any'
            }
            else {
                return 'number'
            }
        }
    })
    let label = $('<label>', {
        text: `${name_attribute}`,
        for: `${slug_name}`,
    })
    div_elem.append(input_field)
    div_elem.append(label)
    last_field.append(div_elem)
    field_form_last_div.after(last_field)
    $("#attribute_modal_window").modal('hide');
}

$(`#attribute_modal_window`).on('hide.bs.modal', function () {
    $("#attribute_modal_window form")[0].reset()
})
