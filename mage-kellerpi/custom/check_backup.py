import os
import time

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def get_backup_properties(*args, **kwargs):
    """
    Get the file size
    """
    time.sleep(300)
    backup_file = "/home/pgbackup/dbdump.gz"
    file_stats = os.stat(backup_file)
    return file_stats.st_size / (1024 * 1024)


@test
def test_backup_file_size_is_adequate(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output >= 73, "The backup file is smaller than expected!"
