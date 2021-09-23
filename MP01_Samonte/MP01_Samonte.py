import operator

input_str = ''
gantt_str = '│'
top_border_str = '┌{}┬{}┬{}┐'.format('─' * 7, '─' * 15, '─' * 12) + "\n"
bottom_border_str = '└{}┴{}┴{}┘'.format('─' * 7, '─' * 15, '─' * 12) + "\n"
mid_border_str = '├{}┼{}┼{}┤'.format('─' * 7, '─' * 15, '─' * 12) + "\n"
table_str = "Table: \n" + top_border_str
def main():
    global input_str, gantt_str, table_str
    input_str = ''
    gantt_str = '│'
    top_border_str = '┌{}┬{}┬{}┐'.format('─' * 7, '─' * 15, '─' * 12) + "\n"
    bottom_border_str = '└{}┴{}┴{}┘'.format('─' * 7, '─' * 15, '─' * 12) + "\n"
    mid_border_str = '├{}┼{}┼{}┤'.format('─' * 7, '─' * 15, '─' * 12) + "\n"
    table_str = "Table: \n" + top_border_str
    print("Programmed by: Danielle Samonte")
    print("MP01 - FCFS \n")

    # extract input file
    processes = extract_input()

    # MAIN FCFS
    output_list = fcfs(processes)

    # Table
    create_table(output_list)

    # output everything
    print(input_str)
    print(gantt_str)
    print(table_str)

    rerun_input = ''
    while (rerun_input.lower() != 'n' and rerun_input.lower() != 'y'):
        rerun_input = input("Do you want to run again [y/n]: ")

    main() if rerun_input.lower() == 'y' else append_to_file()


def fcfs(processes):
    global gantt_str
    lbl_str = '0'
    counter = 0
    completed = 0

    # in sequence of process
    output_list = [0] * len(processes)

    while completed != len(processes):
        current = get_process(processes, counter)
        if current == None:
            counter += 1
            gantt_str += "│"
            lbl_str += " "
            continue

        current_index = processes.index(current)

        counter += current[1]
        gantt_str += "{name:^{spacing}}│".format(name = "P" + str(current_index + 1),
                                                spacing = current[1])

        lbl_str += "{ctr:>{spacing}}".format(ctr = counter,
                                            spacing = current[1]+1 if current[1] > 1 else 3)

        output_list[current_index] = (counter - current[0], (counter - current[0]) - current[1])
        processes[current_index] = (current[0], 0)
        completed += 1

    # fix gantt chart
    temp_str = "┌" + ("─" * (len(lbl_str) - 2)) + "┐ \n"
    temp_str2 = "└" + ("─" * (len(lbl_str) - 2)) + "┘ \n"
    gantt_str = "Gantt Chart: \n" + temp_str + gantt_str + "\n" + temp_str2 + lbl_str + '\n'

    return output_list

def extract_input():
    global input_str
    with open("MP01 Checker.txt", "r", encoding="utf-8") as f:
        file_input = f.read().split("\n")

    process_amt = int(file_input[0])
    init_arrival_times = file_input[1].split()
    init_burst_times = file_input[2].split()

    arrival_times = [int(val) for val in init_arrival_times]
    burst_times = [int(val) for val in init_burst_times]


    input_str += "Enter no. of processes: {} \n".format(process_amt)
    input_str += "Arrival Time: \n"
    for i in range(1, process_amt + 1):
        input_str += " P{}: {} \n".format(i, arrival_times[i - 1])

    input_str += "\nBurst Time: \n"
    for i in range(1, process_amt + 1):
        input_str += " P{}: {} \n".format(i, burst_times[i - 1])

    processes = list(zip(arrival_times, burst_times))

    return processes[:process_amt]

def create_table(output_list):
    global table_str, top_border_str, botton_border_str
    table_skeleton = '│{process:^7}│{turnaround:^15}│{waiting:^12}│ \n'
    table_str += table_skeleton.format(process = 'PROCESS',
                                        turnaround = 'TURNAROUND TIME',
                                        waiting = 'WAITING TIME')
    table_str += mid_border_str
    for i in range(1, len(output_list) + 1):
        table_str += table_skeleton.format(process = "P" + str(i),
                                            turnaround = output_list[i - 1][0],
                                            waiting = output_list[i - 1][1])
        table_str += mid_border_str

    total_turnaround = sum([tpl[0] for tpl in output_list])
    total_waiting = sum([tpl[1] for tpl in output_list])

    table_str += table_skeleton.format(process = "TOTAL",
                                        turnaround = total_turnaround,
                                        waiting = total_waiting)

    table_str += mid_border_str

    table_str += table_skeleton.format(process = "AVE",
                                        turnaround = total_turnaround / len(output_list),
                                        waiting = total_waiting / len(output_list) if total_waiting != 0 else 0)

    table_str += bottom_border_str

def append_to_file():
    global input_str, gantt_str, table_str
    with open("MP01 Checker.txt", "a", encoding="utf-8") as f:
        f.write('\n')
        f.write(input_str)
        f.write(gantt_str)
        f.write(table_str)


def get_process(processes, arrival_ctr):
    eligible = [job for job in processes if arrival_ctr >= job[0] and job[1] != 0]
    return sorted(eligible, key=operator.itemgetter(0))[0] if eligible else None


# Rerun prompt
main()
