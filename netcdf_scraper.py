__author__ = 'mustafa_dogan'
import urllib, time, os

# **********************
# this module downloads netcdf climate data from cal-adapt.org
# **********************

# Example paths
# loca_vic-output
example_path = 'http://albers.cnr.berkeley.edu/data/scripps/loca_vic-output/GFDL-CM3/rcp45/rainfall.2088.v0.CA_NV.nc'
# observed data (livneh)
example_path = 'http://albers.cnr.berkeley.edu/data/scripps/livneh/CA_NV/ET.1915.v0.CA_NV.nc'

# give study name
study_path = 'http://albers.cnr.berkeley.edu/data/scripps/loca_vic-output/'
# climate scenario
climate_scenario = 'GFDL-CM3'
# rcp scenraio
rcp = 'rcp45'

# inital and ending year that you want to donwload data for
init_year = 2015
end_year = 2100

# enter list of variables you want to download
variables = ['ET','Tair','baseflow','precip','rainfall','runoff','snow_melt','snowfall','tot_runoff']

# start scarping
for variable in variables:
	folder = str(study_path+climate_scenario+'/'+rcp+'/')
	save_path = str('./'+climate_scenario+'/'+rcp+'/'+variable)
	# if directory does not exist, create one
	try:
		os.makedirs(save_path)
	except OSError:
		pass
	for year in range(init_year,end_year+1):
		data_file = str(variable+'.'+str(year)+'.v0.CA_NV.nc')
		path = str(folder+data_file)
		print('now downloading: '+path)
		testfile = urllib.URLopener()
		testfile.retrieve(path, save_path+'/'+data_file)
		time.sleep(1) # wait for a second