# pylint: disable=I0011,R0903
"""
Module name: timeunits

Calculate and return a value of one time unit converted from another time unit.

Example:
    TimeUnit(1, 'min', 'sec').doconvert()
    returns: 60.0

Exportables:
    Classes:
        TimeUnit
            Functions:
                doconvert: Return calculated conversion between two units
"""


class TimeUnit(object):
    """
    Initialize a TimeUnit to return the results of doconvert(), for the
    purpose of converting one time unit to another time unit

    :param amt: float, amount to convert from
    :param ufrom: string, unit to convert from
    :param uto: string, unit to convert to
    """
    def __init__(self, amt, ufrom, uto):
        self.time_base = 1.0  # minutes in a minute
        self.amt = amt
        self.ufrom = ufrom
        self.uto = uto

    def _getuval(self, argument):
        """Return a function to calculate the unit's value"""
        function = '_unit_{0}'.format(str(argument))
        function = getattr(self, function)
        return function()

    def doconvert(self):
        """
        Return calculated conversion between two units

        :returns: string containing original unit and value with converted
        unit and value
        :raises ValueError: if the amount (amt) is less than 0
        """
        if self.amt < 0:
            raise ValueError('Amount must be a positive number')
        conv = (self.amt * self._getuval(self.ufrom)) / self._getuval(self.uto)
        return conv

    def _unit_ms(self):
        """Return the value of one Millisecond (ms)
        based on a base time value"""
        return (self.time_base / 1000.0) / 60.0

    def _unit_sec(self):
        """Return the value of one Second (sec)
        based on a base time value"""
        return self.time_base / 60.0

    def _unit_min(self):
        """Return the value of one Minute (min)
        based on a base time value"""
        return self.time_base

    def _unit_hr(self):
        """Return the value of one Hour (hr)
        based on a base time value"""
        return self.time_base * 60.0

    def _unit_day(self):
        """Return the value of one Day (day)
        based on a base time value"""
        return (self.time_base * 60.0) * 24.0

    def _unit_wk(self):
        """Return the value of one Week (wk)
        based on a base time value"""
        return ((self.time_base * 60.0) * 24.0) * 7

    def _unit_mo(self):
        """Return the value of one Month (mo)
        based on a base time value"""
        return (((self.time_base * 60.0) * 24.0) * 365.0) / 12

    def _unit_yr(self):
        """Return the value of one Year (yr)
        based on a base time value"""
        return ((self.time_base * 60.0) * 24.0) * 365.0
