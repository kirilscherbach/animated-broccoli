import subprocess

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    command = f"pg_dumpall -h $PG_HOST -p 5432 -U postgres --no-password | gzip -c  > {kwargs['backup_file']}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    exit_status = process.wait()
    if exit_status == 0:
        print(f"Backup completed successfully. File is {kwargs['backup_file']}")
    else:
        print("Backup failed with exit status:", exit_status)

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
