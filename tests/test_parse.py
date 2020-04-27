# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest
from hypothesis import assume, given, settings, HealthCheck

from parver import ParseError, Version

from .strategies import version_string, whitespace


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(whitespace, version_string(), whitespace)
def test_parse_hypothesis(prefix, version, suffix):
    Version.parse(prefix + version + suffix)


@given(whitespace, version_string(strict=True), whitespace)
def test_parse_strict_hypothesis(prefix, version, suffix):
    Version.parse(prefix + version + suffix, strict=True)


@given(version_string(strict=False))
def test_parse_strict_error(version):
    v = Version.parse(version)

    # Exclude already normalized versions
    assume(str(v.normalize()) != version)

    # 0!1 normalizes to '1'
    assume(v.epoch != 0 or v.epoch_implicit)

    with pytest.raises(ParseError):
        Version.parse(version, strict=True)


@given(version_string())
def test_roundtrip(version):
    assert str(Version.parse(version)) == version


@pytest.mark.parametrize('version', [
    '1+ABC',
    '1+2-3',
    '1+2_3',
    '1+02_3',
])
def test_parse_local_strict(version):
    with pytest.raises(ParseError):
        Version.parse(version, strict=True)
    Version.parse(version)
