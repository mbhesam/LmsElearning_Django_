from django.shortcuts import render
from  django.views.generic import  (ListView ,FormView ,DetailView,TemplateView,CreateView,UpdateView,DeleteView)
from .models import Topics,Grade,Lesson
from django.views.generic.edit import FormMixin
from .forms import Topic_Form
from users.models import Profile
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from  .forms import  Comment_Form,Reply_Form,Topic_Form
class grade_list_view(ListView):
    context_object_name = "grades"
    medels = Grade
    template_name = "grade_list_view.html"
    def get_queryset(self):
        return Grade.objects.order_by('id')

class lesson_list_view(DetailView):
    context_object_name = "grades"
    medels = Grade
    template_name = "lesson_list_view.html"
    def get_queryset(self):
        return Grade.objects.order_by('id')

class topic_list_view(DetailView):
    context_object_name = "lessons"
    model = Lesson
    template_name = "topic_list_view.html"
    def get_queryset(self):
        return Lesson.objects.order_by('id')

class topic_detail_view(DetailView , FormMixin):
    context_object_name = "topics"
    model = Topics
    template_name = "topic_detail_view.html"
    form_class = Comment_Form
    second_form_class = Reply_Form
    def get_context_data(self, **kwargs):
        context = super(topic_detail_view,self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        elif 'form2' not in context:
            context['form'] = self.second_form_class()
        return context

    def get_success_url(self):
        self.object = self.get_object()
        grade = self.object.grade
        lesson = self.object.lesson
        return reverse_lazy('curriculum:topic_detail_view', kwargs={'standard': grade.slug,'object':lesson.slug, 'slug': self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fcommit = form.save(commit=False)
        fcommit.author = self.request.user
        fcommit.topic_name = self.object.comments.name
        fcommit.topic_name_id = self.object.id
        fcommit.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fcommit = form.save(commit=False)
        fcommit.author = self.request.user
        fcommit.comment_name_id= self.request.POST.get('comment.id')
        fcommit.save()
        return HttpResponseRedirect(self.get_success_url())


    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.form_class
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'
        form = self.get_form(form_class)
        if form_name == "form" and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name == "form2" and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def get_queryset(self):
        return Topics.objects.order_by('id')

class create_topic_view(CreateView):
    form_class = Topic_Form
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'topic_create_view.html'

    def get_success_url(self):
        self.object=self.get_object()
        grade=self.object.grade
        return reverse_lazy('curriculum:topic_list_view',kwargs={'standard':grade.slug,'slug':self.object.slug})

    def form_valid(self,form,*args,**kwargs):
        self.object=self.get_object()
        fcommit=form.save(commit=False)
        fcommit.created_by=self.request.user
        fcommit.grade=self.object.grade
        fcommit.lesson=self.object
        fcommit.save()
        return HttpResponseRedirect(self.get_success_url())

class topic_update_view(UpdateView):
    fields = ["name", "chapter", "video", "ppt", "notes"]
    medels = Topics
    context_object_name = 'topics'
    template_name = "topic_update_view.html"
    def get_success_url(self):
        grade=self.object.grade
        lesson = self.object.lesson
        return reverse_lazy('curriculum:topic_list_view',kwargs={'standard':grade.slug,'slug':lesson.slug})

    def get_queryset(self):
        return Topics.objects.order_by('id')

class topic_delete_view(DeleteView):
    medels = Topics
    context_object_name = 'topics'
    template_name = "topic_delete_view.html"

    def get_success_url(self):
        grade=self.object.grade
        lesson = self.object.lesson
        return reverse_lazy('curriculum:topic_list_view',kwargs={'standard':grade.slug,'slug':lesson.slug})

    def get_queryset(self):
        return Topics.objects.order_by('id')

def create_grade(request):
    fobj=Topics.objects.create(topic_id='first',grade=Grade.objects.get(name='6th'),created_by=Profile.objects.get(email='zizizi@gmail.com'),lesson=Lesson.objects.get(name='mathematics'),name='diffrential',chapter=1)

    return HttpResponse('hello')