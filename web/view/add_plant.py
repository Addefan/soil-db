from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute, Entity

from web.forms import PlantForm, AttributeForm, AttributeFormView
from web.models import Plant


class PlantCreateFormView(CreateView):
    form_class = PlantForm
    template_name = "web/plant_form.html"

    def _render(self, request, *args, **kwargs):
        return render(request, "web/plant_form.html",
                      {"plant_form": PlantForm(),
                       "attr_form": AttributeForm(),
                       "attr_form_view": AttributeFormView(),
                       })

    #
    def get(self, request, *args, **kwargs):
        return self._render(request)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Plant.objects.none()
        return Plant.objects.all()

    # TODO изменить
    def get_success_url(self):
        # return reverse("plant", args=(self.object.title, self.object.id))
        return reverse("view_test")

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs),
                "plant_form": PlantForm(),
                "attr_form": AttributeForm(),
                "attr_form_view": AttributeFormView(),
                }

    def post(self, request, *args, **kwargs):
        print(request.POST)
        PLANT = None
        form_plant = PlantForm(request.POST)
        if form_plant.is_valid():
            print('Ура')
            print(form_plant.cleaned_data)
            PLANT = form_plant.save()
        else:
            print('Все плохо')
        # print(request.POST)
        form_attr = AttributeFormView(request.POST)
        print(PLANT)
        if form_attr.is_valid():
            print('Ура')
            print(form_attr.cleaned_data)
            if form_attr.is_valid():
                plant = PLANT
                obj = Entity(Plant.objects.first())
                print(form_attr.cleaned_data)
                for i in obj.get_all_attributes():
                    print(i)
                    plant.eav.__setattr__(i.name, form_attr.cleaned_data[i.name])
                plant.save()
                print('НАЙС')
        else:
            print('Все плохо')
        # for key, val in request.POST.items():
        #     if key in ['number', 'organization', 'latin_name', 'name', 'genus']:
        #         request_args[key] = val
        #     else:
        #         plant_attrs[key] = val
        # print(request_args)
        # print(plant_attrs)
        # if form.is_valid():
        #     plant = form.save()
        #     obj = Entity(plant)
        # else:
        #     return HttpResponse('Увы')
        # for i in obj.get_all_attributes():
        #     print(i)
        #     plant.eav.__setattr__(i.name, plant_attrs[i.name])
        #     plant.save()
        return HttpResponse("Ку")
        # return render(request, "web/plant_form.html", {"plant_form": PlantForm(),
        #         "attr_form": AttributeForm(),
        #         "attr_form_view": AttributeFormView(),
        #         })


def success_url(request):
    return HttpResponse('<h1>Все ок</h1>')


def view_test(request):
    response_data = {}
    print(request.POST)
    name = request.POST.get('name')
    type_attr = request.POST.get('type_attr')
    print(name, type_attr)
    response_data['name'] = name
    response_data['type_attr'] = type_attr
    if type_attr == 'integer':
        Attribute.objects.create(name=name, datatype=Attribute.TYPE_INT)
    elif type_attr == 'string':
        Attribute.objects.create(name=name, datatype=Attribute.TYPE_TEXT)
    elif type_attr == 'date':
        Attribute.objects.create(name=name, datatype=Attribute.TYPE_DATE)
    elif type_attr == 'float':
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
