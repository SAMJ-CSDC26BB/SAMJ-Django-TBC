# samj/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from .models import Zielnummer
from .forms import EntryForm, ZielnummerForm

class TbcView(TemplateView):
    template_name = 'tbc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EntryForm()
        context['entries'] = [
            {
                'id': 1,
                'kopfnummer': '4327',
                'durchwahl': '001',
                'zielnummer': 'Beierl',
                'anfangsdatum': '2024-05-31 10:00',
                'endedatum': '2024-05-31 12:00',
                'dauer': '2 hours',
            },
            {
                'id': 2,
                'kopfnummer': '4328',
                'durchwahl': '002',
                'zielnummer': 'Info',
                'anfangsdatum': '2024-05-31 14:00',
                'endedatum': '2024-05-31 16:00',
                'dauer': '2 hours',
            },
        ]
        return context

def add_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            # Implement your logic here
            return redirect('tbc')
    else:
        form = EntryForm()
    return render(request, 'tbc.html', {'form': form, 'entries': []})

def edit_entry(request, entry_id):
    # Implement your logic to edit an entry
    pass

def delete_entry(request, entry_id):
    # Implement your logic to delete an entry
    pass

def copy_entry(request, entry_id):
    # Implement your logic to copy an entry
    pass

class ZielnummernView(TemplateView):
    template_name = 'zielnummern.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zielnummern'] = Zielnummer.objects.all()
        context['form'] = ZielnummerForm()
        return context

class AddZielnummer(View):
    def post(self, request):
        form = ZielnummerForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('zielnummern')

class EditZielnummer(View):
    def post(self, request, pk):
        zielnummer = get_object_or_404(Zielnummer, pk=pk)
        form = ZielnummerForm(request.POST, instance=zielnummer)
        if form.is_valid():
            form.save()
        return redirect('zielnummern')

class DeleteZielnummer(View):
    def post(self, request, pk):
        zielnummer = get_object_or_404(Zielnummer, pk=pk)
        zielnummer.delete()
        return redirect('zielnummern')
