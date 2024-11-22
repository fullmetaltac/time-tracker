import pandas as pd
import matplotlib.pyplot as plt
from os.path import dirname, abspath, join

REPORT_FILE = join(dirname(abspath(__file__)), "report.csv")

data = pd.read_csv(REPORT_FILE)
data['date'] = pd.to_datetime(data['date'])
data['decimal_hours'] = data['hours'] + data['minutes'] / 60

plt.figure(figsize=(12, 6))
plt.bar(data['date'], data['decimal_hours'], color='skyblue', edgecolor='black', alpha=0.7)

plt.title('Date vs Time Spent (Hours and Minutes)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Time Spent (Hours)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()