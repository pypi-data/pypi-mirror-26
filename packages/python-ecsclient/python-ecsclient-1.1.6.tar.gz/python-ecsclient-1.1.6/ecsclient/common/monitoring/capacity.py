import logging

log = logging.getLogger(__name__)


class Capacity(object):

    def __init__(self, connection):
        """
        Initialize a new instance
        """
        self.conn = connection

    def get_cluster_capacity(self, v_array_id=None):
        """
        Gets the capacity of the cluster. The details includes the provisioned
        capacity in GB and available capacity in GB.

        Required role(s):

        SYSTEM_ADMIN
        SYSTEM_MONITOR

        Example JSON result from the API:

        {
            u'totalFree_gb': 1272085,
            u'totalProvisioned_gb': 2578400
        }

        :param v_array_id: Storage pool identifier for which to retrieve
        capacity (optional)
        """
        if v_array_id:
            log.info("Getting capacity of varray '{0}'".format(v_array_id))
            return self.conn.get(url='object/capacity/{0}'.format(v_array_id))
        else:
            log.info("Getting capacity of storage cluster")
            return self.conn.get(url='object/capacity')
