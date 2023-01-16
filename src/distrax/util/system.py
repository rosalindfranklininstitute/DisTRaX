import re
import subprocess


def is_systemd():
    """
    Check if the system is using systemd

    If this is the case the file /proc/1/comm will have systemd within it

    :return: True if systemd else False
    """
    try:
        file = open("/proc/1/comm")
    except FileNotFoundError:
        return False
    for line in file:
        if re.search("systemd", line):
            return True
    return False


def enable_service(service):
    """
    Enables systemd service
    :param service: The systemd service to enable
    :return: N/A
    """
    if is_systemd():
        subprocess.run(
            [
                "systemctl",
                "enable",
                "{service}".format(service=service),
            ]
        )


def disable_service(service):
    """
    Disables systemd service
    :param service: The systemd service to disable
    :return: N/A
    """
    if is_systemd():
        subprocess.run(
            [
                "systemctl",
                "disable",
                "{service}".format(service=service),
            ]
        )


def is_systemd_service_enabled(service):
    """
    Check if systemd service is enabled or not
    :param service: service to check
    :return: True if enabled else 0
    """
    result = subprocess.run(
        [
            "systemctl",
            "is-enabled",
            "--quiet",
            "{service}".format(service=service),
        ]
    )
    return result.returncode == 0


def start_service(service):
    """
    Starts systemd service
    :param service: The systemd service to start
    :return: N/A
    """
    if is_systemd():
        subprocess.run(
            [
                "systemctl",
                "start",
                "{service}".format(service=service),
            ]
        )


def stop_service(service):
    """
    Stops systemd service
    :param service: The systemd service to stop
    :return: N/A
    """
    if is_systemd():
        subprocess.run(
            [
                "systemctl",
                "stop",
                "{service}".format(service=service),
            ]
        )


def is_systemd_service_active(service):
    """
    Check if systemd service is active or not
    :param service: service to check
    :return: True if active else 0
    """
    result = subprocess.run(
        [
            "systemctl",
            "is-active",
            "--quiet",
            "{service}".format(service=service),
        ]
    )
    return result.returncode == 0
