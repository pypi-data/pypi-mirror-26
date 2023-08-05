"""Main functions to simulates reads"""

import sys

from mirtop.libs.logger import initialize_logger
from mirtop.libs.parse import parse_cl
from mirtop.libs.simulator import simulate
from mirtop.gff import reader
import mirtop.libs.logger as mylog
import time


def main(**kwargs):
    kwargs = parse_cl(sys.argv[1:])
    initialize_logger(kwargs['args'].out, kwargs['args'].debug, kwargs['args'].print_debug)
    logger = mylog.getLogger(__name__)
    start = time.time()
    if "gff" in kwargs:
        logger.info("Run annotation")
        reader(kwargs["args"])
    elif "simulator" in kwargs:
        logger.info("Run simulation")
        simulate(kwargs["args"])
    elif "check" in kwargs["args"]:
        logger.info("Not yet ready: This will check GFF files.")
    elif "query" in kwargs["args"]:
        logger.info("Not yet ready: This will allow queries to GFF files.")
    elif "convert" in kwargs["args"]:
        logger.info("Not yet ready: This will output tabular format from GFF files.")
    logger.info('It took %.3f minutes' % ((time.time()-start)/60))
