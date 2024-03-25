import os

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def transform_custom(*args, **kwargs):
    os.remove(kwargs["backup_file"])
    return True
