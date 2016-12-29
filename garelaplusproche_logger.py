import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s -  %(message)s')

#System out handler
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
root.addHandler(ch)

#File Handler
fh = logging.FileHandler('garelaplusproche.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
root.addHandler(fh)


def get_logger(name):
    return logging.getLogger(name)
