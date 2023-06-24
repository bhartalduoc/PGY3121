from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import NoticiaForm
from .models import Categoria, Noticia
from django.core.files.storage import default_storage
from django.conf import settings

# Create your views here.

def index (request):
    noticias_destacadas = Noticia.objects.filter(destacada=True, estado=3)
    noticias_varias = Noticia.objects.filter(destacada=False, estado=3)
    context = {
        'noticias_destacadas': noticias_destacadas,
        'noticias_varias': noticias_varias,
    }
    return render (request,'noticias/index.html',context)

def noticia(request):
    id_noticia = request.GET.get('id')
    noticia = get_object_or_404(Noticia, idNoticia=id_noticia)
    usuario = get_object_or_404(User, username=noticia.idUsuario)
    categoria = get_object_or_404(Categoria, categoria=noticia.categoria)
    return render(request, 'noticias/noticia.html', {'noticia': noticia, 'usuario': usuario, 'categoria': categoria})

def categorias (request):
    context = {}
    return render (request,'noticias/categorias.html',context)

def periodistas (request):
    context = {}
    return render (request,'noticias/periodistas.html',context)

def contacto (request):
    context = {}
    return render (request,'noticias/contacto.html',context)

def signin (request):
    form_context = {
        'form': AuthenticationForm
    }
    if request.method == 'GET':
        return render (request,'noticias/signin.html',form_context)
    else:
        try:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                form_context = {
                    'form': AuthenticationForm,
                    'error_form': "Username or password is incorrect."
                }
                return render(request, 'signin.html', form_context)
            login(request, user)
            return redirect('index')
        except:
            form_context = {
                'form': AuthenticationForm,
                'error_form': "Username or password is incorrect."
            }
            return render(request,'noticias/signin.html',form_context)

def signup (request):
    form_context = {
        'form': UserCreationForm
    }
    
    if request.method == 'GET':
        return render (request,'noticias/signup.html',form_context)
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                        request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                form_context = {
                    'form': UserCreationForm,
                    'error_form': "El usuario ya existe"
                }
                return render(request,'noticias/signup.html',form_context)
        elif request.POST["password1"] != request.POST["password2"]:
            form_context = {
                'form': UserCreationForm,
                'error_form': "Las contraseñas deben coincidir"
            }
            return render(request,'noticias/signup.html',form_context)
    return render (request,'noticias/signup.html',form_context)

@login_required
def signout(request):
    logout(request)
    return redirect('index')

@login_required
def add_news(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        #form = NoticiaForm(request.POST, request.FILES)
        #if form.is_valid():
        # Procesar el formulario y guardar la noticia en la base de datos
        noticia = Noticia()
        noticia.noticia = request.POST['titulo']
        noticia.cuerpo = request.POST['cuerpo']
        noticia.ubicacion = request.POST['ubicacion']
        
        categoria_input = request.POST['categoria']
        idCategoria = get_object_or_404(Categoria, categoria=categoria_input)
        noticia.categoria = idCategoria
        
        try:
            destacada_input = request.POST['destacada']
        except:
            destacada_input = False
        
        if destacada_input == "on": flag_destacada = True
        else: flag_destacada = False
        
        noticia.destacada = flag_destacada
        
        idUsuario = get_object_or_404(User, username=request.user)
        noticia.idUsuario = idUsuario
        print(idUsuario)
        
        # Realizar las operaciones necesarias con los datos
        imagen = request.FILES['imagen']
        ruta_imagen = default_storage.save('img/' + imagen.name, imagen)
        url_imagen = settings.MEDIA_URL + ruta_imagen
        noticia.imagen = url_imagen
        
        #Guardar noticia
        noticia.save()
        
        # Redireccionar a la página de éxito o realizar otra acción
        return render (request,'noticias/add_news.html',
                  {'categorias': categorias})
    else:
        return render(request, 'noticias/add_news.html',
                  {'categorias': categorias})










def noticia1 (request):
    context = {}
    return render (request,'noticias/noticia1.html',context)

def noticia2 (request):
    context = {}
    return render (request,'noticias/noticia2.html',context)

def noticia3 (request):
    context = {}
    return render (request,'noticias/noticia3.html',context)

def noticia4 (request):
    context = {}
    return render (request,'noticias/noticia4.html',context)

def noticia5 (request):
    context = {}
    return render (request,'noticias/noticia5.html',context)

def noticia6 (request):
    context = {}
    return render (request,'noticias/noticia6.html',context)

def noticia7 (request):
    context = {}
    return render (request,'noticias/noticia7.html',context)

def noticia8 (request):
    context = {}
    return render (request,'noticias/noticia8.html',context)

def noticia9 (request):
    context = {}
    return render (request,'noticias/noticia9.html',context)