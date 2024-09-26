from baybe.targets import NumericalTarget
from baybe.objectives import SingleTargetObjective
from baybe.parameters import (
    CategoricalParameter,
    NumericalDiscreteParameter,
    SubstanceParameter,
)
from baybe.searchspace import SearchSpace
from baybe import Campaign
import sys
import pandas as pd
import os

# Initialize here -- refer to baybe documentation as needed.

target = NumericalTarget(
    name="Yield",
    mode="MAX",
)
objective = SingleTargetObjective(target=target)

parameters = [
    CategoricalParameter(
        name="Granularity",
        values=["coarse", "medium", "fine"],
        encoding="OHE",  # one-hot encoding of categories
    ),
    NumericalDiscreteParameter(
        name="Pressure[bar]",
        values=[1, 5, 10],
    ),
    SubstanceParameter(
        name="Solvent",
        data={
            "Solvent A": "COC",
            "Solvent B": "CCC",  # label-SMILES pairs
            "Solvent C": "O",
            "Solvent D": "CS(=O)C",
        },
        encoding="MORDRED",  # chemical encoding via mordred package
    ),
]

searchspace = SearchSpace.from_product(parameters)

campaign = Campaign(searchspace, objective)
"""
Don't edit here.
"""

iteration = int(sys.argv[1])
batch_size = int(sys.argv[2])

if iteration == 0:
    df = campaign.recommend(batch_size) # make the recommendation
    df[target.name] = ['PENDING' for _ in range(batch_size)]
else:
    old_df = pd.read_csv(f'joint_recommendation{iteration-1}.csv') # read previous recommendations with updated results.
    campaign.add_measurements(old_df) # add the measuremens to the campaign
    df = campaign.recommend(batch_size)
    df[target.name] = ['PENDING' for _ in range(batch_size)]

if os.path.exists(f'joint_recommendation{iteration}.csv'):
    df.to_csv(f'joint_recommendation{iteration}.csv', header=False, mode='a', index=False)
else:
    if iteration > 0:
        old_df = pd.read_csv(f'joint_recommendation{iteration-1}.csv')
        df = pd.concat([old_df, df])
    df.to_csv(f'joint_recommendation{iteration}.csv', mode='a', index=False)