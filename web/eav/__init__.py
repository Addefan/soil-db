def custom_register(model_cls, config_cls=None):
    from web.eav.registry import CustomRegistry

    CustomRegistry.register(model_cls, config_cls)
