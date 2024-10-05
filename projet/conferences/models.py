from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator,FileExtensionValidator
from django.core.exceptions import ValidationError
# Create your models here.
from django.utils import timezone

class Conferences(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    start_date=models.DateField(default=timezone.now().date())
    end_date=models.DateField()
    location=models.CharField(max_length=255)
    price=models.FloatField()
    capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=900,message="capacity must be under 900")])

    program=models.FileField(upload_to='files/',validators=[FileExtensionValidator(allowed_extensions=['pdf','png','jpg','jpeg'],message="only pdf,png,jpg,jpeg are allowed ")])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #quand tu suppr cat->suppr conf
    #et ca related_name="conferences" pour acceder a conference a partir de categorie
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="conferences")
    def clean(self) :
        if self.end_date<=self.start_date:
            raise ValidationError('end date must be after start date')
    class Meta:
        verbose_name_plural="Conferences"
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start_date__gte=timezone.now().date(),
                   ), name="the start date must be greater than today or equal")]

