# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from mathmaker.lib import shared
from mathmaker.lib.tools.wording import setup_wording_format_of
from mathmaker.lib.core.base_calculus import Item, Product, Quotient
from mathmaker.lib.core.calculus import Equality
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, numbers_to_use, picture='true', **options):
        super().setup("minimal", **options)
        if numbers_to_use[0] < 11:
            raise ValueError('numbers_to_use[0] == {} whereas it should be '
                             '>= 11'.format(str(numbers_to_use[0])))
        numbers_to_use = (numbers_to_use[0] / 10, ) + numbers_to_use[1:]
        super().setup("numbers", nb=numbers_to_use,
                      shuffle_nbs=False, **options)
        super().setup("length_units", **options)
        super().setup("intercept_theorem_figure",
                      butterfly=True,
                      **options)

        self.figure.setup_labels([True, False, True, True, False, True],
                                 segments_list=self.figure.small
                                 + self.figure.side)

        self.line1 = self.figure.small[1].length_name
        self.line2 = self.figure.side[1].length_name

        self.wording = _('The drawn figure is out of shape. {newline} '
                         'The lengths are given in {length_unit}. '
                         '{newline} {newline} '
                         'Prove that {line1} is parallel to {line2}.')
        setup_wording_format_of(self)

        self.ratio1 = shared.machine.write_math_style1(Equality([
            Quotient(('+', self.figure.small[0].length_name,
                      self.figure.side[0].length_name)),
            Quotient(('+', self.figure.small[0].length,
                      self.figure.side[0].length))]
        ).printed)

        self.ratio2 = shared.machine.write_math_style1(Equality([
            Quotient(('+', self.figure.small[2].length_name,
                      self.figure.side[2].length_name)),
            Quotient(('+', self.figure.small[2].length,
                      self.figure.side[2].length))]
        ).printed)

        self.crossproduct = shared.machine.write_math_style1(Equality([
            Quotient(('+',
                      Product([Item(self.figure.small[0].length),
                               Item(self.figure.side[2].length)]),
                      Item(self.figure.side[0].length))),
            Item(self.figure.small[2].length)]
        ).printed)

        self.equal_ratios = shared.machine.write_math_style1(
            self.figure.ratios_for_converse().into_str())

        ans_variant = options.get('ans_variant', 'default')
        ans_texts = {
            'default': _('\\begin{tabular}{ll}'
                         'We have: & '
                         '{main_vertex_name} {belongs_to} {chunk0_length_name}'
                         ' \\\\ '
                         ' & '
                         '{main_vertex_name} {belongs_to} {chunk1_length_name}'
                         ' \end{tabular}'),
            'alternative2': _('{vertex1_name}, {main_vertex_name} and '
                              '{point0_name} on one hand, '
                              '{vertex2_name}, {main_vertex_name} and '
                              '{point1_name} on the other hand,'
                              'are aligned in the same order. ')
        }

        ratios = _('\\begin{multicols}{2} '
                   'On one hand: {ratio1} '
                   'and on the other hand: {ratio2} '
                   '\end{multicols} '
                   'ans as: {crossproduct} '
                   'then: {equal_ratios} {newline} ')

        conclusion = _('Hence by the converse of the intercept theorem, '
                       '{line1} is parallel to {line2}.')

        self.answer_wording = ans_texts[ans_variant] + ratios + conclusion
        setup_wording_format_of(self, w_prefix='answer_')

    def q(self, **options):
        return shared.machine.write_layout(
            (1, 2),
            [10, 10],
            [self.wording.format(**self.wording_format),
             shared.machine.insert_picture(self.figure,
                                           scale=0.7,
                                           top_aligned_in_a_tabular=True)])

    def a(self, **options):
        return self.answer_wording.format(**self.answer_wording_format)

    # TODO: create the "js" answer (for interactive pdf)
    # def js_a(self, **kwargs):
    #     return [self......jsprinted]
