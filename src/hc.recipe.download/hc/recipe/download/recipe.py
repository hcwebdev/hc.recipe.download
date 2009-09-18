# -*- coding: utf-8 -*-
"""Recipe for downloading files and packages"""

import os
import shutil
import re

import zc.buildout
import zc.recipe.egg

import logging


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(self.name)
        
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        
        python = buildout['buildout']['python']
        options['executable'] = buildout[python]['executable']
        options['bin-directory'] = buildout['buildout']['bin-directory']

    def install(self):
        """Installer"""
        options                     = self.options
        recipe                      = options['recipe']
        requirements, working_set   = self.egg.working_set([ recipe ])
        
        return []
    
    def update(self):
        """Updater"""
        pass
    

