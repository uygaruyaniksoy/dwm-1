""" Main class for DWM """

from .cleaning import DataLookup
from .cleaning import RegexLookup
from .cleaning import IncludesLookup

from .wrappers import DeriveDataLookupAll


##########################################################################
# Constants
##########################################################################

LOOKUP_TYPES = ['genericLookup', 'genericRegex', 'fieldSpecificRegex',
                'fieldSpecificLookup', 'normLookup', 'normRegex',
                'normIncludes']

DERIVE_TYPES = ['deriveValue', 'copyValue', 'deriveRegex', 'deriveIncludes']

DERIVE_OPTIONS = ['overwrite', 'blankIfNoMatch']

UDF_POSITIONS = ['beforeGenericValLookup', 'beforeGenericValRegex',
                 'beforeFieldSpecificLookup', 'beforeFieldSpecificRegex',
                 'beforeNormLookup', 'beforeNormRegex',
                 'beforeNormIncludes', 'beforeDerive', 'afterAll']

##########################################################################
# DWM
##########################################################################


class Dwm(object):
    """ class for DWM config """

    def __init__(self, name, mongo, fields=None, udfs=None):
        """
        Set configuration for DWM runtime

        :param str name: Name of configuration; for logging
        :param MongoClient mongo: MongoDB connection
        :param list fields: list of field configurations (dict)
        :param dict udfs: dict of udfs to run
        """

        if fields is None:
            fields = []

        if udfs is None:
            udfs = {}

        # validate input values
        for field in fields:
            # lookup values
            for lookup in fields[field]['lookup']:
                if lookup not in LOOKUP_TYPES:
                    raise ValueError('Invalid lookup type %s' % lookup)

            # derive types and options
            for derive in fields[field]['derive']:
                if derive['type'] not in DERIVE_TYPES:
                    raise ValueError('Invalid derive type %s' % derive['type'])

                for opt in derive['options']:
                    if opt not in DERIVE_OPTIONS:
                        raise ValueError('Invalid derive option %s' % opt)

        for udf in udfs:
            if udf not in UDF_POSITIONS:
                raise ValueError('Invalid UDF position %s' % udf)

        self.name = name
        self.mongo = mongo
        self.fields = fields
        self.udfs = udfs

    @staticmethod
    def data_lookup_method(fields_list, mongo_db_obj, hist, record,
                           lookup_type):
        """

        :param fields_list:
        :param mongo_db_obj:
        :param hist:
        :param record:
        :param lookup_type:
        """

        if hist is None:
            hist = {}

        for field in record:

            if record[field] != '' and record[field] is not None:

                if field in fields_list:

                    if lookup_type in fields_list[field]['lookup']:

                        field_val_new, hist = DataLookup(
                            fieldVal=record[field],
                            db=mongo_db_obj,
                            lookupType=lookup_type,
                            fieldName=field,
                            histObj=hist)

                        record[field] = field_val_new

        return record, hist

    @staticmethod
    def data_regex_method(fields_list, mongo_db_obj, hist, record, lookup_type):
        """

        :param fields_list:
        :param mongo_db_obj:
        :param hist:
        :param record:
        :param lookup_type:
        """

        if hist is None:
            hist = {}

        for field in record:

            if record[field] != '' and record[field] is not None:

                if field in fields_list:

                    if lookup_type in fields_list[field]['lookup']:

                        field_val_new, hist = RegexLookup(
                            fieldVal=record[field],
                            db=mongo_db_obj,
                            fieldName=field,
                            lookupType=lookup_type,
                            histObj=hist)

                        record[field] = field_val_new

        return record, hist

    def _val_g_lookup(self, record, hist=None):
        """
        Perform generic validation lookup

        :param dict record: dictionary of values to validate
        :param dict hist: existing input of history values
        """

        record, hist = self.data_lookup_method(fields_list=self.fields,
                                               mongo_db_obj=self.mongo,
                                               hist=hist,
                                               record=record,
                                               lookup_type='genericLookup')
        return record, hist

    def _val_g_regex(self, record, hist=None):
        """
        Perform generic validation regex

        :param dict record: dictionary of values to validate
        :param dict hist: existing input of history values
        """

        record, hist = self.data_regex_method(fields_list=self.fields,
                                              mongo_db_obj=self.mongo,
                                              hist=hist,
                                              record=record,
                                              lookup_type='genericRegex')
        return record, hist

    def _val_fs_lookup(self, record, hist=None):
        """
        Perform field-specific validation lookup

        :param dict record: dictionary of values to validate
        :param dict hist: existing input of history values
        """

        record, hist = self.data_lookup_method(fields_list=self.fields,
                                               mongo_db_obj=self.mongo,
                                               hist=hist,
                                               record=record,
                                               lookup_type=
                                               'fieldSpecificLookup')

        return record, hist

    def _val_fs_regex(self, record, hist=None):
        """
        Perform field-specific validation regex

        :param dict record: dictionary of values to validate
        :param dict hist: existing input of history values
        """

        record, hist = self.data_regex_method(fields_list=self.fields,
                                              mongo_db_obj=self.mongo,
                                              hist=hist,
                                              record=record,
                                              lookup_type='fieldSpecificRegex')
        return record, hist

    def _norm_lookup(self, record, hist=None):
        """
        Perform generic validation lookup

        :param dict record: dictionary of values to validate
        :param dict hist: existing input of history values
        """

        record, hist = self.data_lookup_method(fields_list=self.fields,
                                               mongo_db_obj=self.mongo,
                                               hist=hist,
                                               record=record,
                                               lookup_type='normLookup')
        return record, hist
