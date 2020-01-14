from setuptools import setup, find_packages
from kbsbot.intents_managment import __version__

setup(name='intents_managment',
      description="This microservice is used to identify the requirements of an intent, provide options to complete information and return answer if the intent is completed",
      long_description=open('README.rst').read(),
      version=__version__,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      dependency_links=["https://github.com/Runnerly/flakon.git#egg=flakon"],
      install_requires=["flask", "rdflib"],
      author="André Herrera",
      author_ewmail="andreherrera97@hotmail.com",
      license="MIT",
      keywords=["chatbots", "microservices", "linked data"],
      entry_points={
          'console_scripts': [
              'intents_managment = kbsbot.intents_managment.run:main',
          ],
      }
      )
