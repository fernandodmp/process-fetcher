from django import forms


class SearchForm(forms.Form):
    """
    The search form of the index page
    """
    tribunal_choice = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tribunal', 'required':'true'}), 
        choices = [('TJSP', 'TJSP'), ('TJMS', 'TJMS'),], label = 'Tribunal')
    process_number = forms.CharField(max_length=25, min_length=25, required = True, label = 'Numero do Processo', widget=forms.TextInput(attrs={'class': 'form-control'}))