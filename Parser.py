import xmltodict
import numpy as np
from Tools import Tools
import pandas as pd


class EventLogParser:
    CASE_ID_COLUMN_NAME = 'Case_ID'

    def __init__(self, csv_path):
        self.path = csv_path
        self.event_log = self._parse()

    def _parse(self):
        return pd.read_csv(self.path,
                           error_bad_lines=False,
                           index_col=False,
                           low_memory=False)

    def get_num_cases(self):
        case_ids = self.event_log[self.CASE_ID_COLUMN_NAME].values
        return np.max(case_ids)

    def get_trace(self, case_id):
        case = self.event_log.loc[self.event_log['Case_ID'] == case_id].values
        trace = case[:, 6] + '|' + case[:, 7]
        return np.asarray(trace, dtype=np.str)


class PNetParser:
    PNML = 'pnml'
    NET = 'net'
    DIC_KEY_ID = 'id'
    DIC_KEY_LABEL = 'label'

    def __init__(self, xml_path):
        self.path = xml_path
        self.dictionary = self._parse()

    def _parse(self):
        with open(self.path, 'r') as file:
            data = file.read()
        return xmltodict.parse(data)

    def _get_places(self):
        places_dic = self.dictionary[self.PNML][self.NET]['place']
        ids = []
        for place in places_dic:
            ids.append(Tools.string_id_to_int_id(place['@id']))  # convert string 'n##' to integer ##

        names = ['place'] * len(ids)

        return {self.DIC_KEY_ID: ids, self.DIC_KEY_LABEL: names}

    def _get_transitions(self):
        transitions = self.dictionary[self.PNML][self.NET]['transition']

        ids = []
        names = []
        for transition in transitions:
            ids.append(Tools.string_id_to_int_id(transition['@id']))  # convert string 'n##' to integer ##
            label = transition['name']['text']
            if 'tau' in label:
                names.append('tau')
            else:
                names.append(label)

        return {self.DIC_KEY_ID: ids, self.DIC_KEY_LABEL: names}

    def get_nodes(self):
        places = self._get_places()
        transitions = self._get_transitions()

        places[self.DIC_KEY_ID].extend(transitions[self.DIC_KEY_ID])
        places[self.DIC_KEY_LABEL].extend(transitions[self.DIC_KEY_LABEL])

        node = {self.DIC_KEY_ID: np.asarray(places[self.DIC_KEY_ID], dtype=np.int16),
                self.DIC_KEY_LABEL: np.asarray(places[self.DIC_KEY_LABEL])}

        init_marking_index = np.argwhere(node[self.DIC_KEY_ID] == 1)[0, 0]
        final_marking_index = np.argwhere(node[self.DIC_KEY_ID] == self._get_final_marking())[0, 0]

        node[self.DIC_KEY_LABEL][init_marking_index] = 'initial_marking'
        node[self.DIC_KEY_LABEL][final_marking_index] = 'final_marking'

        return node

    def get_arcs(self):
        arcs = self.dictionary[self.PNML][self.NET]['arc']

        source = []
        target = []
        for arc in arcs:
            source.append(Tools.string_id_to_int_id(arc['@source']))  # convert string 'n##' to integer ##
            target.append(Tools.string_id_to_int_id(arc['@target']))  # convert string 'n##' to integer ##

        return {'source': np.asarray(source, dtype=np.int16), 'target': np.asarray(target, dtype=np.int16)}

    def _get_final_marking(self):
        marking = self.dictionary[self.PNML][self.NET]['finalmarkings']['marking']['place']
        for objs in marking:
            if objs['text'] == '1':
                return int(objs['@idref'][1:])
