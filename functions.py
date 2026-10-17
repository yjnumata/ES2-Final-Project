# A starter file for holding your functions
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

def CleanSumatraData(data):
    """
    Cleans the pandas dataframe by:
    1) Dropping duplicates of data with the same forest Cover
    2) Dropping rows with NaN values

    Parameters
    ----------
    data: pandas dataframe with original data of forest cover
 
    Returns
    -------
    data: cleaned and updated dataframe 
    """
  data = data.drop_duplicates(subset=['intact_forest_ha'], keep='first', inplace=True)
  data = pd.DataFrame(data)
  data = data.dropna()
  return data

def AddColumns(data):
   """
    Adds three columns of data:
    1) Latitude and Longitude to be able to input latitude and longitude for future use with geopandas
    2) Size to visualize the size of the forest cover marker on the map 

    Parameters
    ----------
    data: pandas dataframe with input data of forest cover
 
    Returns
    -------
    data: pandas dataframe with new data columns
    """
  lat=0.0
  long=0.0
  size = data['intact_forest_ha']/5 #Used later for the markersize of the forest cover on the map

  data.insert(12,'lat', lat)
  data.insert(13,'long',lat)
  data.insert(14, 'size', size)
  return data

def SepValuesForest(data):
    """
    Adds the Lat and Long data (found by Googling) and seperates each of the six rows of data into a seperate dataframes
    Combines the seperated dataframes together into Aceh Dataframe and North Sumatra Dataframe
    Parameters
    ----------
    data: pandas dataframe with input data of forest cover
 
    Returns
    -------
    data_1: dataframe with three rows of Aceh Data 
    data_2: dataframe with three rows of North Sumatra Data
    """
  df_77 = data[data['id'] == 77]
  df_77.loc[:,'lat'] = 2.6422
  df_77.loc[:,'long'] = 98.0022

  df_64 = data[data['id'] == 64]
  df_64.loc[:,'lat'] = 3.1613
  df_64.loc[:,'long'] = 97.4273

  df_89 = data[data['id'] == 89]
  df_89.loc[:,'lat'] = 4.3203
  df_89.loc[:,'long'] = 97.9103

  df_84 = data[data['id'] == 84]
  df_84.loc[:,'lat'] = 3.7275
  df_84.loc[:,'long'] = 97.9811

  df_28 = data[data['id'] == 28]
  df_28.loc[:,'lat'] = 3.7562
  df_28.loc[:,'long'] = 98.1448

  df_51 = data[data['id'] == 51]
  df_51.loc[:,'lat'] = 1.7972
  df_51.loc[:,'long'] = 100.3554

  data_1 = pd.concat([ df_64,df_77, df_89])
  data_1 = data_1.reset_index()

  data_2 = pd.concat([df_28, df_51, df_84])
  data_2 = data_2.reset_index()
  return data_1, data_2

def SepValuesSightings(data):
   """
   Seperates the data into Aceh sightings and North Sumatra (Sumatera Utara) sightings
    Parameters
    ----------
    data: pandas dataframe with input data of orangutan sightings
 
    Returns
    -------
    data_1: pandas dataframe with only Aceh Orangutan sightings
    data_2: pandas dataframe with only North Sumatra Orangutan sightings
    """
  data_1 = data[data['stateProvince'] == 'Aceh']
  data_2 = data[data['stateProvince'] == 'Sumatera Utara']
  return data_1, data_2

def GeoYearsForest(data):
   """
   Seperates the data into four dataframes based on year (1990, 2000, 2010, and 2020) 
   Converts the new dataframes into a geopandas dataframe
    Parameters
    ----------
    data: pandas dataframe with input data of forest cover
 
    Returns
    -------
    gdf_90: geopandas dataframe of 1990
    gdf_00: geopandas dataframe of 2000
    gdf_10: geopandas dataframe of 2010
    gdf_20: geopandas dataframe of 2020
    """
  df_90 = data[data['forest_year'] == 1990]
  df_90 = df_90.reset_index() 
  df_00 = data[data['forest_year'] == 2000]
  df_00 = df_00.reset_index()
  df_10 = data[data['forest_year'] == 2010]
  df_10 = df_10.reset_index()
  df_20 = data[data['forest_year'] == 2020]
  df_20 = df_20.reset_index()

# convert to geopandas
  gdf_90 = gpd.GeoDataFrame(df_90, geometry=gpd.points_from_xy(df_90.long, df_90.lat), crs="EPSG:4326")
  gdf_00 = gpd.GeoDataFrame(df_00, geometry=gpd.points_from_xy(df_00.long, df_00.lat), crs="EPSG:4326")
  gdf_10 = gpd.GeoDataFrame(df_10, geometry=gpd.points_from_xy(df_10.long, df_10.lat), crs="EPSG:4326")
  gdf_20 = gpd.GeoDataFrame(df_20, geometry=gpd.points_from_xy(df_20.long, df_20.lat), crs="EPSG:4326")
  return gdf_90, gdf_00, gdf_10, gdf_20
 
def GeoYearsSightings(data):
    """
   Seperates the data into four dataframes based on decade (90s, 00s, 10s, and 20s) 
   Converts the new dataframes into a geopandas dataframe
    Parameters
    ----------
    data: pandas dataframe with input data of orangutan sightings
 
    Returns
    -------
    gdf_90: geopandas dataframe of 1990
    gdf_00: geopandas dataframe of 2000
    gdf_10: geopandas dataframe of 2010
    gdf_20: geopandas dataframe of 2020
    """
  data_90 = data[data['year'].between(1990, 1999)] 
  data_00 = data[data['year'].between(2000, 2009)]
  data_10 = data[data['year'].between(2010, 2019)]
  data_20 = data[data['year'].between(2020, 2029)]

# convert to geopandas
  gdf_90 = gpd.GeoDataFrame(data_90, geometry=gpd.points_from_xy(data_90.decimalLongitude, data_90.decimalLatitude), crs="EPSG:4326")
  gdf_00 = gpd.GeoDataFrame(data_00, geometry=gpd.points_from_xy(data_00.decimalLongitude, data_00.decimalLatitude), crs="EPSG:4326")
  gdf_10 = gpd.GeoDataFrame(data_10, geometry=gpd.points_from_xy(data_10.decimalLongitude, data_10.decimalLatitude), crs="EPSG:4326")
  gdf_20 = gpd.GeoDataFrame(data_20, geometry=gpd.points_from_xy(data_20.decimalLongitude, data_20.decimalLatitude), crs="EPSG:4326")
  return gdf_90, gdf_00, gdf_10, gdf_20

def MapAceh(back_map, f_90, s_90, f_00, s_00, f_10, s_10, f_20, s_20):
    """
   Creates a plot of the forest cover and orangutan sightings in Aceh for every decade
    Parameters
    ----------
    back_map: Background map of Aceh to show the borders of the Province
    f_90: dataframe of the forest cover in 1990
    s_90: dataframe of the orangutan sightings in the 90s
    f_00: dataframe of the forest cover in 2000
    s_00: dataframe of the orangutan sightings in the 00s
    f_10: dataframe of the forest cover in 2010
    s_10: dataframe of the orangutan sightings in the 10s
    f_20: dataframe of the forest cover in 2020
    s_20: dataframe of the orangutan sightings in the 20s
 
    Returns
    -------
    plt: Final Plot of the Maps of Aceh
    """
  fig, axes = plt.subplots(2,2)
  plt.suptitle('Forest Cover in Aceh (in Ha) and Orangutan Sightings')
  
  a = back_map.plot(ax=axes[0,0], color = "white", edgecolor = 'black')
  f_90.plot(ax=axes[0,0], alpha=0.5, markersize = 'size', column='intact_forest_ha', cmap='rainbow', vmin=0, vmax=6200, legend=True) 
  # alpha is reduced to 0.5 to be able to see border and overlap of data, and markersize is changed for a clearer visual
  s_90.plot(ax=axes[0,0], color = "green", alpha=0.1, label='Orangutan Sightings') #alpha set to 0.1 to keep constant with all other subplots
  a.set_axis_off() #reduces clutter on the map, the lat and long do not contribute to the plot
  axes[0,0].set_title('Aceh in 1990')

  a = back_map.plot(ax=axes[0,1], color = "white", edgecolor = 'black')
  f_00.plot(ax=axes[0,1], column='intact_forest_ha', alpha=0.5, markersize = 'size', cmap='rainbow', vmin=0, vmax=6200, legend=True)
  s_00.plot(ax=axes[0,1], color = "green", alpha=0.1, legend=True)
  a.set_axis_off()
  axes[0,1].set_title('Aceh in 2000')

  a = back_map.plot(ax=axes[1,0], color = "white", edgecolor = 'black')
  f_10.plot(ax=axes[1,0], column='intact_forest_ha', alpha=0.5, markersize = 'size', cmap='rainbow', vmin=0, vmax=6200, legend=True)
  s_10.plot(ax=axes[1,0], color = "green", alpha=0.1, label='Orangutan Sightings')
  axes[1, 0].legend(loc='upper left', bbox_to_anchor=(0, 0))
  a.set_axis_off()
  axes[1,0].set_title('Aceh in 2010')

  a = back_map.plot(ax=axes[1,1], color = "white", edgecolor = 'black')
  f_20.plot(ax=axes[1,1], column='intact_forest_ha', alpha=0.5, markersize = 'size', cmap='rainbow', vmin=0, vmax=6200, legend=True)
  s_20.plot(ax=axes[1,1], color = "green", alpha=0.1, legend=True)
  a.set_axis_off()
  axes[1,1].set_title('Aceh in 2020')

  plt.savefig("Aceh_Map.png")
  plt.close()
  return plt

def MapNSumatra(back_map, f_90, s_90, f_00, s_00, f_10, s_10, f_20, s_20):
    """
    Creates a plot of the forest cover and orangutan sightings in North Sumatra for every decade
    Parameters
    ----------
    back_map: Background map of North Sumatra to show the borders of the Province
    f_90: dataframe of the forest cover in 1990
    s_90: dataframe of the orangutan sightings in the 90s
    f_00: dataframe of the forest cover in 2000
    s_00: dataframe of the orangutan sightings in the 00s
    f_10: dataframe of the forest cover in 2010
    s_10: dataframe of the orangutan sightings in the 10s
    f_20: dataframe of the forest cover in 2020
    s_20: dataframe of the orangutan sightings in the 20s
 
    Returns
    -------
    plt: Final Plot of the Maps of North Sumatra
    """
  fig, axes = plt.subplots(2,2)
  plt.suptitle('Forest Cover in North Sumatra (in Ha) and Orangutan Sightings')
  
  a = back_map.plot(ax=axes[0,0], color = "white", edgecolor = 'black')
  f_90.plot(ax=axes[0,0], alpha=0.5, markersize = 'size', column='intact_forest_ha', cmap='rainbow', vmin=0, vmax=6200, legend=True)
  s_90.plot(ax=axes[0,0], color = "green", alpha=0.1, label='Orangutan Sightings') 
  a.set_axis_off()
  axes[0,0].set_title('North Sumatra in 1990')

  a = back_map.plot(ax=axes[0,1], color = "white", edgecolor = 'black')
  f_00.plot(ax=axes[0,1], column='intact_forest_ha', alpha=0.5, markersize = 'size', cmap='rainbow', vmin=0, vmax=6200, legend=True)
  s_00.plot(ax=axes[0,1], color = "green", alpha=0.1, legend=True)
  a.set_axis_off()
  axes[0,1].set_title('North Sumatra in 2000')

  a = back_map.plot(ax=axes[1,0], color = "white", edgecolor = 'black')
  f_10.plot(ax=axes[1,0], column='intact_forest_ha', alpha=0.5, markersize = 'size', cmap='rainbow', vmin=0, vmax=6200, legend=True)
  s_10.plot(ax=axes[1,0], color = "green", alpha=0.1, label='Orangutan Sightings')
  axes[1, 0].legend(loc='upper left', bbox_to_anchor=(0, 0))
  a.set_axis_off()
  axes[1,0].set_title('North Sumatra in 2010')

  a = back_map.plot(ax=axes[1,1], color = "white", edgecolor = 'black')
  f_20.plot(ax=axes[1,1], column='intact_forest_ha', alpha=0.5, markersize = 'size', cmap='rainbow', vmin=0, vmax=6200, legend=True)
  s_20.plot(ax=axes[1,1], color = "green", alpha=0.1, legend=True)
  a.set_axis_off()
  axes[1,1].set_title('Aceh in 2020')

  plt.savefig("N_Sumatra_Map.png")
  plt.close()
  return plt






