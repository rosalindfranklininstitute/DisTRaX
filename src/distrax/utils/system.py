import re
import subprocess
import os


def is_systemd() -> bool:
    """
    Check if the system is using systemd

    Returns:
        True if the system uses systemd else False

    Examples:
        >>> distrax.utils.system.is_systemd()
        True
    """
    # If this is the case the file /proc/1/comm will have systemd within it
    PROCESS_PATH = "/proc/1/comm"
    if os.path.exists(PROCESS_PATH):
        file = open(PROCESS_PATH)
    else:
        return False
    for line in file:
        if re.search("systemd", line):
            return True
    return False


def enable_service(service: str):
    """
    Enables systemd service

    Args:
        service: The systemd service to enable

    Examples:
        >>> distrax.utils.system.enable_service("service_to_enable")
    """
    if is_systemd():
        subprocess.run(
            [
                "systemctl",
                "enable",
                "{service}".format(service=service),
            ]
        )


def disable_service(service: str):
    """
    Disables systemd service

    Args:
        service: The systemd service to disable

    Examples:
        >>> distrax.utils.system.disable_service("service_to_disable")
    """
    if is_systemd():
        subprocess.run(
            [
                "systemctl",
                "disable",
                "{service}".format(service=service),
            ]
        )


def is_systemd_service_enabled(service: str) -> bool:
    """
    Check if systemd service is enabled or not

    Args:
        service: The systemd process to check

    Returns:
        True if enabled else False
    Examples:
        >>> distrax.utils.system.is_systemd_service_enabled("enabled_service")
        True
        >>> distrax.utils.system.is_systemd_service_enabled("disabled_service")
        False
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


def start_service(service: str):
    """
    Start systemd service

    Args:
        service: The systemd service to start

    Examples:
        >>> distrax.utils.system.start_service("service_to_start")
    """
    if is_systemd():
        subprocess.run(
            [
                "systemctl",
                "start",
                "{service}".format(service=service),
            ]
        )


def stop_service(service: str):
    """
    Stops systemd service

    Args:
        service: The systemd service to stop running

    Examples:

        >>> distrax.utils.system.stop_service("service_to_stop")
    """
    if is_systemd():
        subprocess.run(
            [
                "systemctl",
                "stop",
                "{service}".format(service=service),
            ]
        )


def is_systemd_service_active(service: str) -> bool:
    """
    Check if systemd service is active or not

    Args:
        service: The systemd process to check

    Returns:
        True if enabled else False

    Examples:

        >>> distrax.utils.system.is_systemd_service_active("active_service")
        True
        >>> distrax.utils.system.is_systemd_service_active("stopped_service")
        False
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


def free_memory() -> int:
    """
    Get the amount of free RAM available on the system
    Returns:

    Examples:
        >>> free_memory()
            14623096
    """
    with open("/proc/meminfo") as file:
        for line in file:
            if "MemFree" in line:
                free_mem = line.split()[1]
                return int(free_mem)
