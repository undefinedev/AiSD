import sys
import os
import time
testTimes = {}
testResults = {}

def test(file):
    sys.stdin = open('input/{}'.format(file), "r", encoding="utf8")
    sys.stdout = open('output/{}'.format(file), "w", encoding="utf8")
    import program
    startTime = time.time()
    try:
        program.main()
    except Exception as e:
        print("ERROR:", e)
    endTime = time.time()
    testTimes[file] = (endTime-startTime)
    sys.stdout = sys.__stdout__
    sys.stdin = sys.__stdin__

inputs = next(os.walk(os.path.join('input')), (None, None, []))[2]

print("Testing")
for file in inputs:
    test(file)
    time.sleep(0.05)

print("Writing timings")

sys.stdout = open('output/{}'.format("timings.txt"), "w", encoding="utf8")
for _ in testTimes.keys():
    print("{} {}".format(_, testTimes[_]))
sys.stdout = sys.__stdout__

print("Comparing results")

answers = next(os.walk(os.path.join('answers')), (None, None, []))[2]
output = next(os.walk(os.path.join('answers')), (None, None, []))[2]
for f1, f2 in zip(answers, output):
    with open("answers/{}".format(f1), "r") as ff1:
        d1 = ff1.readlines()
    with open("output/{}".format(f2), "r") as ff2:
        d2 = ff2.readlines()
    if len(d1) != len(d2):
        testResults[f2] = "WRONG"
        continue
    for _ in range(len(d1)):
        if d1[_] != d2[_]:
            testResults[f2] = "WRONG"
            break
    else:
        testResults[f2] = "ok"

sys.stdout = open('output/{}'.format("results.txt"), "w", encoding="utf8")
for _ in testResults.keys():
    print("{} {}".format(_, testResults[_]))
sys.stdout = sys.__stdout__
