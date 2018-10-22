import os
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = {'db.url': 'sqlite:///oracle.sqlite',
            'db.echo':'True'
            }

LOGGER = {'level': logging.INFO}

#basedir = os.path.abspath(os.path.dirname(__file__))
