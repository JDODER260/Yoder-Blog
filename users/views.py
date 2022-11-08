from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from main.models import Category
from chat.models import Chat
import operator
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if username != "Admin" or username != "admin" or username != "Administrator" or username != "administrator" or username != "Admin " or username != "admin " or username != "Administrator " or username != "administrator ":
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'You have successfully created a new account with the username {username}')
            else:
                messages.warning(request, 'You are not allowed a username like that!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    notifications = Chat.objects.filter(person_to_id=request.user.id).order_by('-date_posted')
    notifics = []
    savenot = []
    for notification in notifications:
            notifics.append(notification)
    for x in notifics:
        for y in notifications:
            if x.author == y.author:
                if savenot:
                    hello = False
                    for i in savenot:
                        if x.person_to == i.person_to:
                            hello = True
                            break
                    if not hello:
                        savenot.append(x)
                elif not savenot:
                    savenot.append(x)             
    savenot.sort(key = operator.attrgetter('date_posted'), reverse = True)
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been updated {username}')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    notifications = Chat.objects.filter(person_to_id=request.user.id).order_by('-date_posted')
    notifics = []
    savenot = []
    for notification in notifications:
            notifics.append(notification)
    for x in notifics:
        for y in notifications:
            if x.author == y.author:
                if savenot:
                    hello = False
                    for i in savenot:
                        if x.person_to == i.person_to:
                            hello = True
                            break
                    if not hello:
                        savenot.append(x)
                elif not savenot:
                    savenot.append(x)             
    savenot.sort(key = operator.attrgetter('date_posted'), reverse = True)
    context = {
        'u_form': u_form,
        'p_form': p_form
        }
    return render(request, 'users/profile.html', context)


class DeleteUser(DeleteView):
    model = User
    template_name = 'users/delete.html'

    def get_success_url(self):
        return reverse('blog-home')

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        chat_menu = User.objects.all()
        context = super().get_context_data(*args, **kwargs)
        notifications = Chat.objects.filter(person_to_id=self.request.user.id).order_by('-date_posted') 
        notifics = []
        savenot = []
        for notification in notifications:
            notifics.append(notification)
        for x in notifics:
            for y in notifications:
                if x.author == y.author:
                    if savenot:
                        hello = False
                        for i in savenot:
                            if x.person_to == i.person_to:
                                hello = True
                                break
                        if not hello:
                            savenot.append(x)
                    elif not savenot:
                        savenot.append(x)             
        savenot.sort(key = operator.attrgetter('date_posted'), reverse = True)
        if savenot: context["sidebar"] = savenot
        context["cat_menu"] = cat_menu
        context["chat_menu"] = chat_menu
        return(context)
    