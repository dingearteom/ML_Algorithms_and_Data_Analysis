import random
# implementaion of Dawid-Skene algorithm in Croudsourcing for data aggregation
# One of possible usages of EM-algorithm

crowd_labels = open('/home/artem/Desktop/programming/croudsourcing/Hw3/tlkAgg5/TlkAgg5/crowd_labels.tsv', 'r')
golden_labels = open('/home/artem/Desktop/programming/croudsourcing/Hw3/tlkAgg5/TlkAgg5/golden_labels.tsv', 'r')
output_answers = open('/home/artem/Desktop/programming/croudsourcing/Hw3/HW/TlkAgg5/ds.tsv', 'w')

eps = 0.000001
major_vote = {}
K = 5 #catigories
J = 0 # objects
W = 0 # workers
steps = 15 #number of steps of the algorithm

z = {} #distribution of right answers
p = [0 for c in range(K)] #distribution of catigories
e = {} #expertise of workers
y = {} #answers of workers
workers_task = {} #workesrs which performed particular task
tasks_worker = {} #tasks performed by particular worker

stack_t_id = []
stack_w_id = []
stack_answer = []

set_t_id = []
set_w_id = []


initial_z = {}
history_z = [{} for i in range(steps)]
initial_p = [0 for c in range(K)]
history_p = [[0 for c in range(K)] for i in range(steps)]
initial_e = {}
history_e = [{} for i in range(steps)]

def preprocessing():
    votes = {}
    met = {}

    for line in crowd_labels:
        w_id, t_id, answer_str = line.strip().split('\t')
        answer = int(answer_str)
        answer -= 1

        stack_t_id.append(t_id)
        stack_w_id.append(w_id)
        stack_answer.append(answer)

        if (not t_id in met):
            set_t_id.append(t_id)
            met[t_id] = 1
            votes[t_id] = [answer]
        else:
            votes[t_id].append(answer)
    for t_id in set_t_id:
        quantity = [0 for i in range(K)]
        for j in votes[t_id]:
            quantity[j] += 1
        max_quantity = 0
        mv = []
        for j in range(K):
            if (quantity[j] > max_quantity):
                mv.clear()
                mv.append(j)
                max_quantity = quantity[j]
            elif(quantity[j] == max_quantity):
                mv.append(j)
        major_vote[t_id] = mv

def preprocessing_initialization():
    #initialisation J
    """set_t_id.clear()
    met = {}
    for t_id in stack_t_id:
        if (not t_id in met):
            set_t_id.append(t_id)
            met[t_id] = 1"""
    J = len(set_t_id)

    #initialisation W
    met = {}
    for w_id in stack_w_id:
        if (not w_id in met):
            set_w_id.append(w_id)
            met[w_id] = 1
    W = len(set_w_id)

    #intialisation p
    for t_id in set_t_id:
        for answer in major_vote[t_id]:
            p[answer] += 1 / len(major_vote[t_id])
    p[0] /= J
    p[1] /= J

    #initialisation z
    sum_of_votes = {}
    quantity_of_votes = {}
    for t_id in set_t_id:
        z[t_id] = [0 for c in range(K)]
        sum_of_votes[t_id] = [0 for c in range(K)]
        quantity_of_votes[t_id] = 0
    for i in range(len(stack_t_id)):
        t_id = stack_t_id[i]
        answer = stack_answer[i]
        quantity_of_votes[t_id] += 1
        sum_of_votes[t_id][answer] += 1
    for t_id in set_t_id:
        for c in range(K):
            z[t_id][c] = sum_of_votes[t_id][c] / quantity_of_votes[t_id]
    #print_z()

    #intialisation y

    for i in range(len(stack_t_id)):
        t_id = stack_t_id[i]
        w_id = stack_w_id[i]
        answer = stack_answer[i]
        y[(t_id, w_id)] = answer


    # initialisation workers_task
    met.clear()
    for i in range(len(stack_t_id)):
        t_id = stack_t_id[i]
        w_id = stack_w_id[i]
        if (not t_id in met):
            workers_task[t_id] = [w_id]
            met[t_id] = 1
        else:
            workers_task[t_id].append(w_id)

    #initialisation tasks_worker
    met.clear()
    for i in range(len(stack_t_id)):
        t_id = stack_t_id[i]
        w_id = stack_w_id[i]
        if (not w_id in met):
            tasks_worker[w_id] = [t_id]
            met[w_id] = 1
        else:
            tasks_worker[w_id].append(t_id)

    #initialisation e

    e_catigories = {}
    for w_id in set_w_id:
        e_catigories[w_id] = [[0 for k in range(K)] for c in range(K)]
        e[w_id] = [[0 for k in range(K)] for c in range(K)]
    for w_id in set_w_id:
        for t_id in tasks_worker[w_id]:
            for c in range(K):
                for k in range(K):
                    e_catigories[w_id][c][k] += z[t_id][c] * int(y[(t_id, w_id)] == k)

    for w_id in set_w_id:
        for c in range(K):
            sum = 0
            for k in range(K):
                sum += e_catigories[w_id][c][k]
            for k in range(K):
                if (sum != 0):
                    e[w_id][c][k] = e_catigories[w_id][c][k] / sum
                else:
                    e[w_id][c][k] = int(k == c)



def E_step(n_step):
    for t_id in set_t_id:
        probability_of_catigory = [0 for c in range(K)]
        for c in range(K):
            expression = p[c]
            for w_id in workers_task[t_id]:
                expression *= e[w_id][c][y[(t_id, w_id)]]
            if (expression < eps):
                epression = eps
            probability_of_catigory[c] = expression
        sum = 0
        for c in range(K):
            sum += probability_of_catigory[c]
        for c in range(K):
            probability_of_catigory[c] /= sum
            z[t_id][c] = probability_of_catigory[c]

    #debug
    for t_id in set_t_id:
        history_z[n_step][t_id] = [0 for c in range(K)]
        for c in range(K):
            history_z[n_step][t_id][c] = z[t_id][c]
    #print_z()

def M_step(n_step):
    #e
    e_catigories = {}
    for w_id in set_w_id:
        e_catigories[w_id] = [[0 for k in range(K)] for c in range(K)]
    for i in range(len(stack_t_id)):
        t_id = stack_t_id[i]
        w_id = stack_w_id[i]
        for c in range(K):
            for k in range(K):
                e_catigories[w_id][c][k] += z[t_id][c] * (y[(t_id, w_id)] == k)
    for w_id in set_w_id:
        for c in range(K):
            sum = 0
            for k in range(K):
                sum += e_catigories[w_id][c][k]
            for k in range(K):
                if (sum != 0):
                    e[w_id][c][k] = e_catigories[w_id][c][k] / sum
                else:
                    e[w_id][c][k] = int(k == c)

    #p

    for c in range(K):
        p[c] = 0
    for c in range(K):
        for t_id in set_t_id:
            p[c] += z[t_id][c]
        p[c] /= len(set_t_id)

    #debug
    #history_p
    for c in range(K):
        history_p[n_step][c] = p[c]

    #history_e
    for w_id in set_w_id:
        arr = [[0 for k in range(K)] for c in range(K)]
        history_e[n_step][w_id] = arr
        for c in range(K):
            for k in range(K):
                history_e[n_step][w_id][c][k] = e[w_id][c][k]

def ds():
    #debug_initial
    #z
    for t_id in set_t_id:
        initial_z[t_id] = [0 for c in range(K)]
        for c in range(K):
            initial_z[t_id][c] = z[t_id][c]

    #p
    for c in range(K):
        initial_p[c] = p[c]

    #e
    for w_id in set_w_id:
        arr = [[0 for k in range(K)] for c in range(K)]
        initial_e[w_id] = arr
        for c in range(K):
            for k in range(K):
                initial_e[w_id][c][k] = e[w_id][c][k]


    #code
    for i in range(steps):
        E_step(i)
        M_step(i)

def ans(t_id):
    max_ = -1
    answer = -1
    for c in range(K):
        if (z[t_id][c] > max_):
            max_ = z[t_id][c]
            answer = c
    return answer + 1

def print_history(param):

    if (param == 'z'):
        for t_id in set_t_id:
            print("task_id: ", t_id)
            print("initial: ", end="")
            for c in range(K):
                print(initial_z[t_id][c], end=" ")
            print()
            for i in range(steps):
                print(f"step{i}", end=" ")
                for c in range(K):
                    print(history_z[i][t_id][c], end=" ")
                print()
    elif(param == 'p'):
        print("initial_p: ", end="")
        for c in range(K):
            print(initial_p[c], end=" ")
        print()
        for i in range(steps):
            print(f"p_step{i}", end=" ")
            for c in range(K):
                print(history_p[i][c], end=" ")
            print()
    elif(param == 'e'):
        for w_id in set_w_id:
            print("w_id: ", w_id)
            print("tasks_id: ", end="")
            for t_id in tasks_worker[w_id]:
                print(t_id, end=" ")
            print()
            print("initial_e: ")
            for c in range(K):
                for k in range(K):
                    print(initial_e[w_id][c][k], end=" ")
                print()
            print("initial_tasks_z: ")
            for t_id in tasks_worker[w_id]:
                print(t_id, end=" z: ")
                for c in range(K):
                    print(initial_z[t_id][c], end=" ")
                print()
            for n_step in range(steps):
                print(f"e_step{n_step}")
                for c in range(K):
                    for k in range(K):
                        print(history_e[n_step][w_id][c][k], end=" ")
                    print()
                print(f"z_step{n_step}")
                for t_id in tasks_worker[w_id]:
                    print(f"t_id: {t_id}")
                    print("z: ", end="")
                    for c in range(K):
                        print(history_z[n_step][t_id][c], end=" ")
                    print()




def evaluation(write_answer):
    possible_answers = {}
    met = {}
    set_t_id_golden = []
    for line in golden_labels:
        t_id, answer_str = line.strip().split('\t')
        answer = int(answer_str)
        if (not t_id in met):
            met[t_id] = 1
            set_t_id_golden.append(t_id)
            possible_answers[t_id] = [answer]
        else:
            possible_answers[t_id].append(answer)
    right = 0
    for t_id in set_t_id_golden:
        if (ans(t_id) in possible_answers[t_id]):
            right += 1
    print(right / len(set_t_id_golden))
    if (write_answer):
        for t_id in set_t_id_golden:
            output_answers.write(t_id + '\t' + str(ans(t_id)) + '\n')

preprocessing()
preprocessing_initialization()
ds()
#print_history('e')
evaluation(True)
