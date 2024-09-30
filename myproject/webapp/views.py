from django.shortcuts import render,redirect
from .forms import CreateUserForm, LoginForm, CreateAssetForm, UpdateAssetForm
from django.db import connection
from django.db.models import Q
import pandas as pd

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from .models import assets
from django.contrib.auth.decorators import login_required
# import message
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'webapp/home.html')

# Register a user
def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()
            
            return redirect('my-login')

    context = {'form':form}

    return render(request,'webapp/register.html',context=context)

# Login a user
def my_login(request):

    form = LoginForm()
    if request.method =="POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)

                return redirect('dashboard')
                
    context = {'form':form}
    return render(request,'webapp/my-login.html', context=context)

# User logout

def user_logout(request):
    auth.logout(request)
    return redirect('my-login')

# Dashboard
@login_required(login_url='my-login')
def dashboard(request):
    query = request.GET.get('q')
    
    if query:
        all_asset = assets.objects.filter(
            Q(asset_no__icontains=query) |
            Q(asset_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(serial_no__icontains=query) |
            Q(department_name__icontains=query) |
            Q(owner_name__icontains=query) |
            Q(location__icontains=query) |
            Q(status__icontains=query)
            # Q(remark__icontains=query)
        )  # ค้นหาโดยใช้ชื่อทรัพย์สิน (asset_name)
    else:
        all_asset = assets.objects.all()

    return render(request,'webapp/dashboard.html',{"all_asset":all_asset})

# Create- Assets
@login_required(login_url='my-login')
def create_assets(request):
    if request.method == "POST":
        # รับข้อมูล/บันทึก
        
        assets.objects.create(
            asset_no = request.POST.get("asset_no"),
            asset_name = request.POST.get("asset_name"),
            brand = request.POST.get("brand"),
            model = request.POST.get("model"),
            serial_no = request.POST.get("serial_no"),
            department_name = request.POST.get("department_name"),
            owner_name = request.POST.get("owner_name"),
            location = request.POST.get("location"),
            status = request.POST.get("status"),
            remark = request.POST.get("remark"),

            
        )
        # form.save()
        messages.success(request,"บันทึกข้อมูลเรียบร้อย")

        # เปลี่ยนเส้นทาง
        return redirect("/") #
   
    return render(request, 'webapp/create-asset.html')
    

# Update - Assets
@login_required(login_url='my-login')
def update_assets(request, pk):
    asset = assets.objects.get(id = pk)

    if request.method == "POST":
        # อัพเดทข้อมูล    
        asset.asset_no = request.POST.get("asset_no")
        asset.asset_name = request.POST.get("asset_name")
        asset.brand = request.POST.get("brand")
        asset.model = request.POST.get("model")
        asset.serial_no = request.POST.get("serial_no")
        asset.department_name = request.POST.get("department_name")
        asset.owner_name = request.POST.get("owner_name")
        asset.location = request.POST.get("location")
        asset.status = request.POST.get("status")
        asset.remark = request.POST.get("remark")

        # form = UpdateAssetForm(instance=asset)
        # form = UpdateAssetForm(request.POST, instance=asset)
        # เปลี่ยนข้อมูลใหม่
        # if form.is_valid():
                        
        # บันทึก
        asset.save()

            #Alert Message
        messages.success(request,'Updated Success')

            # เปลี่ยนเส้นทาง
        return redirect('view-assets',pk=pk)
    
    return render(request,'webapp/update-asset.html',{"asset":asset}) 

# Read / View - Assets
@login_required(login_url='my-login')
def read_assets(request, pk):
    view_assets = assets.objects.get(id=pk)
    return render(request, 'webapp/view-asset.html',{'view_assets':view_assets})

# Delete - Assets
@login_required(login_url='my-login')
def delete_assets(request, pk):

    delete_assets = assets.objects.get(id = pk)
    delete_assets.delete()

    #Alert Message
    messages.success(request,'Deleted Success')

    # เปลี่ยนเส้นทาง
    return redirect('dashboard')

# Import - Asset
@login_required(login_url='my-login')
def import_assets(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]

        # ลบข้อมูลทั้งหมดในโมเดล assets ก่อน
        assets.objects.all().delete()

        # รีเซ็ตค่า id ให้เริ่มต้นจาก 1 ใหม่
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='webapp_assets';")

        # อ่านไฟล์ Excel โดยใช้ pandas
        df = pd.read_excel(excel_file, engine='openpyxl')

        # Loop ผ่าน Data Frame และบันทึกลงในฐานข้อมูล
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            asset = assets(
                asset_no=row_dict['รหัสทรัพย์สิน'],
                asset_name=row_dict['ชื่อทรัพย์สิน'],
                brand=row_dict['ยี่ห้อ'],
                model=row_dict['รุ่น'],
                serial_no=row_dict['S/N'],
                department_name=row_dict['หน่วยงาน/โครงการ'],
                owner_name=row_dict['ผู้ดูแล'],
                location=row_dict['สถานที่ใช้งาน'],
                status=row_dict['สถานะใช้งาน'],
                remark=row_dict['หมายเหตุ'],
            )
            asset.save()
        
        messages.success(request,'Import Success')

        return redirect('import-assets')
    
    return render(request,'webapp/import-assets.html') 
