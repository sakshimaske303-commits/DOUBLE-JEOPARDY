import pandas as pd

df = pd.read_csv('data/coral_bleaching/canary_dhw_timeseries.csv', skiprows=[1])
df['time'] = pd.to_datetime(df['time'])
df['year'] = df['time'].dt.year

early_avg = df[df['year'] <= 2000]['degree_heating_week'].mean()
recent_avg = df[df['year'] >= 2016]['degree_heating_week'].mean()
max_dhw = df['degree_heating_week'].max()
non_null_count = df['degree_heating_week'].notna().sum()

print(f'Early period avg DHW: {early_avg:.2f}')
print(f'Recent period avg DHW: {recent_avg:.2f}')
print(f'Change: {recent_avg - early_avg:+.2f}')
print(f'Max DHW: {max_dhw:.2f}')
print(f'Non-null: {non_null_count} out of {len(df)}')