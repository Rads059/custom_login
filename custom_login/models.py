from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """custom user manager class"""
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
        

class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model class"""
    email = models.EmailField(('email'), unique=True, default='')
    name = models.CharField(('name'), max_length=50, blank=False)
    is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng representation"""
        return self.email



# IPL Team WorkOut Model

class Tags(models.Model):
    name = models.CharField(max_length=250)
    
    
class Exercise(models.Model):
    name = models.CharField(max_length=250)
    tags = models.ManyToManyField(Tags)

class Workout_Exercise(models.Model):
    workout = models.ForeignKey( 'Workout', on_delete=models.CASCADE,)
    exercise = models.ForeignKey( Exercise, on_delete=models.CASCADE,)
    reps = models.IntegerField()
    sets = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)


class Workout(models.Model):
    name = models.CharField(max_length=100)
    body_weight = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(
        Exercise, through=Workout_Exercise)