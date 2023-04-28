from web.views.auth import LoginView, LogoutView
from web.views.delete_plant import PlantDeleteView
from web.views.plant import PlantDetailView
from web.views.plant_crud import PlantCreateView, PlantUpdateView, ajax_response
from web.views.plants import PlantsListView, XlsxColumnsView
from web.views.profile import ProfileFormView, ChangePasswordView
from web.views.errors import Page404View, Page500View
