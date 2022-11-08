from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Post, Comment
from main.models import Category
from chat.models import Chat
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .utils import NewPost, Backup
from .forms import AddCommentForm, PostForm
import operator
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from users.forms import Profile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class PostListView(FilterView):
    paginate_by = 7
    ordering = ['-date_posted']
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    @method_decorator(csrf_exempt)
    def get_queryset(self):
      queryset = Post.objects.filter(category='Complaints') | Post.objects.filter(category='Feature-Requests') | Post.objects.filter(category='Conversation') | Post.objects.filter(category='Coding').order_by('-date_posted') | Post.objects.filter(category='Implemented-requests').order_by('-date_posted')
      return queryset
    @method_decorator(csrf_exempt)
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        chat_menu = User.objects.all()
        context = super().get_context_data(*args, **kwargs)
        notifications = Chat.objects.filter(person_to_id=self.request.user.id).order_by('-date_posted')
        notifics = []
        savenot = True
        for notification in notifications:
          if notifics:
            for notific in notifics:
              if notification.person_to == notific.person_to:
                savenot == False
            if savenot:
              notifics.append(notification)
          else:
              notifics.append(notification)
        if notifics: context["sidebar"] = notifics
        context["cat_menu"] = cat_menu
        context["chat_menu"] = chat_menu
        context["hello"] = True
        return(context)
        


  
@login_required
def viewpost(request, pk):
    post = Post.objects.get(id=pk)
    total_comments = 0
    for c in post.comments.all():
        total_comments += 1
    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form.instance.post_id = pk
            form.instance.author_id = request.user.id
            print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
        form = AddCommentForm()
    else:
        form = AddCommentForm()
    cat_menu = Category.objects.all()
    chat_menu = User.objects.all()
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
    return render(request, 'blog/details.html', {'post': post, 'liked': liked, 'total_likes': total_likes, 'pk': pk, 'form': form, 'total_comments': total_comments, 'sidebar': savenot, 'chat_menu': chat_menu, 'cat_menu': cat_menu})






class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        NewPost(self.request.user.username, form.instance.title, form.instance.content, emails=[self.request.user.email])
        Backup()
        return super().form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        chat_menu = User.objects.all()
        cat_menu = Category.objects.all()
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
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




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

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



class UserPostListView(LoginRequiredMixin, ListView):
    paginate_by = 7
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        quser = Profile.objects.filter(user__username=self.kwargs.get('username')).first()
        stuff = get_object_or_404(Profile, user=quser.id)
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        cat_menu = Category.objects.all()
        chat_menu = User.objects.all()
        context = super().get_context_data(*args, **kwargs)
        
        user = get_object_or_404(User, username=self.kwargs.get('username'))
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
        context["total_likes"] = total_likes
        context["liked"] = liked
        context["cat_menu"] = cat_menu
        context["chat_menu"] = chat_menu
        context["postuser"] = user
        return(context)

@login_required

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


@login_required
def UserLikeView(request, pk):
    post = get_object_or_404(Profile, user_id=request.POST.get('postuser_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('user-posts', args=[str(post.user.username)]))



class CreateComment(CreateView):
    model = Comment
    form_class = AddCommentForm
    template_name = 'blog/create_new_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)
      
    def get_success_url(self):
        return reverse('close')


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
        context["cat_menu"] = cat_menu
        context["chat_menu"] = chat_menu
        return(context)

class DeleteComment(DeleteView):
    model = Comment
    template_name = 'blog/delete_comment.html'

    def get_success_url(self):
        qp = Post.objects.filter(comments=self.kwargs['pk']).first()
        return reverse('post-detail', kwargs={'pk': qp.id})

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
