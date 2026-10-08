from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, ProfileForm, SignUpForm
from .models import Post


def lista_posts(request):
    posts = Post.objects.select_related("autor").order_by("-fecha_creacion")
    return render(request, "posts/lista_posts.html", {"posts": posts})


def detalle_post(request, pk):
    post = get_object_or_404(Post.objects.select_related("autor"), pk=pk)
    return render(request, "posts/detalle_post.html", {"post": post})


@login_required
def crear_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.autor = request.user
        post.save()
        return redirect("posts:detalle", pk=post.pk)
    return render(request, "posts/post_form.html", {"form": form, "titulo": "Crear publicación"})


@login_required
def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.autor_id != request.user.pk:
        raise PermissionDenied("Solo el autor puede editar esta publicación.")
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("posts:detalle", pk=post.pk)
    return render(request, "posts/post_form.html", {"form": form, "titulo": "Editar publicación"})


@login_required
def eliminar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.autor_id != request.user.pk:
        raise PermissionDenied("Solo el autor puede eliminar esta publicación.")
    if request.method == "POST":
        post.delete()
        return redirect("posts:lista")
    return render(request, "posts/post_confirm_delete.html", {"post": post})


def registro(request):
    if request.user.is_authenticated:
        return redirect("posts:lista")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("posts:lista")
    return render(request, "registration/registro.html", {"form": form})


@login_required
def perfil(request):
    posts = Post.objects.filter(autor=request.user).order_by("-fecha_creacion")
    return render(request, "registration/perfil.html", {"posts": posts})


@login_required
def editar_perfil(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("perfil")
    return render(request, "registration/editar_perfil.html", {"form": form})
