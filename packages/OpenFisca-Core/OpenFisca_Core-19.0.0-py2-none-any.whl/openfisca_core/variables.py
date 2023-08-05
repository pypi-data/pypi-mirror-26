# -*- coding: utf-8 -*-


import inspect
import textwrap
import datetime

from openfisca_core.formulas import new_filled_column


class Variable(object):

    def __init__(self, name, attributes, variable_class):
        self.name = name
        self.attributes = attributes
        self.variable_class = variable_class

    def get_introspection_data(self, tax_benefit_system):
        comments = inspect.getcomments(self.variable_class)

        # Handle dynamically generated variable classes or Jupyter Notebooks, which have no source.
        try:
            absolute_file_path = inspect.getsourcefile(self.variable_class)
        except TypeError:
            source_file_path = None
        else:
            source_file_path = absolute_file_path.replace(tax_benefit_system.get_package_metadata()['location'], '')
        try:
            source_lines, start_line_number = inspect.getsourcelines(self.variable_class)
            source_code = textwrap.dedent(''.join(source_lines))
        except (IOError, TypeError):
            source_code, start_line_number = None, None

        return comments, source_file_path, source_code, start_line_number

    def to_column(self, tax_benefit_system):
        entity = self.attributes.pop('entity', None)

        # For reform variable that replaces an existing baseline one
        baseline_variable = self.attributes.pop('baseline_variable', None)
        if baseline_variable:
            if not entity:
                entity = baseline_variable.entity

        comments, source_file_path, source_code, start_line_number = self.get_introspection_data(tax_benefit_system)

        if entity is None:
            raise Exception('Variable {} must have an entity'.format(self.name))

        end = self.attributes.pop('end', None)
        end_date = None
        if end:
            assert isinstance(end, str), 'Type error on {}. String expected. Found: {}'.format(self.name + '.end', type(end))
            try:
                end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(u"Incorrect 'end' attribute format in '{}'. 'YYYY-MM-DD' expected where YYYY, MM and DD are year, month and day. Found: {}".format(self.name, end).encode('utf-8'))

        reference = self.attributes.pop('reference', None)
        if reference:
            if isinstance(reference, basestring):
                reference = [reference]
            elif isinstance(reference, list):
                pass
            elif isinstance(reference, tuple):
                reference = list(reference)
            else:
                raise TypeError('The reference of the variable {} is a {} instead of a String or a List of Strings.'.format(self.name, type(reference)))

            for element in reference:
                if not isinstance(element, basestring):
                    raise TypeError(
                        'The reference of the variable {} is a {} instead of a String or a List of Strings.'.format(
                            self.name, type(reference)))

        return new_filled_column(
            name = self.name,
            entity = entity,
            end = end_date,
            baseline_variable = baseline_variable,
            comments = comments,
            start_line_number = start_line_number,
            source_code = source_code,
            source_file_path = source_file_path,
            reference = reference,
            **self.attributes
            )
