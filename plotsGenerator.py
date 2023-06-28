import pandas as pd
import json
import matplotlib.pyplot as plt


def generate_plot(file, x_axis):
    df = pd.read_csv(file, delimiter='+')

    cost_data = pd.json_normalize(df["cost"].apply(json.loads))
    df = pd.concat([df, cost_data], axis=1)
    df.drop("cost", axis=1, inplace=True)

    print(df)

    df['total_cost'] = df['cable_cost'] + df['host_cost'] + df['router_cost']

    plt.bar(df[x_axis], df['total_cost'])
    plt.xlabel('Routers')
    plt.ylabel('Total Cost [PLN]')
    plt.title('Sum of costs while increasing ' + x_axis)
    plt.savefig('plots/sum_of_cost_from_{}.png'.format(x_axis))
    plt.show()


routers_data_file_path = "measurements/changing_routers_no.csv"
channels_data_file_path = "measurements/changing_channels_no.csv"
generate_plot(routers_data_file_path, 'routers')
generate_plot(channels_data_file_path, 'channels')
