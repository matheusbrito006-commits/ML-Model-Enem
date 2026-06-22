import pandas as pd

df = pd.read_csv('simulados_clean.csv')
df['created_at'] = pd.to_datetime(df['created_at'])

df['cluster_size'] = df.groupby(['aluno_id', 'created_at'])['created_at'].transform('size')
print(df['cluster_size'].value_counts())

# split into two groups: rows that are already unique, and rows that need collapsing
unique_rows = df[df['cluster_size'] == 1].copy()
# .copy() avoids a pandas warning about modifying a view of the original dataframe later
clustered_rows = df[df['cluster_size'] > 1].copy()

print("Unique rows: ", len(unique_rows))
print("Clustered rows (before collapsing): ", len(clustered_rows))

areas = ['matematica', 'linguagens', 'humanas', 'natureza']

collapsed = clustered_rows.groupby(['aluno_id', 'created_at'], as_index=False)[areas].mean()

print("Collapsed clusters (should be ~17 rows):")
print(collapsed)

unique_trimmed = unique_rows[['aluno_id', 'created_at'] + areas]
final_df = pd.concat([unique_trimmed, collapsed], ignore_index=True)
final_df = final_df.sort_values(['aluno_id', 'created_at']).reset_index(drop=True)
fully_empty = final_df[areas].isnull().all(axis=1)
print("Dropping", fully_empty.sum(), "fully empty rows")

final_df = final_df[~fully_empty].reset_index(drop=True)

print("Row count after dropping empty rows:", len(final_df))

print("Final row count:", len(final_df))
print(final_df.head(15))

# check: does every (aluno_id, created_at) pair now appear only once?
duplicate_check = final_df.duplicated(subset=['aluno_id', 'created_at'], keep=False)
print("Remaining duplicate timestamps:", duplicate_check.sum())

final_df.to_csv('simulados_paired_ready.csv', index=False)
print("Saved simulados_paired_ready.csv")