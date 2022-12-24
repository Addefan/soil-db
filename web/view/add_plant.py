from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute, Entity

from web.forms import (
    PlantForm,
    AttributeForm,
    AttributeFormView,
    FamilyForm,
    OrderForm,
    ClassForm,
    PhylumForm,
    GenusForm,
)
from web.models import Plant, Phylum, Class, Order, Family, Genus


class PlantCreateFormView(CreateView):
    form_class = PlantForm
    template_name = "web/plant_form.html"

    def _take_names_attributes(self, set_objects):
        basket = set()
        for obj in set_objects:
            basket.add(obj.title)
        return basket

    def _render(self, request, plant_form=None, attr_form_view=None, is_success=None):
        genus = set()
        family = self._take_names_attributes(Family.objects.all())
        order = self._take_names_attributes(Order.objects.all())
        klass = self._take_names_attributes(Class.objects.all())
        phylum = self._take_names_attributes(Phylum.objects.all())
        genus = self._take_names_attributes(Genus.objects.all())
        return render(
            request,
            "web/plant_form.html",
            {
                "plant_form": PlantForm() or plant_form,
                "attr_form": AttributeForm(),
                "attr_form_view": AttributeFormView() or attr_form_view,
                "family_form": FamilyForm(),
                "order_form": OrderForm(),
                "class_form": ClassForm(),
                "phylum_form": PhylumForm(),
                "genus_form": GenusForm(),
                "is_success": is_success,
                "genus": genus,
                "family": family,
                "order": order,
                "class": klass,
                "phylum": phylum,
            },
        )

    # todo приудмать как сделать так, чтобы при выболее более высокой
    # стадии на нижних этапах выводились только соответствующией ей низшие стадии
    def get(self, request, *args, **kwargs):
        return self._render(request)

    def _make_obj(self, req, stage, pref):
        print(req, stage, pref)
        ans = stage(req).save()
        return ans

    def post(self, request, *args, **kwargs):
        is_success = False
        req = request.POST
        print(req)
        if not Phylum.objects.filter(title=req["phylum-title"]):
            phylum_obj = Phylum(req["phylum-title"], req["phylum-latin_title"]).save()
        else:
            phylum_obj = Phylum.objects.filter(title=req["phylum-title"]).first()
        if not Class.objects.filter(title=req["klass-title"]):
            class_obj = self._make_obj(req, ClassForm, "klass")
            class_obj.phylum = phylum_obj
            class_obj.save()
        else:
            class_obj = Class.objects.filter(title=req["klass-title"]).first()
        if not Order.objects.filter(title=req["order-title"]):
            order_obj = self._make_obj(req, OrderForm, "order")
            order_obj.class_name = class_obj
            order_obj.save()
        else:
            order_obj = Order.objects.filter(title=req["order-title"]).first()
        if not Family.objects.filter(title=req["family-title"]):
            family_obj = self._make_obj(req, FamilyForm, "family")
            family_obj.order = order_obj
            family_obj.save()
        else:
            family_obj = Family.objects.filter(title=req["family-title"]).first()
        if not Genus.objects.filter(title=req["genus-title"]):
            genus_obj = self._make_obj(req, GenusForm, "genus")
            print(genus_obj.family)
            genus_obj.family = family_obj
            genus_obj.save()
        else:
            genus_obj = Genus.objects.filter(title=req["genus-title"]).first()

        form_plant = PlantForm(req)
        form_attr = AttributeFormView(req)
        if form_plant.is_valid():
            plant = form_plant.save()
            plant.genus = genus_obj
            if form_attr.is_valid():
                obj = Entity(Plant.objects.first())
                for i in obj.get_all_attributes():
                    plant.eav.__setattr__(i.slug, form_attr.cleaned_data[i.name])
                plant.save()
                is_success = True
                print("второй")
        else:
            print("первый")
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
