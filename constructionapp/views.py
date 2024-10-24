import os
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from constructionapp.models import ArchitectBooking, Architectures, ContractorBooking, Contractors, DesignerBooking, Designers, Payment, Users, Works
import bcrypt
from django.conf import settings
# Create your views here.
def index(request):
    if 'id' in request.session:
        user_id = request.session['id']
        current_user = request.GET.get('name')
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'user':
                user_model = Users
            elif user_model_name == 'architecture':
                user_model = Architectures
            elif user_model_name == 'designer':
                user_model = Designers
            elif user_model_name == 'contractor':
                user_model = Contractors
            logged_in_user = user_model.objects.get(id=user_id)
            return render(request,'index.html',{'logged_in_user': logged_in_user,'user':user_model_name})
    return render(request,'index.html')
def registration(request):
    if request.method=='POST':
        usertype=request.POST['usertype']
        name=request.POST['fullname']
        email=request.POST['email']
        passw=request.POST['password']
        cpass=request.POST['cpassword']
        phone=request.POST['phonenumber']
        pic=request.FILES.get('profilepic')
        if usertype=='user':
            user_model = Users
        elif usertype == 'architecture':
            user_model = Architectures
        elif usertype == 'designer':
            user_model = Designers
        elif usertype == 'contractor':
            user_model = Contractors
        try:
            emailexists=user_model.objects.filter(Email=email)
            if emailexists:
                messages.error(request,'Email ID already registered')
            elif passw!=cpass:
                messages.error(request,'Password does not match')
            else:
                user_model.objects.create(Name=name,Email=email,Password=passw,PhoneNumber=phone,ProfilePic=pic)
                return redirect('/')
        except user_model.DoesNotExist:
            # User not found
            messages.error(request,"Invalid email or password")
    return render(request,'registration.html')
def login(request):
    if request.method=='POST':
        usertype=request.POST['usertype']
        email=request.POST['email']
        passw=request.POST['password']
        if usertype == 'user':
            user_model = Users
        elif usertype == 'architecture':
            user_model = Architectures
        elif usertype == 'designer':
            user_model = Designers
        elif usertype == 'contractor':
            user_model = Contractors
        try:
            user1=user_model.objects.filter(Email=email,Password=passw)
            user = user_model.objects.get(Email=email)
            if user1:
                # Password matches, set user ID in session and redirect
                request.session['id'] = user.id
                request.session['user_model'] = usertype
                print(user.Name)
                return redirect('/?name={}'.format(user.Name))
            else:
                # Password doesn't match
                messages.error(request,"Invalid email or password")
        except user_model.DoesNotExist:
            # User not found
            messages.error(request,"Invalid email or password")
    return render(request,'login.html')
def logout(request):
    del request.session['id']
    return redirect('/')
def services(request):
    return render(request,'services.html')
def team(request):
    return render(request,'team.html')
def teammembers(request,user):
    print(user)
    if user=='architecture':
        users=Architectures.objects.all()
        return render(request,'teammembers.html',{'users':users,'user':user})
    elif user=='designer':
        users=Designers.objects.all()
        return render(request,'teammembers.html',{'users':users,'user':user})
    elif user=='contractor':
        users=Contractors.objects.all()
        return render(request,'teammembers.html',{'users':users,'user':user})
def about(request):
    return render(request,"about.html")
def profile(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'user':
                user_model = Users
            elif user_model_name == 'architecture':
                user_model = Architectures
            elif user_model_name == 'designer':
                user_model = Designers
            elif user_model_name == 'contractor':
                user_model = Contractors
            logged_in_user = user_model.objects.get(id=user_id)
            print(user_model_name)
            return render(request,'profile.html',{'logged_in_user': logged_in_user,'usertype':user_model_name})
    return render(request,'profile.html')
def profile_update(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'user':
                user_model = Users
            elif user_model_name == 'architecture':
                user_model = Architectures
            elif user_model_name == 'designer':
                user_model = Designers
            elif user_model_name == 'contractor':
                user_model = Contractors
            logged_in_user = user_model.objects.get(id=user_id)
            if request.method=='POST':
                name=request.POST['fullname']
                email=request.POST['email']
                passw=request.POST['password']
                cpass=request.POST['cpassword']
                phone=request.POST['phonenumber']
                pic=request.FILES.get('profilepic')
                if passw!=cpass:
                    messages.error(request,'Password does not match')
                else:
                    logged_in_user.Name=name
                    logged_in_user.Email=email
                    logged_in_user.Password=passw
                    logged_in_user.PhoneNumber=phone
                    if pic:
                        logged_in_user.ProfilePic=pic
                    logged_in_user.save()
                    return redirect('profile')
            return render(request,'updateprofile.html',{'logged_in_user': logged_in_user,'user_model':user_model_name})
    return render(request,"updateprofile.html")
def work_upload(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'user':
                user_model = Users
            elif user_model_name == 'architecture':
                user_model = Architectures
                type="architecture"
            elif user_model_name == 'designer':
                user_model = Designers
                type="designer"
            elif user_model_name == 'contractor':
                user_model = Contractors
            logged_in_user = user_model.objects.get(id=user_id)
            name=logged_in_user.Name
            if request.method=='POST':
                pic=request.FILES.get('workpic')
                Works.objects.create(Picture=pic,TypeOfDesign=type,Upload_by=name)
                return redirect('profile')
            return render(request,"work_upload.html",{'logged_in_user':logged_in_user})
    return render(request,"work_upload.html")
def myworks(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'user':
                user_model = Users
            elif user_model_name == 'architecture':
                user_model = Architectures
            elif user_model_name == 'designer':
                user_model = Designers
            elif user_model_name == 'contractor':
                user_model = Contractors
            logged_in_user = user_model.objects.get(id=user_id)
            work=Works.objects.filter(Upload_by=logged_in_user.Name)
            return render(request,"myworks.html",{'logged_in_user':logged_in_user,'work':work})
    return render(request,"myworks.html")
def booking_fun(request,user,id):
    if user == 'architecture':
        user_mode = Architectures
    elif user == 'designer':
        user_mode = Designers
    elif user == 'contractor':
        user_mode = Contractors
    booking_for=user_mode.objects.get(id=id)
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'user':
                user_model = Users
            else:
                messages.error(request,'No Access to appoinment page')
            logged_in_user = user_model.objects.get(id=user_id)
            if user == 'architecture':
                if request.method=='POST':
                    req_name=request.POST['fullname']
                    req_id=request.POST['id']
                    sqft=request.POST['sqft']
                    budget=request.POST['budget']
                    # architect=request.POST['architect']
                    plotsize=request.POST['plotsize']
                    plotpic=request.FILES.get('plotpic')
                    roughpic=request.FILES.get('roughpic')
                    message=request.POST['message']
                    architect=user_mode.objects.get(pk=booking_for.id)
                    ArchitectBooking.objects.create(BookingPerson=req_name,PersonID=req_id,SquareFeet=sqft,Budget=budget,Architect=architect,Plotsize=plotsize,Plotpic=plotpic,Message=message,Rougharchitecture=roughpic)
                    return redirect('/')
            elif user == 'designer':
                if request.method=='POST':
                    req_name=request.POST['fullname']
                    req_id=request.POST['id']
                    homestyle=request.POST['homestyle']
                    # designer=request.POST['contractor']
                    plotsize=request.POST['plotsize']
                    plotpic=request.FILES.get('plotpic')
                    message=request.POST['message']
                    designer=user_mode.objects.get(pk=booking_for.id)
                    DesignerBooking.objects.create(BookingPerson=req_name,PersonID=req_id,HomeStyle=homestyle,designer=designer,Plotsize=plotsize,Plotpic=plotpic,Message=message)
                    return redirect('/')
            elif user == 'contractor':
                if request.method=='POST':
                    req_name=request.POST['fullname']
                    req_id=request.POST['id']
                    sqft=request.POST['sqft']
                    timelimit=request.POST['timelimit']
                    # contractor=request.POST['contractor']
                    plotsize=request.POST['plotsize']
                    plotpic=request.FILES.get('plotpic')
                    plan=request.FILES.get('plan')
                    message=request.POST['message']
                    contractor=user_mode.objects.get(pk=booking_for.id)
                    ContractorBooking.objects.create(BookingPerson=req_name,PersonID=req_id,SquareFeet=sqft,TimeLimit=timelimit,Contractor=contractor,Plotsize=plotsize,Plan=plan,Plotpic=plotpic,Message=message)
                    return redirect('/')
            return render(request,"booking.html",{'logged_in_user':logged_in_user,'user':user,'booking_for':booking_for})
            
    return render(request,"booking.html")
def projects(request):
    data=Works.objects.all()
    return render(request,'projects.html',{'data':data})
def view_request(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'architecture':
                user_model = Architectures
                data=ArchitectBooking.objects.filter(Architect=user_id)
                return render(request,"view_requests.html",{'data':data,'user_model':user_model_name})
            elif user_model_name == 'designer':
                user_model = Designers
                data=DesignerBooking.objects.filter(designer=user_id)
                print(user_model_name)
                return render(request,"view_requests.html",{'data':data,'user_model':user_model_name})
            elif user_model_name == 'contractor':
                user_model = Contractors
                data=ContractorBooking.objects.filter(id=user_id)
                print(user_model_name)
                return render(request,"view_requests.html",{'data':data,'user_model':user_model_name})
    return render(request,"view_requests.html")
def user_requests(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'user':
                data=ArchitectBooking.objects.filter(PersonID=user_id)
                data2=DesignerBooking.objects.filter(PersonID=user_id)
                data3=ContractorBooking.objects.filter(PersonID=user_id)
                print(data)
                if data:
                    for i in data:
                        booked=i.Architect
                    print(booked)
                    return render(request,"user_request.html",{'data':data,'data2':data2,'data3':data3,'booked':booked})
                if data2:
                    for i in data2:
                        booked1=i.designer
                        print(booked1)
                    print(booked1)
                    return render(request,"user_request.html",{'data':data,'data2':data2,'data3':data3,'booked':booked,'booked1':booked1})
                if data3:
                    for i in data3:
                        booked2=i.Contractor
                    return render(request,"user_request.html",{'data':data,'data2':data2,'data3':data3,'booked':booked,'booked1':booked1,'booked2':booked2})
    return render(request,"user_request.html")
def download_image(request, image_path):
    file_path = os.path.join(settings.MEDIA_ROOT, image_path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        raise Http404("Image not found")
def architect_rate(request,person_id):
    if request.method=='POST':
        rate=int(request.POST['rate'])
        if 'id' in request.session:
            user_id = request.session['id']
            if 'user_model' in request.session:
                user_model_name = request.session['user_model']
                if user_model_name=='architecture':
                    data=ArchitectBooking.objects.get(PersonID=person_id)
                    if data.status=="accept":
                        data.Price=rate
                        data.RequesttoArchitect='accepted'
                        data.save()
                        return redirect('/viewrequest')
                    else:
                        data.RequesttoArchitect='declined'
                        data.save()
                        return redirect('/viewrequest')
                elif user_model_name == 'designer':
                    data=DesignerBooking.objects.get(PersonID=person_id)
                    if data.status=="accept":
                        data.Price=rate
                        data.RequesttoDesigner='accepted'
                        data.save()
                        return redirect('/viewrequest')
                    else:
                        data.RequesttoDesigner='declined'
                        data.save()
                        return redirect('/viewrequest')
                elif user_model_name == 'contractor':
                    data=ContractorBooking.objects.get(PersonID=person_id)
                    if data.status=="accept":
                        data.Price=rate
                        data.RequesttoContractor='accepted'
                        data.save()
                        return redirect('/viewrequest')
                    else:
                        data.RequesttoContractor='declined'
                        data.save()
                        return redirect('/viewrequest')
def user_submit_to_architect(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if request.method=='POST':
                userstatus=request.POST['userstatus']
                data=ArchitectBooking.objects.get(PersonID=user_id)
                data.RequestfromArchitect=userstatus
                data.save()
                print(data.RequestfromArchitect)
                print(userstatus)
                return redirect('/userrequest')
def user_submit_to_designer(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if request.method=='POST':
                userstatus=request.POST['userstatus']
                data=DesignerBooking.objects.get(PersonID=user_id)
                data.RequestfromDesigner=userstatus
                data.save()
                return redirect('/userrequest')
def user_submit_to_contractor(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if request.method=='POST':
                userstatus=request.POST['userstatus']
                data=ContractorBooking.objects.get(PersonID=user_id)
                data.RequestfromContractor=userstatus
                data.save()
                return redirect('/userrequest')
def payment(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if request.method=='POST':
                cardnumber=request.POST['cardnumber']
                cardholder=request.POST['cardholder']
                amount=request.POST['amount']
                edate=request.POST['edate']
                cvv=request.POST['cvv']
                logged_in_user = Users.objects.get(id=user_id)
                Payment.objects.create(UserName=logged_in_user.Name,User_ID=user_id,Account_Number=cardnumber,Cvv=cvv,ExpiryDate=edate,Amount=amount)
                return redirect('/')
        return render(request,"paymentform.html")
    return render(request,"paymentform.html")
def architect_design(request,person_id):
    if request.method=='POST':
        design=request.FILES.get('design')
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if user_model_name == 'architecture':
                user_model = ArchitectBooking
            elif user_model_name == 'designer':
                user_model = DesignerBooking
            elif user_model_name == 'contractor':
                user_model = ContractorBooking  
            data=user_model.objects.get(PersonID=person_id)
            data.File=design
            data.save()
            return redirect('/')
def status_update(request,person_id):
    if request.method=='POST':
        if 'id' in request.session:
            user_id = request.session['id']
            if 'user_model' in request.session:
                user_model_name = request.session['user_model']
                if request.method=='POST':
                    status=request.POST['status']
                    if user_model_name=='architecture':
                        data=ArchitectBooking.objects.get(PersonID=person_id)
                        data.status=status
                        data.save()
                        return redirect('/viewrequest')
                    elif user_model_name == 'designer':
                        data=DesignerBooking.objects.get(PersonID=person_id)
                        data.status=status
                        data.save()
                        return redirect('/viewrequest')
                    elif user_model_name == 'contractor':
                        data=ContractorBooking.objects.get(PersonID=person_id)
                        data.status=status
                        data.save()
                        return redirect('/viewrequest')
def user_architecture_interest(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if request.method=='POST':
                userstatus=request.POST['status']
                data=ArchitectBooking.objects.get(PersonID=user_id)
                data.interest=userstatus
                data.save()
                return redirect('/userrequest')   
def user_designer_interest(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if 'user_model' in request.session:
            user_model_name = request.session['user_model']
            if request.method=='POST':
                userstatus=request.POST['status']
                data=DesignerBooking.objects.get(PersonID=user_id)
                data.interest=userstatus
                data.save()
                return redirect('/userrequest')    
def delete_request(request,id):
    x=ArchitectBooking.objects.get(id=id) 
    x.delete()
    return redirect('profile') 
def delete_request1(request,id):
    x=DesignerBooking.objects.get(id=id) 
    x.delete()
    return redirect('profile')
def delete_request2(request,id):
    x=ContractorBooking.objects.get(id=id) 
    x.delete()
    return redirect('profile')     