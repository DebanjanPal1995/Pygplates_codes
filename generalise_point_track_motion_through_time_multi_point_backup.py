import pygplates
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import time
#import pygmt

#matplotlib inline

#input parameters
rotation_filename = 'Global_EarthByte_230-0Ma_GK07_AREPS.rot'
input_topology_filename = 'Global_EarthByte_230-0Ma_GK07_AREPS_PlateBoundaries.gpml'
topology_features = pygplates.FeatureCollection(input_topology_filename)
rotation_model = pygplates.RotationModel(rotation_filename)

time_step = 10.
oldest_seed_time = 100.
start_time=100
end_time=40

#### load the gmt file which has the points
File_data = np.loadtxt("India.txt", dtype=int)

# Empty array for storing Long/Lat of 
point_longitude = []
point_latitude = []
time_list = np.arange(oldest_seed_time,time_step,-time_step)

for seed_time in time_list:

    # Location of seed point for Kerguelenc
    #seed_geometry = pygplates.PointOnSphere(-50, 80)
    
    # Seed point for Hawaii
    seed_geometry = pygplates.MultiPointOnSphere([(lat,lon) for lat, lon in File_data])

    #seed_geometry = pygplates.MultiPointOnSphere(
    #[
     #   (42,-114),
      #  (37,-110),
      #  (54,-116)
    #])

    for time in np.arange(seed_time,end_time,-time_step):
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
        PlateID = 550

        #print PlateID

        # Get the stage rotation that will move the point from where it is at the current time
        # to its location at the next time step, based on the plate id that contains the point at the 
        # current time
        stage_rotation = rotation_model.get_rotation(time-time_step, PlateID, time, anchor_plate_id=3)

        # use the stage rotation to reconstruct the tracked point from position at current time 
        # to position at the next time step
        seed_geometry = stage_rotation * seed_geometry
        

    #print('seed time = %d, plume is within plate %i' % (seed_time, PlateID))
    
    #point_longitude.append(seed_geometry.to_lat_lon_list().get_longitude())
    point_latitude.append(seed_geometry.to_lat_lon_list())


a=np.array(point_latitude)


##### define function to isolate lat & lon
def lat_lon(coord, no_of_time_steps,no_of_points):

    for x in range(no_of_points):
        globals()['lons%s' %x] = [coord[i][x][1] for i in range(no_of_time_steps)]
        globals()['lats%s' %x] = [coord[i][x][0] for i in range(no_of_time_steps)]
            
       
    #@ This was used previously in the early stage and is suitable while using only one data file
    #for x in range(no_of_points):
        #coordinates=[[]]
        #or j in range(no_of_time_steps):
        #coordinates=eval("lons" + str(x)), eval("lats" + str(x))
        #coordinates=[[eval("lons" + str(x)), eval("lats" + str(x))]]
        #return(['lons%s' %x], ['lats%s' %x] )
    
    #@ This is now used as this meant to do fo multiple data files
    coordinates=[[eval("lons" + str(x)), eval("lats" + str(x))] for x in range (no_of_points)]
    return(coordinates)
    

    


total_time_steps=int((start_time-end_time)/time_step + 1)
no_of_data_points=len(seed_geometry)
ages=np.arange(start=end_time,stop=start_time+time_step,step=time_step,dtype=int)
ages1=np.flip(ages)

### pass the co-oridnates, total_time_steps, & no of data points  to the fucntion lon_lat
b = lat_lon(a, total_time_steps, no_of_data_points)

#### create figure
import pygmt
import geopandas as gpd
fig=pygmt.Figure()
pygmt.makecpt(cmap="seis", series=[ages1.min(), ages1.max(), time_step])
#fig.basemap(region = [220, 300, 10, 60], projection="M8c", frame=True)
fig.basemap(region="g", projection="W270/12c", frame=True)
fig.coast(shorelines="0.8p,white")

##### loop over the data points
for i in range(no_of_data_points):

    #@ This was used previously in the early stages and is suitable while using only one data file
    #fig.plot(x=eval("lons" + str(i)), y=eval("lats" + str(i)),

    #@ This is now used and is easy to plot while using more than one data files
    fig.plot(x=b[i][0], y=b[i][1],
    fill=ages1,
    style="c0.1c",
    cmap=True,
    pen="black",    
    )
rgi = gpd.read_file('reconstructed_40.00Ma.shp')
fig.plot(data=rgi, pen="0.5p,black")
fig.colorbar(frame='af+l"Age (Ma)"')
fig.show()





