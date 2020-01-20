Intents-Managment
=================



.. image:: https://readthedocs.org/projects/cb-intents-management-ms/badge/?version=latest
   :target: https://cb-intents-management-ms.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/astandre/cb-intents-management-ms.svg?branch=master
    :target: https://travis-ci.org/astandre/cb-intents-management-ms


This project is part of the architecture described in:
Herrera, Andre & Yaguachi, Lady & Piedra, Nelson. (2019). Building Conversational Interface for Customer Support Applied to Open Campus an Open Online Course Provider. 11-13. 10.1109/ICALT.2019.00011.


Running scripts


``docker build -t astandre/kbsbot_intents_managment . -f docker/Dockerfile``


``docker run --rm  --name=intents-managment -p 5002:8002 -it astandre/kbsbot_intents_managment``

