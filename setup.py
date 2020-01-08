import sys
from setuptools import setup, find_packages
from kbsbot.intents_managment import __version__

with open('requirements.txt') as f:
    deps = [dep for dep in f.read().split('\n') if dep.strip() != ''
            and not dep.startswith('-e')]
    install_requires = deps

setup(name='intents_managment',
      description="This microservice is used to identify the requirements of an intent, provide options to complete information and return answer if the intent is completed",
      long_description=open('README.rst').read(),
      version=__version__,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=install_requires,
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
