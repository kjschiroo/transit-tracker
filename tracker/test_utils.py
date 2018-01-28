from unittest.mock import patch
import pytest
from . import utils


def test_current_time_doesnt_error():
    utils.current_time()


def test_parse_time_parses_valid_time_string():
    result = utils.parse_time('/Date(12345678901111-0600)/')

    assert result == 1234567890


def test_parser_time_raises_value_error_if_bad_string():
    with pytest.raises(ValueError):
        result = utils.parse_time('I M BAD')


@patch('tracker.utils.current_time')
@patch('tracker.utils.parse_time')
def test_seconds_from_now_takes_diff_of_current_and_parsed_string_time(
    mock_parse_time,
    mock_current_time
):
    mock_parse_time.return_value = 10
    mock_current_time.return_value = 1

    result = utils.seconds_from_now('time_str')

    assert result == 9
