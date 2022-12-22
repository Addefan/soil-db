from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute, Entity

from web.forms import PlantForm, AttributeForm, AttributeFormView, FamilyForm, OrderForm, ClassForm, PhylumForm
from web.models import Plant


class PlantCreateFormView(CreateView):
    form_class = PlantForm
    template_name = "web/plant_form.html"

    def _render(self, request, plant_form=None, attr_form_view=None, is_success=None):
        return render(request, "web/plant_form.html",
                      {
                          "plant_form": PlantForm() or plant_form,
                          "attr_form": AttributeForm(),
                          "attr_form_view": AttributeFormView() or attr_form_view,
                          "family_form": FamilyForm(),
                          "order_form": OrderForm(),
                          "class_form": ClassForm(),
                          "phylum_form": PhylumForm(),

                          "is_success": is_success
                      })

    #
    def get(self, request, *args, **kwargs):
        return self._render(request)

    def post(self, request, *args, **kwargs):
        is_success = False
        form_plant = PlantForm(request.POST)
        form_attr = AttributeFormView(request.POST)
        if form_plant.is_valid():
            plant = form_plant.save()
            if form_attr.is_valid():
                obj = Entity(Plant.objects.first())
                for i in obj.get_all_attributes():
                    plant.eav.__setattr__(i.slug, form_attr.cleaned_data[i.name])
                plant.save()
                is_success = True
        return self._render(request, form_plant, form_attr, is_success)


def success_url(request):
    return HttpResponse("<h1>Все ок</h1>")


def view_test(request):
    response_data = {}
    print(request.POST)
    name = request.POST.get("name")
    type_attr = request.POST.get("type_attr")
    print(name, type_attr)
    response_data["name"] = name
    response_data["type_attr"] = type_attr
    if type_attr == "integer":
        Attribute.objects.create(name=name, datatype=Attribute.TYPE_INT)
    elif type_attr == "string":
        Attribute.objects.create(name=name, datatype=Attribute.TYPE_TEXT)
    elif type_attr == "date":
        Attribute.objects.create(name=name, datatype=Attribute.TYPE_DATE)
    elif type_attr == "float":
        Attribute.objects.create(name=name, datatype=Attribute.TYPE_FLOAT)
    return JsonResponse(response_data)


# def view_test(request):
#     Attribute.objects.create(name='address', datatype=Attribute.TYPE_TEXT)
#     plant_1 = Plant.objects.first()
#     plant_1.eav.address = 'Пушкина'
#     plant_1.save()
#     print(plant_1.eav_values.all())
#     # print(plant_1.eav.age)
#     print(Entity(plant_1).get_all_attributes())
#     plant_1 = Plant.objects.first()
#
#     for i in Entity(plant_1).get_all_attributes():
#         print(i.name, plant_1.eav.__getattr__(i.name))
#
#     for i in Entity(Plant).get_all_attributes():
#         print(i.name)
#
#     return HttpResponse("<h1>Страница для успешного завершения добавления растения</h1>")


class PlantUpdateView(UpdateView):
    pass
