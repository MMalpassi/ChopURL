from django.shortcuts import render, redirect, get_object_or_404
from .models import shortURL
import string, random
import pyshorteners

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def chop_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        shortener_option = request.POST.get('chopurl_option')

        if shortener_option == 'chopservice':
            code = generate_short_code()
            chop_short_url = shortURL.objects.create(original_url=url, short_code=code)
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
    short_url = get_object_or_404(shortURL, short_code=code)
    return redirect(short_url.original_url)
