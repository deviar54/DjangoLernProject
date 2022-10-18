from multiprocessing import context
from .models import News, Category
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewsForm
from django.views.generic import ListView, DetailView, CreateView
from typing import *
from django.db import models
from django.forms import BaseForm
from django.urls import reverse_lazy

#Фрагмент кода ниже позволяет использовать модели в шаблонах через классы

class HomeNews(ListView):
    model: Optional[Type[models.Model]] = News
    template_name = 'news/home_news_list.html' #Переопределение стандартного имени шаблона Имя_класса_list
    context_object_name = 'news' #Что бы обратится к экземплярам класса из шаблона можно 
                                 #переопределить стандартное имя object_list на какое удобно
    # extra_context = {'title': 'Главная'} применяется если  необходимо переопределить статический контент

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published = True)


class NewsByCategory(ListView):
    model: Optional[Type[models.Model]] = News
    template_name: str = 'news/home_news_list.html'
    context_object_name: str = 'news'
    allow_empty: bool = False

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: dict = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id = self.kwargs['category_id'], is_published = True)
    

class ViewNews(DetailView):
    model: Type[models.Model] = News
    #pk_url_kwarg: str = 'news_id'
    success_url = reverse_lazy('home') #в случае если в модели не реализован метод get_absolute_url после создания экземпляра
                                       #переход будет осуществлен по данной ссылке


class CreateNews(CreateView):
    form_class: Optional[Type[BaseForm]] = NewsForm
    template_name: str = 'news/add_news.html'
            
#Здесь модели используются через функции

# def index(request):
#     news = News.objects.all()

#     context = {
#         'news': news,
#         'title': 'Список новостей ',
#     }
#     return render(request, 'news/index.html', context = context)

# def view_news(request, news_id):
#     #news_item = News.objects.get(pk = news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item':news_item
#     }
#     return render(request, 'news/view_news.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id = category_id)
#     category = Category.objects.get(pk = category_id)
#     context={
#         'news':news,
#         'category': category,
#     }
#     return render(request, 'news/category.html', context = context)

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             news = form.save()
#             return redirect('home')
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', context={'form': form})
