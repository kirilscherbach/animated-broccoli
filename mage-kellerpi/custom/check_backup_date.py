import os
from datetime import datetime

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    backup_file = kwargs["backup_file"]
    object_name = os.path.basename(backup_file)
    update_date = datetime.utcfromtimestamp(os.path.getmtime(backup_file)).strftime(
        "%Y-%m-%d"
    )
    return update_date


@test
def test_output(output, *args) -> None:
    assert output == datetime.now().strftime(
        "%Y-%m-%d"
    ), f"The backup file {kwargs['backup_file']} has not been updated"
