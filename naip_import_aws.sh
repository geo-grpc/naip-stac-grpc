#!/usr/bin/env bash
STATES=(al ar az ca co ct de fl ga ia id il in ks ky la ma md me mi mn mo ms mt nc nd ne nh nj nm nv ny oh ok or pa ri sc sd tn tx ut va vt wa wi wv wy)
END_YEAR=$(date +'%Y')
FAILING_SHAPEFILES=(naip_3_172_6_fl naip_3_17_2_8_sc naip_3_17_2_2_pa)

cd index

# TODO contact ESRI bucket owner about broken prj files
# Failures
# naip_3_13_2_1_al
# GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]
docker rm -f naip-metadata-postgis
docker run -d --env POSTGRES_PASSWORD=cabbage \
              --env POSTGRES_USER=user \
              --env POSTGRES_DB=testdb \
              -p 5432:5432 --name=naip-metadata-postgis mdillon/postgis
echo starting db
sleep 40

for i in *.shp
do
   [[ -f "$i" ]] || break

   bad_bananas=$(basename ${i} .shp)
   # if equals naip_3_172_6_fl.shp skip
   # TODO contact ESRI about broken shp file:
   # naip_3_172_6_fl.shp
   if [[ ! ${FAILING_SHAPEFILES[*]} =~ "${bad_bananas}" ]]
   then
      no_ext=${i%.*}

      # # repair projection file
      cat $no_ext".prj"
      echo "overwrite pr file $no_ext.prj"
      echo -e "GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]" > $no_ext".prj"

      # # # write sql
      echo "write shapefile $1 to db"
      ogr2ogr -f "PostgreSQL" PG:"host='localhost' port=5432 dbname='testdb' user='user' password='cabbage'" -append $i -nln naip_visual -t_srs EPSG:4326

      # TODO contact ESRI about broken dbf files:
      # naip_3_17_2_2_pa
      # naip_3_17_2_8_sc
      # look for shapefiles that are missing rows. if missing then sound an alarm
      NULL_COUNT=$(docker exec -it naip-metadata-postgis /bin/bash -c "psql -qtA -d testdb -U user -c \"SELECT COUNT(*) FROM naip_visual WHERE res IS NULL\"")
      echo null row count: $NULL_COUNT
   else
      echo skipping bad shapefile: $bad_bananas
   fi
done

# TODO check that shapefile count matches the postgres row count

# add demical places to numeric field for resolution
# ALTER TABLE naip_visual
#    ALTER COLUMN res
#    SET DATA TYPE NUMERIC(10,2);
echo altering resolution column type
docker exec -it naip-metadata-postgis /bin/bash -c "psql -qtA -d testdb -U user -c \"ALTER TABLE naip_visual ALTER COLUMN res SET DATA TYPE NUMERIC(10,2);\""
# update all 0 values to be .6m
# UPDATE naip_visual
# SET res = 0.6
# WHERE res = 0;
echo altering resolution data from 0s to 0.6s
docker exec -it naip-metadata-postgis /bin/bash -c "psql -qtA -d testdb -U user -c \"UPDATE naip_visual SET res = 0.6 WHERE res = 0;\""

# fix all the date columns to correct type
# ALTER TABLE naip_visual
#     ALTER COLUMN verdate TYPE DATE
# USING to_date(verdate, 'YYYYMMDD');
# ALTER TABLE naip_visual
#     ALTER COLUMN srcimgdate TYPE DATE
# USING to_date(srcimgdate, 'YYYYMMDD');
echo altering dates from varchar to dates
docker exec -it naip-metadata-postgis /bin/bash -c "psql -qtA -d testdb -U user -c \"ALTER TABLE naip_visual ALTER COLUMN verdate TYPE DATE USING to_date(verdate, 'YYYYMMDD'); ALTER TABLE naip_visual ALTER COLUMN srcimgdate TYPE DATE USING to_date(srcimgdate, 'YYYYMMDD');\""

echo finished all tasks!