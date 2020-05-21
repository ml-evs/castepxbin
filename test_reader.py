"""
Test the reader
"""
import os
import pytest
import numpy as np

from castep_bin_reader import read_pdos_bin, reorder_pdos_data, compute_pdos, Spin, Orbital


@pytest.fixture
def pdos_bin():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.pdos_bin')


@pytest.fixture
def bands_file():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.bands')


def test_pdos_reader(pdos_bin):
    """Test the reader for pdos_bin"""
    output = read_pdos_bin(pdos_bin)
    assert output['pdos_weights'].shape == (8, 23, 110, 1)


def test_pdos_reorder(pdos_bin):
    """Test reordering of the PDOS"""
    raw_output = read_pdos_bin(pdos_bin)
    reordered = reorder_pdos_data(raw_output)
    assert reordered[0][Orbital.s][Spin.up].shape == (23, 110)


def test_pdos_compute(pdos_bin, bands_file):
    """Test computing pdos"""
    from sumo.io.castep import (_read_bands_header_verbose,
                                read_bands_eigenvalues, _is_metal, _get_vbm,
                                _ry_to_ev)

    raw_output = read_pdos_bin(pdos_bin)
    ordered_weights = reorder_pdos_data(raw_output)
    header = _read_bands_header_verbose(bands_file)
    _, weights, eigenvalues = read_bands_eigenvalues(bands_file, header)

    bin_width = 0.01
    bins = np.arange(0.0, 10.0 + bin_width, bin_width)

    pdos = compute_pdos(ordered_weights, eigenvalues, weights, bins)