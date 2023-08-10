Message to Sysadmins
====================

Hello Sysadmin, a user has asked you to give them escalated privileges to use DisTRaX. Understandably your first reaction is no. Hopefully, this document will change your mind and help you understand why escalated privileges are required and kept at a minimum. If there are any questions are not answered, please raise an issue on  https://github.com/rosalindfranklininstitute/DisTRaX/issues


Why Are Escalated Privileges Needed?
------------------------------------

DisTRaX deploys and removes a storage cluster, i.e. ceph, onto RAM block devices which requires starting/stopping daemons and creating/removing RAM block devices. These operations require system-level access and, therefore, cannot be used at a user level.


Could This Be Containerised?
------------------------------

Unfortunately, not as DisTRaX requires the BRD kernel module to be loaded. Thus, containerisation is not an option, as the container would need root access to read and write to the block device. Therefore containerisation would introduce additional security issues.

Solution
--------
These sections outline the solution used and the reasoning behind it.

Sudoers File
~~~~~~~~~~~~
Sudoers files are provided at https://github.com/rosalindfranklininstitute/DisTRaX/blob/main/sudoers to prevent the need for complete escalated privileges access on the system.
These files contain all the commands the user will require escalated privileges for to run DisTRaX.

Why a Sudoers File
++++++++++++++++++

A sudoers file is used as this allows for easy and secure control of what DisTRaX can do on systems. Without this file being present and the user added to the `distrax` group, DisTRaX cannot deploy a storage cluster and will render the application useless.

The additional benefit is that it prevents users from modifying the codebase to allow themselves unvetted access to the system, as the commands will not be within the sudoers file.
