# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pbr.version

__version__ = pbr.version.VersionInfo('dopplerr').release_string()
version = __version__
dopplerr_version = __version__

__all__ = [
    '__version__',
    'dopplerr_version',
    'version',
]
