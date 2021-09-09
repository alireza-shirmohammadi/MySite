from django.shortcuts import render,redirect
from .models import Cat
import csv
from django.http import HttpResponse

# Create your views here.
def cat_list (request):
      # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end
    cat=Cat.objects.all()
    return render (request,'back/cat_list.html',{'cat':cat})
def cat_add (request):
      # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end
    if request.method=='POST':
        name=request.POST.get('name')
        if name=='':
                error= "All Fields Requirded"
                return render (request,'back/error.html',{'error':error})
        if len(Cat.objects.filter(name=name))!=0 :
             error = "This Name Used Before"
             return render(request, 'back/error.html' , {'error':error})
        b=Cat(name=name)
        b.save()
        return redirect('cat_list')

    return render(request,'back/cat_add.html')

def export_cat_csv(request):
    responde=HttpResponse(content_type="text/csv")
    responde['Content_Disposition']='attachment; filename="cat.csv"'
    writer=csv.writer(responde)
    writer.writerow(['title','counter'])
    for i in Cat.objects.all():
        writer.writerow([i.name,i.count])
    return responde

def import_cat_csv(request):
    if request.method=='POST':
        file=request.FILES['csv_file']
        if not file.name.endwith('csv'):
            error = "Please Input Csv File"
            return render(request, 'back/error.html' , {'error':error})
        if file.multiple_chunks():
            error = "File Too Large"
            return render(request, 'back/error.html' , {'error':error})
        file_data=file.read().decode('utf-8')
        lines=file_data.split("\n")
        for line in lines :
            field=line.split(",")
            try:
                if len(Cat.objects.filter(name=field[0]))==0 and field[0] != 'title' and field[0] != '':
                    print(field[0])

                    b=Cat(name=field[0])
                    b.save()

            except:
                print('finish')
    return redirect('cat_list')
