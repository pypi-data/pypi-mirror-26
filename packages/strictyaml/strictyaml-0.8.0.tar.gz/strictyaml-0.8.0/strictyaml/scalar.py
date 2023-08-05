from ruamel.yaml.comments import CommentedSeq, CommentedMap
from strictyaml.exceptions import raise_exception
from strictyaml.validators import Validator
from strictyaml import constants
from strictyaml import utils
import dateutil.parser
import decimal
import sys
import re


if sys.version_info[0] == 3:
    unicode = str


class Scalar(Validator):
    @property
    def rule_description(self):
        return "a {0}".format(self.__class__.__name__.lower())

    def validate(self, chunk):
        val = chunk.contents

        if type(val) == CommentedSeq or type(val) == CommentedMap:
            raise_exception(
                "when expecting a {0}".format(self.__class__.__name__.lower()),
                "found mapping/sequence",
                chunk,
            )
        else:
            return self.validate_scalar(chunk)


class Enum(Scalar):
    def __init__(self, restricted_to, item_validator=None):
        self._item_validator = Str() if item_validator is None else item_validator
        assert isinstance(self._item_validator, Scalar)
        self._restricted_to = restricted_to

    def validate_scalar(self, chunk):
        val = self._item_validator(chunk)
        if val._value not in self._restricted_to:
            raise_exception(
                "when expecting one of: {0}".format(", ".join(self._restricted_to)),
                "found '{0}'".format(val),
                chunk,
            )
        else:
            return val

    def __repr__(self):
        return u"Enum({0})".format(repr(self._restricted_to))


class CommaSeparated(Scalar):
    def __init__(self, item_validator):
        self._item_validator = item_validator

    def validate_scalar(self, chunk):
        return [
            self._item_validator.validate_scalar(chunk.textslice(positions[0], positions[1]))
            for positions in utils.comma_separated_positions(chunk.contents)
        ]

    def __repr__(self):
        return "CommaSeparated({0})".format(self._item_validator)


class Regex(Scalar):
    def __init__(self, regular_expression):
        """
        Give regular expression, e.g. u'[0-9]'
        """
        self._regex = regular_expression
        self._matching_message = "when expecting string matching {0}".format(self._regex)

    def validate_scalar(self, chunk):
        if re.compile(self._regex).match(chunk.contents) is None:
            raise_exception(
                self._matching_message,
                "found non-matching string",
                chunk,
            )
        return chunk.contents


class Email(Regex):
    def __init__(self):
        self._regex = constants.REGEXES['email']
        self._matching_message = "when expecting an email address"


class Url(Regex):
    def __init__(self):
        self._regex = constants.REGEXES['url']
        self._matching_message = "when expecting a url"


class Str(Scalar):
    def validate_scalar(self, chunk):
        return chunk.contents

    def __repr__(self):
        return u"Str()"


class Int(Scalar):
    def validate_scalar(self, chunk):
        val = chunk.contents
        if not utils.is_integer(val):
            raise_exception(
                "when expecting an integer",
                "found non-integer",
                chunk,
            )
        else:
            return int(val)

    def __repr__(self):
        return u"Int()"


class Bool(Scalar):
    def validate_scalar(self, chunk):
        val = chunk.contents
        if unicode(val).lower() not in constants.BOOL_VALUES:
            raise_exception(
                """when expecting a boolean value (one of "{0}")""".format(
                    '", "'.join(constants.BOOL_VALUES)
                ),
                "found non-boolean",
                chunk,
            )
        else:
            if val.lower() in constants.TRUE_VALUES:
                return True
            else:
                return False

    def __repr__(self):
        return u"Bool()"


class Float(Scalar):
    def validate_scalar(self, chunk):
        val = chunk.contents
        if not utils.is_decimal(val):
            raise_exception(
                "when expecting a float",
                "found non-float",
                chunk,
            )
        else:
            return float(val)

    def __repr__(self):
        return u"Float()"


class Decimal(Scalar):
    def validate_scalar(self, chunk):
        val = chunk.contents
        if not utils.is_decimal(val):
            raise_exception(
                "when expecting a decimal",
                "found non-decimal",
                chunk,
            )
        else:
            return decimal.Decimal(val)

    def __repr__(self):
        return u"Decimal()"


class Datetime(Scalar):
    def validate_scalar(self, chunk):
        try:
            return dateutil.parser.parse(chunk.contents)
        except ValueError:
            raise_exception(
                "when expecting a datetime",
                "found non-datetime",
                chunk,
            )

    def __repr__(self):
        return u"Datetime()"


class EmptyNone(Scalar):
    def validate_scalar(self, chunk):
        val = chunk.contents
        if val != "":
            raise_exception(
                "when expecting an empty value",
                "found non-empty value",
                chunk,
            )
        else:
            return self.empty(chunk)

    def empty(self, chunk):
        return None

    def __repr__(self):
        return u"EmptyNone()"


class EmptyDict(EmptyNone):
    def empty(self, chunk):
        return {}

    def __repr__(self):
        return u"EmptyDict()"


class EmptyList(EmptyNone):
    def empty(self, chunk):
        return []

    def __repr__(self):
        return u"EmptyList()"
