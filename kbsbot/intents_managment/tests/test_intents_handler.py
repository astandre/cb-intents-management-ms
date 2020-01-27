from unittest import TestCase
from kbsbot.intents_managment.knowledge_graph import KGHandler


class IntentsHandlerTest(TestCase):
    def setUp(self):
        base_url = "http://127.0.0.1"
        path = "C:\\Users\\andre\\Documents\\PythonTutos\\cb-intents-management-ms\\kbsbot\\intents_managment\\kg.rdf"
        self.kg = KGHandler(base_url, path)

    def test_not_direct_answer(self):
        answer = self.kg.get_intent_answer("ObtenerInformacion", [
            {"type": "http://127.0.0.1/ockb/course/ontology/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}])
        self.assertEqual(answer["answer"][0]["property"], "description")
        self.assertIn("template", answer)
        self.assertIn("answer", answer)
        self.assertGreater(len(answer["answer"]), 0)
        self.assertIn("property", answer["answer"][0])
        self.assertIn("value", answer["answer"][0])

    def test_direct_answer(self):
        answer = self.kg.get_intent_answer("listarCursos", [
            {"type": "http://127.0.0.1/ockb/course/ontology/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}])

        self.assertIn("template", answer)
        self.assertIn("answer", answer)
        self.assertIn("property", answer["answer"][0])
        self.assertIn("value", answer["answer"][0])
        self.assertTrue(len(answer["answer"][0]["value"]) > 1)
        self.assertEqual(answer["answer"][0]["property"], "courseName")
        self.assertIsInstance(answer["answer"][0]["value"], list)

    def test_related_answer(self):
        answer = self.kg.get_intent_answer("ObtenerDocente", [
            {"type": "http://127.0.0.1/ockb/course/ontology/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}])
        self.assertIn("template", answer)
        self.assertIn("answer", answer)
        self.assertIn("property", answer["answer"][0])
        self.assertEqual(answer["answer"][0]["property"], "teacherName")
        self.assertIn("value", answer["answer"][0])
        self.assertIsInstance(answer["answer"][0]["value"], list)

    def test_multiple_property_answer(self):
        answer = self.kg.get_intent_answer("ObtenerFechas", [
            {"type": "http://127.0.0.1/ockb/course/ontology/Course", "value": "http://127.0.0.1/ockb/resources/EAIG5"}])
        self.assertIn("template", answer)
        self.assertIn("answer", answer)
        self.assertIn("property", answer["answer"][0])
        self.assertTrue(answer["answer"][0]["property"] == "endDate" or answer["answer"][0]["property"] == "beginDate")
        self.assertEqual(len(answer["answer"]), 2)
        self.assertIn("value", answer["answer"][0])
        self.assertIsInstance(answer["answer"][0]["value"], list)

    def test_build_uri(self):
        result = self.kg._build_uri("http://127.0.0.1/ockb/course/ontology/Course")
        self.assertIn("http", result)
        result = self.kg._build_uri("Course")
        self.assertIn("http", result)
        self.assertIn("resources", result)

    def test_get_requirements(self):
        """
        .. todo:: handle wrong Intent
        """
        result = self.kg.get_intent_requirements("ObtenerDocente")
        self.assertGreater(len(result["requires"]), 0)
        self.assertIn("ObtenerDocente", result["intent"])
        result = self.kg.get_intent_requirements("listarCursos")
        self.assertEqual(len(result["requires"]), 0)
        # result = self.kg.get_intent_requirements("ObtenerColores")
        # print(result)

    def test_get_intent_options(self):
        result = self.kg.get_intent_options("ObtenerDocente")
        self.assertIn("type", result["options"][0])
        self.assertIn("value", result["options"][0])
        self.assertIn("intent", result)
        self.assertIn("question", result)
        result = self.kg.get_intent_options("ObtenerColores")
        self.assertEqual(None, result)

    def test_get_entity_options(self):
        result = self.kg.get_entity_options("http://127.0.0.1/ockb/course/ontology/Course")
        self.assertIn("entity", result)
        self.assertIn("options", result)
        self.assertGreater(len(result["options"]), 0)
        result = self.kg.get_entity_options("Course")
        self.assertEqual(len(result["options"]), 0)
