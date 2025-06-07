# import strategies from strategies directory
from strategies import Cooperate, Defect
from game import PrisonersDilemma

# initialize the strategies
AC = Cooperate()
AD = Defect()

# initialize the game
PD = PrisonersDilemma(AD, AC)
 
def main():
    s1 = PD.strategy1
    s2 = PD.strategy2

    m1 = s1.make_move()
    m2 = s2.make_move()
    result = PD.award(m1, m2)


    # printing the result

    padding = 14
    print(f"{s1.name : <{padding}} | {s2.name : <{padding}}")
    print((2 * padding + 2) * '-')
    print(f"{result[0] : <{padding}} | {result[1] : <{padding}}")

if __name__ == '__main__':
    main()

