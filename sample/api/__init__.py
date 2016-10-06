"""
RESTful API view definitions
"""

import os.path

# load all views in this directory
__all__ = [os.path.basename(p)[:-3]
           for p in os.listdir(os.path.dirname(__file__))
           if p.endswith('.py') and not p.startswith('_')]
