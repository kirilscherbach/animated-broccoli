import os
from datetime import datetime

if "sensor" not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def check_condition(*args, **kwargs) -> bool:
    """
    Check backup dump is updated
    """
    backup_file = kwargs["backup_file"]
    object_name = os.path.basename(backup_file)
    update_date = datetime.utcfromtimestamp(os.path.getmtime(backup_file)).strftime(
        "%Y-%m-%d"
    )
    if update_date == datetime.now().strftime("%Y-%m-%d"):
        print(f"Backup file has been updated at {update_date}")
        return True
    else:
        print(
            f"As of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} the backup has not been updated"
        )
        return False
