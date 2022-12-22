from django.urls import path

from web.views.plant import PlantDetailView

urlpatterns = [path("plant/<int:number>", PlantDetailView.as_view(), name="plant")]
