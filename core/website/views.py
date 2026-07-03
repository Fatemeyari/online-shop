from django.shortcuts import render , redirect
from django.views.generic import TemplateView , CreateView
from django.views import View
from django.contrib import messages

from .forms import ContactForm , NewsLetterForm
from .models import ContactUs
# Create your views here.


class IndexView(TemplateView):
    template_name='website/index.html'

class ContactView(TemplateView):
    template_name = "website/contact.html" 
    def get(self , request):
        form=ContactForm()
        return render(request , self.template_name , {"form":form})
    def post(self , request):
        form=ContactForm(request.POST)
        if form.is_valid():
            fullname=form.cleaned_data['fullname']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            subject=form.cleaned_data['subject']
            message=form.cleaned_data['message']
    
            ContactUs.objects.create(
                fullname=fullname,
                email=email,
                phone_number=phone_number,
                subject=subject,
                message=message,
                is_seen=False

            )
            messages.success(request ,"تیکت شما با موفقیت ثبت شد.")
            return redirect("website:contact")
        messages.error(request ,"ارسال ناموفق بود. لطفاً اطلاعات را بررسی کنید.")
        return render(request, self.template_name, {"form": form})

    
class AboutView(TemplateView):
    template_name = 'website/about.html'

    
class NewsLetterView(CreateView):
    http_method_names=['post']
    form_class=NewsLetterForm
    success_url = '/'

    def form_valid(self , form):
        form.save()
        messages.success(
            self.request ,'از ثبت نام شما متشکریم. اخبار جدید به شما اطلاع رسانی خواهد شد .'
        )
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(
            self.request , 'ارسال ناموفق بود لطفا اطلاعات را بررسی کنید.'
        )
        return redirect('website:index')
