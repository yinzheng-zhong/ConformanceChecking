import argparse
from Parser import PNetParser
from Parser import EventLogParser
from ConformanceChecking import ConformanceChecking

num_passed = 0

pnet_parser = PNetParser('/home/yinzheng/Documents/model/Wednesday_DoS.pnml')
event_log_parser = EventLogParser('/home/yinzheng/Documents/original csv/anomalous/split/Tuesday_BruteForce_modified_test.csv')

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
