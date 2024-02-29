import os
from datetime import datetime

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def get_backup_modified_date(*args, **kwargs):
    """
    Get time when file was last modified
    """
    backup_file = "/home/pgbackup/dbdump.gz"
    object_name = os.path.basename(backup_file)
    ts = os.path.getmtime(backup_file)
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")


@test
def test_backup_is_updated(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output == datetime.now().strftime("%Y-%m-%d"), "The backup is outdated!"
