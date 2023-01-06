from django.http import JsonResponse
import pyrebase
from django.views import View

firebaseConfig = {
  "apiKey": "AIzaSyA5gLxlK2_hOYTPhl6ptuEv2jcPujsuEH0",
  "authDomain": "bvmpjc.firebaseapp.com",
  "projectId": "bvmpjc",
  "databaseURL" : "https://bvmpjc-default-rtdb.firebaseio.com/",
  "storageBucket": "bvmpjc.appspot.com",
  "messagingSenderId": "531712044042",
  "appId": "1:531712044042:web:86c2f3aa901758ba69c3f3",
  "measurementId": "G-XYGE1JFZBQ"
}

firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database=firebase.database()

class RenderTableDetails(View):

    def get(self, request):
        id = database.child('user').get().val()
        name = database.child('user').get().val()
        context = {
            'id': id,
            'name':name,
        }
        return JsonResponse(context)
