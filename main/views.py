from django.shortcuts import render, redirect
import requests

def index(request):
    return render(request, 'main/index.html')

from django.shortcuts import render

def new_service_view(request):
    return render(request, 'main/moto_service.html')

def delivery_view(request):
    return render(request, 'main/delivery.html')

def conctacts_view(request):
    return render(request, 'main/contacts.html')

def submit_callback(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname', 'Не указано')
        phone = request.POST.get('phone', 'Не указано')
        
        service_type = request.POST.get('service_type')

        bot_token = '8993125417:AAGgsRtPqxBSSMNnaJDtepzld1Ue5m2S5-0' 
        chat_id = '5133348979'

        text = f"🚨 Новая заявка!\n\nИмя: {fullname}\nТелефон: {phone}"

        if service_type:
            services_map = {
                'delivery': 'Доставка техники',
                'parts': 'Подбор запчастей',
                'service': 'Сервисное обслуживание'
            }
            service_name = services_map.get(service_type, service_type)
            text += f"\nУслуга: {service_name}"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text
        }
        
        try:
            requests.post(url, data=data, timeout=5)
        except requests.exceptions.RequestException:
            pass

        return redirect(request.META.get('HTTP_REFERER', '/'))
        
    return redirect('/')