import re

import numpy as np

from .las_items import (
    HeaderItem, SectionItems, OrderedDict
)


def get_default_items():
    return {
        'Version': SectionItems([
            HeaderItem('VERS', '', 2.0, 'CWLS log ASCII Standard -VERSION 2.0'),
            HeaderItem('WRAP', '', 'NO', 'One line per depth step'),
            HeaderItem('DLM', '', 'SPACE', 'Column Data Section Delimiter'),
        ]),
        'Well': SectionItems([
            HeaderItem('STRT', 'm', np.nan, 'START DEPTH'),
            HeaderItem('STOP', 'm', np.nan, 'STOP DEPTH'),
            HeaderItem('STEP', 'm', np.nan, 'STEP'),
            HeaderItem('NULL', '', -9999.25, 'NULL VALUE'),
            HeaderItem('COMP', '', '', 'COMPANY'),
            HeaderItem('WELL', '', '', 'WELL'),
            HeaderItem('FLD', '', '', 'FIELD'),
            HeaderItem('LOC', '', '', 'LOCATION'),
            HeaderItem('PROV', '', '', 'PROVINCE'),
            HeaderItem('CNTY', '', '', 'COUNTY'),
            HeaderItem('STAT', '', '', 'STATE'),
            HeaderItem('CTRY', '', '', 'COUNTRY'),
            HeaderItem('SRVC', '', '', 'SERVICE COMPANY'),
            HeaderItem('DATE', '', '', 'DATE'),
            HeaderItem('UWI', '', '', 'UNIQUE WELL ID'),
            HeaderItem('API', '', '', 'API NUMBER')
        ]),
        'Curves': SectionItems([]),
        'Parameter': SectionItems([]),
        'Other': '',
        'Data': np.zeros(shape=(0, 1)),
    }


ORDER_DEFINITIONS = {
    1.2: OrderedDict([
        ('Version', ['value:descr']),
        ('Well', [
            'descr:value',
            ('value:descr', ['STRT', 'STOP', 'STEP', 'NULL'])]),
        ('Curves', ['value:descr']),
        ('Parameter', ['value:descr']),
    ]),
    2.0: OrderedDict([
        ('Version', ['value:descr']),
        ('Well', ['value:descr']),
        ('Curves', ['value:descr']),
        ('Parameter', ['value:descr'])
    ])}

DEPTH_UNITS = {
    'FT': ("FT", "F", "FEET", "FOOT"),
    'M': ("M", "METER", "METERS", "METRE", "METRES"),
    }

SUB_PATTERNS = [
    (re.compile(r'(\d)-(\d)'), r'\1 -\2'),
    (re.compile('-?\d*\.\d*\.\d*'), ' NaN NaN '),
    (re.compile('NaN.\d*'), ' NaN NaN '),
    ]