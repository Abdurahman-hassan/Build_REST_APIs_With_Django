# from django.contrib.auth import get_user_model
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
#
# user = get_user_model()
#
# # we need to import model into
# @receiver(post_save, sender=user)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
