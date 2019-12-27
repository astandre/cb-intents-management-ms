import rdflib
import os
from rdflib import URIRef, Namespace


class KGHandler:
    # TODO add this url to settings.ini
    BASE_URL = "http://127.0.0.1"
    RESOURCE_URI = f"{BASE_URL}/ockb/resources/"
    ONTOLOGY_URI = f"{BASE_URL}/ockb/ontology/"

    def __init__(self):
        try:
            path = os.path.dirname(__file__) + "/kg.rdf"
            self.grafo = rdflib.Graph()
            self.grafo.parse(path, format="xml")
        except Exception as e:
            print(e)

    def _build_intent_uri(self, intent):
        if not isinstance(intent, Namespace):
            return Namespace(self.RESOURCE_URI + intent)
        else:
            return intent

    def get_intent_requirements(self, intent):
        intent = self._build_intent_uri(intent)
        requires = Namespace(self.ONTOLOGY_URI + "requiresEntity")
        query = "SELECT ?entity WHERE {<" + intent + "> <" + requires + "> ?entity}"

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
        intent = self._build_intent_uri(intent)
        answer = Namespace(self.ONTOLOGY_URI + "hasAnswer")
        requires = Namespace(self.ONTOLOGY_URI + "requiresEntity")
        ans_prop = Namespace(self.ONTOLOGY_URI + "answerProperty")
        refers_to = Namespace(self.ONTOLOGY_URI + "refersTo")
        template = Namespace(self.ONTOLOGY_URI + "answerTemplate")
        ans_from = Namespace(self.ONTOLOGY_URI + "answerFrom")
        query = f"""SELECT ?property ?refers ?template ?from ?entity
                          WHERE {{
                                  <{intent}> <{answer}> ?answer .
                                  OPTIONAL {{
                                  ?answer <{ans_prop}> ?property .
                                  }}
                                  OPTIONAL {{
                                  ?answer <{refers_to}> ?refers .
                                  }}
                                  OPTIONAL {{
                                  ?answer <{template}> ?template .
                                  }} 
                                  OPTIONAL {{
                                  ?answer <{ans_from}> ?from .
                                  }}
                                  OPTIONAL {{
                                  <{intent}> <{requires}> ?entity .
                                  }}
                      }}"""
        qres = self.grafo.query(query)
        if len(qres) >= 1:
            for row in qres:
                print(row)
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
                print("Referred Answer")
                refers_to = Namespace(refers_to)
                # print(refers_to)
                query = f"""SELECT ?answer  WHERE {{
                                    <{ans_from}> <{refers_to}> ?related .
                                    ?related <{ans_prop}> ?answer.
                                                   }}"""
            else:
                print("Not referred Answer")
                query = f"""SELECT ?answer WHERE {{
                                    <{ans_from}> <{ans_prop}> ?answer
                                                    }}"""

        else:
            print("Not direct answer")
            entity_value = None
            for entity_iter in entities:
                aux_type = Namespace(entity_iter["type"])
                if aux_type == entity:
                    entity_value = entity_iter["value"]
                    break

            if entity_value is not None:
                entity_value = Namespace(entity_value)
                if refers_to is None:
                    print("Not referred answer")
                    query = f"""SELECT ?answer WHERE {{
                                            <{entity_value}> <{ans_prop}> ?answer
                                                       }}"""

                else:
                    print("Referred answer")
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

#     TODO handle when no answer is configured
# TODO handle multi properties in answer
# TODO write tests with this information
# kg = KGHandler()
# print(kg.get_intent_answer("ObtenerInformacion", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))

# print(kg.get_intent_answer("ObtenerFechas", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))

# print(kg.get_intent_answer("ObtenerFechasInicio", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))
# print(kg.get_intent_answer("ObtenerPrerequisitos", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))
# print(kg.get_intent_answer("ObtenerDuracion", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))
# print(kg.get_intent_answer("ObtenerPrecio", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))

# print(kg.get_intent_answer("ObtenerDocente", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))
# print(kg.get_intent_answer("ObtenerContenidos", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))
# print(kg.get_intent_answer("listarCursos", [
#     {"type": "http://127.0.0.1/ockb/resources/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}]))
