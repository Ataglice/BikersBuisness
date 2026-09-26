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

import requests
from django.shortcuts import redirect
from django.conf import settings

def submit_callback(request):
    if request.method == 'POST':
        # 1. Проверка Honeypot
        honeypot = request.POST.get('website_url', '')
        if honeypot:
            # Если поле заполнено, это бот. Прерываем логику и отдаем стандартный редирект.
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # 2. Сбор данных
        fullname = request.POST.get('fullname', 'Не указано')
        phone = request.POST.get('phone', 'Не указано')
        service_type = request.POST.get('service_type')

        text = f"🚨 Новая заявка!\n\nИмя: {fullname}\nТелефон: {phone}"

        if service_type:
            services_map = {
                'delivery': 'Доставка техники',
                'parts': 'Подбор запчастей',
                'service': 'Сервисное обслуживание'
            }
            service_name = services_map.get(service_type, service_type)
            text += f"\nУслуга: {service_name}"

        # 3. Отправка в Telegram с использованием токенов из настроек
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': text
        }
        
        try:
            # Таймаут снижен до 3 секунд. Синхронный requests.post блокирует 
            # поток Django; длительное ожидание ответа Telegram замедлит работу сайта.
            requests.post(url, data=data, timeout=3)
        except requests.exceptions.RequestException:
            pass # Логирование ошибки будет уместным вместо pass в production-среде

        return redirect(request.META.get('HTTP_REFERER', '/'))
        
    return redirect('/')