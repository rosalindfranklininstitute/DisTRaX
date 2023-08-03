Installing DisTRaX
==================

This guide will get you up and running with installing DisTRaX.

1. Pip install
2. Setting up the DisTRaX group
3. Adding users to the DisTRaX Group
4. Adding the sudoers file

Installing From GitHub
----------------------

To pip install the distrax program use the following:

.. code-block::
   :caption: pip install distrax

    pip install "git+https://github.com/rosalindfranklininstitute/DisTRaX.git#egg=distrax"

Creating the DisTRaX Group
--------------------------

As some of the commands used by DisTRaX require escalated privileges, therefore a group needs to be created.

.. code-block::
   :caption: distrax group creation

    sudo groupadd distrax


Adding your user to the DisTRaX Group
-------------------------------------

The user then needs to be added to this group:

.. code-block::
   :caption: distrax group creation

    sudo usermod -a -G distrax exampleusername



Adding the DisTRaX Sudoers File
-------------------------------

For each storage system, there will be a separate sudoers file. The sudoers file allows the set commands to run without requiring the root password such that the system can run without user interaction.
To see the sudoers files, please see: https://github.com/rosalindfranklininstitute/DisTRaX/blob/main/sudoers

If you have any questions or queries surrounding this, please raise an issue on the GitHub repo: https://github.com/rosalindfranklininstitute/DisTRaX/issues

Ceph
++++
The following block is the sudoers file required for distrax to be able to deploy a Ceph storage cluster. Please copy this or the version in the github repo to `/etc/sudoers.d/`

.. code-block::
   :caption: distrax-ceph sudoers

   # allow distrax group to create a ceph cluster

    # Create the Monitor node
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.conf /etc/ceph/ceph.conf
    %distrax ALL=NOPASSWD: /usr/bin/mkdir -p -m * /var/lib/ceph/mon/ceph-*
    %distrax ALL=NOPASSWD: /usr/bin/ceph-mon --cluster ceph --mkfs -i * --monmap */ceph.monmap --keyring */ceph.mon..keyring
    %distrax ALL=NOPASSWD: /usr/bin/chown ceph\:ceph  /var/lib/ceph/mon/ceph-*
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.client.admin.keyring /etc/ceph/ceph.client.admin.keyring
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.mon..keyring /var/lib/ceph/mon/ceph-*/keyring
    %distrax ALL=NOPASSWD: /usr/bin/systemctl start ceph-mon@*

    # Create the MGR node
    %distrax ALL=NOPASSWD: /usr/bin/mkdir -p -m * /var/lib/ceph/mgr/ceph-*
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.mgr.keyring /var/lib/ceph/mgr/ceph-*/keyring
    %distrax ALL=NOPASSWD: /usr/bin/chown ceph\:ceph  /var/lib/ceph/mgr/ceph-*
    %distrax ALL=NOPASSWD: /usr/bin/systemctl start ceph-mgr@*

    # Create the MDS node
    %distrax ALL=NOPASSWD: /usr/bin/mkdir -p -m * /var/lib/ceph/mds/ceph-*
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.mds.keyring /var/lib/ceph/mds/ceph-*/keyring
    %distrax ALL=NOPASSWD: /usr/bin/chown ceph\:ceph  /var/lib/ceph/mds/ceph-*
    %distrax ALL=NOPASSWD: /usr/bin/systemctl start ceph-mds@*

    # Create BRD Block Device
    %distrax ALL=NOPASSWD: /usr/sbin/modprobe brd rd_size=* max_part=1 rd_nr=*

    # Create OSD
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.client.admin.keyring /etc/ceph/ceph.keyring
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.conf /etc/ceph/ceph.conf
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.client.bootstrap-osd.keyring /etc/ceph/ceph.keyring
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.client.bootstrap-osd.keyring /var/lib/ceph/bootstrap-osd/ceph.keyring
    %distrax ALL=NOPASSWD: /usr/sbin/ceph-volume lvm create --data /dev/ram*

    # Create RGW
    %distrax ALL=NOPASSWD: /usr/bin/mkdir -p -m * /var/lib/ceph/radosgw/ceph-radosgw.*
    %distrax ALL=NOPASSWD: /usr/bin/cp */ceph.client.radosgw.keyring /var/lib/ceph/radosgw/ceph-radosgw.*/keyring
    %distrax ALL=NOPASSWD: /usr/bin/chown ceph\:ceph /var/lib/ceph/radosgw/ceph-radosgw.*
    %distrax ALL=NOPASSWD: /usr/bin/systemctl start ceph-radosgw@radosgw.*


    # Create FS
    %distrax ALL=NOPASSWD: /usr/bin/mkdir -p -m * /mnt/distrax/*
    %distrax ALL=NOPASSWD: /usr/bin/mount -t ceph \:/ /mnt/distrax/* -o name=admin\,secret=*
    %distrax ALL=NOPASSWD: /usr/bin/chown *\:* /mnt/distrax
    %distrax ALL=NOPASSWD: /usr/bin/chmod 775 /mnt/distrax

    # Remove Ceph

    ## Remove FS mount

    %distrax ALL=NOPASSWD: /usr/bin/umount /mnt/distrax
    %distrax ALL=NOPASSWD: /usr/bin/find /mnt/distrax -mindepth 0 -delete

    ## Stopping services
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop ceph.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop ceph-mon.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop ceph-mgr.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop ceph-mds.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop ceph-radosgw.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop ceph-osd@*
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop var-lib-ceph-osd-ceph\\\\x2d*.mount
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop ceph-osd.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop ceph-crash.service

    ## Disable services
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable ceph.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable ceph-mon.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable ceph-mgr.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable ceph-mds.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable ceph-radosgw.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable ceph-osd.target
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable ceph-crash.service

    ## Cleaning folders
    %distrax ALL=NOPASSWD: /usr/bin/find /etc/systemd/system/multi-user.target.wants/ceph-volume@lvm-* -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/bootstrap-mgr -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/bootstrap-osd -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/bootstrap-rbd -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/bootstrap-rgw -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/bootstrap-mds -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/mgr/ceph-* -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/mon/ceph-* -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/mds/ceph-* -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/radosgw/ceph-radosgw.* -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/osd -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/tmp -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/lib/ceph/crash -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/log/ceph -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /etc/ceph -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /etc/ceph -mindepth 0 -delete
    %distrax ALL=NOPASSWD: /usr/bin/find /var/run/ceph/ceph-*.asok -mindepth 0 -delete
    ## Stopping extra deamons
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop system-ceph\\\\x2dmgr.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop system-ceph\\\\x2dmon.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop system-ceph\\\\x2dosd.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop system-ceph\\\\x2dmds.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop system-ceph\\\\x2dradosgw.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl stop system-ceph\\\\x2dvolume.slice

    ## Disable extra deamons
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable system-ceph\\\\x2dmgr.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable system-ceph\\\\x2dmon.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable system-ceph\\\\x2dosd.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable system-ceph\\\\x2dmds.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable system-ceph\\\\x2dradosgw.slice
    %distrax ALL=NOPASSWD: /usr/bin/systemctl disable system-ceph\\\\x2dvolume.slice

    # Removing OSDs
    %distrax ALL=NOPASSWD: /usr/sbin/ceph-volume lvm zap --destroy  *
    %distrax ALL=NOPASSWD: /usr/sbin/pvs --separator \, -o pv_name\,vg_name

    ## Removing BRD block device
    %distrax ALL=NOPASSWD: /usr/sbin/rmmod brd



.. toctree::
   :hidden:
