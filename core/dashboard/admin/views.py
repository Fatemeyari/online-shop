from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views.generic import View , TemplateView , UpdateView , ListView , UpdateView , DeleteView , CreateView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin 

from dashboard.permissions import HasAdminAccessPermission
from accounts.models import User , Profile
from dashboard.admin.forms import AdminPasswordChangeForm ,AdminProfileEditForm,ProductForm , ProductImageFormSet , AdminCouponForm
from shop.models import Product,ProductCategory,ProductStatusType
from order.models import CouponModel , OrderModel , OrderStatusType
from review.models import ReviewModel
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


class AdminProductEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    template_name="dashboard/admin/product_edit.html"
    queryset=Product.objects.all()
    form_class=ProductForm
    success_message="ویرایش محصول با موفقیت انجام شد."
    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit" , kwargs={"pk":self.get_object().pk}) 


    def get_context_data(self , **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["images_formset"] = ProductImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance = self.object
            )
        else:
            context["images_formset"] = ProductImageFormSet(
                instance=self.object,
            )
        
        return context

    def form_valid(self , form):
        context = self.get_context_data()
        images_formset=context["images_formset"]
        
        if images_formset.is_valid():
            self.object = form.save()
            images_formset.instance = self.object
            images_formset.save()

            return super().form_valid(form)
            
        return self.render_to_response(context)        

class AdminProductCreateView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,CreateView):
    template_name = "dashboard/admin/product_create.html"
    queryset = Product.objects.all()
    form_class = ProductForm
    success_message = "ایجاد محصول با موفقیت انجام شد."

    def get_context_data(self , **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.POST:
            context["images_formset"] = ProductImageFormSet(
                self.request.POST,
                self.request.FILES,
            )
        else:
            context["images_formset"] = ProductImageFormSet()
        
        return context


    def form_valid(self, form):
        form.instance.user = self.request.user
        context=self.get_context_data()
        images_formset=context["images_formset"]

        if images_formset.is_valid():
            form.instance.user = self.request.user
            self.object=form.save()
            images_formset.instance=self.object
            images_formset.save()

            return super().form_valid(form)
            
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-list")

class AdminProductDeleteView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,DeleteView):
    template_name="dashboard/admin/product_delete.html"
    queryset=Product.objects.all()
    success_message="حذف محصول با موفقیت انجام شد."
    success_url = reverse_lazy("dashboard:admin:product-list")


class CouponListView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,ListView):
    template_name="dashboard/admin/coupon_list.html"

    def get_queryset(self):
        queryset = CouponModel.objects.all()
        
        if search_q:= self.request.GET.get("coupon"):
            queryset = queryset.filter(code__icontains=search_q)

        if search_q := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

class CouponCreateView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,CreateView):
    template_name="dashboard/admin/coupon_create.html"
    form_class=AdminCouponForm
    success_message= "کپن با موفقیت ثبت شد."

    def get_queryset(self):
        return CouponModel.objects.all()

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupon-list")

class CouponEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    template_name="dashboard/admin/coupon_edit.html"
    form_class=AdminCouponForm
    success_message= "کپن با موفقیت تغییر یافت."

    def get_queryset(self):
        return CouponModel.objects.all()
    
    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupon-list")


class CouponDeleteView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,DeleteView):
    template_name="dashboard/admin/coupon_delete.html"
    success_url=reverse_lazy("dashboard:admin:coupon-list")
    success_message= "کپن با موفقیت حذف شد."


    def get_queryset(self):
        return CouponModel.objects.all()
    
   
   

class AdminSuccessOrderListView(LoginRequiredMixin,HasAdminAccessPermission,ListView):
    template_name="dashboard/admin/success_order_list.html"
    paginate_by = 5 
    
    def get_queryset(self):
        queryset = OrderModel.objects.all()
        
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    
    def get_context_data(self , **kwargs):
        context=super().get_context_data(**kwargs)

        success_orders=OrderModel.objects.filter(status=OrderStatusType.success)
        context["success_orders"] =success_orders

        return context

    
class AdminFailedOrderListView(LoginRequiredMixin,HasAdminAccessPermission,ListView):
    template_name="dashboard/admin/failed_order_list.html"
    paginate_by = 5 
    
    def get_queryset(self):
        queryset = OrderModel.objects.all()
        
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    
    def get_context_data(self , **kwargs):
        context=super().get_context_data(**kwargs)

        failed_orders=OrderModel.objects.filter(status=OrderStatusType.failed)
        context["failed_orders"] =failed_orders

        return context




class AdminOrderDetailView(LoginRequiredMixin,HasAdminAccessPermission,DetailView):
    template_name="dashboard/admin/order_detail.html"

    def get_queryset(self):
        return OrderModel.objects.all()



class CustomerOrderInvoiceView(LoginRequiredMixin,HasAdminAccessPermission,DetailView):
    template_name="dashboard/customer/order_invoice.html"

    def get_queryset(self):
        return OrderModel.objects.all()


class CustomerReviewListView(LoginRequiredMixin,HasAdminAccessPermission,ListView):
    template_name="dashboard/admin/review_list.html"
    paginate_by = 5 
    
    def get_queryset(self):
        queryset = ReviewModel.objects.all()
        return queryset

    
    def get_context_data(self , **kwargs):
        context=super().get_context_data(**kwargs)
        review=ReviewModel.objects.all()
        context["total_items"] = self.get_queryset().count()  
        return context




