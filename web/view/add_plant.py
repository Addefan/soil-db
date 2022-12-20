from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute, Entity

from web.forms import PlantForm
from web.models import Plant


class PlantCreateFormView(CreateView):
    form_class = PlantForm
    template_name = 'web/plant_form.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Plant.objects.none()
        return Plant.objects.all()

    # TODO изменить
    # def get_success_url(self):
    #     return reverse("plant", args=(self.object.title, self.object.id))

    # def post(self, request, *args, **kwargs):
    #     # req_post = {'number': request.POST['number'],
    #     #             'organization': request.POST['organization'],
    #     #             'genus': request.POST['genus'],
    #     #             'latin_name': request.POST['latin_name'],
    #     #             'name': request.POST['name'],
    #     #             }
    #     form = PlantForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     # obj = get_object_or_404(Entity(plant))
    #     # for i in obj.get_all_attributes():
    #     #     plant.eav.__setattr__(i.name, self.cleaned_data[i.name])
    #     # obj.save()
    #     return render(request, "web/plant_form.html", {
    #         "form": form or PlantForm(),
    #     })


def view_test(request):
    # Attribute.objects.create(name='date', datatype=Attribute.TYPE_DATE)
    plant_1 = Plant.objects.first()
    # plant_1.eav.age = 2
    # plant_1.save()
    # print(plant_1.eav_values.all())
    # print(plant_1.eav.age)
    # print(Entity(plant_1).get_all_attributes())
    for i in Entity(plant_1).get_all_attributes():
        print(i.name, plant_1.eav.__getattr__(i.name))

    # for i in Entity(Plant).get_all_attributes():
    #     print(i.name)

    return HttpResponse()


class PlantUpdateView(UpdateView):
    pass
