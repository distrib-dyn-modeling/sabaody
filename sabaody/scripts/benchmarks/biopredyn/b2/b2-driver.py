# Driver code for B2 parameter fitting problem.
from __future__ import print_function, division, absolute_import

from sabaody.scripts.benchmarks.biopredyn.benchsetup import BiopredynConfiguration
from params import getDefaultParamValues, getUpperBound, getLowerBound
from b2problem import B2_UDP
from b2problem_validator import B2Validator_UDP

from os.path import dirname, realpath

def get_udp(validation_mode,n):
    if not validation_mode:
        return B2_UDP(getLowerBound(),getUpperBound())
    else:
        return B2Validator_UDP(getLowerBound(),getUpperBound(),n=n)

config = BiopredynConfiguration.from_cmdline_args('b2-driver', '../../../../../sbml/b2.xml', dirname(realpath(__file__)), get_udp, getDefaultParamValues)

config.run_command(config.command)
