__author__ = 'mustafa_dogan'
import netCDF4 as nc
import pandas as pd

# find closest index to specified value
def near(array,value):
    idx=(abs(array-value)).argmin()
    return idx

# list of netcdf files
# netcdfs = ['snow_melt.2009.v0.CA_NV.nc']

# First comment out the rest and look at variable name
# print(nc.Dataset(netcdfs[0]).variables)
# print('************')
# print('keys: ',nc.Dataset(netcdfs[0]).variables.keys())

# create a list of netcdf files
netcdfs = []
init_year = 2009
end_year = 2015
variable = 'precip'
for year in range(init_year,end_year+1):
	netcdfs.append(variable+'.'+str(year)+'.v0.CA_NV.nc')

# variable name
var_name = nc.Dataset(netcdfs[0]).variables.keys()[3] # usually fourth element is the variable name

# specify some location to extract time series. it will extract the closest location
latitude = 41.4; longitude = -116.15625

## Migrate NetCDF data to CSV (only need to do once to get CSVs)
df = pd.Series()
for netcdf in netcdfs:
	# open netcdf file
	fp = nc.Dataset(netcdf)

	# get information
	lat = fp.variables['Lat'][:]
	lon = fp.variables['Lon'][:]
	# Find nearest point to desired location (could also interpolate, but more work)
	ix = near(lat, latitude)
	iy = near(lon, longitude)
	# fish variables out of the netcdf file
	var = fp.variables[var_name]
	# Q.append(var[:,iy,ix])
	Q = var[:,iy,ix]

 	# # Determine the date range of data
	time_var = fp.variables['Time']
	first = nc.num2date(time_var[0],time_var.units)
	last = nc.num2date(time_var[-1],time_var.units)
	days = pd.date_range(first,last,freq = 'D')
	ts = pd.Series(Q,index=days,name=var_name)
	df = df.append(ts,verify_integrity=True)
	fp.close()

# Create another time series to save
data = pd.Series(df, index=df.index, name=var_name)

# Save to csv
data.to_csv(var_name+'.csv',index=True, header=True)
