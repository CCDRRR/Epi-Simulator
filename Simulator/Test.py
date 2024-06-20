import pandas as pd
import matplotlib.pyplot as plt

# 读取结果数据
district_infected = pd.read_csv("results/district_infected_mayor.csv")

# 可视化每个区的感染人数随时间变化
infected_by_district = district_infected[district_infected['State'] == 'Infected'].groupby(['Step', 'DistrictID']).size().unstack(fill_value=0)

plt.figure(figsize=(12, 8))
for district in infected_by_district.columns:
    plt.plot(infected_by_district.index, infected_by_district[district], label=f'District {district}')

plt.xlabel('Step')
plt.ylabel('Number of Infected Agents')
plt.title('Infected Agents by District Over Time')
plt.legend()
plt.show()
