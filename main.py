from functions import *

# Import Data
df_sumatra = pd.read_csv("Sumatra_processed_forest_data.csv")
df_sightings = pd.read_csv('Orangutan_Sighting.csv')

# Clean Data and Prepare Data
CleanSumatraData(df_sumatra)
df_sightings = df_sightings[df_sightings['countryCode'] == 'ID']
AddColumns(df_sumatra)

df_aceh, df_nsumatra = SepValuesForest(df_sumatra)
df_sightings_a, df_sightings_n = SepValuesSightings(df_sightings)

gdf_90_a, gdf_00_a, gdf_10_a, gdf_20_a = GeoYearsForest(df_aceh)
gdf_sightings_90_a, gdf_sightings_00_a, gdf_sightings_10_a, gdf_sightings_20_a = GeoYearsSightings(df_sightings_a)

gdf_90_n, gdf_00_n, gdf_10_n, gdf_20_n = GeoYearsForest(df_nsumatra)
gdf_sightings_90_n, gdf_sightings_00_n, gdf_sightings_10_n, gdf_sightings_20_n = GeoYearsSightings(df_sightings_n)

# Making Map
data = gpd.read_file("indonesia.geojson")
aceh = gpd.GeoSeries(data.loc[0]['geometry'])
n_sumatra = gpd.GeoSeries(data.loc[3]['geometry'])
MapAceh(aceh, gdf_90_a, gdf_sightings_90_a, gdf_00_a, gdf_sightings_00_a, gdf_10_a, gdf_sightings_10_a, gdf_20_a, gdf_sightings_20_a)
MapNSumatra(n_sumatra, gdf_90_n, gdf_sightings_90_n, gdf_00_n, gdf_sightings_00_n, gdf_10_n, gdf_sightings_10_n, gdf_20_n, gdf_sightings_20_n)

# Show General Trends
fig, axes = plt.subplots(1,2)
year = df_aceh['forest_year']
forest_aceh = df_aceh['intact_forest_ha']
forest_nsumatra = df_nsumatra['intact_forest_ha']
axes[0].scatter(year, forest_aceh, marker = 'v', label = 'Aceh')
axes[0].scatter(year, forest_nsumatra, label = 'N Sumatra')
axes[0].legend()
axes[0].set_ylabel('Intact Forest (ha)')
axes[0].set_title('Intact Forest over Time')

x = ['1990s', '2000s', '2010s', '2020s']
values_a = [len(gdf_sightings_90_a), len(gdf_sightings_00_a), len(gdf_sightings_10_a), len(gdf_sightings_20_a)]
values_n = [len(gdf_sightings_90_n), len(gdf_sightings_00_n), len(gdf_sightings_10_n), len(gdf_sightings_20_n)]
axes[1].bar(x, values_a, label = 'Aceh')
axes[1].bar(x, values_n, bottom=values_a, label = 'N Suamtra')
axes[1].legend(loc='upper left')
axes[1].set_ylabel('Orangutan Sightings')
axes[1].set_title('Orangutan Sightings per Decade')
fig.tight_layout()
plt.savefig('trends.png')
