#!/usr/bin/env python

from sys import argv
from yaml import load
from re import match

##########
#  HELPERS
##################

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def input_checking(inputArgs):
        if check_length(inputArgs, 2) is False or \
           check_extension(inputArgs, ".md") is False:
            print "usage: render.py index.md"
            sys.exit()
        else:
                return inputArgs[1]

    @staticmethod
    def check_length(inputArgs, length):
        if len(inputArgs) == length:
            return True
        else:
            return False

    @staticmethod
    def check_extension(inputArgs, extension):
        extensionLength = len(extension)
        fileToCheck = inputArgs[1]
        if fileToCheck[-extensionLength:] == extension:
            return True
        else:
            return False

    @staticmethod
    def enum(*sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        reverse = dict((value, key) for key, value in enums.iteritems())
        enums['reverse_mapping'] = reverse
        return type('Enum', (), enums)

    @staticmethod
    def load_configuration():
        CONFIG_FILE  = "config.yaml"
        config_data  = {}
        stream       = open(CONFIG_FILE, 'r')
        config_steam = load(stream)
        for key, value in config_steam.items():
            config_data.update({key : value})
        return config_data

    @staticmethod
    def is_header(entry):
        matched = match('^[\#]{1}([a-z-A-Z-0-9- ._:)($\[\]!~@,-]{1,})$', entry)
        return matched is not None

    @staticmethod
    def is_sub_header(entry):
        matched = match('^[\#]{2}([a-z-A-Z-0-9- ._:)($\[\]!~@,-]{1,})$', entry)
        return matched is not None

    @staticmethod
    def is_paragraph(entry):
        matched = match('^[\-]{3}([a-z-A-Z-0-9- ._:)($\[\]!~@,-]{1,})[\-]{3}$', entry)
        return matched is not None

#################

FORMAT_TYPE = Utils.enum(HEADER = 0, SUB_HEADER = 1, PARAGRAPH = 2, UNKNOWN = 3)
LINK_TYPE   = Utils.enum(IMAGE  = 0, YOUTUBE    = 1, LINK = 2, UNKNOWN = 3)

class Render:
    def __init__(self, markdown_source):
        self.markdown_source = markdown_source
        self.configuration = Utils.load_configuration()

    def scan_source(self, source):
        markdown_data = []
        with open(source) as stream:
            for line in stream:
                markdown_data.append((Render.check_entry_type(line), line))
                print line
        print markdown_data

    def scan_entry(self, entry):
        match = Render.match_links(entry)
        if match is not None:
            Render.check_match_type(match)
        return None

    @staticmethod
    def match_links(line):
        matched = match('\[([a-zA-Z]*)\]\((https?:\/\/[a-zA-Z-0-9-.-\/$?&=%$]*)\)', line)
        return matched

    @staticmethod
    def check_entry_type(entry):
        if Utils.is_header(entry) is True:
            return FORMAT_TYPE.HEADER
        elif Utils.is_sub_header(entry) is True:
            return FORMAT_TYPE.SUB_HEADER
        elif Utils.is_paragraph(entry) is True:
            return FORMAT_TYPE.PARAGRAPH
        else:
            return FORMAT_TYPE.UNKNOWN
    
    @staticmethod
    def check_match_type(match):
        if Utils.is_image(match.group(2)) is True:
            return LINK_TYPE.IMAGE
        elif Utils.is_youtube(match.group(2)) is True:
            return LINK_TYPE.YOUTUBE
        else:
            return LINK_TYPE.LINK


    @staticmethod
    def generate_html(entry_type):
        pass

