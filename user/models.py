from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='E-Mail',unique=True)

    # ===============Basic===============
    name = models.CharField(verbose_name='姓名',max_length=50, blank=True)
    gender = models.CharField(verbose_name='性別',max_length=10, blank=True, choices=[
        ('male', '男生'),
        ('female','女生'),
        ('else', '其他')
    ])

    # ===============Prefer===============

    # ===============Permission===============
    is_admin = models.BooleanField(
        'staff status',
        default=False
    )

    # ===============Setting===============
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]
    objects = MyUserManager()
