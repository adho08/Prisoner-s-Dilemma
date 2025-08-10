from strategies import *
from game import PrisonersDilemma as PD

results_path = "../data/results.csv"
results = ""

rounds = 20
repeated = 100
spacing = 20

AC = AlwaysCooperate()
AVR = Average()
ADT = Adapt()
ADT2 = Adapt2()
RND = RandomNeutral()
RNDC = RandomNeutral()
RNDD = RandomDiscrete()
T4T = Tit4Tat()
AD = AlwaysDefect()

PB_strategies: list[PBStrategy] = [AVR, RND]

def main() -> None:
    global results

    print("Games: ")
    strategy1 = PB_strategies[0]
    strategy2 = PB_strategies[1]

    # csv header
    results += f"{strategy1}.parameter, {strategy1}.points, {strategy2}.parameter, {strategy2}.points\n"

    # increment the parameter every time a new ICPD is played
    for parameter_2 in strategy2.parameter_list:
        strategy2.parameter = parameter_2
        for parameter_1 in strategy1.parameter_list:
            strategy1.parameter = parameter_1
            play_ICPD(strategy1, strategy2)
        strategy1.reset_parameter()

    print_in_csv(results)


def play_ICPD(stg1: PBStrategy, stg2: Strategy):
    global results

    # play the ICPD multiple times to smooth out the peaks due to noise
    for _ in range(repeated):

        # the iterated continuous prisoner's dilemma
        for round in range(rounds):
            play_CPD(stg1, stg2, round)

        print(f"\n{stg1}: {stg1.parameter}, {stg2}: {stg2.parameter}")
        print(stg1, stg1.points)
        print(stg2, stg2.points)

        # add the total points gained after the ICPD of both strategies
        results += f"{stg1.parameter}, {stg1.points:0.2f}, {stg2.parameter}, {stg2.points:0.2f}\n"

        stg1.reset()
        stg2.reset()

def play_CPD(stg1: PBStrategy, stg2: Strategy, round: int):
    try:
        m1 = stg1.make_move(round)
        m2 = stg2.make_move(round)
    except ValueError as e:
        print(e)
    else:
        r1, r2 = PD.award_algebraic(m1, m2)
        stg1.update(m1, m2, r1)
        stg2.update(m2, m1, r2)

def print_in_csv(string):
    f = open(results_path, 'w')

    # overwrite the content of the file
    f.write(string)

if __name__ == "__main__":
    main()
