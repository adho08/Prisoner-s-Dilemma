# import strategies from strategies directory
from strategies import AlwaysCooperate, AlwaysDefect, ForgivingTFT, Strategy, Tit4Tat, Random
from game import PrisonersDilemma
import subprocess
import os
import csv

# initialize the strategies
AC = AlwaysCooperate()
AD = AlwaysDefect()
RND = Random()
T4T = Tit4Tat()
T4T2 = Tit4Tat()
FT4T = ForgivingTFT()

# list of all strategies that take participate in the tournament
strategies_list = [FT4T, AD, T4T]

spacing = 20
rounds = 200

tournament_path = "./../data/tournament.txt"
results_path = "./../data/results.csv"
plot_path = "./../data/plot.png"

# Store current directory
original_dir = os.getcwd()
# Get the directory of the R script
r_script_path = "../data/results.r"  # Path to R script from Python script
r_script_dir = os.path.dirname(os.path.abspath(r_script_path))
plot_abs_path = os.path.abspath(plot_path)

# initialize the game
PD = PrisonersDilemma(strategies_list)

def main() -> None:
    f = open(tournament_path, 'w')
    f.write("")

    strategies: list[Strategy] = PD.strategies

    print("Games: ")

    # Loop through the strategies so every strategy playes against each strategy
    for i in range(len(strategies)):
        for j in range(i, len(strategies)):
            strategy1: Strategy = PD.strategies[i]
            strategy2: Strategy = PD.strategies[j]
            playIPD(strategy1, strategy2)

    print("\nResults: ")

    # Sort the ranking list based on their points
    strategies.sort(reverse=True)
    for index, strategy in enumerate(strategies):
        print(f"{index + 1}. {strategy.name : <{spacing}} {strategy.points : >5}pts")

    # Print results in csv file
    printResultsInBarPlot(strategies)

    # Change to the Rscript's directory
    os.chdir(r_script_dir)
    # Execute results.r in shell
    subprocess.call("Rscript results.r", shell=True)

    print(f"\nPrinting Plot in {plot_abs_path}")

    # Return to original directory
    os.chdir(original_dir)


def playPD(s1: Strategy, s2: Strategy, round) -> None:
    m1 = s1.make_move(round=round)
    m2 = s2.make_move(round=round)
    result1, result2 = PD.award(m1, m2)

    # updating the strategy
    s1.update(m1, m2, result1)
    s2.update(m2, m1, result2)

    # print the results in the 'tournament.txt' file
    printInTournament(f"{result1 : ^{spacing}} | {result2 : ^{spacing}}\n")


def printInTournament(content: str = "") -> None:
    f = open(tournament_path, 'a')
    f.write(content)

# play the Iterated Prisoner's Dilemma
def playIPD(strategy1: Strategy, strategy2: Strategy):

    printTournamentHeader(strategy1, strategy2)

    strategy1.reset()
    strategy2.reset()
    for i in range(rounds):
        print(f"[{i+1}/{rounds}]\r{strategy1.name} vs. {strategy2.name} ", end='', flush=True)
        playPD(strategy1, strategy2, i)
    printInTournament("\n")    
    print()


def printTournamentHeader(s1: Strategy, s2: Strategy) -> None:
    f = open(tournament_path, 'w')
    f.write(f"{s1.name : <{spacing}} | {s2.name : <{spacing}}\n")
    f.write((2 * spacing + 3) * '-')
    f.write('\n')

def printResultsInBarPlot(strategies):
    # clear the file
    f = open(results_path, 'w')
    f.write("")

    # write in form of dictionary the strategies and the points
    f = open(results_path, 'a')
    fieldnames: list[str] = ['strategy', 'points']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    # write the strategies with their points
    for strategy in strategies:
        writer.writerow({'strategy': strategy.name, 'points': strategy.points})


if __name__ == '__main__':
    main()
