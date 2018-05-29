import pandas as pd

df = pd.DataFrame(columns=['Search Method', 'Expansions', 'Goal Tests', 'Plan Length', ' Execution Time', 'Optimality'])

optimality = {
    1: 6,
    2: 9,
    3: 14
}

'''

part 1

'''

for p in [1, 2, 3]:

    data = []
    for s in range(1,8):
        with open(f'results/raw/p_{p}_s_{s}.txt') as fh:
            lines = fh.readlines()

            if len(lines) > 3:

                search_type = lines[1].split(' ')[-1].replace('...', '').rstrip()

                if search_type == 'h_1':
                    search_type = lines[1].split(' ')[-3]


                info = [x for x in lines[4].split(' ') if x != '' and x != '\n']
                expansions = int(info[0])
                goal_tests = int(info[1])

                plan_length = int(lines[6].split(' ')[2])
                time = round(float(lines[6].split(' ')[-1].rstrip()),3)

                optimal = plan_length == optimality[p]

                data.append([search_type, expansions, goal_tests, plan_length, time, optimal])
            else:
                data.append(['--']*6)

    df = pd.DataFrame(data,
                      index=range(1, 8),
                      columns=['Search Method', 'Expansions', 'Goal Tests', 'Plan Length', ' Execution Time',
                               'Optimality'])
    df.to_csv(f'results/part_1/p_{p}.csv', index=False)



'''
part 2
'''

for p in [1, 2, 3]:

    data = []
    for s in range(8,11):
        with open(f'results/raw/p_{p}_s_{s}.txt') as fh:
            lines = fh.readlines()

            if len(lines) > 3:

                search_type = lines[1].split(' ')[-1].replace('...', '').rstrip()

                if 'h_' in search_type:
                    search_type = f"{lines[1].split(' ')[-3]} with {search_type}"

                info = [x for x in lines[4].split(' ') if x != '' and x != '\n']
                expansions = int(info[0])
                goal_tests = int(info[1])

                plan_length = int(lines[6].split(' ')[2])
                time = round(float(lines[6].split(' ')[-1].rstrip()),3)

                optimal = plan_length == optimality[p]

                data.append([search_type, expansions, goal_tests, plan_length, time, optimal])
            else:
                data.append(['--']*6)

    df = pd.DataFrame(data,
                      index=range(3),
                      columns=['Search Method', 'Expansions', 'Goal Tests', 'Plan Length', ' Execution Time',
                               'Optimality'])
    df.to_csv(f'results/part_2/p_{p}.csv', index=False)


