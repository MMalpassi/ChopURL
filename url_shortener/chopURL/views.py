from django.shortcuts import render, redirect, get_object_or_404
from .models import shortURL
import string, random

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def chop_url(request):
    if request.method == 'POST':
        url = request.POST['url']
        code = generate_short_code()
        short_url = shortURL.objects.create(original_url=url, short_code=code)
        return render(request, 'result.html', {'short_url': short_url})
    
    # If method == GET:
    return render(request, 'index.html')

def redirect_url(request, code):
    short_url = get_object_or_404(shortURL, short_code=code)
    return redirect(short_url.original_url)
