import logging
import subprocess
import time
from math import floor, log
from typing import Union

import distrax.utils.ceph as ceph
from distrax.pools import POOL

logger = logging.getLogger(__name__)


class CephPool:
    """CephPool class this allows for the creation and removal of the Ceph Pools.

    To read more about the Ceph Pools please see:
    https://docs.ceph.com/en/latest/rados/operations/pools/

    Examples:
        >>> pool = CephPool()
    """

    @staticmethod
    def create_pool(name: str = "distrax", percentage: float = 1.0) -> None:
        """Create the Pool to store objects.

        Args:
            name: The name of the pool
            percentage: The percentage of the cluster to allocate to the pool.

        Examples:
            >>> pool.create_pool(name="distrax", percentage=1.0)
                pool 'distrax' created

        """
        logger.info(f"Creating Pool {name}")
        current_cluster_pgs = ceph.get_current_pg()
        TARGET_PGS = 100
        # Calculate pgs based off https://old.ceph.com/pgcalc/
        pool_pgs = int(
            2
            ** floor(
                log((TARGET_PGS * ceph.osd_status()["num_osds"] * percentage) / log(2))
                + 0.5
            )
        )
        subprocess.run(
            ["ceph", "osd", "pool", "create", name, str(pool_pgs), str(pool_pgs)]
        )
        new_cluster_pg = current_cluster_pgs + pool_pgs
        clean_pgs: Union[int, str] = -1
        while new_cluster_pg != clean_pgs:
            time.sleep(0.1)
            status = ceph.pool_status()["pgs_by_state"]
            for stat in status:
                if stat["state_name"] == "active+clean":
                    clean_pgs = stat["count"]
                    break

    @staticmethod
    def remove_pools() -> None:
        """Remove and purge pools.

        Examples:
            >>> ceph.remove_pools()
            Warning: using slow linear search
            Removed 2 objects
            successfully purged pool .mgr
            pool '.mgr' removed
        """
        pools = ceph.lspools()
        for pool in pools:
            subprocess.run(
                [
                    "rados",
                    "purge",
                    pool["poolname"],
                    "--yes-i-really-really-mean-it",
                    "--connect-timeout",
                    "5",
                ]
            )
            subprocess.run(
                [
                    "ceph",
                    "osd",
                    "pool",
                    "delete",
                    pool["poolname"],
                    pool["poolname"],
                    "--yes-i-really-really-mean-it",
                    "--connect-timeout",
                    "5",
                ]
            )


_pool = POOL("ceph", CephPool)
