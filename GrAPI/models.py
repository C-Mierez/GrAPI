from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.query import QuerySet

class SoftDeletionQuerySet(QuerySet):
    """ QuerySet que va de la mano con "SoftDeletionManager"
    Toma el mismo comportamiento definido en el Modelo, implementando el marcado 
    en lugar de la eliminación real, para un conjunto de instancias 
    (en lugar de una, como sucede en el Modelo) """
    
    def delete(self):
        """ Invalidación, en lugar de eliminación absoluta"""
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        """ Eliminación absoluta """
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        """ Método adicional para filtrar manualmente instancias válidas"""
        return self.filter(deleted_at=None)

    def dead(self):
        """ Método adicional para filtrar manualmente instancias inválidas"""
        return self.exclude(deleted_at=None)

class SoftDeletionManager(models.Manager):
    """ Manager que va de la mano con "SoftDeletionQuerySet", implementando sus métodos """
    def __init__(self, *args, **kwargs):
        # Se agrega un parámetro adicional para determinar si el manager trabaja con todos los objetos o no
        self.active_only = kwargs.pop('active_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        # Dependiendo del atributo "active_only", se devuelve el QuerySet correspondiente 
        if self.active_only:
            # Se consideran aquellas con "deleted_at" = None, es decir, aquellas activas
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class SoftDeletionModel(models.Model):
    """ Clase abstracta definida para brindar protección ante eliminaciones. En lugar de eliminar 
    la instancia del modelo, delete() es sobre-escrito para que pase a marcar el objeto como inválido
    agregando una fecha de invalidación """
    
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Se establece el default_manager como SOLO los objetos activos 
    objects = SoftDeletionManager()
    # Se proporciona un manager adicional que considera aquellos que fueron 'eliminados' también
    all_objects = SoftDeletionManager(active_only=False)

    class Meta:
        abstract = True

    def delete(self):
        """ En lugar de eliminar, se invalida el objeto, y se establece la fecha en la que
        se realiza esta acción """
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """ En lugar de invalidar, se elimina el objeto completamente """
        super(SoftDeletionModel, self).delete()


#! #################################################################################################
#! ###################### Clases Espejadas que heredan de BaseAbstractUser #########################
#! #################################################################################################

class SoftDeletionUserQuerySet(QuerySet):
    """ QuerySet que va de la mano con "SoftDeletionManager"
    Toma el mismo comportamiento definido en el Modelo, implementando el marcado 
    en lugar de la eliminación real, para un conjunto de instancias 
    (en lugar de una, como sucede en el Modelo) """
    
    def delete(self):
        """ Invalidación, en lugar de eliminación absoluta"""
        return super(SoftDeletionUserQuerySet, self).update(deleted_at=timezone.now(), is_active=False)

    def hard_delete(self):
        """ Eliminación absoluta """
        return super(SoftDeletionUserQuerySet, self).delete()

    def alive(self):
        """ Método adicional para filtrar manualmente instancias válidas"""
        return self.filter(deleted_at=None)

    def dead(self):
        """ Método adicional para filtrar manualmente instancias inválidas"""
        return self.exclude(deleted_at=None)

class SoftDeletionUserManager(BaseUserManager):
    """ Manager que va de la mano con "SoftDeletionUserQuerySet", implementando sus métodos """
    def __init__(self, *args, **kwargs):
        # Se agrega un parámetro adicional para determinar si el manager trabaja con todos los objetos o no
        self.active_only = kwargs.pop('active_only', True)
        super(SoftDeletionUserManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        # Dependiendo del atributo "active_only", se devuelve el QuerySet correspondiente 
        if self.active_only:
            # Se consideran aquellas con "deleted_at" = None, es decir, aquellas activas
            return SoftDeletionUserQuerySet(self.model).filter(is_active=True)
        return SoftDeletionUserQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class SoftDeletionUserModel(AbstractBaseUser):
    """ Similar a "SoftDeletionModel" pero hereda de Abstract User """
    
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Se establece el default_manager como SOLO los objetos activos 
    objects = SoftDeletionUserManager()
    # Se proporciona un manager adicional que considera aquellos que fueron 'eliminados' también
    all_objects = SoftDeletionUserManager(active_only=False)

    class Meta:
        abstract = True

    def delete(self):
        """ En lugar de eliminar, se invalida el objeto, y se establece la fecha en la que
        se realiza esta acción """
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def hard_delete(self):
        """ En lugar de invalidar, se elimina el objeto completamente """
        super(SoftDeletionUserModel, self).delete()