import secrets
import time
import base64
import configparser
import struct
import subprocess
import json

ETC_CEPH = "/etc/ceph"
VAR_MON = "/var/lib/ceph/mon/ceph-"
VAR_MGR = "/var/lib/ceph/mgr/ceph-"
VAR_BOOTSTRAP_OSD = "/var/lib/ceph/bootstrap-osd"
VAR_OSD = "/var/lib/ceph/osd"
VAR_OSD_ID = "/var/lib/ceph/osd/ceph-"
MON_KEYRING = "ceph.mon..keyring"
OSD_KEYRING = "ceph.client.bootstrap-osd.keyring"
ADMIN_KEYRING = "ceph.client.admin.keyring"
CONFIG_FILE = "ceph.conf"
AUTH = "cephx"


def generate_auth_key() -> str:
    """
    Generate Ceph Auth Key

    This is informed from:
    https://github.com/ceph/ceph-deploy/blob/master/ceph_deploy/new.py
    however secrets are used instead of os.urandom due to PEP 506
    https://peps.python.org/pep-0506/

    Returns:
        A string of length 40 containing a valid Ceph Key

    Examples:
        >>> keyring = distrax.utils.ceph.generate_auth_key()
        >>> len(keyring)
            40
    """
    key = secrets.token_bytes(16)
    header = struct.pack(
        "<hiih",
        1,  # le16 type: CEPH_CRYPTO_AES
        int(time.time()),  # le32 created: seconds
        0,  # le32 created: nanoseconds,
        len(key),  # le16: len(key)
    )
    return base64.b64encode(header + key).decode("utf-8")


def create_keyring(folder: str, name: str, permissions: dict) -> str:
    """
    Creates a Ceph Keyring file and writes the keyring with the permissions passed

    Args:
        folder: folder to place keyring
        name: Name of the keyring
        permissions: arguments for the keyring i.e {caps mon: "allow *}

    Returns:
        The filename of the keyring file

    Examples:
        >>> import distrax.utils.ceph as ceph
        >>> mon_keyring = ceph.create_keyring("ceph", "mon", {"caps mon": "allow *"})
        >>> print(mon_keyring)
            ceph.mon.keyring
    """
    config = configparser.ConfigParser()
    filename = f"ceph.{name}.keyring"
    config[name] = {
        "key": generate_auth_key(),
    }
    config[name].update(permissions)
    with open(f"{folder}/{filename}", "w") as configfile:
        config.write(configfile)
    return filename


def create_admin_key(folder: str) -> str:
    """
    Helper function for creating admin_keyring

    Args:
        folder: folder to place keyring

    Returns:
        filename
    """
    return create_keyring(
        folder,
        "client.admin",
        {
            "caps mon": "allow *",
            "caps osd": "allow *",
            "caps mds": "allow *",
            "caps mgr": "allow *",
        },
    )


def create_mon_key(folder: str) -> str:
    """
    Helper function for creating mon_keyring

    Args:
        folder: folder to place keyring

    Returns:
        filename
    """
    return create_keyring(folder, "mon.", {"caps mon": "allow *"})


def create_osd_key(folder: str) -> str:
    """
    Helper function for creating osd_keyring

    Args:
        folder: folder to place keyring

    Returns:
        filename
    """
    return create_keyring(
        folder,
        "client.bootstrap-osd",
        {"caps mon": "profile bootstrap-osd", "caps mgr": "allow r"},
    )


def osd_status() -> dict:
    """
    Get the status of the OSDs

    Returns:
        Where the `int` is a number

        >>> {'epoch': int,
        ...  'num_osds': int,
        ...  'num_up_osds': int,
        ...  'osd_up_since': int,
        ...  'num_in_osds': int,
        ...  'osd_in_since': int,
        ...  'num_remapped_pgs': int}

    """
    status = subprocess.run(
        ["ceph", "osd", "stat", "--format=json"], stdout=subprocess.PIPE
    )
    return json.loads(status.stdout)
