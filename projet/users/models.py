from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import Conferences
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
def email_validator(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('email invalid, only esprit.tn domain are allowed')
# Create your models here.
#primary_key=True pour faire la modification changement de comportement
class Participant(AbstractUser):
    cin_validator=RegexValidator(regex=r'^\d{8}$',message="this field must contain exactly 8 digits")
    cin=models.CharField(primary_key=True,max_length=8,validators=[cin_validator])
    email= models.EmailField(unique=True,max_length=255,validators=[email_validator])
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    username=models.CharField(max_length=255,unique=True)
    USERNAME_FIELD='username'
    CHOICES=(
        ('etudiant','etudiant'),
        ('chercheur','chercheur'),
        ('docteur','docteur'),
        ('enseignant','enseignant'),
    )
    participant_category=models.CharField(max_length=255,choices=CHOICES)
    #related_name='Reservation' : Cela permet d'accéder aux réservations d'un participant à partir d'une instance de Conferences avec conferences_instance.Reservation.all().

    reservations=models.ManyToManyField(Conferences,through='Reservation',related_name='Reservation')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        # Permet de définir la façon dont le nom du modèle est affiché dans l'interface d'administration de Django au pluriel.
        verbose_name_plural="Participants"
    def __str__(self):
            return f"le cin du participant et le username = {self.cin} et le username est {self.username}"



class Reservation(models.Model):
    conference=models.ForeignKey(Conferences,on_delete=models.CASCADE)
    participant=models.ForeignKey(Participant,on_delete=models.CASCADE)
    confirmed=models.BooleanField(default=False)
    reservation_date=models.DateTimeField(auto_now_add=True)
    def clean(self) :
        if self.conference.start_date < timezone.now().date():
            raise ValidationError('you can only reserve from upcomming conference')
        reservation_count=Reservation.objects.filter(
            participant=self.participant,
            reservation_date__date=timezone.now().date()
        )


        if reservation_count.count()>=2:
            raise ValidationError("you can only make up to 2 reservations per day")
    class Meta:
        unique_together=('conference','participant')

