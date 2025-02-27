#!/bin/bash
echo "Starting execute.sh"

echo "STUDY_AREA=$STUDY_AREA"
echo "CONFIG=$CONFIG"
echo "INPUT_MOUNT_DIRECTORY=$INPUT_MOUNT_DIRECTORY"
echo "CONFIG_MOUNT_DIRECTORY=$CONFIG_MOUNT_DIRECTORY"
echo "OUTPUT_MOUNT_DIRECTORY=$OUTPUT_MOUNT_DIRECTORY"
echo "DRY_RUN=$DRY_RUN"

# Create a directory to run everything in
mkdir run
cd run

# Get the Hecras executable and study area information from the input bucket.
cp -R $INPUT_MOUNT_DIRECTORY/hecras . 
chmod +x hecras/scripts/*.sh
chmod +x hecras/bin/*

cp -R $INPUT_MOUNT_DIRECTORY/$STUDY_AREA/* hecras/scripts/

# Print the log file for debugging
filename="hecras_log.txt"
touch $filename
tail -f $filename &

# Run CityCat
if [ "$DRY_RUN" == "true" ]; then
echo "Dry run enabled, not running Hecras"
else
    echo "Running hecras"
    echo $pwd
    cd hecras/scripts/
    ./run_unsteady.sh $STUDY_AREA.p04.tmp.hdf x04
fi

# Write to the output bucket
if [ -d "$OUTPUT_MOUNT_DIRECTORY" ]; then
        OUTPUT_DIRECTORY=$OUTPUT_MOUNT_DIRECTORY/$STUDY_AREA
        mkdir -p $OUTPUT_DIRECTORY
        cp $STUDY_AREA.p04.tmp.hdf $OUTPUT_DIRECTORY
else
echo "Directory does not exist: $OUTPUT_MOUNT_DIRECTORY" 
fi

echo "Hecras simulation ended."