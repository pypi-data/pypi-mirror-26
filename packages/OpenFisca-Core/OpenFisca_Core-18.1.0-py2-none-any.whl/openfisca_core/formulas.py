# -*- coding: utf-8 -*-


from __future__ import division

import collections
import inspect
import datetime
import logging
import warnings
import re
from os import linesep

import numpy as np

from . import columns, holders, periods
from .parameters import ParameterNotFound
from .periods import MONTH, YEAR, ETERNITY
from .base_functions import (
    missing_value,
    permanent_default_value,
    requested_period_default_value,
    requested_period_last_or_next_value,
    requested_period_last_value,
    )
from .commons import empty_clone, stringify_array


log = logging.getLogger(__name__)


ADD = 'add'
DIVIDE = 'divide'

FORMULA_NAME_PREFIX = 'formula'
FORMULA_NAME_SEPARATOR = '_'
DEFAULT_YEAR = '0001'
DEFAULT_MONTH = '01'
DEFAULT_DAY = '01'

# Exceptions


class NaNCreationError(Exception):
    pass


class CycleError(Exception):
    pass

# Formulas


class Formula(object):
    """
    An OpenFisca Formula for a Variable.
    Such a Formula might have different behaviors according to the time period.
    """
    comments = None
    holder = None
    start_line_number = None
    source_code = None
    source_file_path = None
    base_function = None  # Class attribute. Overridden by subclasses
    dated_formulas = None  # A list of dictionaries containing a formula instance and a start instant
    dated_formulas_class = None  # A list of dictionaries containing a formula class and a start instant

    def __init__(self, holder = None):
        assert holder is not None
        self.holder = holder

        if self.dated_formulas_class is not None:
            self.dated_formulas = [
                dict(
                    formula = dated_formula_class['formula_class'](holder = holder),
                    start_instant = dated_formula_class['start_instant'],
                    )
                for dated_formula_class in self.dated_formulas_class
                ]

    def clone(self, holder, keys_to_skip = None):
        """Copy the formula just enough to be able to run a new simulation without modifying the original simulation."""
        new = empty_clone(self)
        new_dict = new.__dict__

        if keys_to_skip is None:
            keys_to_skip = set()
        keys_to_skip.add('dated_formulas')
        keys_to_skip.add('holder')

        for key, value in self.__dict__.iteritems():
            if key not in keys_to_skip:
                new_dict[key] = value
        new_dict['holder'] = holder

        if self.dated_formulas is not None:
            new.dated_formulas = [
                {
                    key: value.clone(holder) if key == 'formula' else value
                    for key, value in dated_formula.iteritems()
                    }
                for dated_formula in self.dated_formulas
                ]

        return new

    def calculate_output(self, period):
        return self.holder.compute(period).array

    def default_values(self):
        '''Return a new NumPy array which length is the entity count, filled with default values.'''
        return self.zeros() + self.holder.column.default

    @property
    def real_formula(self):
        return self

    def set_input(self, period, array):
        self.holder.put_in_cache(array, period)

    def zeros(self, **kwargs):
        '''
        Return a new NumPy array which length is the entity count, filled with zeros.

        kwargs are forwarded to np.zeros.
        '''
        return np.zeros(self.holder.entity.count, **kwargs)

    # Roles & Entities dispatch helpers

    def any_by_roles(self, array_or_dated_holder, entity = None, roles = None):
        holder = self.holder
        simulation = holder.simulation
        persons = simulation.persons
        if entity is None:
            entity = holder.entity
        else:
            assert entity in simulation.tax_benefit_system.entities, u"Unknown entity: {}".format(entity).encode('utf-8')

        assert not entity.is_person
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            assert array_or_dated_holder.entity.is_person
            array = array_or_dated_holder.array
        else:
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            persons_count = persons.count
            assert array.size == persons_count, u"Expected an array of size {}. Got: {}".format(persons_count,
                array.size)
        entity_index_array = simulation.get_entity(entity).members_entity_id

        if roles is None:
            roles = range(entity.roles_count)
        target_array = self.zeros(dtype = np.bool)
        for role in roles:
            # TODO Mettre les filtres en cache dans la simulation
            boolean_filter = simulation.get_entity(entity).members_legacy_role == role
            target_array[entity_index_array[boolean_filter]] += array[boolean_filter]
        return target_array

    def cast_from_entity_to_role(self, array_or_dated_holder, default = None, entity = None, role = None):
        """Cast an entity array to a persons array, setting only cells of persons having the given role."""
        assert isinstance(role, int)
        return self.cast_from_entity_to_roles(array_or_dated_holder, default = default, entity = entity, roles = [role])

    def cast_from_entity_to_roles(self, array_or_dated_holder, default = None, entity = None, roles = None):
        """Cast an entity array to a persons array, setting only cells of persons having one of the given roles.

        When no roles are given, it means "all the roles" => every cell is set.
        """
        holder = self.holder
        simulation = holder.simulation
        persons = simulation.persons
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            if entity is None:
                entity = array_or_dated_holder.entity
            else:
                assert entity in simulation.tax_benefit_system.entities, u"Unknown entity: {}".format(entity).encode('utf-8')

                assert entity == array_or_dated_holder.entity, \
                    u"""Holder entity "{}" and given entity "{}" don't match""".format(entity.key,
                        array_or_dated_holder.column.entity.key).encode('utf-8')
            array = array_or_dated_holder.array
            if default is None:
                default = array_or_dated_holder.column.default
        else:
            assert entity in simulation.tax_benefit_system.entities, u"Unknown entity: {}".format(entity).encode('utf-8')

            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            entity_count = entity.count
            assert array.size == entity_count, u"Expected an array of size {}. Got: {}".format(entity_count,
                array.size)
            if default is None:
                default = 0
        assert not entity.is_person
        persons_count = persons.count
        target_array = np.empty(persons_count, dtype = array.dtype)
        target_array.fill(default)
        entity_index_array = simulation.get_entity(entity).members_entity_id

        if roles is None:
            roles = range(entity.roles_count)
        for role in roles:
            boolean_filter = simulation.get_entity(entity).members_legacy_role == role
            try:
                target_array[boolean_filter] = array[entity_index_array[boolean_filter]]
            except:
                log.error(u'An error occurred while transforming array for role {}[{}] in function {}'.format(
                    entity.key, role, holder.column.name))
                raise
        return target_array

    def filter_role(self, array_or_dated_holder, default = None, entity = None, role = None):
        """Convert a persons array to an entity array, copying only cells of persons having the given role."""
        holder = self.holder
        simulation = holder.simulation
        persons = simulation.persons
        if entity is None:
            entity = holder.entity
        else:
            assert entity in simulation.tax_benefit_system.entities, u"Unknown entity: {}".format(entity).encode('utf-8')

        assert not entity.is_person
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            assert array_or_dated_holder.entity.is_person
            array = array_or_dated_holder.array
            if default is None:
                default = array_or_dated_holder.column.default
        else:
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            persons_count = persons.count
            assert array.size == persons_count, u"Expected an array of size {}. Got: {}".format(persons_count,
                array.size)
            if default is None:
                default = 0
        entity_index_array = simulation.get_entity(entity).members_entity_id

        assert isinstance(role, int)
        entity_count = entity.count
        target_array = np.empty(entity_count, dtype = array.dtype)
        target_array.fill(default)
        boolean_filter = simulation.get_entity(entity).members_legacy_role == role
        try:
            target_array[entity_index_array[boolean_filter]] = array[boolean_filter]
        except:
            log.error(u'An error occurred while filtering array for role {}[{}] in function {}'.format(
                entity.key, role, holder.column.name))
            raise
        return target_array

    def split_by_roles(self, array_or_dated_holder, default = None, entity = None, roles = None):
        """dispatch a persons array to several entity arrays (one for each role)."""
        holder = self.holder
        simulation = holder.simulation
        persons = simulation.persons
        if entity is None:
            entity = holder.entity
        else:
            assert entity in simulation.tax_benefit_system.entities, u"Unknown entity: {}".format(entity).encode('utf-8')

        assert not entity.is_person
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            assert array_or_dated_holder.entity.is_person
            array = array_or_dated_holder.array
            if default is None:
                default = array_or_dated_holder.column.default
        else:
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            persons_count = persons.count
            assert array.size == persons_count, u"Expected an array of size {}. Got: {}".format(persons_count,
                array.size)
            if default is None:
                default = 0
        entity_index_array = simulation.get_entity(entity).members_entity_id
        if roles is None:
            # To ensure that existing formulas don't fail, ensure there is always at least 11 roles.
            # roles = range(entity.roles_count)
            roles = range(max(entity.roles_count, 11))
        target_array_by_role = {}
        entity_count = entity.count
        for role in roles:
            target_array_by_role[role] = target_array = np.empty(entity_count, dtype = array.dtype)
            target_array.fill(default)

            boolean_filter = simulation.get_entity(entity).members_legacy_role == role
            try:
                target_array[entity_index_array[boolean_filter]] = array[boolean_filter]
            except:
                log.error(u'An error occurred while filtering array for role {}[{}] in function {}'.format(
                    entity.key, role, holder.column.name))
                raise
        return target_array_by_role

    def sum_by_entity(self, array_or_dated_holder, entity = None, roles = None):
        holder = self.holder
        simulation = holder.simulation
        persons = simulation.persons
        if entity is None:
            entity = holder.entity
        else:
            assert entity in simulation.tax_benefit_system.entities, u"Unknown entity: {}".format(entity).encode('utf-8')

        assert not entity.is_person
        if isinstance(array_or_dated_holder, (holders.DatedHolder, holders.Holder)):
            assert array_or_dated_holder.entity.is_person
            array = array_or_dated_holder.array
        else:
            array = array_or_dated_holder
            assert isinstance(array, np.ndarray), u"Expected a holder or a Numpy array. Got: {}".format(array).encode(
                'utf-8')
            persons_count = persons.count
            assert array.size == persons_count, u"Expected an array of size {}. Got: {}".format(persons_count,
                array.size)

        entity_index_array = simulation.get_entity(entity).members_entity_id

        if roles is None:  # Here we assume we have only one person per role. Not true with new role.
            roles = range(entity.roles_count)
        target_array = np.zeros(entity.count, dtype = array.dtype if array.dtype != np.bool else np.int16)
        for role in roles:
            # TODO: Mettre les filtres en cache dans la simulation
            boolean_filter = simulation.get_entity(entity).members_legacy_role == role
            target_array[entity_index_array[boolean_filter]] += array[boolean_filter]
        return target_array

    @classmethod
    def at_instant(cls, instant, default = UnboundLocalError):
        assert isinstance(instant, periods.Instant)
        for dated_formula_class in cls.dated_formulas_class:
            start_instant = dated_formula_class['start_instant']
            if (start_instant is None or start_instant <= instant):
                return dated_formula_class['formula_class']
        if default is UnboundLocalError:
            raise KeyError(instant)
        return default

    def check_for_cycle(self, period):
        """
        Return a boolean telling if the current variable has already been called without being allowed by
        the parameter max_nb_cycles of the calculate method.
        """
        def get_error_message():
            return u'Circular definition detected on formula {}<{}>. Formulas and periods involved: {}.'.format(
                column.name,
                period,
                u', '.join(sorted(set(
                    u'{}<{}>'.format(variable_name, period2)
                    for variable_name, periods in requested_periods_by_variable_name.iteritems()
                    for period2 in periods
                    ))).encode('utf-8'),
                )
        simulation = self.holder.simulation
        requested_periods_by_variable_name = simulation.requested_periods_by_variable_name
        column = self.holder.column
        variable_name = column.name
        if variable_name in requested_periods_by_variable_name:
            # Make sure the formula doesn't call itself for the same period it is being called for.
            # It would be a pure circular definition.
            requested_periods = requested_periods_by_variable_name[variable_name]
            assert period not in requested_periods and (column.definition_period != ETERNITY), get_error_message()
            if simulation.max_nb_cycles is None or len(requested_periods) > simulation.max_nb_cycles:
                message = get_error_message()
                if simulation.max_nb_cycles is None:
                    message += ' Hint: use "max_nb_cycles = 0" to get a default value, or "= N" to allow N cycles.'
                raise CycleError(message)
            else:
                requested_periods.append(period)
        else:
            requested_periods_by_variable_name[variable_name] = [period]

    def clean_cycle_detection_data(self):
        """
        When the value of a formula have been computed, remove the period from
        requested_periods_by_variable_name[variable_name] and delete the latter if empty.
        """
        simulation = self.holder.simulation
        column = self.holder.column
        variable_name = column.name
        requested_periods_by_variable_name = simulation.requested_periods_by_variable_name
        if variable_name in requested_periods_by_variable_name:
            requested_periods_by_variable_name[variable_name].pop()
            if len(requested_periods_by_variable_name[variable_name]) == 0:
                del requested_periods_by_variable_name[variable_name]

    def compute(self, period, **parameters):
        """
        Called by `Holder.compute` only when no value is found in cache.
        Return a DatedHolder after checking for cycles in formula.
        """
        holder = self.holder
        column = holder.column
        entity = holder.entity
        simulation = holder.simulation
        debug = simulation.debug

        assert (period is not None) or (column.definition_period == ETERNITY)

        max_nb_cycles = parameters.get('max_nb_cycles')
        extra_params = parameters.get('extra_params')
        if max_nb_cycles is not None:
            simulation.max_nb_cycles = max_nb_cycles

        # Note: Don't compute intersection with column.start & column.end, because holder already does it:
        # output_period = output_period.intersection(periods.instant(column.start), periods.instant(column.end))
        # Note: Don't verify that the function result has already been computed, because this is the task of
        # holder.compute().

        try:
            self.check_for_cycle(period)
            if extra_params:
                array = self.base_function(simulation, period, *extra_params)
            else:
                array = self.base_function(simulation, period)
        except CycleError:
            self.clean_cycle_detection_data()
            if max_nb_cycles is None:
                if simulation.trace:
                    simulation.tracer.record_calculation_abortion(column.name, period, **parameters)
                # Re-raise until reaching the first variable called with max_nb_cycles != None in the stack.
                raise
            simulation.max_nb_cycles = None
            return holder.put_in_cache(self.default_values(), period, extra_params)
        except ParameterNotFound as exc:
            if exc.variable_name is None:
                raise ParameterNotFound(
                    instant_str = exc.instant_str,
                    name = exc.name,
                    variable_name = column.name,
                    )
            else:
                raise
        except:
            log.error(u'An error occurred while calling formula {}@{}<{}> in module {}'.format(
                column.name, entity.key, str(period), self.__module__,
                ))
            raise

        assert isinstance(array, np.ndarray), (linesep.join([
            u"You tried to compute the formula '{0}' for the period '{1}'.".format(column.name, str(period)).encode('utf-8'),
            u"The formula '{0}@{1}' should return a Numpy array;".format(column.name, str(period)).encode('utf-8'),
            u"instead it returned '{0}' of '{1}'.".format(array, type(array)).encode('utf-8'),
            u"Learn more about Numpy arrays and vectorial computing:",
            u"<http://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html.>"
            ]))
        entity_count = entity.count
        assert array.size == entity_count, \
            u"Function {}@{}<{}>() --> <{}>{} returns an array of size {}, but size {} is expected for {}".format(
                column.name, entity.key, str(period), str(period), stringify_array(array),
                array.size, entity_count, entity.key).encode('utf-8')
        if debug:
            try:
                # cf https://stackoverflow.com/questions/6736590/fast-check-for-nan-in-numpy
                if np.isnan(np.min(array)):
                    nan_count = np.count_nonzero(np.isnan(array))
                    raise NaNCreationError(u"Function {}@{}<{}>() --> <{}>{} returns {} NaN value(s)".format(
                        column.name, entity.key, str(period), str(period), stringify_array(array),
                        nan_count).encode('utf-8'))
            except TypeError:
                pass
        if array.dtype != column.dtype:
            array = array.astype(column.dtype)

        self.clean_cycle_detection_data()
        if max_nb_cycles is not None:
            simulation.max_nb_cycles = None

        return holders.DatedHolder(self.holder, period, array, extra_params)

    def find_function(self, period):
        """
        Finds the last active formula for the time interval [period starting date, variable end attribute].
        """
        end = self.holder.column.end
        if end and period.start.date > end:
            return None

        # All formulas are already dated (with default start date in absence of user date)
        for dated_formula in reversed(self.dated_formulas):
            start = dated_formula['start_instant'].date

            if period.start.date >= start:
                return dated_formula['formula'].formula

        return None

    def exec_function(self, simulation, period, *extra_params):
        """
        Calls the right Variable's dated function for current period and returns a NumPy array.

        Retro-compatibility-layer: handles old syntax (with `self` as first argument).
        """
        function = self.find_function(period)

        if function.im_func.func_code.co_varnames[0] == 'self':
            return function(simulation, period, *extra_params)
        else:
            entity = self.holder.entity
            function = function.im_func
            parameters_at = simulation.parameters_at
            if function.func_code.co_argcount == 2:
                return function(entity, period)
            else:
                return function(entity, period, parameters_at, *extra_params)

    def graph_parameters(self, edges, get_input_variables_and_parameters, nodes, visited):
        """Recursively build a graph of formulas."""
        if self.dated_formulas is not None:
            for dated_formula in self.dated_formulas:
                dated_formula['formula'].graph_parameters(edges, get_input_variables_and_parameters, nodes, visited)
        else:
            holder = self.holder
            column = holder.column
            simulation = holder.simulation
            variables_name, parameters_name = get_input_variables_and_parameters(column)
            if variables_name is not None:
                for variable_name in sorted(variables_name):
                    variable_holder = simulation.get_or_new_holder(variable_name)
                    variable_holder.graph(edges, get_input_variables_and_parameters, nodes, visited)
                    edges.append({
                        'from': variable_holder.column.name,
                        'to': column.name,
                        })

    def formula_to_json(self, function, get_input_variables_and_parameters = None, with_input_variables_details = False):
        if function is None:
            return None
        comments = inspect.getcomments(function)
        doc = inspect.getdoc(function)
        self_json = collections.OrderedDict((
            ('@type', u'SimpleFormula'),
            ('comments', comments.decode('utf-8') if comments is not None else None),
            ('doc', doc.decode('utf-8') if doc is not None else None),
            ))
        if get_input_variables_and_parameters is not None:
            holder = self.holder
            column = holder.column
            simulation = holder.simulation
            variables_name, parameters_name = get_input_variables_and_parameters(column)
            if variables_name:
                if with_input_variables_details:
                    input_variables_json = []
                    for variable_name in sorted(variables_name):
                        variable_holder = simulation.get_variable_entity(variable_name).get_holder(variable_name)
                        variable_column = variable_holder.column
                        input_variables_json.append(collections.OrderedDict((
                            ('entity', variable_holder.entity.key),
                            ('label', variable_column.label),
                            ('name', variable_column.name),
                            )))
                    self_json['input_variables'] = input_variables_json
                else:
                    self_json['input_variables'] = list(variables_name)
            if parameters_name:
                self_json['parameters'] = list(parameters_name)
        return self_json

    def to_json(self, get_input_variables_and_parameters = None, with_input_variables_details = False):
        return collections.OrderedDict((
            ('@type', u'DatedFormula'),
            ('dated_formulas', [
                dict(
                    formula = self.formula_to_json(
                        dated_formula['formula'].formula,
                        get_input_variables_and_parameters = get_input_variables_and_parameters,
                        with_input_variables_details = with_input_variables_details,
                        ),
                    start_instant = (None if dated_formula['start_instant'] is None
                        else str(dated_formula['start_instant'])),
                    stop_instant = (None if dated_formula.get('stop_instant') is None
                        else str(dated_formula['stop_instant'])),
                    )
                for dated_formula in self.dated_formulas
                ]),
            ))


def calculate_output_add(formula, period):
    return formula.holder.compute_add(period).array


def calculate_output_divide(formula, period):
    return formula.holder.compute_divide(period).array


def get_neutralized_column(column):
    """
        Return a new neutralized column (to be used by reforms).
        A neutralized column always returns its default value, and does not cache anything.
    """
    return new_filled_column(
        entity = column.entity,
        is_neutralized = True,
        label = u'[Neutralized]' if column.label is None else u'[Neutralized] {}'.format(column.label),
        baseline_variable = column,
        definition_period = column.definition_period,
        set_input = set_input_neutralized,
        )


def deduce_formula_date_from_name(attribute_name):
    """
    Return a day date deduced from attribute name when it is a formula name, None otherwise.
    Valid dated name formats are : 'formula', 'formula_YYYY', 'formula_YYYY_MM' and 'formula_YYYY_MM_DD' where YYYY, MM and DD are a year, month and day.

    Default year is '0001'. Default month and day are '01'. Thus, 'formula' starts on 1st january of year 1.
    """
    if not attribute_name.startswith(FORMULA_NAME_PREFIX):
        # Current attribute isn't a formula
        return None

    formula_name = attribute_name
    if attribute_name == FORMULA_NAME_PREFIX:
        formula_name += (
            FORMULA_NAME_SEPARATOR
            + DEFAULT_YEAR
            + FORMULA_NAME_SEPARATOR
            + DEFAULT_MONTH
            + FORMULA_NAME_SEPARATOR
            + DEFAULT_DAY
            )

    else:
        match = re.match(r'formula_(\d{4}(_\d{2}){0,2})$', attribute_name)  # YYYY or YYYY_MM or YYYY_MM_DD
        assert match, 'Unrecognized formula name. Expecting "formula_YYYY" or "formula_YYYY_MM" or "formula_YYYY_MM_DD where YYYY, MM and DD are year, month and day. Found: ' + attribute_name
        start_str = match.group(1)

        if len(start_str) == 4:  # YYYY
            start_str += FORMULA_NAME_SEPARATOR + DEFAULT_MONTH
            formula_name += FORMULA_NAME_SEPARATOR + DEFAULT_MONTH

        if len(start_str) == 7:  # YYYY_MM
            start_str += FORMULA_NAME_SEPARATOR + DEFAULT_DAY
            formula_name += FORMULA_NAME_SEPARATOR + DEFAULT_DAY

    return datetime.datetime.strptime(formula_name,
    FORMULA_NAME_PREFIX + FORMULA_NAME_SEPARATOR + '%Y_%m_%d').date()


def new_filled_column(
        __doc__ = None,
        __module__ = None,
        base_function = UnboundLocalError,
        calculate_output = UnboundLocalError,
        cerfa_field = UnboundLocalError,
        column = UnboundLocalError,
        comments = UnboundLocalError,
        default = UnboundLocalError,
        definition_period = UnboundLocalError,
        entity = UnboundLocalError,
        is_neutralized = False,
        label = UnboundLocalError,
        name = None,
        baseline_variable = None,
        set_input = UnboundLocalError,
        source_code = UnboundLocalError,
        source_file_path = UnboundLocalError,
        start_line_number = UnboundLocalError,
        end = UnboundLocalError,
        reference = UnboundLocalError,
        **specific_attributes
        ):

    # Validate arguments.

    if baseline_variable is not None:
        assert isinstance(baseline_variable, columns.Column)
        if name is None:
            name = baseline_variable.name

    assert isinstance(name, unicode)

    if calculate_output is UnboundLocalError:
        calculate_output = None if baseline_variable is None else baseline_variable.formula_class.calculate_output.im_func

    if cerfa_field is UnboundLocalError:
        cerfa_field = None if baseline_variable is None else baseline_variable.cerfa_field
    elif cerfa_field is not None:
        assert isinstance(cerfa_field, (basestring, dict)), cerfa_field

    assert column is not None, """Missing attribute "column" in definition of filled column {}""".format(name)
    if column is UnboundLocalError:
        assert baseline_variable is not None, """Missing attribute "column" in definition of filled column {}""".format(
            name)
        column = baseline_variable.empty_clone()
    elif not isinstance(column, columns.Column):
        column = column()
        assert isinstance(column, columns.Column)

    if comments is UnboundLocalError:
        comments = None if baseline_variable is None else baseline_variable.formula_class.comments
    elif isinstance(comments, str):
        comments = comments.decode('utf-8')

    if default is UnboundLocalError:
        default = column.default if baseline_variable is None else baseline_variable.default

    assert entity is not None, """Missing attribute "entity" in definition of filled column {}""".format(
        name)
    if entity is UnboundLocalError:
        assert baseline_variable is not None, \
            """Missing attribute "entity" in definition of filled column {}""".format(name)
        entity = baseline_variable.entity

    if definition_period is UnboundLocalError:
        if baseline_variable:
            definition_period = baseline_variable.definition_period
        else:
            raise ValueError(u'definition_period missing in {}'.format(name).encode('utf-8'))
    if definition_period not in (MONTH, YEAR, ETERNITY):
        raise ValueError(u'Incorrect definition_period ({}) in {}'.format(definition_period, name).encode('utf-8'))

    if label is UnboundLocalError:
        label = None if baseline_variable is None else baseline_variable.label
    else:
        label = None if label is None else unicode(label)

    if start_line_number is UnboundLocalError:
        start_line_number = None if baseline_variable is None else baseline_variable.formula_class.start_line_number
    elif isinstance(start_line_number, str):
        start_line_number = start_line_number.decode('utf-8')

    if set_input is UnboundLocalError:
        set_input = None if baseline_variable is None else baseline_variable.formula_class.set_input.im_func

    if source_code is UnboundLocalError:
        source_code = None if baseline_variable is None else baseline_variable.formula_class.source_code
    elif isinstance(source_code, str):
        source_code = source_code.decode('utf-8')

    if source_file_path is UnboundLocalError:
        source_file_path = None if baseline_variable is None else baseline_variable.formula_class.source_file_path
    elif isinstance(source_file_path, str):
        source_file_path = source_file_path.decode('utf-8')

    if end is UnboundLocalError:
        end = None if baseline_variable is None else baseline_variable.end

    if reference is UnboundLocalError:
        reference = None if baseline_variable is None else baseline_variable.reference
    elif reference is not None:
        if isinstance(reference, list):
            reference = map(unicode, reference)
        else:
            reference = [unicode(reference)]

    # Build formula class and column.

    formula_class_attributes = {}
    if __doc__ is not None:
        formula_class_attributes['__doc__'] = __doc__
    if __module__ is not None:
        formula_class_attributes['__module__'] = __module__
    if comments is not None:
        formula_class_attributes['comments'] = comments
    if start_line_number is not None:
        formula_class_attributes['start_line_number'] = start_line_number
    if source_code is not None:
        formula_class_attributes['source_code'] = source_code
    if source_file_path is not None:
        formula_class_attributes['source_file_path'] = source_file_path

    if column.definition_period == ETERNITY:
        assert base_function == UnboundLocalError, 'Unexpected base_function {}'.format(base_function)
        base_function = permanent_default_value
    elif column.is_period_size_independent:
        assert base_function in (missing_value, requested_period_last_value, requested_period_last_or_next_value, UnboundLocalError), \
            'Unexpected base_function {}'.format(base_function)
        if base_function is UnboundLocalError:
            base_function = requested_period_last_value
    elif base_function is UnboundLocalError:
        base_function = requested_period_default_value

    if base_function is UnboundLocalError:
        assert baseline_variable is not None \
            and issubclass(baseline_variable.formula_class, Formula), \
            """Missing attribute "base_function" in definition of filled column {}""".format(name)
        base_function = baseline_variable.formula_class.base_function
    else:
        assert base_function is not None, \
            """Missing attribute "base_function" in definition of filled column {}""".format(name)
    formula_class_attributes['base_function'] = base_function

    if calculate_output is not None:
        formula_class_attributes['calculate_output'] = calculate_output

    if set_input is not None:
        formula_class_attributes['set_input'] = set_input

    dated_formulas_class = []
    for function_name, function in specific_attributes.copy().iteritems():
        # Turn any formula into a dated formula
        formula_start_date = deduce_formula_date_from_name(function_name)
        if not formula_start_date:
            # Current attribute isn't a formula
            continue

        if end is not None:
            assert end >= formula_start_date, \
                'You declared that "{}" ends on "{}", but you wrote a formula to calculate it from "{}" ({}). The "end" attribute of a variable must be posterior to the start dates of all its formulas.'.format(name, end, formula_start_date, function_name)
        dated_formula_class_attributes = formula_class_attributes.copy()
        dated_formula_class_attributes['formula'] = function
        dated_formula_class = type(name.encode('utf-8'), (Formula,), dated_formula_class_attributes)

        del specific_attributes[function_name]
        dated_formulas_class.append(dict(
            formula_class = dated_formula_class,
            start_instant = periods.instant(formula_start_date),
            ))

    dated_formulas_class.sort(key = lambda dated_formula_class: dated_formula_class['start_instant'])

    # Add dated formulas defined in (optional) baseline variable when they are not overridden by new dated formulas.
    if baseline_variable is not None:
        for baseline_dated_formula_class in baseline_variable.formula_class.dated_formulas_class:
            baseline_dated_formula_class = baseline_dated_formula_class.copy()
            for dated_formula_class in dated_formulas_class:
                if baseline_dated_formula_class['start_instant'] >= dated_formula_class['start_instant']:
                    break

            else:
                dated_formulas_class.append(baseline_dated_formula_class)
        dated_formulas_class.sort(key = lambda dated_formula_class: dated_formula_class['start_instant'])

    formula_class_attributes['dated_formulas_class'] = dated_formulas_class

    assert not specific_attributes.get('start_date'), \
        'Deprecated "start_date" attribute in definition of variable "{}".'.format(name)
    assert not specific_attributes, 'Unexpected attributes in definition of variable "{}": {!r}'.format(name,
        ', '.join(sorted(specific_attributes.iterkeys())))

    formula_class = type(name.encode('utf-8'), (Formula,), formula_class_attributes)

    # Fill column attributes.
    if cerfa_field is not None:
        column.cerfa_field = cerfa_field
    if default != column.default:
        column.default = default
    if end is not None:
        column.end = end
    if reference is not None:
        column.reference = reference
    column.entity = entity
    column.formula_class = formula_class
    column.definition_period = definition_period
    column.is_neutralized = is_neutralized
    column.label = label
    column.name = name

    return column


def set_input_dispatch_by_period(formula, period, array):
    holder = formula.holder
    period_size = period.size
    period_unit = period.unit

    if formula.holder.column.definition_period == MONTH:
        cached_period_unit = periods.MONTH
    elif formula.holder.column.definition_period == YEAR:
        cached_period_unit = periods.YEAR
    else:
        raise ValueError('set_input_dispatch_by_period can be used only for yearly or monthly variables.')

    after_instant = period.start.offset(period_size, period_unit)

    # Cache the input data, skipping the existing cached months
    sub_period = period.start.period(cached_period_unit)
    while sub_period.start < after_instant:
        existing_array = holder.get_array(sub_period)
        if existing_array is None:
            holder.put_in_cache(array, sub_period)
        else:
            # The array of the current sub-period is reused for the next ones.
            # TODO: refactor or document this behavior
            array = existing_array
        sub_period = sub_period.offset(1)


def set_input_divide_by_period(formula, period, array):
    holder = formula.holder
    period_size = period.size
    period_unit = period.unit

    if formula.holder.column.definition_period == MONTH:
        cached_period_unit = periods.MONTH
    elif formula.holder.column.definition_period == YEAR:
        cached_period_unit = periods.YEAR
    else:
        raise ValueError('set_input_divide_by_period can be used only for yearly or monthly variables.')

    after_instant = period.start.offset(period_size, period_unit)

    # Count the number of elementary periods to change, and the difference with what is already known.
    remaining_array = array.copy()
    sub_period = period.start.period(cached_period_unit)
    sub_periods_count = 0
    while sub_period.start < after_instant:
        existing_array = holder.get_array(sub_period)
        if existing_array is not None:
            remaining_array -= existing_array
        else:
            sub_periods_count += 1
        sub_period = sub_period.offset(1)

    # Cache the input data
    if sub_periods_count > 0:
        divided_array = remaining_array / sub_periods_count
        sub_period = period.start.period(cached_period_unit)
        while sub_period.start < after_instant:
            if holder.get_array(sub_period) is None:
                holder.put_in_cache(divided_array, sub_period)
            sub_period = sub_period.offset(1)
    elif not (remaining_array == 0).all():
        raise ValueError(u"Inconsistent input: variable {0} has already been set for all months contained in period {1}, and value {2} provided for {1} doesn't match the total ({3}). This error may also be thrown if you try to call set_input twice for the same variable and period.".format(holder.column.name, period, array, array - remaining_array).encode('utf-8'))


def set_input_neutralized(formula, period, array):
    warnings.warn(
        u"You cannot set a value for the variable {}, as it has been neutralized. The value you provided ({}) will be ignored."
        .format(formula.holder.column.name, array).encode('utf-8'),
        Warning
        )
