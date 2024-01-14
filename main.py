import random

dataSet = []
training = []
test = []
dec_pres = {}

unique_values = []
translator = {}


def get_data():
    with open("car_evaluation.data") as data:
        car_lines = data.readlines()
        for line in car_lines:
            dataSet.append(line.replace("\n", "").split(","))
        shuffle_split_data()


def shuffle_split_data():
    random.shuffle(dataSet)
    for i in range(len(dataSet)):
        if i < 0.7 * len(dataSet):
            training.append(dataSet[i])
        else:
            test.append(dataSet[i])


def check_presence():
    for i in range(len(training)):
        if training[i][-1] in dec_pres.keys():
            dec_pres[training[i][-1]] += 1
        else:
            dec_pres[training[i][-1]] = 1
    keyset = list(dec_pres)
    for i in range(len(keyset)):
        translator[i] = keyset[i]

    for i in range(len(training[1]) - 1):
        temp = [x for x in [line[i] for line in training]]
        unique_values.append(set(temp))


def classify():
    correct = 0
    incorrect = 0
    get_data()
    check_presence()
    keysetlen = len(dec_pres.keys())
    keyset = list(dec_pres.keys())
    print(dec_pres)
    probabilities = [1, 1, 1, 1]

    for row in test:
        test_presence = [[], [], [], []]

        for j in range(keysetlen):
            for i, variable in enumerate(row):
                test_presence[j].append(len([x for x in training if variable == x[i] and x[-1] == keyset[j]]))

        for i in range(len(list(dec_pres.keys()))):
            for j in range(len(training[1]) - 1):
                if test_presence[i][j] == 0 or dec_pres.get(keyset[i]) == 0:
                    probabilities[i] *= 1 / (dec_pres.get(keyset[i]) + len(unique_values[j]))
                else:
                    probabilities[i] *= test_presence[i][j] / dec_pres.get(keyset[i])
            probabilities[i] *= dec_pres.get(keyset[i]) / len(training)
        ans_prob = max(probabilities)

        tmpdict = {}
        for i in range(keysetlen):
            tmpdict[probabilities[i]] = i
        ans = tmpdict.get(ans_prob)

        if row[-1] == translator.get(ans):
            correct += 1
            print(translator.get(ans), "- Correct")
        else:
            incorrect += 1
            print(translator.get(ans), "- Incorrect", "real: ", row[-1])

        probabilities = [1, 1, 1, 1]
    print("Accuracy: ", correct / (correct + incorrect) * 100)


if __name__ == '__main__':
    classify()
