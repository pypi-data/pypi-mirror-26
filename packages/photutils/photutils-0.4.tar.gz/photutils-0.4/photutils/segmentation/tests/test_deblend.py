# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
from numpy.testing import assert_allclose
import pytest

from astropy.tests.helper import catch_warnings
from astropy.utils.exceptions import AstropyUserWarning
from astropy.modeling import models

from ..core import SegmentationImage
from ..deblend import deblend_sources
from ..detect import detect_sources

try:
    import scipy    # noqa
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

try:
    import skimage    # noqa
    HAS_SKIMAGE = True
except ImportError:
    HAS_SKIMAGE = False


@pytest.mark.skipif('not HAS_SCIPY')
@pytest.mark.skipif('not HAS_SKIMAGE')
class TestDeblendSources(object):
    def setup_class(self):
        g1 = models.Gaussian2D(100, 50, 50, 5, 5)
        g2 = models.Gaussian2D(100, 35, 50, 5, 5)
        g3 = models.Gaussian2D(30, 70, 50, 5, 5)
        y, x = np.mgrid[0:100, 0:100]
        self.x = x
        self.y = y
        self.data = g1(x, y) + g2(x, y)
        self.data3 = self.data + g3(x, y)
        self.threshold = 10
        self.npixels = 5
        self.segm = detect_sources(self.data, self.threshold, self.npixels)
        self.segm3 = detect_sources(self.data3, self.threshold, self.npixels)

    @pytest.mark.parametrize('mode', ['exponential', 'linear'])
    def test_deblend_sources(self, mode):
        result = deblend_sources(self.data, self.segm, self.npixels,
                                 mode=mode)
        assert result.nlabels == 2
        assert result.nlabels == len(result.slices)
        mask1 = (result.data == 1)
        mask2 = (result.data == 2)
        assert_allclose(len(result.data[mask1]), len(result.data[mask2]))
        assert_allclose(np.sum(self.data[mask1]), np.sum(self.data[mask2]))
        assert_allclose(np.nonzero(self.segm), np.nonzero(result))

    def test_deblend_multiple_sources(self):
        g4 = models.Gaussian2D(100, 50, 15, 5, 5)
        g5 = models.Gaussian2D(100, 35, 15, 5, 5)
        g6 = models.Gaussian2D(100, 50, 85, 5, 5)
        g7 = models.Gaussian2D(100, 35, 85, 5, 5)
        x = self.x
        y = self.y
        data = self.data + g4(x, y) + g5(x, y) + g6(x, y) + g7(x, y)
        segm = detect_sources(data, self.threshold, self.npixels)
        result = deblend_sources(data, segm, self.npixels)
        assert result.nlabels == 6
        assert result.nlabels == len(result.slices)
        assert result.area(1) == result.area(2)
        assert result.area(1) == result.area(3)
        assert result.area(1) == result.area(4)
        assert result.area(1) == result.area(5)
        assert result.area(1) == result.area(6)

    @pytest.mark.parametrize('mode', ['exponential', 'linear'])
    def test_deblend_sources_norelabel(self, mode):
        result = deblend_sources(self.data, self.segm, self.npixels,
                                 mode=mode, relabel=False)
        assert result.nlabels == 2
        assert len(result.slices) <= result.max
        assert len(result.slices) == 3   # label 1 is None
        assert_allclose(np.nonzero(self.segm), np.nonzero(result))

    @pytest.mark.parametrize('mode', ['exponential', 'linear'])
    def test_deblend_three_sources(self, mode):
        result = deblend_sources(self.data3, self.segm3, self.npixels,
                                 mode=mode)
        assert result.nlabels == 3
        assert_allclose(np.nonzero(self.segm3), np.nonzero(result))

    def test_deblend_sources_segm_array(self):
        result = deblend_sources(self.data, self.segm.data, self.npixels)
        assert result.nlabels == 2

    def test_segment_img_badshape(self):
        segm_wrong = np.zeros((2, 2))
        with pytest.raises(ValueError):
            deblend_sources(self.data, segm_wrong, self.npixels)

    def test_invalid_nlevels(self):
        with pytest.raises(ValueError):
            deblend_sources(self.data, self.segm, self.npixels, nlevels=0)

    def test_invalid_contrast(self):
        with pytest.raises(ValueError):
            deblend_sources(self.data, self.segm, self.npixels, contrast=-1)

    def test_invalid_mode(self):
        with pytest.raises(ValueError):
            deblend_sources(self.data, self.segm, self.npixels,
                            mode='invalid')

    def test_invalid_connectivity(self):
        with pytest.raises(ValueError):
            deblend_sources(self.data, self.segm, self.npixels,
                            connectivity='invalid')

    def test_constant_source(self):
        data = self.data.copy()
        data[data.nonzero()] = 1.
        result = deblend_sources(data, self.segm, self.npixels)
        assert_allclose(result, self.segm)

    def test_source_with_negval(self):
        data = self.data.copy()
        data -= 20
        with catch_warnings(AstropyUserWarning) as warning_lines:
            deblend_sources(data, self.segm, self.npixels)
            assert ('contains negative values' in
                    str(warning_lines[0].message))

    def test_source_zero_min(self):
        data = self.data.copy()
        data -= data[self.segm.data > 0].min()
        result1 = deblend_sources(self.data, self.segm, self.npixels)
        result2 = deblend_sources(data, self.segm, self.npixels)
        assert_allclose(result1, result2)

    def test_connectivity(self):
        """Regression test for #341."""
        data = np.zeros((3, 3))
        data[0, 0] = 2
        data[1, 1] = 2
        data[2, 2] = 1
        segm = np.zeros_like(data)
        segm[data.nonzero()] = 1
        segm = SegmentationImage(segm)
        data = data * 100.
        segm_deblend = deblend_sources(data, segm, npixels=1, connectivity=8)
        assert segm_deblend.nlabels == 1
        with pytest.raises(ValueError):
            deblend_sources(data, segm, npixels=1, connectivity=4)
