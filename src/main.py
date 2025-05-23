# import strategies from strategies directory
from strategies import AlwaysCooperate, AlwaysDefect, Tit4Tat, Random
from game import PrisonersDilemma

# initialize the strategies
AC = AlwaysCooperate()
AD = AlwaysDefect()
RND = Random()
T4T = Tit4Tat()
T4T2 = Tit4Tat()

# initialize the game
PD = PrisonersDilemma(T4T, T4T2)

def main():
    s1 = PD.strategy1
    s2 = PD.strategy2
    
    # printing the head of table
    padding = 14
    print(f"{s1.name : <{padding}} | {s2.name : <{padding}}")
    n = 2 * (padding + 2)
    print(n * '-')

    rounds = 200

    for round in range(rounds):
        m1 = s1.make_move(round=round)
        m2 = s2.make_move(round=round)
        result = PD.award(m1, m2)

        # updating the strategy
        s1.update(m1, m2)
        s2.update(m2, m1)
        s1.points += result[0]
        s2.points += result[1]

        print(f"{result[0] : ^{padding}} | {result[1] : ^{padding}}")

    print("\nMax Points:")
    print(f"{s1.name} -> {s1.points} | {s2.name} -> {s2.points}")
    print(f"Winner: {s1.name if s1.points > s2.points else (s2.name if s1.points < s2.points else "Draw")}")


if __name__ == '__main__':
    main()
