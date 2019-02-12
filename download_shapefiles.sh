#!/usr/bin/env bash

STATES=(al ar az ca co ct de fl ga ia id il in ks ky la ma md me mi mn mo ms mt nc nd ne nh nj nm nv ny oh ok or pa ri sc sd tn tx ut va vt wa wi wv wy)
END_YEAR=$(date +'%Y')
FAILING_SHAPEFILES=(naip_3_172_6_fl naip_3_17_2_8_sc naip_3_17_2_2_pa)

for state in "${STATES[@]}"
do
   for year in $(seq 2011 $END_YEAR)
   do
      echo s3 cp s3://naip-visualization/$state/$year/60cm/index/ ./index/  --request-payer --recursive
      # if the bucket doesn't exist these copies won't do anything at all
      aws s3 cp s3://naip-visualization/$state/$year/60cm/index/ ./index/  --request-payer --recursive
      echo s3 cp s3://naip-visualization/$state/$year/100cm/index/ ./index/  --request-payer --recursive
      aws s3 cp s3://naip-visualization/$state/$year/100cm/index/ ./index/  --request-payer --recursive
   done
done