from edbo.plus.optimizer_botorch import EDBOplus
import sys
import pandas as pd
import os

"""
Initialize here
"""

reaction_components = {
    'Granularity' : ['coarse', 'medium', 'fine'],
    'Pressure[bar]' : [1, 5, 10],
    'Solvent' : ['Solvent A', 'Solvent B', 'Solvent C', 'Solvent D']
}

"""
More initialization -- WIP
"""

"""
Don't edit here
"""

iteration = int(sys.argv[1])
batch_size = int(sys.argv[2])

if iteration == 0: # If this is the first reaction, generates a edbo_helper_file.csv reaction scope, DO NOT DELETE
    EDBOplus().generate_reaction_scope(
        components=reaction_components, 
        filename='edbo_helper_file.csv',
        check_overwrite=False,
        )
    
else:
    df_joint_recommendation = pd.read_csv(f'joint_recommendation{iteration-1}.csv') # Read last iteratino's "joint_recommendation.csv" file
    df_edbo_helper = pd.read_csv('edbo_helper_file.csv') # Read the edbo_helper_file.csv file
    # MERGE the two dataframes on the reaction components using the joint recommendation to fill out PENDING values in edbo_int
    merged_df = pd.merge(df_edbo_helper, df_joint_recommendation, on=list(reaction_components.keys()), how='left', suffixes=('', '_joint_recommendation'))
    df_edbo_helper['Yield'] = merged_df['Yield_joint_recommendation'].combine_first(df_edbo_helper['Yield'])
    df_edbo_helper.to_csv('edbo_helper_file.csv', index=False) # Save the updated edbo_helper_file.csv file


EDBOplus().run( # run one iteration of BO and give recommendations
    filename='edbo_helper_file.csv',  # Previously generated scope.
    objectives=['Yield'],  # Objectives to be optimized.
    objective_mode=['max'],  # Maximize or minimize
    batch=batch_size,  # Number of experiments in parallel that we want to perform in this round.
    columns_features='all', # features to be included in the model.
    init_sampling_method='cvtsampling',  # initialization method.
)

# Take the first batch_size rows and add it to joint_recommendation.
df = pd.read_csv('edbo_helper_file.csv') 
df = df.drop(columns=['priority']) # Drop the priority column
df = df.head(batch_size) # Take the first batch_size rows and add it to join_recommendation.

# Check new file exists, if not then preprocess by adding the old file in here, that way don't have to pickle anything.

# If file exists, add joint_recommendation to t
if os.path.exists(f'joint_recommendation{iteration}.csv'):
    df.to_csv(f'joint_recommendation{iteration}.csv', header=False, mode='a', index=False)
else: # Take previous joint recommendation and add to it at the end
    if iteration > 0:
        old_df = pd.read_csv(f'joint_recommendation{iteration-1}.csv')
        df = pd.concat([old_df, df])
    df.to_csv(f'joint_recommendation{iteration}.csv', mode='a', index=False)