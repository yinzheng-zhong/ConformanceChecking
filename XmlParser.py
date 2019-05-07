import xmltodict


class Tools:
    @staticmethod
    def string_id_to_int_id(dic):
        return int(dic[1:])


class XmlParser:
    PNML = 'pnml'
    NET = 'net'

    def __init__(self, xml_path):
        self.path = xml_path
        self.dictionary = self.parse()

    def parse(self):
        with open(self.path, 'r') as file:
            data = file.read()
        return xmltodict.parse(data)

    def get_places(self):
        places_dic = self.dictionary[self.PNML][self.NET]['place']
        ids = []
        for place in places_dic:
            ids.append(Tools.string_id_to_int_id(place['@id']))  # convert string 'n##' to integer ##

        names = ['place'] * len(ids)

        return {'id': ids, 'label': names}

    def get_transitions(self):
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

        return {'id': ids, 'label': names}

    def get_nodes(self):
        places = self.get_places()
        transitions = self.get_transitions()

        places['id'].extend(transitions['id'])
        places['label'].extend(transitions['label'])

        return places

    def get_arcs(self):
        arcs = self.dictionary[self.PNML][self.NET]['arc']

        source = []
        target = []
        for arc in arcs:
            source.append(Tools.string_id_to_int_id(arc['@source']))  # convert string 'n##' to integer ##
            target.append(Tools.string_id_to_int_id(arc['@target']))  # convert string 'n##' to integer ##

        return {'source': source, 'target': target}

    def get_finalmarking(self):
        marking = self.dictionary[self.PNML][self.NET]['finalmarkings']['marking']['place']
        for objs in marking:
            if objs['text'] == '1':
                return int(objs['@idref'][1:])
