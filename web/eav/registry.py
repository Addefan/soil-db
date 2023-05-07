from eav.registry import Registry, EavConfig

from web.models import PlantQuerySet


class CustomRegistry(Registry):
    """
    Override base manager object to extend EavQuerySet

    This method doesn't work:
    class Plant(models.Model, PlantModelMixin):
        objects = PlantQuerySet.as_manager()
        ...
    """

    manager = PlantQuerySet.as_manager()

    @staticmethod
    def register(model_cls, config_cls=None):
        """
        Registers *model_cls* with eav. You can pass an optional *config_cls*
        to override the EavConfig defaults.

        .. note::
           Multiple registrations for the same entity are harmlessly ignored.
        """
        if hasattr(model_cls, "_eav_config_cls"):
            return

        if config_cls is EavConfig or config_cls is None:
            config_cls = type("%sConfig" % model_cls.__name__, (EavConfig,), {})

        # set _eav_config_cls on the model so we can access it there
        setattr(model_cls, "_eav_config_cls", config_cls)

        reg = CustomRegistry(model_cls)
        reg._register_self()

    def _attach_manager(self):
        """
        Attach the manager to *manager_attr* specified in *config_cls*
        """
        # Save the old manager if the attribute name conflicts with the new one.
        if hasattr(self.model_cls, self.config_cls.manager_attr):
            mgr = getattr(self.model_cls, self.config_cls.manager_attr)

            # For some models, `local_managers` may be empty, eg.
            # django.contrib.auth.models.User and AbstractUser
            if mgr in self.model_cls._meta.local_managers:
                self.config_cls.old_mgr = mgr
                self.model_cls._meta.local_managers.remove(mgr)

            self.model_cls._meta._expire_cache()

        # Attach the new manager to the model.
        # EntityManager ---> PlantQuerySet.as_manager()
        mgr = self.manager
        mgr.contribute_to_class(self.model_cls, self.config_cls.manager_attr)
