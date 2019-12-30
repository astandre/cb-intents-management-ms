from unittest import TestCase


class TestSomething(TestCase):

    def test_my_view(self):
        pass

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

# For options view

# {'intent': 'http://127.0.0.1/ockb/resources/ObtenerInformacion', 'question': '¿De que curso deseas conocer?', 'options': ['Introducción a la Biorremediación ', 'Biología general ', 'Uso de las tecnologías de la información y la comunicación  ', 'Manejo y análisis de bases de datos ', 'Bebidas alcohólicas fermentadas ', 'Marketing ', 'Desarrollo comunitario ', 'Fundamentos matemáticos ', 'Orientación Vocacional ', 'Legislación mercantil y societaria ', 'Prevención integral del consumo de sustancias ', 'Psicología General ', 'Preparación Específica para la Prueba de Admisión ', 'Antropología Básica ', 'Química general ', 'Microbiología Ambiental y Agrícola ', 'Economía a tu alcance ', 'Biología ', 'Emprendimiento y generación de ideas ', 'Justo a tiempo ', 'Biología ', 'Introducción a la Educación Preescolar ', 'Métodos alternativos de resolución de conflictos ', 'Conocimiento ancestral de plantas medicinales ', 'Realidad Nacional ', 'Producción Audiovisual ', 'Ética Moral ', 'Pedagogía General ', 'Educación para una alimentación saludable ', 'Fundamentos informáticos ', 'Comprensión Lectora ', 'Psicología Social ', 'Razonamiento Abstracto  ', 'Huertos familiares ', 'Manejo del recurso suelo ', 'Introducción a la Economía ', 'Razonamiento Abstracto  ', 'Contaminación Atmosférica ', 'Administración I ']}

# kg.get_options("ObtenerInformacion")