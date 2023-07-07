from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Categoria, Noticia, Estado
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
    estado = get_object_or_404(Estado, estado=noticia.estado)
    if estado.idEstado == 3:
      return render(request, 'noticias/noticia.html', {'noticia': noticia, 'usuario': usuario, 'categoria': categoria})
    elif request.user.groups.filter(name='Administradores').exists():
      return render(request, 'noticias/noticia.html', {'noticia': noticia, 'usuario': usuario, 'categoria': categoria})
    elif noticia.idUsuario == get_object_or_404(User, username=request.user):
      return render(request, 'noticias/noticia.html', {'noticia': noticia, 'usuario': usuario, 'categoria': categoria})
    else:
      return redirect('index')

def categorias (request):
    categorias = Categoria.objects.all()
    noticias = Noticia.objects.filter(estado=3)
    context = {
      'categorias':categorias,
      'noticias':noticias,
    }
    return render (request,'noticias/categorias.html',context)

def periodistas (request):
    periodista_group = Group.objects.get(name='Periodista')
    periodistas = periodista_group.user_set.all()
    noticias = Noticia.objects.filter(estado=3)
    context = {
      'periodistas':periodistas,
      'noticias':noticias,
    }
    return render (request,'noticias/periodistas.html',context)

def contacto (request):
    context = {}
    return render (request,'noticias/contacto.html',context)

def signin (request):
    if request.method == 'GET':
        return render (request,'noticias/signin.html')
    else:
        try:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                form_context = {
                    'error_form': "Username or password is incorrect."
                }
                return render(request, 'signin.html', form_context)
            login(request, user)
            return redirect('index')
        except:
            form_context = {
                'error_form': "Username or password is incorrect."
            }
            return render(request,'noticias/signin.html',form_context)

def signup (request):
    if request.method == 'GET':
        return render (request,'noticias/signup.html')
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
                    'error_form': "El usuario ya existe"
                }
                return render(request,'noticias/signup.html',form_context)
        elif request.POST["password1"] != request.POST["password2"]:
            form_context = {
                'error_form': "Las contraseñas deben coincidir"
            }
            return render(request,'noticias/signup.html',form_context)
    return render (request,'noticias/signup.html',form_context)

@login_required
def change_passwd(request):
    if request.method == 'POST':
        contrasena_actual = request.POST['contrasena_actual']
        nueva_contrasena = request.POST['nueva_contrasena']
        confirmar_contrasena = request.POST['confirmar_contrasena']

        # Verificar si la contraseña actual del usuario es correcta
        if not request.user.check_password(contrasena_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('change_passwd')

        # Verificar si la nueva contraseña y la confirmación coinciden
        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, 'La nueva contraseña y la confirmación no coinciden.')
            return redirect('change_passwd')

        # Cambiar la contraseña del usuario y actualizar la sesión de autenticación
        request.user.set_password(nueva_contrasena)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, 'La contraseña ha sido cambiada exitosamente.')
        return redirect('index')
    return render(request, 'noticias/change_passwd.html')

@login_required
def signout(request):
    logout(request)
    return redirect('index')

@login_required
def administrador(request):
    context = {}
    return render (request,'noticias/categorias.html',context)

@login_required
def admin_noticia(request):
  estado_noticia = 3
  if request.GET.get('type'):
    estado_noticia = request.GET.get('type')
  noticias = Noticia.objects.filter(estado=estado_noticia)
  context = {
    'noticias': noticias,
  }
  if request.user.groups.filter(name='Administradores').exists():
    return render (request,'noticias/admin_noticia.html',context)
  else:
    return redirect('index')

@login_required
def accion_noticia(request):
  estados = Estado.objects.all()
  id_noticia = request.GET.get('id')
  noticia = get_object_or_404(Noticia, idNoticia=id_noticia)
  usuario = get_object_or_404(User, username=noticia.idUsuario)
  categoria = get_object_or_404(Categoria, categoria=noticia.categoria)
  context = {
    'noticia': noticia,
    'usuario': usuario,
    'categoria': categoria,
    'estados': estados
  }
  if request.user.groups.filter(name='Administradores').exists():
    if request.method == 'POST':
      comentario_input = request.POST['comentario']
      estado_input = request.POST['estado']
      if comentario_input.strip():
        noticia.comentario = comentario_input
        estado_noticia = get_object_or_404(Estado, estado=estado_input)
        noticia.estado = estado_noticia
        noticia.save()
        return redirect('admin_noticia')
      else:
        return render (request,'noticias/accion_noticia.html',context)
    else:
      context = {
        'noticia': noticia,
        'usuario': usuario,
        'categoria': categoria,
        'estados': estados,
        'err_msg': "Debe ingresar un comentario"
      }
      return render (request,'noticias/accion_noticia.html',context)
  else:
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
        
        #fix noadmin
        #noticia.estado = get_object_or_404(Estado, idEstado=3)
        
        #Guardar noticia
        noticia.save()
        
        # Redireccionar a la página de éxito o realizar otra acción
        return render (request,'noticias/add_news.html',
                  {'categorias': categorias})
    else:
        return render(request, 'noticias/add_news.html',
                  {'categorias': categorias})

@login_required
def my_news(request):
  idUsuario = get_object_or_404(User, username=request.user)
  noticias = Noticia.objects.filter(idUsuario=idUsuario)
  context = {
    'noticias': noticias,
  }
  if request.user.groups.filter(name='Periodista').exists():
    return render (request,'noticias/my_news.html',context)
  else:
    return redirect('index')

@login_required
def admin_users(request):
  usuarios = User.objects.all
  context = {
    'usuarios': usuarios,
  }
  if request.user.groups.filter(name='Administradores').exists():
    return render (request,'noticias/admin_users.html',context)
  else:
    return redirect('index')

@login_required
def user_chng(request):
    usuario = get_object_or_404(User, pk=request.GET.get('id'))
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        grupo = request.POST['grupo']
        
        usuario.first_name = first_name
        usuario.last_name = last_name

        # Obtener el grupo y asignarlo al usuario
        grupo_obj = Group.objects.get(name=grupo)
        usuario.groups.clear()
        usuario.groups.add(grupo_obj)

        # Guardar el objeto de usuario
        usuario.save()

        messages.success(request, 'La contraseña ha sido cambiada exitosamente.')
        return redirect('admin_users')
    return render(request, 'noticias/user_chng.html',{'usuario':usuario})









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