from unittest.mock import patch, MagicMock
from . import data_gather as dg


# @patch('tracker.data_gather.Client')
def test_get_active_func_returns_function():
    active_station_func = dg.get_active_stations_func('route', 'direction', {})

    assert callable(active_station_func)

@patch('tracker.data_gather._get_closest_station')
@patch('tracker.data_gather.Client')
def test_active_station_func_filters_on_direction(
    mock_client_cls, mock_get_closest_station
):
    mock_station_map = MagicMock()
    direction = 1
    mock_client = MagicMock()
    relevant_vehicle_location = {
        'VehicleLatitude': 1, 'VehicleLatitude': 2, 'Direction': direction
    }
    mock_client.get_vehicle_locations.return_value = [
        relevant_vehicle_location,
        {'VehicleLatitude': 2, 'VehicleLatitude': 1, 'Direction': 2},
    ]
    mock_client_cls.return_value = mock_client
    mock_get_closest_station.side_effect = ['FOO', 'BAR']

    active_station_func = dg.get_active_stations_func(
        'route', direction, mock_station_map
    )
    result = active_station_func()

    assert mock_get_closest_station.call_count == 1
    mock_get_closest_station.assert_called_with(
        relevant_vehicle_location, mock_station_map
    )


def test_get_arrival_func_returns_function():
    arrival_func = dg.get_arrival_func('route', 'direction', 'station_id')

    assert callable(arrival_func)
