from .base import Descriptor

__all__ = ['AcceptDatetimeFormat', 'AccountUnits', 'Currency', 'DateTime', 'DecimalNumber',
           'Unit', 'Direction',
           'InstrumentName', 'InstrumentType']


class AcceptDatetimeFormat(Descriptor):
    """DateTime header
    """

    # Type checking
    typ = str

    # Valid values
    values = {
        'UNIX': 'If “UNIX” is specified DateTime fields will be specified or '
                'returned in the “12345678.000000123” format.',
        'RFC3339': 'If “RFC3339” is specified DateTime will be specified or '
                   'returned in “YYYY-MM-DDTHH:MM:SS.nnnnnnnnnZ” format.'
    }


class AccountUnits(Descriptor):
    """The string representation of a quantity of an Account’s home currency.
    """

    # Type checking
    # TODO keep an eye on this. OANDA specifies this as a str.
    # Though it makes more sense for it to be a float
    # floats automatically get converted to to strings anyway
    # when serialized into JSON
    typ = float

    # Correct syntax of value
    format_syntax = 'A decimal number encoded as a string. The amount of precision ' \
                    'provided depends on the Account’s home currency.'


class Currency(Descriptor):
    """Currency name identifier. Used by clients to refer to currencies.
    """

    # Type checking
    typ = str

    # Correct syntax of value
    format_syntax = 'A string containing an ISO 4217 currency'


class DateTime(Descriptor):
    """A date and time value using either RFC3339 or UNIX time representation.
    """

    # Type checking
    typ = str

    # Correct syntax of value
    format_syntax = 'The RFC 3339 representation is a string conforming to'


class DecimalNumber(Descriptor):
    """The string representation of a decimal number.
    """

    # Type checking
    typ = float

    # Correct syntax of value
    format_syntax = 'A decimal number encoded as a string. The amount of precision ' \
                    'provided depends on what the number represents.'

    def __set__(self, instance, value):
        value = super().type_check(value)
        super().__set__(instance, round(value, 5))

class Unit(Descriptor):
    """A unit is a standard allotment of a currency
    """

    # Type checking
    typ = float

    # Correct syntax of value
    format_syntax = 'A decimal number encoded as a string. The amount of precision ' \
                    'provided depends on what the number represents.'

    def __set__(self, instance, value):
        value = super().type_check(value)
        super().__set__(instance, round(value, 0))


class Direction(Descriptor):
    """In the context of an Order or a
    Trade, defines whether the units are positive or negative.
    """

    # Type checking
    typ = str

    # Valid values
    values = {
        'LONG': 'A long Order is used to to buy units of an Instrument. '
                'A Trade is long when it has bought units of an Instrument.',
        'SHORT': 'A short Order is used to to sell units of an Instrument.'
                 'A Trade is short when it has sold units of an Instrument.'
    }


class InstrumentName(Descriptor):
    """Instrument name identifier. Used by clients to refer to an Instrument.
    """

    # Type checking
    typ = str

    # Correct syntax of value
    format_syntax = 'A string containing the base currency and quote currency delimited by a “_”.'


class InstrumentType(Descriptor):
    """The type of an Instrument.
    """

    # Type checking
    typ = str

    # Valid values
    values = {
        'CURRENCY': 'Currency',
        'CFD': 'Contract For Difference',
        'METAL': 'Metal'
    }
