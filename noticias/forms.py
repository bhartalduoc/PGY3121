from django import forms

class NoticiaForm(forms.Form):
    titulo = forms.CharField(label='Título')
    cuerpo = forms.CharField(label='Cuerpo', widget=forms.Textarea)
    ubicacion = forms.CharField(label='Ubicación')
    archivo = forms.FileField(label='Archivo')
    destacada = forms.BooleanField(label='Destacada', required=False)