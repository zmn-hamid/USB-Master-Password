import subprocess


def get_uuid():
    # This command retrieves the UUID from the BIOS
    cmd = "wmic csproduct get uuid"
    uuid = subprocess.check_output(cmd).decode().split("\n")[1].strip()
    return uuid
