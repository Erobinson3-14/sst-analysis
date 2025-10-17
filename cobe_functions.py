
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
#reads SST dataset and returns it as a 3D array
def read_latest_sst(filename):
    """
    Reads the most recent SST map from a NetCDF file.
    
    Parameters:
        filename (str): Path to the NetCDF file.
        
    Returns:
        np.ndarray: 2D array of the latest SST map.
    """
    ds = xr.open_dataset(filename)  # Open the NetCDF file
    sst = ds['sst']                 # Assuming the SST variable is named 'sst'
    latest_sst = sst.isel(time=-1)  # Select the last time index
    return latest_sst.values        # Return as a 2D NumPy array
#accepts latitude, longitude and returns the timeseries at that point
def read_sst_timeseries(filename, lat, lon):
    ds = xr.open_dataset(filename)
    sst = ds['sst']
    point_timeseries = sst.sel(lat=lat, lon=lon, method="nearest")
    data = point_timeseries.values
    
    print(f"Total points: {len(data)}, NaNs: {np.isnan(data).sum()}")
    return data
#tries to load'time' vector from a SST dataset, then convert it into a python datetime object
#not sure if it works
def read_sst_timeseries_with_time(filename, lat, lon):
    """
    Reads SST timeseries at a given lat/lon and returns both
    the cleaned numeric array and corresponding datetime vector.
    """
    ds = xr.open_dataset(filename)
    sst = ds['sst']

    # Select nearest point
    point_timeseries = sst.sel(lat=lat, lon=lon, method='nearest').values

    # Load and convert time
    time_days = ds['time'].values
    start_date = np.datetime64('1891-01-01')
    datetime_vec = start_date + time_days.astype('timedelta64[D]')
    datetime_vec = datetime_vec.astype('O')  # convert to Python datetime

    # Ensure point_timeseries is numeric
    point_timeseries = np.array(point_timeseries, dtype=np.float64)

    # Remove NaNs and keep corresponding datetime
    mask = ~np.isnan(point_timeseries)
    sst_clean = point_timeseries[mask]
    datetime_clean = datetime_vec[mask]

    # If the result is empty, warn the user
    if len(sst_clean) == 0:
        print(f"Warning: No valid SST data at lat={lat}, lon={lon}. Returning empty arrays.")

    return datetime_clean, sst_clean