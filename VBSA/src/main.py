from strategies import *
from game import PrisonersDilemma as PD

rounds = 20

AC = AlwaysCooperate()
AVR = Average(8)

PBstrategies: list[PBStrategy] = [AVR]

T4T = Tit4Tat()
AD = AlwaysDefect()

strategies_set: list[Strategy] = [AD]

def main() -> None:

    # every PB-strategy plays the ICPD against every strategy that is in strategies_set
    for i, strategy1 in enumerate(PBstrategies):
        print("\n")
        for j, strategy2 in enumerate(strategies_set):
            print(f"{strategy1} vs. {strategy2}")
            play_ICPD(strategy1, strategy2)
            strategy1.parameter += 1

    print(f"{AVR.points}")   

def play_ICPD(stg1: PBStrategy, stg2: Strategy):
    for round in range(rounds):
        play_CPD(stg1, stg2, round)

def play_CPD(stg1: PBStrategy, stg2: Strategy, round: int):
    m1 = stg1.make_move(round)
    m2 = stg2.make_move(round)

    r1, r2 = PD.award(m1, m2)

    stg1.update(m1, m2, r1)
    stg2.update(m2, m1, r2)

    # print(f"{m1} {stg1.parameter} <-> {m2}")

if __name__ == "__main__":
    main()
