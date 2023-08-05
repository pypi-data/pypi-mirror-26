"""Module containing the conversions between different units used"""

from .exceptions import ParameterError

_LOADING_UNITS = {
    "mol": 1,
    "mmol": 0.001,
    "kmol": 1000,
    "cm3 STP": 4.461e-5,
    "cm3(STP)": 4.461e-5,
    "ml": 4.461e-5,
}
_MASS_UNITS = {
    'mg': 0.001,
    'g': 1,
    'kg': 1000,
}
_VOLUME_UNITS = {
    'cm3': 1,
    'ml': 1,
    'dm3': 1e3,
    'l': 1e3,
    'm3': 1e6,
}
_PRESSURE_UNITS = {
    "bar": 100000,
    "Pa": 1,
    "atm": 101325,
    "mmHg": 133.322
}


def convert_pressure(pressure, unit_from, unit_to):
    """
    Converts the pressure values from one unit to another

    Parameters
    ----------
    unit_to : str
        the unit into which the data will be converted into
    """

    if unit_to not in _PRESSURE_UNITS or unit_from not in _PRESSURE_UNITS:
        raise ParameterError(
            "Units selected for pressure are not an option. Viable"
            "units are {}".format(_PRESSURE_UNITS.keys()))

    pressure = pressure * \
        _PRESSURE_UNITS[unit_from] / _PRESSURE_UNITS[unit_to]

    return pressure


def convert_loading(loading, unit_from, unit_to):
    """
    Converts the loading from one unit to another
    """

    if unit_to not in _LOADING_UNITS or unit_from not in _LOADING_UNITS:
        raise ParameterError(
            "Units selected for loading are not an option. Viable"
            " units are {}".format(_LOADING_UNITS.keys()))

    loading = loading * \
        _LOADING_UNITS[unit_from] / _LOADING_UNITS[unit_to]

    return loading
