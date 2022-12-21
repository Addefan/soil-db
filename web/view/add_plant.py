from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute, Entity

from web.forms import PlantForm, AttributeForm
from web.models import Plant


class PlantCreateFormView(CreateView):
    form_class = PlantForm
    template_name = 'web/plant_form.html'

    def _render(self, request, *args, **kwargs):
        return render(request, "web/plant_form.html", {"form_test": PlantForm(*args, **kwargs), "attr_form": AttributeForm()})

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

    # def get_context_data(self, **kwargs):
    #     return {
    #         **super().get_context_data(**kwargs),
    #         "attr_form": AttributeForm(),
    #     }


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
    return JsonResponse(response_data)


# def view_test(request):
# Attribute.objects.create(name='date', datatype=Attribute.TYPE_DATE)
# plant_1 = Plant.objects.first()
# plant_1.eav.age = 2
# plant_1.save()
# print(plant_1.eav_values.all())
# print(plant_1.eav.age)
# print(Entity(plant_1).get_all_attributes())
# plant_1 = Plant.objects.first()
#
# for i in Entity(plant_1).get_all_attributes():
#     print(i.name, plant_1.eav.__getattr__(i.name))

# for i in Entity(Plant).get_all_attributes():
#     print(i.name)

# return HttpResponse("<h1>Страница для успешного завершения добавления растения</h1>")


class PlantUpdateView(UpdateView):
    pass
