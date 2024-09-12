import logging
import os
directory = os.path.dirname(__file__)
logging.basicConfig(filename = directory + '/log.txt', format = '%(asctime)s %(module)s %(funcName)s - %(message)s', level = logging.INFO, filemode = 'w')
