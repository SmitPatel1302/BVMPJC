from django.contrib import admin
from django.urls import path 
from AdminPanel.views import RenderAdminIndex, RenderAddAlumniData ,RenderUserData , RenderLoginPage , RenderRegistrationPage , RenderAlumniData , RenderEditAlumni , UpdateAluminiData, SaveImage
from AdminPanel.AdminTabel import RenderTableDetails
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', RenderAdminIndex.as_view(), name="AdminPanelIndex"),
    path('alumnidata/', RenderAlumniData.as_view(), name="AlumniData"),
    path('addalumnidata/', RenderAddAlumniData.as_view(), name="AddUserData"),
    path('renderTableDetails/', RenderTableDetails.as_view(), name="TableDetails"),
    path('viewalumnidata/<id>', views.viewalumnidata, name="View Alumni Details"),
    path('editalumnidata/<id>', views.editalumnidata, name="Edit Alumni Details"),
    path('editalumnidata/', RenderEditAlumni.as_view(),name="Edit Alumni"),
    path('deleteuser/<id>', views.deleteuser,name="Delete User"),
    path('updateAlumniData', UpdateAluminiData.as_view(), name="Update_Alumni_Data"),
    path('saveImage', SaveImage.as_view(), name="Save Alumini Image"),

    path('login', RenderLoginPage.as_view(), name="Login Page"),
    path('registration', RenderRegistrationPage.as_view(), name="Registration Page"),
    path('userdata/', RenderUserData.as_view(), name="UserData"),
    path('logout/', views.logout, name="Log Out"),

    #path('updatealumni/<string:id>', RenderUpdateAlumni.as_view(), name='update'),
]