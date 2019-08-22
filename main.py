import numpy as np
import random
import matplotlib.pyplot as plt


def create_rewards(k):
    r = []
    for _ in range(k):
        r.append(np.random.normal(0, 5))
    print('Actual reward values are',r)
    return r


def generate_rewards(r, index):
    a = np.random.normal(r[index], 1)
    # print('reward is', a)
    return a


def choose_reward(epsilon, greedy_index, counter, r, best_reward):
    a = random.randint(0, 9)
    if counter == 0:
        reward = generate_rewards(r, a)
        best_reward = reward
        chosen_index = a
        return reward, a, best_reward, chosen_index
    else:
        boundary = random.uniform(0,1)
        if boundary > epsilon:
            reward = generate_rewards(r, greedy_index)
            chosen_index = greedy_index
        else:
            while a == greedy_index:
                a = random.randint(0, 9)
            reward = generate_rewards(r, a)
            chosen_index = a
        if reward > best_reward:
            best_reward = reward
            greedy_index = chosen_index
        # print('reward is', reward)
        return reward, greedy_index, best_reward, chosen_index


def update_rewards(reward_estimate, average_reward, reward, chosen_index, counter, reward_count, repetition_index, temp_average_reward):
    # update average reward
    if counter == 0 and repetition_index == 0:
        average_reward[counter] = reward
    elif counter != 0 and repetition_index == 0:
        new_average_reward = average_reward[counter-1] + ((reward - average_reward[counter-1]) / counter)
        average_reward[counter] = new_average_reward
        # print('average reward is', average_reward[counter])
    elif counter == 0 and repetition_index != 0:
        temp_average_reward[counter] = reward
        new_average_reward = average_reward[counter] + ((temp_average_reward[counter] - average_reward[counter]) / repetition_index)
        average_reward[counter] = new_average_reward
    elif repetition_index != 0:
        temp_average_reward[counter] = temp_average_reward[counter-1] + ((reward - temp_average_reward[counter-1]) / counter)
        new_average_reward = average_reward[counter] + ((temp_average_reward[counter] - average_reward[counter]) / repetition_index)
        average_reward[counter] = new_average_reward
    else:
        print('Possible unstable state')

    # update reward estimate
    new_reward_estimate = reward_estimate[chosen_index] + ((reward - reward_estimate[chosen_index]) / reward_count[chosen_index])
    reward_estimate[chosen_index] = new_reward_estimate
    return reward_estimate, average_reward


def main_loop(iterations, epsilon, r, reward_estimate, average_reward, repetition_index, reward_count):
    best_reward = -999999
    greedy_index = 1000
    # runs for loop iteration steps
    temp_average_reward = np.zeros(iterations)
    for i in range(iterations):
        reward, greedy_index, best_reward, chosen_index = choose_reward(epsilon, greedy_index, i, r, best_reward)
        reward_count[chosen_index] += 1
        reward_estimate, average_reward = update_rewards(reward_estimate, average_reward, reward, chosen_index, i, reward_count, repetition_index, temp_average_reward)
    return reward_estimate, average_reward, reward_count


def plot_results(average_reward):
    plt.plot(average_reward)
    plt.show()


def main(iterations, k, type, value, repetitions):
    if type == 'epsilon':
        eps_greedy = value
    # random.seed(123)
    r = create_rewards(k)
    reward_estimate = [0] * k
    reward_count = [0] * k
    average_reward = np.zeros(iterations)
    # runs the test repetition times
    for i in range(repetitions):
        reward_estimate, average_reward, reward_count = main_loop(iterations, eps_greedy, r, reward_estimate, average_reward, i, reward_count)
        # print('{}th repetition done'.format(i))
    print('The reward estimate is', reward_estimate)
    plot_results(average_reward)
    print(reward_count)

if __name__ == "__main__":
    main(iterations=2000, k=10,type='epsilon', value=0.1, repetitions=100)