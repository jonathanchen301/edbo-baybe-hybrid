#!/bin/sh

echo "Declare total number of iterations."
read iterations

echo "Declare batch size (use even number) -- number of experiments to do per iteration."
read batch_size

for ((i = 0; i <= iterations; i++)); do

    if [ $i -gt 0 ]; then
        echo "Press ENTER when joint_recommendation.csv has been updated."
        read _
    fi

    # echo "Press ENTER when joint_recommendation.csv has been updated."
    # read _

    conda activate edbo_env && python edbo_init.py $i $batch_size &
    conda activate baybe && python baybe_init.py $i $batch_size &
    wait # Wait for both processes to complete

    python post_process.py $i

done