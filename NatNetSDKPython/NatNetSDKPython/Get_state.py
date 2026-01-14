import sys
import time
from NatNetClient import NatNetClient
import DataDescriptions
import MoCapData
import numpy as np

def receive_rigid_body_frame( new_id, position, rotation ):
        global positions
        positions[new_id] = np.array(position)
        # print( "Received frame for rigid body", new_id," ",position," ",rotation )

def my_parse_args(arg_list, args_dict):
        # set up base values
        arg_list_len=len(arg_list)
        if arg_list_len>1:
            args_dict["serverAddress"] = arg_list[1]
            if arg_list_len>2:
                args_dict["clientAddress"] = arg_list[2]
            if arg_list_len>3:
                if len(arg_list[3]):
                    args_dict["use_multicast"] = True
                    if arg_list[3][0].upper() == "U":
                        args_dict["use_multicast"] = False
        return args_dict


def get_state():
    positions = {}
    optionsDict = {}
    optionsDict["clientAddress"] = "127.0.0.1"
    optionsDict["serverAddress"] = "127.0.0.1"
    optionsDict["use_multicast"] = True

    # This will create a new NatNet client
    optionsDict = my_parse_args(sys.argv, optionsDict)
    streaming_client = NatNetClient()
    streaming_client.set_client_address(optionsDict["clientAddress"])
    streaming_client.set_server_address(optionsDict["serverAddress"])
    streaming_client.set_use_multicast(optionsDict["use_multicast"])
    streaming_client.run()
    streaming_client.rigid_body_listener = receive_rigid_body_frame
    time.sleep(0.01)

    Posi_cur = positions
    p1 = Posi_cur[1]
    p2 = Posi_cur[2]
    # P = np.array([p1,p2])
    P = np.concatenate((p1,p2))
    Pos = [np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), P[0],
           np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), P[3],
           np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), P[1],
           np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), P[4],
           np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), P[2],
           np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), P[5]]
    
    return Pos



# if __name__ == "__main__":
#     get_state()

#         positions = {}
#         optionsDict = {}
#         optionsDict["clientAddress"] = "127.0.0.1"
#         optionsDict["serverAddress"] = "127.0.0.1"
#         optionsDict["use_multicast"] = True
#
#         # This will create a new NatNet client
#         optionsDict = my_parse_args(sys.argv, optionsDict)
#         streaming_client = NatNetClient()
#         streaming_client.set_client_address(optionsDict["clientAddress"])
#         streaming_client.set_server_address(optionsDict["serverAddress"])
#         streaming_client.set_use_multicast(optionsDict["use_multicast"])
#         streaming_client.run()
#         streaming_client.rigid_body_listener = receive_rigid_body_frame
#         time.sleep(0.01)
#
#         while True:
#             Posi_cur = positions
#             p1 = Posi_cur[1]
#             p2 = Posi_cur[2]
#             print("p1", p1)
#             print("p2", p2)
#             time.sleep(2)
#
#         # streaming_client.rigid_body_listener = receive_rigid_body_frame
#         #
#         #
#         # i = 1
#         # while i == 1:
#         #     # streaming_client.run()
#         #     streaming_client.rigid_body_listener = receive_rigid_body_frame
#         #     # print("position", positions)
#         #     time.sleep(5)
#         #     i += 1
#         #     if i %2 == 0:
#         #         streaming_client.shutdown()
#         #         print("position", positions)
#         #         # time.sleep(5)
#         #         i=1


