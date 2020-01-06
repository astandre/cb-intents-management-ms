import rdflib
import os
from rdflib import URIRef, Namespace
from rdflib.namespace import RDF, RDFS
import configparser


class KGHandler:
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + '/settings.ini')
    BASE_URL = config['kg']['BASE_URL']
    RESOURCE_URI = f"{BASE_URL}/ockb/resources/"
    ONTOLOGY_URI = f"{BASE_URL}/ockb/ontology/"

    pf_has_rq = Namespace(ONTOLOGY_URI + "hasResolutionQuestion")
    pf_question = Namespace(ONTOLOGY_URI + "hasQuestion")
    pf_resolves = Namespace(ONTOLOGY_URI + "resolves")
    pf_option = Namespace(ONTOLOGY_URI + "hasOption")
    pf_answer = Namespace(ONTOLOGY_URI + "hasAnswer")
    pf_requires = Namespace(ONTOLOGY_URI + "requiresEntity")
    pf_ans_prop = Namespace(ONTOLOGY_URI + "answerProperty")
    pf_refers_to = Namespace(ONTOLOGY_URI + "refersTo")
    pf_template = Namespace(ONTOLOGY_URI + "answerTemplate")
    pf_ans_from = Namespace(ONTOLOGY_URI + "answerFrom")
    pf_requires = Namespace(ONTOLOGY_URI + "requiresEntity")

    def __init__(self):
        try:
            path = os.path.dirname(__file__) + "/" + self.config['kg']['KB_URL']
            self.grafo = rdflib.Graph()
            self.grafo.parse(path, format="xml")
        except Exception as e:
            print(e)

    def _build_uri(self, uri, resource=True):
        if not isinstance(uri, Namespace):
            if "http" in uri:
                return URIRef(uri)
            else:
                if resource:
                    return Namespace(self.RESOURCE_URI + uri)
                else:
                    return Namespace(self.ONTOLOGY_URI + uri)
        else:
            return uri

    def get_intent_requirements(self, intent):
        intent = self._build_uri(intent)

        query = f"""SELECT ?entity WHERE {{ 
                                    <{intent}> <{self.pf_requires}> ?entity}}"""

        qres = self.grafo.query(query)
        requires = []
        for row in qres:
            # print(row)
            entity = row[0]
            requires.append(str(entity))
        return {"intent": str(intent), "requires": requires}

    @staticmethod
    def clean_uri(uri):
        uri = str(uri)
        if uri.find('#') != -1:
            special_char = '#'
        else:
            special_char = '/'
        index = uri.rfind(special_char)
        return uri[index + 1:len(uri)]

    def build_answer(self, qres, ans_prop):
        # TODO handle multiple properties
        answer = []
        ans_prop = self.clean_uri(ans_prop)
        values = []
        for row in qres:
            values.append(str(row[0]))
        answer.append({"property": ans_prop, "value": values})
        return answer

    def get_answer(self, intent):
        intent = self._build_uri(intent)

        query = f"""SELECT ?property ?refers ?template ?from ?entity
                          WHERE {{
                                  <{intent}> <{self.pf_answer}> ?answer .
                                  OPTIONAL {{
                                  ?answer <{self.pf_ans_prop}> ?property .
                                  }}
                                  OPTIONAL {{
                                  ?answer <{self.pf_refers_to}> ?refers .
                                  }}
                                  OPTIONAL {{
                                  ?answer <{self.pf_template}> ?template .
                                  }} 
                                  OPTIONAL {{
                                  ?answer <{self.pf_ans_from}> ?from .
                                  }}
                                  OPTIONAL {{
                                  <{intent}> <{self.pf_requires}> ?entity .
                                  }}
                      }}"""
        qres = self.grafo.query(query)
        if len(qres) >= 1:
            for row in qres:
                # print(row)
                ans_prop, refers_to, template, ans_from, entity = row
                break
            return ans_prop, refers_to, template, ans_from, entity

    def get_intent_answer(self, intent, entities):
        """

        :param intent: an intent
        :param entities: A list of entities
        :return:
            {
            'answer': [{
            'property': 'teacherName',
            'value': ['Diana Lucía Espinoza Torres', 'Glenda Edith Ponce Espinosa']}],
            'template': 'El docente encargado del curso es {%teacherName%}'
            }

        """
        ans_prop, refers_to, template, ans_from, entity = self.get_answer(intent)

        ans_prop = Namespace(ans_prop)
        if ans_from is not None:
            # print("Direct answer")
            ans_from = Namespace(ans_from)
            if refers_to is not None:
                # print("Referred Answer")
                refers_to = Namespace(refers_to)
                # print(refers_to)
                query = f"""SELECT ?answer  WHERE {{
                                    <{ans_from}> <{refers_to}> ?related .
                                    ?related <{ans_prop}> ?answer.
                                                   }}"""
            else:
                # print("Not referred Answer")
                query = f"""SELECT ?answer WHERE {{
                                    <{ans_from}> <{ans_prop}> ?answer
                                                    }}"""

        else:
            # print("Not direct answer")
            entity_value = None
            for entity_iter in entities:
                aux_type = Namespace(entity_iter["type"])
                if aux_type == entity:
                    entity_value = entity_iter["value"]
                    break

            if entity_value is not None:
                entity_value = Namespace(entity_value)
                if refers_to is None:
                    # print("Not referred answer")
                    query = f"""SELECT ?answer WHERE {{
                                            <{entity_value}> <{ans_prop}> ?answer
                                                       }}"""

                else:
                    # print("Referred answer")
                    refers_to = Namespace(refers_to)
                    query = f"""SELECT ?answer WHERE {{
                                        <{entity_value}> <{refers_to}>  ?related .
                                        ?related <{ans_prop}> ?answer .
                                    }}"""
            else:
                return None

        qres = self.grafo.query(query)
        answer = self.build_answer(qres, ans_prop)
        return {"answer": answer, "template": str(template)}

    def get_intent_options(self, intent):
        intent = self._build_uri(intent)

        # TODO handle custom options
        query = f"""SELECT ?question ?option ?resolves
                          WHERE {{
                                  <{intent}> <{self.pf_has_rq}> ?rq .
                                  OPTIONAL {{
                                  ?rq <{self.pf_question}> ?question .
                                  }}
                                  OPTIONAL {{
                                  ?rq <{self.pf_resolves}> ?resolves .
                                  ?option_thing  <{RDF.type}>  ?resolves .
                                  ?option_thing <{RDFS.label}> ?option  .
                                  }}
                      }}"""

        q_res = self.grafo.query(query)

        options = []
        question = None
        for row in q_res:
            # print(row)
            question, option, resolves = row
            if option is not None and resolves is not None:
                options.append({"type": str(resolves), "value": str(option)})
        if question is None:
            return None
        else:
            return {"intent": str(intent), "question": str(question), "options": options}

    def get_entity_options(self, entity):
        entity = self._build_uri(entity, resource=False)
        # print(entity)
        # TODO handle custom options                                                  
        query = f"""SELECT ?option                               
                          WHERE {{                                                    
                                  ?option_thing  <{RDF.type}>  <{entity}> .            
                                  ?option_thing <{RDFS.label}> ?option  .                                                    
                      }}"""
        q_res = self.grafo.query(query)

        options = []
        for row in q_res:
            option = row
            if option is not None:
                options.append(str(option[0]))

        return {"entity": str(entity), "options": options}


# TODO handle multi properties in answer
# TODO write tests with this information
kg = KGHandler()
# print(kg.get_options("ObtenerInformacion"))
# print(kg.get_entity_options("http://127.0.0.1/ockb/course/ontology/Course"))
