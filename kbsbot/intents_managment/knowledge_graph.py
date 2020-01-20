import rdflib
import os
from rdflib import URIRef, Namespace
from rdflib.namespace import RDF, RDFS


class KGHandler:
    """
    KGHandler is the main class of this project.
    It is used to connect to the knowledge base, an retrieve information for intents.

    """
    BASE_URL = os.environ.get("BASE_URL")
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
            # path = os.path.dirname(__file__) + "/kg.rdf"
            # print(os.path.dirname(__file__))
            path = os.environ.get("KG_URL")
            # print(path)
            self.grafo = rdflib.Graph()
            self.grafo.parse(path, format="xml")
        except Exception as e:
            print(e)

    def _build_uri(self, uri, resource=True):
        """
        This method builds an URI from a complete URL or just the URI name.
        This method also checks if the uri is well structured.

        :param uri: the URI or full URL

        :param resource: If the URI is from the ontology or a resource

        :return: The namespace of the full URI
        """
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
        """
        This method returns all required entities of an intent.

        :param intent: The intent from where required entities will ne retrieved.

        :return: a list of the required entities.
        """
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
        """
        This method is used to remove the URL part of the URI to return the clean property.

        :param uri: The URI to be cleaned

        :return: The clean property from the URI
        """
        uri = str(uri)
        if uri.find('#') != -1:
            special_char = '#'
        else:
            special_char = '/'
        index = uri.rfind(special_char)
        return uri[index + 1:len(uri)]

    def build_answer(self, qres, ans_prop):
        """
        This method builds a part of the answer, from the result of a SPARQL query.
        :param qres: The result from a SPARQL query.

        :param ans_prop: The property intended to an answer.

        :return: A dict containing a property and a value from the query result.

        .. todo:: handle multiple properties answer
        """

        answer = []
        ans_prop = self.clean_uri(ans_prop)
        values = []
        for row in qres:
            values.append(str(row[0]))
        answer.append({"property": ans_prop, "value": values})
        return answer

    def get_answer(self, intent):
        """
        This method retrieves the answer class from a SPAQL query.
        The answer has a series of properties that may or may not be present,
        depending on the way the answer is configured

        :param intent: The intent from where the answer will be retrieved

        :return: returns the different properties found in the answer object.
        """
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

    def get_intent_answer(self, intent, entities_aux):
        """
        This method returns the full answer from a intent.
        Depending on the different properties found in the answer object.
        The answer can be from a direct object, or an indirect object or, from a related object.

        :param intent: The intent from where the answer will be retrieved

        :param entities: A list of entities, that can be collected in different ways from other components.

        :return: The full answer in a dictionary displayed in this way:
            {
            'answer': [{
            'property': 'teacherName',
            'value': ['Diana Lucía Espinoza Torres', 'Glenda Edith Ponce Espinosa']}],
            'template': 'El docente encargado del curso es {%teacherName%}'
            }

        """
        intent = self._build_uri(intent)
        entities = []
        for entity in entities_aux:
            entities.append({
                "type": self._build_uri(entity["type"]),
                "value": self._build_uri(entity["value"])
            })
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
                aux_type = entity_iter["type"]
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
        """
        This method returns the options related to an Intent
        To complete the different entities needed to satisfy an intent.

        :param intent: An intent from where options will be retrieved.

        :return: a dict containing, the resolve question, and the different options.

        .. todo:: handle custom options
        """
        intent = self._build_uri(intent)

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
        """
        This method returns options to complete an entity.

        :param entity: The entity type from where options will be retrieved

        :return: returns an entity and their options.

        .. todo:: handle custom options
        """
        entity = self._build_uri(entity, resource=False)
        # print(entity)
        query = f"""SELECT ?option_thing ?option                               
                          WHERE {{                                                    
                                  ?option_thing  <{RDF.type}>  <{entity}> .            
                                  ?option_thing <{RDFS.label}> ?option  .                                                    
                      }}"""
        q_res = self.grafo.query(query)

        options = []
        for row in q_res:
            payload, option = row
            if option is not None and payload is not None:
                options.append({"option": option, "payload": payload})

        return {"entity": str(entity), "options": options}
