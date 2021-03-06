import rdflib
import os
from rdflib import URIRef, Namespace
from rdflib.namespace import RDF, RDFS


class KGHandler:
    """
    KGHandler is the main class of this project.
    It is used to connect to the knowledge base, an retrieve information for intents.

    """

    BASE_URL = ""
    pf_has_rq = ""
    pf_question = ""
    pf_resolves = ""
    pf_option = ""
    pf_answer = ""
    pf_requires = ""
    pf_ans_prop = ""
    pf_refers_to = ""
    pf_template = ""
    pf_ans_from = ""
    pf_requires = ""
    agent_desc = ""
    has_intent = ""
    intent_desc = ""
    intent_name = ""
    RESOURCE_URI = ""
    ONTOLOGY_URI = ""

    def __init__(self, base_url, path):
        try:
            # Setting base URL an properties
            self.BASE_URL = base_url
            self.RESOURCE_URI = f"{self.BASE_URL}/ockb/resources/"
            self.ONTOLOGY_URI = f"{self.BASE_URL}/ockb/ontology/"
            self.pf_has_rq = Namespace(self.ONTOLOGY_URI + "hasResolutionQuestion")
            self.pf_question = Namespace(self.ONTOLOGY_URI + "hasQuestion")
            self.pf_resolves = Namespace(self.ONTOLOGY_URI + "resolves")
            self.pf_option = Namespace(self.ONTOLOGY_URI + "hasOption")
            self.pf_answer = Namespace(self.ONTOLOGY_URI + "hasAnswer")
            self.pf_requires = Namespace(self.ONTOLOGY_URI + "requiresEntity")
            self.pf_ans_prop = Namespace(self.ONTOLOGY_URI + "answerProperty")
            self.pf_refers_to = Namespace(self.ONTOLOGY_URI + "refersTo")
            self.pf_template = Namespace(self.ONTOLOGY_URI + "answerTemplate")
            self.pf_ans_from = Namespace(self.ONTOLOGY_URI + "answerFrom")
            self.pf_requires = Namespace(self.ONTOLOGY_URI + "requiresEntity")
            self.agent_desc = Namespace(self.ONTOLOGY_URI + "agentDescription")
            self.has_intent = Namespace(self.ONTOLOGY_URI + "hasIntent")
            self.intent_desc = Namespace(self.ONTOLOGY_URI + "intentDescription")
            self.intent_name = Namespace(self.ONTOLOGY_URI + "intentName")
            # Setting path por kg
            self.path = path
            self.grafo = rdflib.Graph()
            self.grafo.parse(self.path, format="xml")
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

    def build_answer_prop_val(self, qres, ans_prop):
        """
        This method builds a part of the answer, from the result of a SPARQL query.
        :param qres: The result from a SPARQL query.

        :param ans_prop: The property intended to an answer.

        :return: A dict containing a property and a value from the query result.

        """

        ans_prop = self.clean_uri(ans_prop)
        values = []
        for row in qres:
            values.append(str(row[0]))

        answer = {"property": ans_prop, "value": values}
        return answer

    def get_answer_properties(self, intent):
        """
        This method retrieves the answer properties from an answer class using a SPARQL query.
        The answer has a series of properties that may or may not be present,
        depending on the way the answer is configured.
        If there are more than one properties of an answer, the will be stored in an array.

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
        ans_prop = None
        refers_to = None
        template = None
        ans_from = None
        entity = None
        ans_prop_list = []
        if len(qres) == 1:
            for row in qres:
                ans_prop, refers_to, template, ans_from, entity = row

        elif len(qres) > 1:
            for row in qres:
                ans_prop, refers_to, template, ans_from, entity = row
                ans_prop_list.append(ans_prop)

        return ans_prop, refers_to, template, ans_from, entity, ans_prop_list

    def get_answer_parts(self, ans_prop, refers_to, ans_from, entity, entities):
        """
        This method searches for the real values of the answer of the intent.
        Depending on the different properties found in the answer object.
        The answer can be from a direct object, or an indirect object or, from a related object.

        :param ans_prop: A property to retrieve from an object

        :param refers_to: A related object to obtain a value using ans_prop

        :param ans_from: An object to obtain a value using ans_prop

        :param entity: A direct entity to be used in the answer

        :param entities: A list of auxiliary entities

        :return: The a pair of property an value that conforms an answer.
        """
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
        answer = self.build_answer_prop_val(qres, ans_prop)
        return answer

    def get_intent_answer(self, intent, entities_aux):
        """
        This method returns the full answer from a intent.
        Using and other method (get_answer_properties) to retrieve the different properties of an Answer Object.
        And other method (get_answer_parts) to build the key value of properties of an Entity.

        :param intent: The intent from where the answer will be retrieved

        :param entities_aux: A list of entities, that can be collected in different ways from other components.

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
        ans_prop, refers_to, template, ans_from, entity, ans_prop_list = self.get_answer_properties(intent)
        answer = []
        if len(ans_prop_list) == 0:
            answer.append(self.get_answer_parts(ans_prop, refers_to, ans_from, entity, entities))
        else:
            for ans_prop in ans_prop_list:
                answer.append(self.get_answer_parts(ans_prop, refers_to, ans_from, entity, entities))

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
                options.append({"option": str(option), "payload": payload})

        return {"entity": str(entity), "options": options}

    def find_entity_type(self, entity):
        entity_type = None
        entity = self._build_uri(entity, resource=True)
        # print(entity)
        query = f"""SELECT ?entity_type                               
                                  WHERE {{                                                    
                                          <{entity}>  <{RDF.type}> ?entity_type  .                                                                
                              }}"""

        q_res = self.grafo.query(query)
        for row in q_res:
            entity_type = row[0]
            break
        return {"value": str(entity), "type": str(entity_type)}

    def find_agent_intents(self, agent):
        """
        This method returns information about the chatbot, like name, description and intents.

            :param agent: A valid agent name

        """
        agent = self._build_uri(agent, resource=True)
        query = f"""SELECT  ?name ?description ?ag_des
                                     WHERE {{                                                    
                                             <{agent}>  <{self.has_intent}> ?intent . 
                                             ?intent  <{self.intent_name}> ?name . 
                                             ?intent  <{self.intent_desc}> ?description . 
                            OPTIONAL {{
                                   <{agent}>  <{self.agent_desc}> ?ag_des .
                                  }}
                                 }}"""

        q_res = self.grafo.query(query)
        agent_desc = None
        agent_intents = []
        for row in q_res:
            # print(row)
            intent_name, intent_des, agent_desc_temp = row
            agent_intents.append({"intent": str(intent_name), "description": str(intent_des)})
            if agent_desc is None:
                agent_desc = str(agent_desc_temp)
        return {"agent": str(agent), "description": agent_desc, "intents": agent_intents}

    def get_resolution_question(self, intent, entity):
        """
        This method finds the resolution question of an intent and entity
        :param intent: A valid intent name

        :param entity: A valid entity name

        :return: A dict with the intent, entity and the resolution question
        """
        intent = self._build_uri(intent, resource=True)
        entity = self._build_uri(entity, resource=False)

        query = f"""SELECT ?question 
                               WHERE {{
                                       <{intent}> <{self.pf_has_rq}> ?rq .
                                       ?rq <{self.pf_resolves}> <{entity}> .
                                       ?rq <{self.pf_question}> ?question .
                              }}          
                """

        q_res = self.grafo.query(query)
        rq = None
        for row in q_res:
            # print(row)
            rq = row[0]
            break
        return {"intent": str(intent), "entity": str(entity), "rq": str(rq)}

# base_url = "http://127.0.0.1"
# path = "C:\\Users\\andre\\Documents\\PythonTutos\\cb-intents-management-ms\\kbsbot\\intents_managment\\kg.rdf"
# kg = KGHandler(base_url, path)
