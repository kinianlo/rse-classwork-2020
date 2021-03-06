from times import compute_overlap_time, time_range, iss_passes, fetch_iss_passes, json_to_passes
import pytest
from unittest.mock import patch
import requests

@pytest.mark.parametrize("range1, range2, expected",
[(time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
  time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
  [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]),
  (time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
  time_range("2010-01-12 12:30:00", "2010-01-12 12:45:00", 2, 60),
  []),
  (time_range("2010-01-12 10:00:00", "2010-01-12 13:00:00", 3, 900),
  time_range("2010-01-12 10:40:00", "2010-01-12 11:20:00", 2, 120),
  [("2010-01-12 10:40:00","2010-01-12 10:50:00"), ("2010-01-12 11:05:00", "2010-01-12 11:20:00")]),
  (time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
  time_range("2010-01-12 11:00:00", "2010-01-12 12:45:00"),
  [])
])
def test_param(range1, range2, expected):
    assert compute_overlap_time(range1, range2) == expected


def test_backward():
    with pytest.raises(ValueError) as e:
        time_range("2010-01-12 13:00:00", "2010-01-12 12:00:00")
        assert e.match('End time should be later than Start time.')

def test_fetch_iss_passes():
    with patch.object(requests, "get") as mock_get:
        passes = fetch_iss_passes(0.1, 0.1, 3)
        mock_get.assert_called_with(
                "http://api.open-notify.org/iss-pass.json",
                params={'lat': 0.1, 'lon':0.1, 'n':3}
        )
