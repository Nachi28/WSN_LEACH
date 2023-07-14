import numpy as np
import matplotlib.pyplot as plt


class WSN(object):
    """ The network architecture with desired parameters """

    # PARAMETER 5(DISTANCE)
    # Distance increases transfer energy increases.... nodes die faster

    xm = 200  # Length of the yard
    ym = 200  # Width of the yard
    n = 10  # total number of nodes
    sink = None  # Sink node
    nodes = None  # All sensor nodes set
    # Energy model (all values in Joules)
    # Eelec = ETX = ERX
    ETX = 50 * (10 ** (-9))      # Energy for transferring of each bit:50nJ/bit
    ERX = 50 * (10 ** (-9))      # Energy for receiving of each bit:50nJ/bit
    # Transmit Amplifier types
    Efs = 10 * (10 ** (-12))     # Energy of free space model: 10pJ/bit/m2
    Emp = 0.0013 * (10 ** (-12))  # Energy of multi path model: 0.0013pJ/bit/m4
    EDA = 5 * (10 ** (-9))       # Data aggregation energy: 5nJ/bit

    # PARAMETER 7 (Packet loss percentage)
    f_r = 0.1               # fusion_rate: 0 means perfect fusion

    # PARAMETER 6
    # Message
    CM = 32     # control message size/bit
    DM = 4096   # data size/bit
    # computation of do
    do = np.sqrt(Efs / Emp)     # 87.70580193070293

    # PARAMETER 4
    # malicious sensor node
    m_n = 2     # the number of malicious sensor nodes

    # Node State in Network
    n_dead = 0  # The number of dead nodes
    flag_first_dead = 0  # Flag tells that the first node died
    flag_all_dead = 0  # Flag tells that all nodes died
    flag_net_stop = 0  # Flag tells that network stop working:90% nodes died
    round_first_dead = 0  # The round when the first node died
    round_all_dead = 0  # The round when all nodes died
    round_net_stop = 0  # The round when the network stop working

    def dist(x, y):
        """ Determine the one-dimensional distance between two nodes """
        distance = np.sqrt(np.power((x.xm - y.xm), 2) +
                           np.power((x.ym - y.ym), 2))
        return distance

    def trans_energy(data, dis):
        if dis > WSN.do:
            energy = WSN.ETX * data + WSN.Emp * data * (dis ** 4)
        else:  # min_dis <= do
            energy = WSN.ETX * data + WSN.Efs * data * (dis ** 2)
        return energy

    def node_state(r):
        nodes = WSN.nodes
        n_dead = 0
        for node in nodes:
            # dead node
            if node.energy <= Node.energy_threshold:

                n_dead += 1
                if WSN.flag_first_dead == 0 and n_dead == 1:
                    WSN.flag_first_dead = 1
                    WSN.round_first_dead = r - Leach.r_empty
        if WSN.flag_net_stop == 0 and n_dead >= (WSN.n * 0.9):
            WSN.flag_net_stop = 1
            WSN.round_net_stop = r - Leach.r_empty
        if n_dead == WSN.n - 1:
            WSN.flag_all_dead = 1
            WSN.round_all_dead = r - Leach.r_empty
        WSN.n_dead = n_dead


class Node(object):
    """ Sensor Node """

    # PARAMETER 1 (ENERGY)
    energy_init = 0.5  # initial energy of a node
    # After the energy dissipated in a given node reached a set threshold,

    # that node was considered dead for the remainder of the simulation if value less than threshold.
    energy_threshold = 0.001

    def __init__(self):
        """ Create the node with default attributes """
        self.id = None  # node number
        self.xm = np.random.random() * WSN.xm
        self.ym = np.random.random() * WSN.ym
        self.energy = Node.energy_init
        self.packets = WSN.DM
        self.type = "N"  # "N" = Node (Non-CH):The point type is a normal node
        # G is the set of nodes that have not been cluster-heads in the last 1/p rounds.
        self.G = 0  # the flag determines whether it's a CH or not: 0 means it is not selected as the cluster head, and 1 means it is selected as the cluster head
        self.head_id = None  # The id of its CH: None means that it has not joined any cluster

    def init_nodes():
        """ Initialize attributes of every node in order """
        nodes = []
        # Initial common node
        for i in range(WSN.n):
            node = Node()
            node.id = i
            nodes.append(node)
        # Initial sink node
        sink = Node()
        sink.id = -1
        sink.xm = 0.5 * WSN.xm  # x coordination of base station
        sink.ym = 50 + WSN.ym  # y coordination of base station
        # Add to WSN
        WSN.nodes = nodes
        WSN.sink = sink

    def init_malicious_nodes():
        """ Initialize attributes of every malicious node in order """
        for i in range(WSN.m_n):
            node = Node()
            node.id = WSN.n + i
            WSN.nodes.append(node)

    def plot_wsn():
        nodes = WSN.nodes
        n = WSN.n
        m_n = WSN.m_n
        # base station
        sink = WSN.sink
        plt.plot([sink.xm], [sink.ym], 'r^', label="base station")
        # normal node
        n_flag = True
        for i in range(n):
            if n_flag:
                plt.plot([nodes[i].xm], [nodes[i].ym],
                         'b+', label='normal node')
                n_flag = False
            else:
                plt.plot([nodes[i].xm], [nodes[i].ym], 'b+')
        # malicious node
        m_flag = True
        for i in range(m_n):
            j = n + i
            if m_flag:
                plt.plot([nodes[j].xm], [nodes[j].ym],
                         'kd', label='malicious node')
                m_flag = False
            else:
                plt.plot([nodes[j].xm], [nodes[j].ym], 'kd')
        plt.legend()
        plt.xlabel('X/m')
        plt.ylabel('Y/m')
        plt.show()


class Leach(object):
    """ Leach """
    # Optimal selection probablitity of a node to become cluster head

    # PARAMETER 2 (Cluster Head Probability)
    p = 0.1       # Probability of being selected as a cluster head
    period = int(1/p)  # cycle
    heads = None      # Cluster head node list
    members = None      # List of non-cluster head members
    # Cluster dictionary: {"cluster head 1":[cluster member],"cluster head 2":[cluster member],...}
    cluster = None
    r = 0         # current round

    # PARAMETER 3 (NO. of iterations)
    rmax = 5         # 9999 # default maximum round
    r_empty = 0         # empty wheel

    def show_cluster():
        fig = plt.figure()
        # set title
        # set x-axis labels
        plt.xlabel('X/m')
        # Set the y-axis label
        plt.ylabel('Y/m')
        icon = ['o', '*', '.', 'x', '+', 's']
        color = ['r', 'b', 'g', 'c', 'y', 'm']
        # Show the list of classifications for each cluster
        i = 0
        nodes = WSN.nodes
        for key, value in Leach.cluster.items():
            cluster_head = nodes[int(key)]
            # print("No.", i + 1, "The class cluster centers are: ", cluster_head)
            for index in value:
                plt.plot([cluster_head.xm, nodes[index].xm], [cluster_head.ym, nodes[index].ym],
                         c=color[i % 6], marker=icon[i % 5], alpha=0.4)
                # If a malicious node
                if index >= WSN.n:
                    plt.plot([nodes[index].xm], [nodes[index].ym], 'dk')
            i += 1
        # Show the drawn image
        plt.show()

    def optimum_number_of_clusters():
        """ Optimal number of cluster heads under perfect fusion """
        N = WSN.n - WSN.n_dead
        M = np.sqrt(WSN.xm * WSN.ym)
        d_toBS = np.sqrt((WSN.sink.xm - WSN.xm) ** 2 +
                         (WSN.sink.ym - WSN.ym) ** 2)
        k_opt = (np.sqrt(N) / np.sqrt(2 * np.pi) *
                 np.sqrt(WSN.Efs / WSN.Emp) *
                 M / (d_toBS ** 2))
        p = int(k_opt) / N
        return p

    def cluster_head_selection():
        """ Select the cluster head node according to the threshold """
        nodes = WSN.nodes
        n = WSN.n  # non-malicious node
        # The list of cluster heads, each round is initialized to be empty
        heads = Leach.heads = []
        members = Leach.members = []  # non-cluster member list
        p = Leach.p
        r = Leach.r
        period = Leach.period
        Tn = p / (1 - p * (r % period))  # Threshold Tn
        # If Tn is increased more cluter heads.

        print(Leach.r, Tn)
        for i in range(n):
            # After the energy dissipated in a given node reached a set threshold,
            # that node was considered dead for the remainder of the simulation.
            if nodes[i].energy > Node.energy_threshold:  # The node is not dead
                if nodes[i].G == 0:  # The node is not selected as the cluster head in this cycle
                    temp_rand = np.random.random()
                    # print(temp_rand)

                    # The node whose random number is lower than the threshold is selected as the cluster head
                    if temp_rand <= Tn:
                        # print(temp_rand)
                        # This node is the cluster head of the current cycle
                        nodes[i].type = "CH"
                        # G is set to 1, this cycle can no longer be selected as a cluster head or (1/p)-1
                        nodes[i].G = 1
                        heads.append(nodes[i])
                        # The node is selected as the cluster head, broadcast this message
                        # Announce cluster-head status, wait for join-request messages
                        max_dis = np.sqrt(WSN.xm ** 2 + WSN.ym ** 2)
                        nodes[i].energy -= WSN.trans_energy(WSN.CM, max_dis)
                        # Nodes are likely to die
                if nodes[i].type == "N":  # This node is not a cluster head node
                    members.append(nodes[i])
        m_n = WSN.m_n
        for i in range(m_n):
            j = n + i
            members.append(nodes[j])
        # If no cluster head is found in this round
        if not heads:
            Leach.r_empty += 1
            print("---> No cluster heads found this round!")
            # Leach.cluster_head_selection()
        print("The number of CHs is:", len(heads), (WSN.n - WSN.n_dead))

        # print("Energy of nodes-> ", nodes[i].energy)
        return None  # heads, members

    def cluster_formation():
        """ Perform cluster classification """
        nodes = WSN.nodes
        heads = Leach.heads
        members = Leach.members
        cluster = Leach.cluster = {}  # Cluster dictionary initialization
        # There is no cluster head in this round, no cluster is formed
        if not heads:
            return None
        # If the cluster head exists, use the cluster head id as the key value of the cluster dictionary
        for head in heads:
            cluster[str(head.id)] = []  # members is an empty list
        # print("Classification dictionary with only cluster heads:", cluster)
        # Traversing non-cluster head nodes to create clusters
        for member in members:
            # Pick the node with the smallest distance
            # The broadcast radius within the cluster head node area
            min_dis = np.sqrt(WSN.xm ** 2 + WSN.ym ** 2)
            head_id = None
            # Receive information from all cluster heads
            # Wait for cluster-head announcements
            member.energy -= WSN.ERX * WSN.CM * len(heads)
            # Determine the distance to each cluster head, and join the cluster head with the smallest distance
            for head in heads:
                tmp = WSN.dist(member, head)
                if tmp <= min_dis:
                    min_dis = tmp
                    head_id = head.id
            member.head_id = head_id  # cluster head found
            # Send join information to notify its cluster head to become its member
            # send join-request messages to chosen cluster-head
            member.energy -= WSN.trans_energy(WSN.CM, min_dis)
            # wait for join-request messages
            head = nodes[head_id]
            head.energy -= WSN.ERX * WSN.CM
            # Add to the corresponding cluster head of the out-cluster class
            cluster[str(head_id)].append(member.id)
        # Assign each node in the cluster a point in time to deliver data to it
        # Create a TDMA schedule and this schedule is broadcast back to the nodes in the cluster.
        for key, values in cluster.items():
            head = nodes[int(key)]
            if not values:
                # If there are cluster members, the CH sends schedule by broadcasting
                max_dis = np.sqrt(WSN.xm ** 2 + WSN.ym ** 2)
                head.energy -= WSN.trans_energy(WSN.CM, max_dis)
                for x in values:
                    member = nodes[int(x)]
                    # wait for schedule from cluster-head
                    member.energy -= WSN.ERX * WSN.CM
#        print(cluster)
        return None  # cluster

    def set_up_phase():
        Leach.cluster_head_selection()
        Leach.cluster_formation()

    def steady_state_phase():
        """ Cluster members send data to the cluster head, the cluster head collects data and then sends data to the sink node """
        nodes = WSN.nodes
        cluster = Leach.cluster
        # Exit if no clusters are formed this round
        if not cluster:
            return None
        total_packetloss = 0
        for key, values in cluster.items():

            head = nodes[int(key)]
            # print(f"KEY ==== {key}") cluster head
            # print(f"VALUES ==== {values}") cluster members

            n_member = len(values)  # Number of cluster members
            # Members in the cluster send data to the cluster head node
            total_packetloss_for_ch = 0
            for x in values:
                member = nodes[int(x)]
                dis = WSN.dist(member, head)

                # Cluster members send data
                member.energy -= WSN.trans_energy(WSN.DM, dis)
                head.energy -= WSN.ERX * WSN.DM  # Cluster head receives data

                #  Packet loss
                packetloss = (dis * np.random.random() *
                              10000) % (WSN.f_r * WSN.DM)
                member.packets -= packetloss

                # print(f"\nCurrent node = {x}")
                # print(
                #     f"Nodes --> {x} sent data to cluster head --> {key} \nPACKET loss = {packetloss}\n PACKETS remaining = {member.packets}")

                # adding packet loss for each node in a cluster head
                total_packetloss_for_ch += packetloss
                # print(f"\n\n test addition{total_packetloss_for_ch:.2f}\n\n")
                # adding packet loss for all nodes and all clusteer head

            print(
                f"\n\nData transmission complete for cluster head {key}\nNodes --> {values} sent data to cluster head --> {key}\n Total Packets lost for CH = {total_packetloss_for_ch:.2f}")

            # The distance of from head to sink
            d_h2s = WSN.dist(head, WSN.sink)

            if n_member == 0:  # If there are no cluster members, only the cluster head collects its own information and sends it to the base station
                # 0 packet loss in cluster head to sink
                energy = WSN.trans_energy(WSN.DM, d_h2s)
            else:
                # Plus the data collected by the cluster head itself, the new data package after fusion
                new_data = WSN.DM * (n_member + 1)
                E_DA = WSN.EDA * new_data  # Energy Consumption of Aggregated Data

                if WSN.f_r == 0:  # f_r is 0 to represent the perfect fusion of data
                    new_data_ = WSN.DM
                else:
                    new_data_ = total_packetloss_for_ch
                E_Trans = WSN.trans_energy(new_data_, d_h2s)
                energy = E_DA + E_Trans

            head.energy -= energy
            total_packetloss += total_packetloss_for_ch

        print(
            f"""\n\n##########################################
//////////////////////////////////////////
\nTotal packet loss in this round ==> {total_packetloss:.2f}\n Percentage ==> {(total_packetloss/(WSN.DM * WSN.n )*100):.2f} %\n
//////////////////////////////////////////
########################################## """)

    def leach():
        Leach.set_up_phase()
        Leach.steady_state_phase()

    def run_leach():
        for r in range(Leach.rmax):
            Leach.r = r
            nodes = WSN.nodes
            # G resets to 0 when a new cycle starts
            if (r % Leach.period) == 0:
                print("==============================")
                for node in nodes:
                    node.G = 0
            # When each round starts, the node type is reset to non-cluster-head node
            for node in nodes:
                node.type = "N"
            Leach.leach()
            WSN.node_state(r)
            if WSN.flag_all_dead:
                print("==============================")
                break
            Leach.show_cluster()


def main():
    Node.init_nodes()
    Node.init_malicious_nodes()
    Node.plot_wsn()
    Leach.run_leach()
    # print("The first node died in Round %d!" % (WSN.round_first_dead))
    # print("The network stop working in Round %d!" % (WSN.round_net_stop))
    # print("All nodes died in Round %d!" % (WSN.round_all_dead))


if __name__ == '__main__':
    main()
