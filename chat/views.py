from django.shortcuts import render
from django.views.generic import CreateView
from .models import Chat
from main.models import Category
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from .forms import ChatForm
import operator
from django.contrib.auth.decorators import login_required



@login_required
def ChatView(request, pk):
    chats = Chat.objects.filter(author_id=pk)
    user_chats = Chat.objects.filter(author=request.user)
    cat_menu = Category.objects.all()
    chat_menu = User.objects.all()
    if request.method == 'POST':
        form = ChatForm(request.POST, instance=request.user)
        def form_valid(self, form):
            form.instance.author = self.request.user
            form.instance.person_to_id = self.kwargs.get('pk')
            return super().form_valid(form)
    else:
        form = ChatForm(request.POST)
    all_chats = []
    for chat in chats:
      if chat.person_to == request.user:
        all_chats.append(chat)
    for chat in user_chats:
      if chat.person_to.id == pk:
        all_chats.append(chat)
    all_chats.sort(key = operator.attrgetter('date_posted'), reverse = True)
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
    return render(request,  'chat/chat.html', {'chats': all_chats, 'pk': pk, 'chat_menu': chat_menu, 'cat_menu': cat_menu, 'sidebar': savenot, 'form': form})




class CreateChat(CreateView):
    model = Chat
    template_name = 'chat/create_chat.html'
    form_class = ChatForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.person_to_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('close')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["pk"] = self.kwargs['pk']
        return(context)

def close(request):
    return HttpResponse('<script type="text/javascript">window.close()</script>')