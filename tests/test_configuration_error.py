import pytest

from ai_video.config.configuration_error import (
    ConfigurationError,
)


def test_configuration_error_is_value_error():
    with pytest.raises(ValueError):
        raise ConfigurationError("invalid configuration")