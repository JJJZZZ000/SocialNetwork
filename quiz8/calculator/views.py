from django.shortcuts import render
from calculator.forms import CalcForm
# Create your views here.
def calculator(request):
    if request.method == "GET":
        return render(request, "calculator.html", {'form': CalcForm()})
    form = CalcForm(request.POST)
    if not form.is_valid():
        return render(request,"calculator.html",{'form':form})
    x = form.cleaned_data['x']
    y = form.cleaned_data['y']
    print(x/y)
    return render(request, "calculator.html", {'form':form, 'message':f"{x} / {y} = {x/y}"})
