from django.contrib.auth import get_user_model
from django.db import models
from django.http import response
from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from .models import Snack
# Create your tests here.

class SnackTest(TestCase):
    def setup(self):
        self.user = get_user_model().objects.create_user(user_name="suhibkh", email="suhaib_khsrwash@outlook.com", password="0000")
        self.sanck = Snack.objects.create_user(title="burger", purchaser=self.user, description="cheese burger")

    def test_string_representation(self):
        self.assertEqual(str(self.sanck), "burger")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "burger")
        self.assertEqual(f"{self.snack.purchaser}", "suhib")
        self.assertEqual(self.snack.description, "with extra cheese")


    
    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "burger")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(reverse("snack_create"),
        {"title": "purger",
        "description": "with extra cheese",
        "purchaser": self.user.id,},
        follow=True)
        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "this is roasted_duck")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "roasted duck","description":"this is roasted_duck","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)
