from __future__ import print_function, division, absolute_import

import sabaody
from sabaody.scripts.biopredyn.b2.b2problem import B2Problem
from sabaody.scripts.biopredyn.b2.params import getDefaultParamValues

import os

def test_datapoint_usage():
    b2 = B2Problem(os.path.join(os.path.dirname(__file__),'..','sbml','b2.xml'))
    # call evaluate to trigger residual calc
    b2.evaluate(getDefaultParamValues())
    # get data point usage info
    total,total_used,usage_for_quantity = b2.getUsageByQuantity()
    # ensure positive
    assert total > 0
    assert total_used > 0
    # did we use all data points?
    #print('B2 total data point usage: {}/{}'.format(total,total_used))
    assert total == total_used
    # check the usage per quantity
    for q,used in usage_for_quantity.items():
        a = b2.measurement_map[q]
        n = a.shape[0]
        assert used == n