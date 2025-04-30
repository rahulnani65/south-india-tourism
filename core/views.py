# # from django.shortcuts import render
# # from .models import State

# # def home(request):
# #     states = State.objects.all()
# #     return render(request, 'core/home.html', {'states': states})

# from django.shortcuts import render, redirect
# from .models import State, Contact

# def home(request):
#     states = State.objects.all()
#     return render(request, 'core/index.html', {'states': states})

# def state_detail(request, state_name):
#     return render(request, 'core/state.html', {'state_name': state_name})

# def contact_submit(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         Contact.objects.create(
#             name=name,
#             email=email,
#             phone=phone,
#             subject=subject,
#             message=message
#         )
#         return redirect('home')
#     return redirect('home')
from django.shortcuts import render, redirect
from .models import State, Contact

def home(request):
    states = State.objects.all()
    return render(request, 'core/index.html', {'states': states})

def state_detail(request, state_name):
    state = State.objects.get(name__iexact=state_name.replace('-', ' '))
    return render(request, 'core/state.html', {'state': state})

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        return redirect('home')
    return redirect('home')