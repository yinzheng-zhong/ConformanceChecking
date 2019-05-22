import argparse
from Parser import PNetParser
from Parser import EventLogParser
from ConformanceChecking import ConformanceChecking

num_passed = 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('petri_net_path', help='The path of the Petri Net file.', type=str)
    parser.add_argument('event_log_path', help='The path of the event log.', type=str)

    args = parser.parse_args()

    pnet_parser = PNetParser(args.petri_net_path)
    event_log_parser = EventLogParser(args.event_log_path)

    edges = pnet_parser.get_arcs()
    nodes = pnet_parser.get_nodes()
    cc = ConformanceChecking(nodes, edges)

    ids = event_log_parser.get_cases_ids()
    num_ids = len(ids)
    for i in ids:
        trace = event_log_parser.get_trace(i)

        if cc.verify_trace(trace) is True:
            num_passed += 1

    print('The percentage of traces passed the conformance checking is ' + str(num_passed)+'/'+str(num_ids), '=',
          num_passed / num_ids)
