from strategies import *
from game import PrisonersDilemma as PD
import csv

results_path = "../data/results.csv"
results = ""

rounds = 20
increment_rounds = 7
spacing = 20

AC = AlwaysCooperate()
AVR = Average(2)
ADT = Adapt(1)
RND = Random(1)

PBstrategies: list[PBStrategy] = [AVR, RND]

T4T = Tit4Tat()
AD = AlwaysDefect()

strategies_set: list[Strategy] = [AD]

def main() -> None:

    print("Games: ")
    strategy1 = PBstrategies[0]
    strategy2 = PBstrategies[1]
            # increment the parameter every time a new ICPD is played
    for _ in range(increment_rounds):
        for _ in range(increment_rounds):
            # print(f"{strategy1} vs. {strategy2}")
            play_ICPD(strategy1, strategy2)
            strategy1.parameter += 1
            print(strategy1, strategy1.points)
            print(strategy2, strategy2.points)
            strategy1.reset()
            strategy2.reset()
        strategy2.parameter += 1
        strategy1.reset_parameter()


    # print("\n")
    # print("Results: ")
    # for i, strategy in enumerate(PBstrategies):
    #     print(f"{i + 1}. {strategy : <{spacing}} {strategy.points : >5}pts")

    printInCSV(results)

def play_ICPD(stg1: PBStrategy, stg2: Strategy):
    print(f"\n{stg1}: {stg1.parameter}, {stg2}: {stg2.parameter}")
    for round in range(rounds):
        play_CPD(stg1, stg2, round)

def play_CPD(stg1: PBStrategy, stg2: Strategy, round: int):
    global results

    try:
        m1 = stg1.make_move(round)
        m2 = stg2.make_move(round)
    except ValueError as e:
        print(e)
    else:
        r1, r2 = PD.award_algebraic(m1, m2)
        stg1.update(m1, m2, r1)
        stg2.update(m2, m1, r2)
        results += f"{stg1.parameter}, {r1}, {stg2.parameter}, {r2}\n"

def printInCSV(string):
    f = open(results_path, 'w')

    # deleting content of file
    f.write(string)

if __name__ == "__main__":
    main()
