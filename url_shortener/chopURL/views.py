from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import shortURL
import string, random
import pyshorteners

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def chop_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        shortener_option = request.POST.get('chopurl_option')
        custom_domain = request.POST.get('custom_domain')

        if shortener_option == 'chopservice':
            code = generate_short_code()
            chop_short_url = shortURL.objects.create(
                original_url=url, 
                short_code=code,
                custom_domain=custom_domain if custom_domain else None
            )
            return render(request, 'result.html', {
                'url': url,
                'chop_short_url': chop_short_url,
                'pyservice_short_url': None,
            })
        
        elif shortener_option == 'pyservice':
            s = pyshorteners.Shortener()
            try:
                pyservice_short_url = s.tinyurl.short(url)
            except Exception as e:
                pyservice_short_url = None
            return render(request, 'result.html', {
                'url': url,
                'chop_short_url': None,
                'pyservice_short_url': pyservice_short_url,
            })
    
    return render(request, 'index.html')

def redirect_url(request, code):
    host = request.get_host()

    try:
        short_url = shortURL.objects.get(short_code=code, custom_domain=host)
    except shortURL.DoesNotExist:
        try:
            short_url = shortURL.objects.get(short_code=code, custom_domain__isnull=True)
        except shortURL.DoesNotExist:
            return HttpResponseBadRequest("Invalid short URL")

    return redirect(short_url.original_url)
