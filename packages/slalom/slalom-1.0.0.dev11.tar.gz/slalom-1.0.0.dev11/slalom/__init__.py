

from pkg_resources import get_distribution as _get_distribution
from pkg_resources import DistributionNotFound as _DistributionNotFound

try:
    __version__ = _get_distribution('slalom').version
except _DistributionNotFound:
    __version__ = 'unknown'

from .utils import (initFA, load_hdf5, load_txt, preTrain, plotLoadings, plotFactors, plotRelevance, saveFA, dumpFA)
from .core import (CSparseFA)

