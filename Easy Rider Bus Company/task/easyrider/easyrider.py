import json
from itertools import combinations


def control_dict(checking_list):
    """return dict with keys as bus id's"""
    list_of_bus_id = []
    for i in checking_list:
        list_of_bus_id.append(i['bus_id'])
    return {x: [] for x in set(sorted(list_of_bus_id))}


def time_dict(checking_list):
    """return timetable with bus id and a list of tuples (stop_name, time)"""
    cd = control_dict(checking_list)
    for i in checking_list:
        cd[i["bus_id"]].append((i["stop_name"], i["a_time"], i["stop_type"]))
    return cd


def is_ascending(time_list):
    """check if list with time is ascending and return time otherwise"""
    previous = time_list[0][1]
    for number in time_list:
        if number[1] < previous:
            return number
        previous = number[1]
    return 0


def time_order_check(checking_list: "main list"):
    time_table = time_dict(checking_list)
    arrival_time_errors = {}
    for key, value in time_table.items():
        res_check = is_ascending(value)
        if not res_check:
            continue
        else:
            new_item = {key: res_check}
            arrival_time_errors.update(new_item)
    return arrival_time_errors


def check_start_final(checking_dictionary):
    wrong_start_final = []
    for key, value in checking_dictionary.items():
        if value[0][2] != 'S' or value[-1][2] != 'F':
            wrong_start_final.append(value[0][0])
    return wrong_start_final


def count_transfers(checking_list):
    """count transfers, return sorted list"""
    h = control_dict(checking_list)
    for hh in checking_list:
        h[hh["bus_id"]].append(hh["stop_name"])
    stops = []  # a set of strops for each route
    for ii in h:
        stops.append(set(h.get(ii)))
    pairs = combinations(stops, 2)
    transfer = []
    for i in pairs:
        transfer.append(i[0].intersection(i[1]))
    for b in transfer:
        transfer[0].update(b)
    return sorted(list(transfer[0]))


def check_transfers(checking_dictionary, transfer_list):
    transfer_errors = []
    for value in checking_dictionary.values():
        for jj in value:
            for k in transfer_list:
                if jj[0] == k:
                    if jj[2] == 'O':
                        transfer_errors.append(jj[0])
    return transfer_errors


def main():
    bus_data = input()
    data_deser = json.loads(bus_data)  # data deserialization from json
    check_dict = time_dict(data_deser)
    start_final = check_start_final(check_dict)
    transfers = count_transfers(data_deser)
    transf_faults = check_transfers(check_dict, transfers)
    total_list = sorted(start_final + transf_faults)
    print("On demand stops test:")
    if not total_list:
        print("OK")
    else:
        print(f"Wrong stop type: {total_list}")


if __name__ == '__main__':
    main()
