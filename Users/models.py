from django.db import models, transaction
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager, Group)
from django.utils import timezone
from GrAPI.models import SoftDeletionUserModel, SoftDeletionUserManager
from django.conf import settings

class Role(models.Model):
    # Constantes
    ADMIN = 1
    GUARD = 2
    
    # Tuplas para elegir
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (GUARD, 'Guard'),
    )
    
    id      = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    
    def __str__(self):
      return self.get_id_display()
    

class UserManager(SoftDeletionUserManager):
    
    # def create(self, **kwargs):
    #     print('Estoy en el create de Manager')
    #     return super(SoftDeletionUserManager, self).create(**kwargs)
    
    def create(self, username=None, role=None, created_by=None, password=None, **kwargs):
        if not username:
            raise ValueError('Usuario debe tener el parametro username')
        if not role:
            raise ValueError('Usuario debe tener el parametro role')
        elif role.id == Role.ADMIN:
            raise ValueError('Usuario debe tener un rol no administrador')
        if not password:
            raise ValueError('Usuario debe tener el parametro  password')
        if not created_by:
            raise ValueError('Usuario debe tener el parametro created_by')
            
        # if not kwargs["group_id"]:
        #     raise ValueError('Usuario debe ser parte de un grupo')
        try:
            with transaction.atomic():
                user = self.model(username= username, role=role, created_by=created_by, updated_by=created_by, **kwargs)
                # group = Group.objects.get(pk=kwargs["group_id"])
                # group.user_set.add(user)
                user.set_password(password)
                user.save(using= self._db)
        except:
            raise
        return user
    
    def create_superuser(self, username, password=None):
        """ No es lo mismo crear un superusuario. Hay algunos datos que no aplican, por lo que
        es mejor no reutilizar el metodo """
        if not username:
            raise ValueError('Usuario debe tener un username')
        if not password:
            raise ValueError('Usuario debe tener una contraseña')
        role = Role.ADMIN
            
        # if not kwargs["group_id"]:
        #     raise ValueError('Usuario debe ser parte de un grupo')
        
        try:
            with transaction.atomic():
                user = self.model(username= username, role_id=role,)
                # group = Group.objects.get(pk=kwargs["group_id"])
                # group.user_set.add(user)
                user.set_password(password)
                user.is_superuser = True
                user.is_staff = True
                user.save(using= self._db)
        except:
            raise        
        return user

class User(SoftDeletionUserModel, PermissionsMixin):
    """ Modelo para representar al usuario """
    id          = models.AutoField(primary_key=True)
    username    = models.CharField(max_length=127, unique=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    role        = models.ForeignKey(Role, on_delete=models.PROTECT, default=2)
    
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.PROTECT,
                                    blank=True,
                                    null=True,
                                    related_name='created')
    updated_by  = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.PROTECT,
                                    blank=True,
                                    null=True,
                                    related_name='updated')
    
    #? "SoftDeletionUserModel" define un manager como 'objects'. 
    #? UserManager extiende de SoftDeletionUserManager
    objects = UserManager()
    
    #? Además, se define 'actives' para ver todos los usuarios activos
    
    
    # Se define el atributo a ser considerado como Unique por el backend
    # de Django
    USERNAME_FIELD = 'username'
    
    #* Campos obligatorios al crear un superuser
    #! SUPERUSER SOLAMENTE
    # EJEMPLO: REQUIRED_FIELDS = ['name']
    # Implicitamente, username y password ya son required
    REQUIRED_FIELDS = []
    
    def get_full_name(self):
        return self.username
    
    def __str__(self):
        return self.username