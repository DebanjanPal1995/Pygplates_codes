import pygplates
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import pygmt

#matplotlib inline


rotation_filename = 'Seton_etal_Modified_PlateModel.rot'

input_topology_filename = 'Seton_etal_ESR2012_PP_2012.1.gpml'

topology_features = pygplates.FeatureCollection(input_topology_filename)
rotation_model = pygplates.RotationModel(rotation_filename)

time_step = 10.
oldest_seed_time = 200.

# Empty array for storing Long/Lat of 
point_longitude = []
point_latitude = []
time_list = np.arange(oldest_seed_time,time_step,-time_step)

for seed_time in time_list:

    # Location of seed point for Kerguelenc
    #seed_geometry = pygplates.PointOnSphere(-50, 80)
    
    # Seed point for Hawaii
    #seed_geometry = pygplates.MultiPointOnSphere([(19,-155),(25,-155)])

    seed_geometry = pygplates.MultiPointOnSphere(
    [
        (42,-114),
        (37,-110),
        (28,-103)
    ])

    for time in np.arange(seed_time,40.,-time_step):
        #print max_time, time

        # Get the plate polygons for this time
        resolved_topologies = []
        pygplates.resolve_topologies(topology_features, rotation_model, resolved_topologies, time)

        # make plate partitioner from polygons
        plate_partitioner = pygplates.PlatePartitioner(resolved_topologies, rotation_model)

        # Find the plate id of the polygon that contains the point
        partitioned_inside_geometries = []
        plate_partitioner.partition_geometry(seed_geometry, partitioned_inside_geometries)
        #PlateID = partitioned_inside_geometries[0][0].get_feature().get_reconstruction_plate_id()
        PlateID = 902

        #print PlateID

        # Get the stage rotation that will move the point from where it is at the current time
        # to its location at the next time step, based on the plate id that contains the point at the 
        # current time
        stage_rotation = rotation_model.get_rotation(time-time_step, PlateID, time, anchor_plate_id=1)

        # use the stage rotation to reconstruct the tracked point from position at current time 
        # to position at the next time step
        seed_geometry = stage_rotation * seed_geometry
        

    #print('seed time = %d, plume is within plate %i' % (seed_time, PlateID))
    
    #point_longitude.append(seed_geometry.to_lat_lon_list().get_longitude())
    point_latitude.append(seed_geometry.to_lat_lon_list())
    #print(point_latitude)
    #exit()

#print('coordinates of reconstructed plume products')
#print(zip(time_list,point_longitude,point_latitude))
a=np.array(point_latitude)
#print(a)
#print(a[0][1][1])
#exit()
i=0
lons1=[]
lons2=[]
lats1=[]
lats2=[]
values = range(7)
#values=[0,2]
#no=[0]
for i in values:
    #for j in no:
       #print(a[i][j][1])
        lon1=a[i][0][1]
        lons1.append(lon1)
        lon2=a[i][1][1]
        lons2.append(lon2)
        lat1=a[i][0][0]
        lats1.append(lat1)
        lat2=a[i][1][0]
        lats2.append(lat2)


#exit()       
#print(lons1,lons2)
#exit()
#points1=str([point_latitude])
#with open('points.txt', 'w') as f:
 #   f.write(points1)       



#exit()        


time_list=[100,90,80,70,60,50,40]
#print(len(lons1),len(lats1),len(time_list))
#exit()
import pygmt
import geopandas as gpd
#data = pygmt.datasets.load_sample_data(name="reconstructed_80.00Ma.xy")
fig=pygmt.Figure()
pygmt.makecpt(cmap="seis", series=[100, 40,10])
#rgi = gpd.read_file('reconstructed_140.00Ma.shp')
#print(rgi.head())
#fig = pygmt.Figure()
fig.basemap(region="g", projection="W12c", frame=True)
fig.coast(shorelines="0.5p,white")
#fig.plot(data=rgi, pen="black")
fig.plot(x=lons1, y=lats1,
    fill=time_list,
    style="c0.08c",
    cmap=True,
    pen="black",
)
fig.plot(x=lons2, y=lats2,
   color=time_list,
    style="c0.08c",
    cmap=True,
    pen="black",
)
rgi = gpd.read_file('reconstructed_40.00Ma.shp')
fig.plot(data=rgi, pen="1p,black")
fig.colorbar(frame='af+l"Age (Ma)"')
fig.show()
exit()

#import cartopy.crs as ccrs
#import cartopy.feature as cfeature
#import cartopy.io.shapereader as shpreader
#matplotlib inline





