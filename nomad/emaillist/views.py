from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render

from django.views import generic

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime

from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import RenewManagerForm

from .models import (Subscription, Manager, Department, Title, WorkingUser)


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Генерация "количеств" некоторых главных объектов
    num_Managers = Manager.objects.filter(status='+').count()
    num_Subscriptions = Subscription.objects.count()
    num_Departments = Department.objects.count()
    num_Titles = Title.objects.count()

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_Managers': num_Managers,
                 'num_Subscriptions': num_Subscriptions,
                 'num_Departments': num_Departments,
                 'num_Titles': num_Titles,
                 'num_visits': num_visits
                 },
    )


class ManagerListView(generic.ListView):
    model = Manager

    context_object_name = 'manager_list'  # имя переменной контекста в шаблоне
    # queryset = Manager.objects.filter(status='+')[:5]  # Получение 5 актуальных менеджеров
    template_name = 'managers/template_manger_list.html'  # Определение имени шаблона и его расположения

    paginate_by = 10

    # context_object_name = 'all_search_results'
    def get_queryset(self):
        result = super(ManagerListView, self).get_queryset()
        query = self.request.GET.get('search')
        print(query)
        if query:
            postresult = Manager.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
            # помни почему в sqlite не работает нормально бпоиск без учета регистра!!!
            # https://docs.djangoproject.com/en/2.1/ref/databases/#sqlite-string-matching
            result = postresult
        else:
            result = Manager.objects.filter(status='+')
        return result


class ManagerDetailView(generic.DetailView):
    model = Manager


class DepartmentDetailView(generic.DetailView):
    model = Department


class DepartmentListView(generic.ListView):
    model = Department


class TitleDetailView(generic.DetailView):
    model = Title


class TitleListView(generic.ListView):
    model = Title


class SearchView(generic.ListView):
    model = Manager
    template_name = 'manager_list.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Manager.objects.filter(first_name__icontains=query)
            result = postresult
        else:
            result = None
        return result


def renew_Manager(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    manager_inst = get_object_or_404(Manager, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewManagerForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            manager_inst.first_name = form.cleaned_data['first_name']
            manager_inst.middle_name = form.cleaned_data['middle_name']
            manager_inst.last_name = form.cleaned_data['last_name']
            manager_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('managers'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today()
        form = RenewManagerForm(initial={"first_name": manager_inst.first_name,
                                         "middle_name": manager_inst.middle_name,
                                         "last_name": manager_inst.last_name,
                                         })

    return render(request, 'emaillist/renew_Manager.html',
                  {'form': form, 'managerinst': manager_inst})


class SubscriptionDetailView(generic.DetailView):
    model = Subscription


class SubscriptionListView(LoginRequiredMixin, generic.ListView):
    model = Subscription

    def get_queryset(self):
        return Subscription.objects.filter(created_by=self.request.user).order_by('id')


class SubscriptionCreate(LoginRequiredMixin, CreateView):
    model = Subscription
    fields = ['name', 'status', 'frequency']
    success_url = reverse_lazy('subscriptions')


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(SubscriptionCreate, self).form_valid(form)

    # def __init__(self, *args, **kwargs):
    #     super(SubscriptionCreate, self).__init__(*args, **kwargs)
    #     self.fields['created_by'] = self.request.user


class SubscriptionUpdate(UpdateView):
    model = Subscription
    fields = ['name', 'status', 'frequency']
    success_url = reverse_lazy('subscriptions')


class SubscriptionDelete(DeleteView):
    model = Subscription
    success_url = reverse_lazy('subscriptions')
