.. _isotherms-manual:

The Isotherm classes
====================

.. _isotherms-manual-general:

Overview
--------

In pyGAPS, an isotherm can be represented in two ways: as a
:meth:`~pygaps.classes.pointisotherm.PointIsotherm` object or as a
:meth:`~pygaps.classes.modelisotherm.ModelIsotherm` object.
These two classes have many common methods and attributes, but they
differ in the way they hold the relationship between pressure and loading:

    - The PointIsotherm class is a collection of discrete points,
      stored in a pandas.DataFrame object. It can contain both an
      adsorption and desorption branch, which are determined automatically
      at instantiation.
    - The ModelIsotherm class is a collection of parameters which are used
      to describe a model of adsorption behaviour. It can only model a single
      branch of the data, either adsorption or desorption.

Both classes are derived from the :meth:`~pygaps.classes.isotherm.Isotherm` class.
This class holds all descriptions of the experiment, such as the adsorbate used, the material
name and the temperature at which the isotherm was taken. These parameters are inherited
in the two child isotherm objects, therefore, the user should not have to use this class
directly.


To work with pyGAPS isotherms check out the following topics:

    - :ref:`Creating an isotherm <isotherms-manual-create>`
    - :ref:`Accessing isotherm data <isotherms-manual-data>`
    - :ref:`Converting isotherm units, modes and basis <isotherms-manual-convert>`
    - :ref:`Ensuring isotherm uniqueness <isotherms-manual-unique>`
    - :ref:`Exporting an isotherm <isotherms-manual-export>`

.. _isotherms-manual-create:

Creating an isotherm
--------------------

There are several ways to create a PointIsotherm object:

    - Raw construction, from a dictionary with parameters and a pandas.DataFrame. This is the
      most extensible way to create a PointIsotherm, as parameters can be manually specified.
    - A json string or file. This can be done either using the
      :meth:`~pygaps.parsing.jsoninterface.isotherm_from_json`
      function, or with the :meth:`~pygaps.classes.pointisotherm.PointIsotherm.from_json`
      class method, which is just a wrapper around the other for convenience.
    - Parsing an excel file of a standard format. See :ref:`parsing from excel <parsing-manual-excel>`.
    - Parsing a csv file of a standard format. :ref:`See parsing from csv <parsing-manual-csv>`.
    - From an sqlite database: pyGAPS contains functionality to store and retrieve constructed
      isotherms in a sqlite database. See :ref:`database <parsing-manual-sqlite>`.

If using raw data, two components of the isotherm should be created first:
a dictionary with the parameters and a DataFrame with the data.

The pandas DataFrame which contains the data should have at least two columns: the pressures
at which each point was recorded, and the loadings for each point. Other data columns, such
as calorimetry data, magnetic field strengths, or other simultaneous measurements are also
supported.

::

    isotherm_data = pandas.DataFrame({
        'pressure' : [1, 2, 3, 4, 5, 3, 2],
        'loading' : [1, 2, 3, 4, 5, 3, 2],
        'enthalpy' : [15, 15, 15, 15, 15, 15, 15],
    })

.. caution::

    The data in the columns is assumed to be free of errors and anomalies. Negative
    pressures or loadings, noisy signals or erroneous points may give undefined
    behaviour.

The isotherm parameters dictionary has to have at least four specific components: the sample
name (``sample_name``), the sample batch(``sample_batch``), the adsorbate used (``adsorbate``) and
the temperature, in K at which the data was recorded (``t_exp``).

Other user parameters can be passed as well, and will be stored in the isotherm object. Some
are named, and can be accessed directly, such as sample activation temperature (``t_act``),
the person who measured the isotherm (``user``) and the machine on which the isotherm was
recorded (``machine``). Unknown parameters which are in the parameters dictionary are also stored,
in an internal dictionary called ``isotherm_parameters``. For a complete list of named internal parameters, see
:class:`~pygaps.classes.isotherm.Isotherm` reference, the :class:`~pygaps.classes.pointisotherm.PointIsotherm` reference
and the :class:`~pygaps.classes.modelisotherm.ModelIsotherm` reference.

An example parameters dictionary
::

    isotherm_parameters = {
        'sample_name' : 'carbon',       # Required
        'sample_batch' : 'X1',          # Required
        'adsorbate' : 'nitrogen',       # Required
        't_exp' : 77,                   # Required
        't_act' : 150,                  # Recognised / named
        'user'  : 'John',               # Recognised / named
        'DOI'   : '10.000/mydoi',       # Unknown / user specific
        'something' : 'something',      # Unknown / user specific
    }


With these two components, the PointIsotherm can be created. This is done by passing the two
components previously created, as well as a few required or optional parameters.

    - The ``loading_key`` and ``pressure_key`` are required parameters which specify which
      column in the DataFrame contain which data of the isotherm. If other columns are to be
      stored in the isotherm object, put their names in a list and pass it as the ``other_keys``
      parameter
    - The unit parameters ``unit_loading`` and ``unit_pressure`` are optional and specify
      the unit the isotherm is created in. By default, the loading is read in *mmmol* and the
      pressure is read in *bar*.
    - The optional ``mode_pressure`` parameter specifies if the pressure is relative or absolute
    - The optional ``basis_adsorbent`` parameter specifies if the loading is measured per mass or per
      volume of adsorbent material.

These parameters can also be included in the ``isotherm_parameters`` dictionary.

The code then becomes:

::

    point_isotherm = pygaps.PointIsotherm(
        isotherm_data,
        loading_key='loading',
        pressure_key='pressure',
        other_keys=['enthalpy'],
        unit_loading='mmol',
        unit_pressure='bar',
        mode_pressure='absolute',
        basis_adsorbent='mass',
        **isotherm_parameters
    )


ModelIsotherm creation from raw data is very similar to the PointIsotherm creation.
The same data and dictionary can be used, but with a couple of extra parameters:

    - The ``model`` parameter specifies which model to use to attempt to fit the data
    - The ``param_guess`` specifies the initial model parameter guesses where optimisation should
      start. It is optional, and will be automatically filled unless the user specifies it.
    - The ``optimization_method`` parameter tells scipy.optimise which optimisation method to use.
      If blank, will default to "Nelder-Mead"

.. note::

    The ModelIsotherm cannot be used to model tertiary data. Therefore, only loading and pressure
    can be used internally. Any other columns in the DataFrame will be ignored.

The code to generate a ModelIsotherm is then:

::

    model_isotherm = pygaps.ModelIsotherm(
            isotherm_data,
            loading_key='loading',
            pressure_key='pressure',
            model='Henry',
            unit_loading='mmol',
            unit_pressure='bar',
            mode_pressure='absolute',
            basis_adsorbent='mass',
            **isotherm_parameters
        )

ModelIsotherms can also be constructed from PointIsotherms and vice-versa. The model can also be
guessed automatically. For more info on isotherm modelling read the :ref:`section <modelling-manual>` of
the manual.

A detailed explanation of each isotherm methods is written in the docstrings and can be accessed in the
:ref:`reference <isotherms-ref>`. Only a general overview will be given here.




.. _isotherms-manual-data:

Accessing isotherm data
-----------------------

Once an isotherm is created, the first thing most users will want would be to see is a visual representation of the isotherm.
The isotherm classes contain a useful ``print_info`` function which will display the isotherm parameters, as well as a graph
of the data.

    - PointIsotherm :meth:`~pygaps.classes.pointisotherm.PointIsotherm.print_info`
    - ModelIsotherm :meth:`~pygaps.classes.modelisotherm.ModelIsotherm.print_info`

To access isotherm data, one of several functions can be used. There are individual methods for each data type:
``pressure``, ``loading`` and ``other_data``. The first two are applicable to both PointIsotherms and ModelIsotherms.
While PointIsotherms return the actual discrete data, ModelIsotherms use the internal model to generate data with the
characteristics required.

    - For loading: PointIsotherm :meth:`~pygaps.classes.pointisotherm.PointIsotherm.loading`
      and ModelIsotherm :meth:`~pygaps.classes.modelisotherm.ModelIsotherm.loading`

    - For pressure: PointIsotherm :meth:`~pygaps.classes.pointisotherm.PointIsotherm.pressure`
      and ModelIsotherm :meth:`~pygaps.classes.modelisotherm.ModelIsotherm.pressure`

    - For other data columns: PointIsotherm :meth:`~pygaps.classes.pointisotherm.PointIsotherm.other_data`

All data-specific functions can return either a pandas.Series object, or a numpy array, depending on the
parameters passed to it. Other optional parameters can specify the unit, the mode/basis, the branch the
data is returned in as well as a particular range the data should be selected in. For example:

::

    # Will return the loading points of the adsorption part of the
    # isotherm in the range if 0.5-0.9 cm3 STP
    isotherm.loading(
        branch='ads',
        loading_unit='cm3 STP',
        min_range = 0.5,
        max_range = 0.9,
    )

The ``other_data`` function is built for accessing user-specific data stored in the isotherm object. Its use is
similar to the loading and pressure functions, but the column of the DataFrame where the data is held should
be specified in the function call as the ``key`` parameter. It is only applicable to the PointIsotherm object.

For the PointIsotherm, a special :meth:`~pygaps.classes.pointisotherm.PointIsotherm.data` function returns all or a
branch of the internal pandas.DataFrame. This is generally not very useful for quick processing, and also non-applicable
to the ModelIsotherm object but can be used to inspect the data directly or obtain the initial DataFrame that was used
to construct it.

Besides functions which give access to the internal datapoints, the isotherm object can also return
the value of pressure and loading at any point specified by the user.
To differentiate them from the functions returning internal data, the functions have 'at' in their name.

In the ModelIsotherm class, the internal model is used to calculate the data required.
In the PointIsotherm class, the functions rely on an internal interpolator, which uses the scipy.interpolate
module. To optimize performance working with isotherms, the interpolator is constructed only
on the units the isotherm is in. If the user requests the return values in a different type than the
interpolator, they will be converted. Conversion is slower than directly using the interpolator, therefore,
if a large number of requests are to be made, it is better to use the isotherm conversion function

    - For loading: PointIsotherm :meth:`~pygaps.classes.pointisotherm.PointIsotherm.loading_at`
      and ModelIsotherm :meth:`~pygaps.classes.modelisotherm.ModelIsotherm.loading_at`

    - For pressure: PointIsotherm :meth:`~pygaps.classes.pointisotherm.PointIsotherm.pressure_at`
      and ModelIsotherm :meth:`~pygaps.classes.modelisotherm.ModelIsotherm.pressure_at`

The methods take parameters that describe the unit/mode of both the input parameters and the output parameters.

::

    isotherm.loading_at(
        1,
        pressure_unit = 'atm',      # the pressure is passed in atmospheres (= 1 atm)
        branch='des',               # use the desorption branch of the isotherm
        loading_unit='mol',         # return the loading in mol/basis
        adsorbent_mode='mass',      # return the loading in unit/mass
    )


.. caution::

    Interpolation can be dangerous. pyGAPS does not implicitly allow interpolation outside the bounds of the
    data, although the user can force it to by passing an ``interp_fill`` parameter to the interpolating
    functions, usually if the isotherm is known to have reached the maximum adsorption plateau. Otherwise,
    the user is responsible for making sure the data is fit for purpose.



.. _isotherms-manual-convert:

Converting isotherm units, modes and basis
------------------------------------------

The PointIsotherm class also includes methods which can be used to convert the internal data permanently
to a new state. This is useful in certain cases, like when you want to export the isotherm in a converted
excel or json form.
If what is desired is instead a set of data in a particular format, it is easier to get it directly via the data access
functions :ref:`above <isotherms-manual-data>`. The conversion functions are:

    - :meth:`~pygaps.classes.pointisotherm.PointIsotherm.convert_unit_loading`
      will permanently convert the unit of the
      loading of the isotherm, for example from the *mmol* to *cm3 STP*
    - :meth:`~pygaps.classes.pointisotherm.PointIsotherm.convert_unit_pressure`
      will permanently convert the unit of
      pressure, for example from *bar* to *atm*
    - :meth:`~pygaps.classes.pointisotherm.PointIsotherm.convert_mode_pressure`
      will permanently convert the pressure
      from a relative to an absolute mode or vice-versa
    - :meth:`~pygaps.classes.pointisotherm.PointIsotherm.convert_basis_adsorbent`
      will permanently convert the adsorbent
      basis, for example from a mass basis to a volume basis

In order for pyGAPS to correctly convert between pressure modes and adsorbent basis, the user might have to
take some extra steps.

To convert an absolute pressure in a relative pressure, the critical pressure of the gas at the experiment
temperature must be known. Of course this conversion only works when the isotherm is not measured in a
supercritical regime. To do the conversion, pyGAPS relies on the CoolProp library. Therefore, the name
of the gas must be somehow passed to the CoolProp backend. pyGAPS does this by having an internal list
of adsorbates, which is loaded from the database at the moment of import. The logical steps follows are:

    - User requests conversion from absolute to relative pressure for an isotherm object
    - The adsorbate name is taken from the isotherm parameter and matched against the name of an
      adsorbate in the internal list
    - If the adsorbate is found, the name of the CoolProp name of the adsorbate is retrieved
    - CoolProp calculates the critical point pressure for the adsorbate
    - The relative pressure is calculated by dividing by the critical point pressure

If using common gasses, the user should not be worried about this process, as the list of adsorbates is
stored in the internal database. However, if a new adsorbate is to be used, the user should add it to the
master list themselves. For more info on this see the :ref:`Adsorbate class manual <adsorbate-manual>`

For adsorbent basis conversions, the density of the adsorbent should be known. The way the density is retrieved
is very similar to property retrieval from the adsorbates. A list of Samples is kept by pyGAPS,
loaded at import-time from the database. The user must create a Sample instance, populate it with the density
parameter and then upload it either to the internal list or the internal database. For more info on this
see the :ref:`Sample class manual <sample-manual>`

.. note::

    The ModelIsotherm model parameters cannot be converted permanently to new states (although the data
    can still be obtained in that state by using the data functions). For fast calculations, it is better to first
    convert the data in the format required, then generate the ModelIsotherm.



.. _isotherms-manual-unique:

Ensuring isotherm uniqueness
----------------------------

After its construction, each PointIsotherm generates an id. This id is supposed to be a fingerprint of the
isotherm and should be unique to each object. The id string is actually an md5 hash of the isotherm
parameters and data. The id can then be used, both internally for database storage or for identification
purposes.

Internal logic is as follows:

    - After isotherm instantiation, the isotherm object calls the json converter and obtains a string
      of itself in json format
    - The hashlib.md5 function is used to obtain a hash of the json string
    - The hash is saved in the internal id parameter and the instantiation is complete

Any internal change in the isotherm, such as changing the sample activation temperature, adding a new
member in the data dictionary or converting/deleting the isotherm datapoints will lead to the id to
be regenerated from the new data. This should be taken into account if writing a function that would
modify a large number of isotherms or if repeatedly modifying each isotherm.

It can be read directly from the isotherm using the following code but should never be directly modified.

::

    point_isotherm.id

.. note::

    The ModelIsotherm class does not currently contain an ID. Therefore it cannot be checked for uniqueness.


.. _isotherms-manual-export:

Exporting an isotherm
---------------------

To export an isotherm, pyGAPS provides several choices to the user:

    - Converting the isotherm in a JSON format, using the :meth:`~pygaps.parsing.jsoninterface.isotherm_to_json` function
    - Converting the isotherm to a CSV file, using the :meth:`~pygaps.parsing.csvinterface.isotherm_to_csv` function
    - Converting the isotherm to an Excel file, using the :meth:`~pygaps.parsing.excelinterface.isotherm_to_excel` function
      (of course only valid if Excel is installed on the system)
    - Uploading the isotherm to a sqlite database, either using the internal database or
      a user-specified external one. For more info on interacting with the sqlite database
      see the respective :ref:`section<sqlite-manual>` of the manual.

More info can be found on the respective parsing page of the manual.
