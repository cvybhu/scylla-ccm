from . import TEST_DIR
from ccmlib.cluster import Cluster
from ccmlib.node import Node
from ccmtest import Tester

CLUSTER_PATH = TEST_DIR

class TestCCMIssues(Tester):

    def issue_150_test(self):
        self.cluster = Cluster(CLUSTER_PATH, "150", cassandra_version='2.0.9')
        self.cluster.populate([1, 2], use_vnodes=True)
        self.cluster.start()
        dcs = [node.data_center for node in self.cluster.nodelist()]
        dcs.append('dc2')

        n = Node('node4', self.cluster, True, ('127.0.0.4', 9160), ('127.0.0.4', 7000),
            '7400', '2000', None)
        self.cluster.add(n, False, 'dc2')
        n.start()

        dcs_2 = [node.data_center for node in self.cluster.nodelist()]
        self.assertItemsEqual(dcs, dcs_2)
        n.nodetool('status')