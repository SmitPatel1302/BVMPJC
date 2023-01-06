from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect,JsonResponse
from .forms import LoginForm , RegistrationForm
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import base64
from uuid import uuid4
from firebase_admin import credentials, initialize_app, storage


# Application Default credentials are automatically created.
cred = credentials.Certificate("serviceAccountKey.json")
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
firebase_admin.initialize_app(cred, {'storageBucket': 'bvmpjc-58b2c.appspot.com'})
db = firestore.client()

# Class to render Admin Page
class RenderAdminIndex(View):
    template_name = 'AdminPanel/demo.html'
    
    def get(self, request):
        if 'name' in request.session:
            users_ref = db.collection('Alumni')
            users = db.collection('User')

            context = {}
            context['alumni'] = len(list(users_ref.where('Student',"==","No").get()))
            context['user'] = len(list(users.get()))
            context['kit'] = len(list(users_ref.where('status', '==', "1").where('Student',"==","No").get()))
            context['remaining'] = len(list(users_ref.where('status', '==', 0).where('Student',"==","No").get()))
            context['volunteer'] = len(list(users_ref.where('Student',"==","Yes").get()))
            return render(request, self.template_name,context)
        else:
            return HttpResponseRedirect('login')

#Class to render User Data Page
class RenderAlumniData(View):
    template_name = 'AdminPanel/alumnidata.html'
    
    def get(self, request):
        if request.session['name'] != None :
                users_ref = db.collection(u'Alumni')
                dt = users_ref.where('Student','==','No').stream()

                context = {}
                li = []
                count = 1
                for data in dt:
                    dict = {}
                    dict.update({'count':count})

                    dict.update(data.to_dict())
                    li.append(dict)
                    count+=1
                context['data'] = li
                return render(request,self.template_name, context)
        else:
            return redirect('Log Out')

#Class to render Add User Data Page
class RenderAddAlumniData(View):
    template_name = 'AdminPanel/addalumnidata.html'

    def get(self, request):
        if (request.session['name'] != None) & (request.session['role'] != "Volunteer"):
            return render(request, self.template_name)
        else:
            return redirect('Login Page')
    
    def post(self,request):
        
        collection = db.collection(u'Alumni')

        name = request.POST.get('name')
        department = request.POST.get('department')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        year = request.POST.get('year')
        country = request.POST.get('country')
        paymate = request.POST.get('payment')
        lm = request.POST.get('lm')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        receipt = request.POST.get('date')

        try:
            doc = collection.document()
            data = {
                "name" : name,
                "email" : email,
                "branch": department,
                "mobileNumber" : contact,
                "graduationYear" : year,
                "city" :country,
                "payment":paymate,
                "imNumber":lm,
                "amount":amount,
                "date":date,
                "receipt":receipt,
                "status" : 0,
                "profile":"",
                "doc": doc.id,
            }
            doc.set(data)
        except:
            return render(request, self.template_name)
        return HttpResponseRedirect("/alumnidata")


#Class to render Login Page
class RenderLoginPage(View):
    template_name = 'AdminPanel/login.html'

    def get(self,request):
        form = LoginForm()
        return render(request,self.template_name, {'form': form})
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password') 

        users_ref = db.collection(u'User')
        dt = users_ref.stream()
        for data in dt:
            dict = data.to_dict()
            if (dict['email'] == username) & (dict['password'] == password):
                request.session['name'] = dict['name']
                request.session['role'] = dict['role']
                request.session['email']=str(username)
                return HttpResponseRedirect("/")
        message="Invalid Credentials!!  Please ChecK your Data"
        form = LoginForm()
        return render(request,self.template_name,{"message":message,"form":form})

# Class to Render Registration Page
class RenderRegistrationPage(View):
    template_name = 'AdminPanel/registration.html'

    def get(self,request):
        if (request.session['name'] != None) & (request.session['role'] == "Admin"):
            form = RegistrationForm()
            return render(request,self.template_name,{'form':form})
        else:
            return render("Log Out")
    
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        department = request.POST.get('department')
        contact = request.POST.get('contact')
        role = request.POST.get('role')
        year = request.POST.get('year')
        try:
            data={"name":name,
                  "email":username,
                  "password":password,
                  "department":department,
                  "contact" : contact,
                  "role" : role,
                  "year" : year
                }
            collection = db.collection(u'User')
            doc = collection.document(username)
            doc.set(data)
        except:
            form = RegistrationForm()
            return render(request, self.template_name,{'form':form})
        return HttpResponseRedirect('/') 

#Class to render User Data Page
class RenderUserData(View):
    template_name = 'AdminPanel/userdata.html'
    
    def get(self, request):
        if (request.session['name'] != None) & (request.session['role'] == "Admin"):
            users_ref = db.collection(u'User')
            dt = users_ref.stream()

            context = {}
            li = []
            for data in dt:
                dict = {}

                dict.update(data.to_dict())
                li.append(dict)
            context['data'] = li
            return render(request,self.template_name, context)
        else:
            return render("Log Out")
       
#Logout view
def logout(request):
    try:
        request.session.flush()
    except:
        pass
    return HttpResponseRedirect('/login')   

import datetime
def viewalumnidata(request,id):
    collection = db.collection('Alumni') 
    doc = collection.document(id)
    res = doc.get().to_dict()

    bucket = storage.bucket()
    blob = bucket.blob('bvmpjc-58b2c.appspot.com/AlumniImages')
    print(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))
    return render(request,'AdminPanel/alumnidetails.html',{'data':res})

def editalumnidata(request,id):
    collection = db.collection('Alumni') 
    doc = collection.document(id)
    res = doc.get().to_dict()
    return render(request,'AdminPanel/editalumnidetails.html',{'data':res})

# Class to render Rnder Alumini Edit Page
class RenderEditAlumni(View):
    def post(self,request):
        collection = db.collection('Alumni')
        res = collection.document(request.POST.get('doc')).update(
            {'name': request.POST.get('name'),
             'branch':request.POST.get('department'),
             'mobileNumber':request.POST.get('contact'),
             'email':request.POST.get('email'),
             'graduationYear':request.POST.get('year'),
             'city':request.POST.get('country'),
             'imNumber':request.POST.get('lm'),
            })
        return redirect('AlumniData')

def deleteuser(request,id):
    doc_ref = db.collection(u'User').document(id)
    doc_ref.delete()
    return redirect('UserData')

# Class to update the aluminidata
class UpdateAluminiData(View):

    def post(self, request):
        collection = db.collection('Alumni')
        res = collection.document(request.POST.get('ID')).update({'status': 1})
        response = {
            'success':'True'
        }
        return JsonResponse(response)




# Class to save the image on the server after converting in wep3 format
class SaveImage(View):
     def post(self, request):
        collection = db.collection('Alumni')
        collection.document(request.POST.get('id')).update({'profile': request.POST.get('imageUrl')})

        # Response dictionary to send back as a reply of ajax request
        respons = {
            'success':'True'
        }
        return JsonResponse(respons)