import pandas as pd
import matplotlib.pyplot as plt
from os.path import dirname, abspath, join

REPORT_FILE = join(dirname(abspath(__file__)), "report.csv")

data = pd.read_csv(REPORT_FILE)

data['date'] = pd.to_datetime(data['date'])

data['decimal_hours'] = data['hours'] + data['minutes'] / 60

def format_hours_minutes(value):
    hours = int(value)
    minutes = int((value - hours) * 60)
    return f"{hours}h {minutes}m"

plt.figure(figsize=(10, 6))
plt.plot(data['date'], data['decimal_hours'], marker='o', linestyle='-', color='b', label='Time Spent')

plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: format_hours_minutes(x)))

plt.title('Date vs Time Spent (Hours and Minutes)')
plt.xlabel('Date')
plt.ylabel('Time (Hours and Minutes)')
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()