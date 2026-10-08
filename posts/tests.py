import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.autor = user_model.objects.create_user(username="autor", password="ClaveSegura123!")
        cls.otro = user_model.objects.create_user(username="otro", password="ClaveSegura123!")
        cls.post = Post.objects.create(
            autor=cls.autor, titulo="Una pista", contenido="Contenido de prueba"
        )

    def test_lista_y_detalle_publicos(self):
        lista = self.client.get(reverse("posts:lista"))
        detalle = self.client.get(reverse("posts:detalle", args=[self.post.pk]))
        self.assertEqual(lista.status_code, 200)
        self.assertContains(lista, "Una pista")
        self.assertEqual(detalle.status_code, 200)
        self.assertContains(detalle, "Contenido de prueba")

    def test_crear_requiere_login_y_asigna_autor(self):
        url = reverse("posts:crear")
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.autor)
        respuesta = self.client.post(url, {"titulo": "Nuevo post", "contenido": "Texto"})
        nuevo = Post.objects.get(titulo="Nuevo post")
        self.assertRedirects(respuesta, reverse("posts:detalle", args=[nuevo.pk]))
        self.assertEqual(nuevo.autor, self.autor)

    def test_solo_autor_puede_editar_y_eliminar(self):
        editar = reverse("posts:editar", args=[self.post.pk])
        eliminar = reverse("posts:eliminar", args=[self.post.pk])
        self.client.force_login(self.otro)
        self.assertEqual(self.client.get(editar).status_code, 403)
        self.assertEqual(self.client.post(editar, {"titulo": "Intruso", "contenido": "X"}).status_code, 403)
        self.assertEqual(self.client.post(eliminar).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
        self.client.force_login(self.autor)
        self.assertEqual(self.client.get(eliminar).status_code, 200)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
        self.client.post(editar, {"titulo": "Editado", "contenido": "Texto nuevo"})
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, "Editado")
        self.client.post(eliminar)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_registro_login_logout_y_perfil(self):
        respuesta = self.client.post(reverse("registro"), {
            "username": "nuevo", "email": "nuevo@example.com",
            "password1": "ClaveSegura123!", "password2": "ClaveSegura123!",
        })
        self.assertRedirects(respuesta, reverse("posts:lista"))
        self.assertEqual(self.client.get(reverse("perfil")).status_code, 200)
        self.client.post(reverse("editar_perfil"), {
            "first_name": "Ana", "last_name": "García", "email": "ana@example.com",
        })
        self.assertEqual(get_user_model().objects.get(username="nuevo").first_name, "Ana")
        self.assertEqual(self.client.post(reverse("logout")).status_code, 302)
        self.assertEqual(self.client.get(reverse("perfil")).status_code, 302)
        respuesta = self.client.post(reverse("login"), {
            "username": "nuevo", "password": "ClaveSegura123!",
        })
        self.assertRedirects(respuesta, reverse("posts:lista"))

    def test_imagen_opcional_y_enlace_visible(self):
        imagen = SimpleUploadedFile(
            "prueba.gif",
            b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;",
            content_type="image/gif",
        )
        self.client.force_login(self.autor)
        with tempfile.TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                respuesta = self.client.post(reverse("posts:crear"), {
                    "titulo": "Con imagen", "contenido": "Texto", "imagen": imagen,
                })
                self.assertEqual(respuesta.status_code, 302)
                post = Post.objects.get(titulo="Con imagen")
                self.assertContains(self.client.get(reverse("posts:detalle", args=[post.pk])), post.imagen.url)
