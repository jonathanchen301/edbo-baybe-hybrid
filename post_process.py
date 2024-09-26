import pandas as pd
import sys

iteration = int(sys.argv[1])

df = pd.read_csv(f'joint_recommendation{iteration}.csv')
df = df.drop_duplicates()
df.to_csv(f'joint_recommendation{iteration}.csv', index=False)