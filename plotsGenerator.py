import pandas as pd
import json
import matplotlib.pyplot as plt


def generate_plot(file, x_axis, params):
    df = pd.read_csv(file, delimiter='+')

    cost_data = pd.json_normalize(df["cost"].apply(json.loads))
    df = pd.concat([df, cost_data], axis=1)
    df.drop("cost", axis=1, inplace=True)

    print(df)

    df['total_cost'] = df['cable_cost'] + df['host_cost'] + df['router_cost']

    plt.bar(df[x_axis], df['total_cost'])
    plt.xlabel(x_axis)
    plt.ylabel('Total Cost [PLN]')
    plt.title(f'Sum of costs while increasing {x_axis} number\n{params}')
    plt.savefig('plots/sum_of_cost_from_{}.png'.format(x_axis))
    plt.show()


def generate_plot_per_costs(file, x_axis, params):
    df = pd.read_csv(file, delimiter='+')

    cost_data = pd.json_normalize(df["cost"].apply(json.loads))
    df = pd.concat([df, cost_data], axis=1)
    df.drop("cost", axis=1, inplace=True)

    print(df)

    plt.bar(df[x_axis], df['cable_cost'], label='cables costs')
    plt.bar(df[x_axis], df['host_cost'], bottom=df['cable_cost'], label='hosts costs')
    plt.bar(df[x_axis], df['router_cost'], bottom=df['cable_cost']+df['host_cost'], label='routers costs')
    plt.legend()
    plt.xlabel(x_axis)
    plt.ylabel('Cost [PLN]')
    plt.title(f'Costs while increasing {x_axis} number\n{params}')
    plt.savefig('plots/sum_of_cost_from_{}_per.png'.format(x_axis))
    plt.show()


routers_data_file_path = "measurements/changing_routers_no.csv"
channels_data_file_path = "measurements/changing_channels_no.csv"
generate_plot(routers_data_file_path, 'routers', '2 hosts, 1 channel')
generate_plot(channels_data_file_path, 'channels', '2 hosts, 5 routers')
generate_plot_per_costs(routers_data_file_path, 'routers', '2 hosts, 1 channel')
generate_plot_per_costs(channels_data_file_path, 'channels', '2 hosts, 5 routers')
