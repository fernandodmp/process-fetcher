from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from crawler.forms import SearchForm
from crawler.crawler_script import tribunal_crawler
from bs4 import BeautifulSoup


# Create your views here.
def search_page(request):
    """ 
    View of the main page where the user can enter the query data
    """
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            tribunal_choice = form.cleaned_data['tribunal_choice']
            process_number = form.cleaned_data['process_number']
            return redirect(reverse('results_page', args=(tribunal_choice, process_number)))
    return render(request, 'crawler/search_page.html', context={'form':form})

def results_page(request, tribunal_choice, process_number):
    """
    View of the page where the fetched data will be shown 
    """
    #Dict associating each tribunal to it's url
    tribunals_links = {
        'TJSP' : "https://esaj.tjsp.jus.br/cpopg/open.do",
        'TJMS': "https://www.tjms.jus.br/cpopg5/open.do"
    }

    #Try to fetch the data
    try:
        #Ask a Celery worker to crawl into the tribunal website and fetch the data
        tables = tribunal_crawler.delay(tribunals_links[tribunal_choice], process_number).get()
        messages.success(request, 'Por favor aguarde enquanto buscamos as informações')
        #If tables is none that means that the crawler did not find the process or something went wrong
        if tables == None:
            return render(request, 'crawler/error.html')

        #Context dict to be shown in the web-page        
        context_dict = {
            'Numero': process_number,
            'Tribunal': tribunal_choice,
            'Dados': tables[0],
            'Partes': tables[1],
            'Movimentacoes': tables[2]     
        }

        return render(request, 'crawler/results_page.html',context=context_dict)
    except:
        return render(request, 'crawler/error.html')
    