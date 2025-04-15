# import strategies from strategies directory
from strategies import AlwaysCooperate, AlwaysDefect, Tit4Tat, Random
from game import PrisonersDilemma

# initialize the strategies
AC = AlwaysCooperate()
AD = AlwaysDefect()
T4T = Tit4Tat()
RND = Random()

# initialize the game
PD = PrisonersDilemma([AD, T4T, AC])

def main():
    f = open("tournament.txt", 'w')
    f.write("")
    
    rounds = 200

    # loop through the strategies so every strategy playes against each strategy
    for i in range(len(PD.strategies) - 1, 0, -1):
        for j in range(i - 1, -1, -1):
            strategy1 = PD.strategies[i]
            strategy2 = PD.strategies[j]
            playIPD(strategy1, strategy2, rounds)

    # sort the list of strategies based on the points
    for strategy in sorted(PD.strategies):
        print(f"{strategy}: {strategy.points}")


def playIPD(strategy1, strategy2, rounds):
    print(f"{strategy1.name} vs. {strategy2.name}")
    pf(strategy1, strategy2)
    strategy1.reset()
    strategy2.reset()
    for i in range(rounds):
        playPD(strategy1, strategy2, i)


def playPD(strategy1, strategy2, round):
    m1 = strategy1.make_move(round=round)
    m2 = strategy2.make_move(round=round)
    result = PD.award(m1, m2)

    # updating the strategy
    strategy1.update(m1, m2)
    strategy2.update(m2, m1)
    strategy1.points += result[0]
    strategy2.points += result[1]
    pr(result[0], result[1])

def pf(s1, s2):
    f = open("tournament.txt", 'a')
    f.write(f"\n\n{s1}                    {s2}")


def pr(r1, r2):
    f = open("tournament.txt", 'a')
    f.write(f"\n{r1}                    {r2}")

if __name__ == '__main__':
    main()
