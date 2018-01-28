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


@patch('tracker.data_gather.vincenty')
def test_get_closest_station_returns_code_of_closest(mock_vincenty):
    mock_station_map = MagicMock()
    mock_station_map.items.return_value = [
        ('CLOSE', 'COORDS'),
        ('FAR', 'COORDS')
    ]
    # Order of values here must correspond to the order of the stations above
    # since this is the order they will be returned by `vincenty`
    mock_vincenty.side_effect = [MagicMock(meters=1), MagicMock(meters=1000)]
    vehical_location = {'VehicleLatitude': 'some', 'VehicleLongitude': 'where'}

    result = dg._get_closest_station(vehical_location, mock_station_map)

    assert result == 'CLOSE'


def test_get_arrival_func_returns_function():
    arrival_func = dg.get_arrival_func('route', 'direction', 'station_id')

    assert callable(arrival_func)


@patch('tracker.data_gather.utils')
@patch('tracker.data_gather.Client')
def test_arrival_func_uses_route_dir_and_station(mock_client_cls, mock_utils):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client

    arrival_func = dg.get_arrival_func('route', 'direction', 'station_id')
    arrival_func()

    mock_client.get_timepoint_departures.assert_called_with(
        'route', 'direction', 'station_id'
    )
