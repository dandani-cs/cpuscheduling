import operator, os, stat


def extract_input():
    global input_str, orig_burst
    with open("MP04 Checker.txt", "r", encoding="utf-8") as f:
        file_input = f.read().split("\n")

    process_amt = int(file_input[0])
    init_arrival_times = file_input[1].split()
    init_burst_times = file_input[2].split()
    init_priorities = file_input[3].split()
    init_classification = file_input[4].split()
    fp_algo = int(file_input[5])
    bg_algo = int(file_input[6])

    process_names = ["P" + str(i) for i in range(1, process_amt + 1)]
    arrival_times = [int(val) for val in init_arrival_times]
    burst_times = [int(val) for val in init_burst_times]
    priorities = [int(val) for val in init_priorities]
    classifications= [int(val) for val in init_classification]

    input_str += "Enter no. of processes: {} \n".format(process_amt)
    input_str += "Arrival Time: \n"
    for i in range(1, process_amt + 1):
        input_str += " P{}: {} \n".format(i, arrival_times[i - 1])

    input_str += "\nBurst Time: \n"
    for i in range(1, process_amt + 1):
        input_str += " P{}: {} \n".format(i, burst_times[i - 1])

    input_str += "\nPriority: \n"
    for i in range(1, process_amt + 1):
        input_str += " P{}: {} \n".format(i, priorities[i - 1])

    input_str += "\nClassification(1-FP/2-BP):\n"
    for i in range(1, process_amt + 1):
        input_str += " P{}: {} \n".format(i, classifications[i - 1])

    input_str += """\nAlgorithm Choices:
 1. FCFS
 2. SJF-P
 3. SJF-NP
 4. P-P
 5. P-NP
 6. RR\n"""

    input_str += "\nForeground Process: " + str(fp_algo) + "\n"
    input_str += "Background Process: " + str(bg_algo) + "\n"

    for i in range(process_amt):
        orig_burst[process_names[i]] = burst_times[i]

    processes = [list(a) for a in zip(process_names, arrival_times, burst_times, priorities, classifications)]

    return processes[:process_amt]

def multilevel_queue(processes):
    global gantt_str, gantt_borders, lbl_str, orig_burst
    counter = 0
    completed = 0
    previous = None
    streak = 0

    output_dict = {}

    fg_processes = [p for p in processes if p[4] == 1]
    bg_processes = [p for p in processes if p[4] == 2]

    while completed != len(processes):
        # process name, arrival, burst, priority, classification
        current = get_process(fg_processes, counter, 3)

        if not current:
            current = get_process(bg_processes, counter, 2)

        if current[4] == 1:
            previous, streak, current, counter = priority_preemptive(previous, streak, current, counter)
        if current[4] == 2:
            previous, streak, current, counter = sjf_np(previous, streak, current, counter)


        if current[2] == 0:
            output_dict[current[0]] = (counter - current[1], (counter - current[1]) - orig_burst[current[0]])
            completed += 1

    gantt_update(previous, streak, counter, True)

    # gantt_borders = gantt_borders[:-1]

    gantt_str = '┌' + gantt_borders.replace('*', '┬') + '┐\n' + gantt_str + '\n└' +  gantt_borders.replace('*', '┴') + '┘\n' + lbl_str + '\n'

    return output_dict

def priority_preemptive(previous, streak, current, counter):
    if previous != current[0]:
        if streak != 0:
            gantt_update(previous, streak, counter, False)
        previous = current[0]
        streak = 0
    current[2] -= 1
    streak += 1

    counter += 1

    return previous, streak, current, counter

def sjf_np(previous, streak, current, counter):
    # process name, arrival, burst, priority, classification
    if previous != current[0]:
        if streak != 0:
            gantt_update(previous, streak, counter, False)
        previous = current[0]
        streak = 0
    current[2] -= 1
    streak += 1

    counter += 1

    return previous, streak, current, counter


def gantt_update(previous, streak, counter, end):
    global gantt_str, gantt_borders, lbl_str

    gantt_str += "{prev:^{spacing}}│".format(prev = previous,
                                                spacing = streak if streak > 1 else streak + 1)
    gantt_borders += ("─" * streak) if streak > 1 else ("─" * (streak + 1))
    lbl_str += "{ctr:>{spacing}}│".format(ctr = counter,
                                            spacing = streak if streak > 1 else streak + 1)

    if not end:
        gantt_borders += '*'


def get_process(processes, arrival_ctr, classification):
    # process name, arrival, burst, priority
    eligible = [job for job in processes if arrival_ctr >= job[1] and job[2] != 0]
    return sorted(eligible, key=operator.itemgetter(classification, 0))[0] if eligible else None


def tabulate(output_dict):
    global table_str
    border_str = '{}*{}*{}'.format('─' * 7, '─' * 15, '─' * 12)
    table_skeleton = '│{process:^7}│{turnaround:^15}│{waiting:^12}│ \n'
    table_str += table_skeleton.format(process = 'PROCESS',
                                        turnaround = 'TURNAROUND TIME',
                                        waiting = 'WAITING TIME')
    table_str += '├' + border_str.replace('*', '┼') + '┤\n'
    for i in range(1, len(output_dict) + 1):
        table_str += table_skeleton.format(process = "P" + str(i),
                                            turnaround = output_dict["P" + str(i)][0],
                                            waiting = output_dict["P" + str(i)][1])
        table_str += '├' + border_str.replace('*', '┼') + '┤\n'

    total_turnaround = sum([val[0] for key, val in output_dict.items()])
    total_waiting = sum([val[1] for key, val in output_dict.items()])

    table_str += table_skeleton.format(process = "TOTAL",
                                        turnaround = total_turnaround,
                                        waiting = total_waiting)

    table_str += '├' + border_str.replace('*', '┼') + '┤\n'

    table_str += table_skeleton.format(process = "AVERAGE",
                                        turnaround = total_turnaround / len(output_dict),
                                        waiting = total_waiting / len(output_dict))

    table_str = '┌' + border_str.replace('*', '┬') + '┐\n' + table_str + '└' + border_str.replace('*', '┴') + '┘\n'


def append_to_file():
    global input_str, gantt_str, table_str
    # os.chmod(resource_path("MP02 Checker.txt"), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    try:
        with open("MP04 Checker.txt", "a", encoding="utf-8") as f:
            f.write('\n')
            f.write(input_str)
            f.write(gantt_str)
            f.write(table_str)
    except Exception as e:
        print(e)
        print("If the error is permission denied, please disable your antivirus")
        checker = input("Press any key to continue")


def main():
    while True:
        # main program
        global input_str, orig_burst, gantt_str, gantt_borders, lbl_str, table_str

        input_str = "Programmed by: Danielle Samonte \nMP04 - MULTILEVEL QUEUE ALGORITHM\n"
        orig_burst = {}
        gantt_str = '│'
        gantt_borders = ''
        lbl_str = '0'
        table_str = ''

        processes = extract_input()

        output = multilevel_queue(processes)

        tabulate(output)

        gantt_str = "\nGantt Chart\n" + gantt_str
        table_str = "\nTable\n" + table_str
        print(input_str)
        print(gantt_str)
        print(table_str)

        while True:
            answer = str(input('Do you want to run again [y/n]: ')).lower()
            if answer in ('y', 'n'):
                break
        if answer == 'y':
            continue
        else:
            append_to_file()
            break

main()
