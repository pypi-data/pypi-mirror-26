# (C) British Crown Copyright 2014 - 2017, Met Office
#
# This file is part of iris-grib.
#
# iris-grib is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iris-grib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with iris-grib.  If not, see <http://www.gnu.org/licenses/>.
"""
Unit tests for :meth:`iris_grib._save_rules.grid_definition_section`.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris_grib.tests first so that some things can be initialised before
# importing anything else.
import iris_grib.tests as tests

from iris.coord_systems import Orthographic
from iris.exceptions import TranslationError

from iris_grib._save_rules import grid_definition_section
from iris_grib.tests.unit.save_rules import GdtTestMixin


class Test(tests.IrisGribTest, GdtTestMixin):
    def setUp(self):
        GdtTestMixin.setUp(self)

    def test__fail_irregular_latlon(self):
        test_cube = self._make_test_cube(x_points=(1, 2, 11, 12),
                                         y_points=(4, 5, 6))
        with self.assertRaisesRegexp(
                TranslationError,
                'irregular latlon grid .* not yet supported'):
            grid_definition_section(test_cube, self.mock_grib)

    def test__fail_unsupported_coord_system(self):
        cs = Orthographic(0, 0)
        test_cube = self._make_test_cube(cs=cs)
        with self.assertRaisesRegexp(
                ValueError,
                'Grib saving is not supported for coordinate system:'):
            grid_definition_section(test_cube, self.mock_grib)


if __name__ == "__main__":
    tests.main()
