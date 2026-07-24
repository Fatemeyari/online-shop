from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views.generic import View , TemplateView , UpdateView , ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin 

from dashboard.permissions import HasAdminAccessPermission
from accounts.models import User , Profile
from dashboard.admin.forms import AdminPasswordChangeForm ,AdminProfileEditForm
from shop.models import Product,ProductCategory,ProductStatusType
class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccessPermission,TemplateView):
    template_name="dashboard/admin/home.html"


class AdminSecurityEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name="dashboard/admin/security_edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message= "به روزرسانی پسورد با موفقیت انجام شد."

    def form_invalid(delf , form):
        return super().form_invalid(form)


class AdminProfileEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    template_name="dashboard/admin/profile_edit.html"
    form_class = AdminProfileEditForm
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message= "به روزرسانی پروفایل  با موفقیت انجام شد."

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)




class AdminProductListView(LoginRequiredMixin,HasAdminAccessPermission,ListView):
    template_name="dashboard/admin/product_list.html"
    paginate_by = 9


    def get_queryset(self):
        queryset = Product.objects.all()

        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(
                title__icontains=search_q
            )

        if category := self.request.GET.get("category"):
            queryset = queryset.filter(
                category__id=category
            )

        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(
                price__gte=min_price
            )

        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(
                price__lte=max_price
            )

        if sort := self.request.GET.get("sort"):

            if sort == "newest":
                queryset = queryset.order_by("-created_time")

            elif sort == "oldest":
                queryset = queryset.order_by("created_time")

            elif sort == "cheap":
                queryset = queryset.order_by("price")

            elif sort == "expensive":
                queryset = queryset.order_by("-price")

        return queryset.distinct()
                

    def get_context_data(self , **kwargs):
        context= super().get_context_data(**kwargs)
        context["total_items"] =self.get_queryset().count()
        context["categories"]= ProductCategory.objects.all()
        return context  





        