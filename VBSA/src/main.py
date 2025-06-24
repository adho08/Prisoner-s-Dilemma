from strategies import *

T4T = Tit4Tat()
AD = AlwaysDefect()

strategies: list[Strategy] = [T4T, AD]

AC = AlwaysCooperate()
AVR2 = Average2()

strategies_set: list[Strategy] = [AC, AVR2]

def main() -> None:
    

    for i, strategy1 in enumerate(strategies):
        for j, strategy2 in enumerate(strategies_set):
            playICP(strategy1, strategy2)

    print("running main")

def playICP(stg1: Strategy, stg2: Strategy):
    m1 = stg1.make_move()
    m2 = stg2.make_move()


    

if __name__ == "__main__":
    main()
