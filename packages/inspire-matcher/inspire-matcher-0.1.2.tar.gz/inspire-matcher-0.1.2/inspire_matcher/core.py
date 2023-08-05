# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

from inspire_utils.helpers import force_list
from inspire_utils.record import get_value


def compile(query, record):
    type_ = query['type']

    if type_ == 'exact':
        return _compile_exact(query, record)

    raise NotImplementedError(type_)


def _compile_exact(query, record):
    match, search = query['match'], query['search']

    collections = query.get('collections', [])

    values = force_list(get_value(record, match))
    if not values:
        return

    result = {
        'query': {
            'bool': {
                'minimum_should_match': 1,
                'should': [],
            },
        },
    }

    if collections:
        result['query']['bool']['filter'] = {'bool': {'should': []}}

        for collection in collections:
            result['query']['bool']['filter']['bool']['should'].append({
                'match': {
                    '_collections': collection,
                },
            })

    for value in values:
        result['query']['bool']['should'].append({
            'term': {
                search: {
                    'value': value,
                },
            },
        })

    return result
