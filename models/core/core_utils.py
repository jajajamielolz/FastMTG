def get_authorizeable_models() -> dict:
    """
    Retrieves all models extending the AuthorizableEntityMixin from the SQLAlchemy class registry and
    returns a dictionary.

    :return: A dictionary of model classes with the schema { <str:class name>: <DeclarativeMeta> }
    :rtype: dict
    """
    from models.core.base import Base
    from sqlalchemy.orm import DeclarativeMeta

    dict_ = {
        k: v
        for k, v in Base.registry._class_registry.items()
        if (
            isinstance(v, DeclarativeMeta)
            and any(
                cls for cls in v.__bases__ if cls.__name__ == "AuthorizableEntityMixin"
            )
        )
    }
    return dict_


def get_model(obj_name) -> "DeclarativeMeta":  # noqa
    """
    Retrieves a models from the SQLAlchemy class registry by its name

    :return: A model class
    :rtype: DeclarativeMeta
    """
    from models.core.base import Base

    return Base.registry._class_registry.get(obj_name)


def get_pks(obj):
    """
    Retrieves the primary key(s) from the model or instance and returns a dictionary

    :return: A dictionary of model classes with the schema { <str:primary key>: <sqlalchemy.types> }
    :rtype: dict
    """
    from sqlalchemy.inspection import inspect

    inspected = inspect(obj)
    if inspected.__class__.__name__ == "InstanceState":
        # if it is an instance, inspect its class
        inspected = inspect(inspected.class_)
    primary_keys = {pk.key: pk.type for pk in inspected.primary_key}

    # exceptions for models that aren't specified on primary key
    uuid_identified_models = ["ColCollection", "OcEvidence"]
    if inspected.class_.__name__ in uuid_identified_models:
        primary_keys = {inspected.class_.uuid.key: inspected.class_.uuid.type}

    return primary_keys
