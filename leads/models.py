from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save


# Create your models here.


class CustomUser(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=0)
    organisation = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True)
    lead_status = models.ForeignKey("LeadStatus", related_name="leads", on_delete=models.SET_NULL, null=True,
                                    blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.first_name


class LeadStatus(models.Model):
    # Open lead, contacted lead, converted lead, unconverted lead
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "LeadStatuses"


class Agent(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)

    # many agents can be of one org
    organisation = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


# action listener for when a user is created

def user_created_signal(sender, instance, created, **kwargs):
    # create a user profile
    if created:
        UserProfile.objects.create(user=instance)
    pass


# takes in a func name
post_save.connect(user_created_signal, sender=CustomUser)
