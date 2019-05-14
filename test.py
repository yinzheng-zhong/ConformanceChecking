import argparse
from Parser import PNetParser
from Parser import EventLogParser
from ConformanceChecking import ConformanceChecking

num_passed = 0

pnet_parser = PNetParser('model_xml/normal_20k.pnml')
event_log_parser = EventLogParser('trace_csv/Thursday_Inf_Dropbox_modified.csv')

edges = pnet_parser.get_arcs()
nodes = pnet_parser.get_nodes()
cc = ConformanceChecking(nodes, edges)

num_traces = event_log_parser.get_num_cases()
for i in range(num_traces):
    trace = event_log_parser.get_trace(i)

    if cc.verify_trace(trace) is True:
        num_passed += 1

print('The percentage of traces passed the conformance checking is ', num_passed / num_traces)
