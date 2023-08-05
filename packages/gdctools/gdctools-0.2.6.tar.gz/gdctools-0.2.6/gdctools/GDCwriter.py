#!/usr/bin/env python
# encoding: utf-8

# Front Matter {{{
'''
Copyright (c) 2017 The Broad Institute, Inc.  All rights are reserved.

GDCwriter: this file is part of gdctools.  See the <root>/COPYRIGHT
file for the SOFTWARE COPYRIGHT and WARRANTY NOTICE.

@author: Michael S. Noble
@date:  2017_09_12
'''

# }}}

from abc import ABCMeta, abstractmethod

class GDCwriter(object):

    __metaclass__ = ABCMeta

    def __init__(self, filename, mode='w'):
        self.filep = open(filename, mode)

    def __del__(self):
        close(self.filep)

    @abstractmethod
    def emit_participants_header(self, fp):
        pass

    def write_particpants(self, filep, header, data):
        self.emit_participants_required_header(filep)
        for participant in data:
            filep.write(participant + "\n")

    @abstractmethod
    def emit_samples_header(self):
        pass

    def write_samples(self, ):
        self.emit_samples_header()

    @abstractmethod
    def emit_set_header(self):
        pass

    def write_set(self):
        self.write_set_header()

class FireCloudWriter(GDCwriter):
    def emit_participants_header(self):
        self.filep.write("entity:participant_id\n")

    def emit_samples_header(self):
        self.filep.write("entity:sample_id\tparticipant_id\n")

if __name__ == "__main__":
    w = FireCloudWriter("test.dat")
    w.write_samples(["
