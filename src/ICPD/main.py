# import strategies from strategies directory
from strategies import *
from game import PrisonersDilemma
import csv
import subprocess
import os

# initialize the strategies
AC = AlwaysCooperate()
AD = AlwaysDefect()
AD2 = AlwaysDefect()
T4T = Tit4Tat()
RND = Random()
IN = Inverse()

spacing = 20
rounds = 200

tournament_path = "../../data/tournament.txt"
results_path = "../../data/results.csv"

# Store current directory
original_dir = os.getcwd()
# Get the directory of the R script
r_script_path = "../../data/results.R"  # Path to R script from Python script
r_script_dir = os.path.dirname(os.path.abspath(r_script_path))

# list of all strategies that take participate in the tournament
strategies_list = [AD, AD2, T4T, IN]
    
# initialize the game
PD = PrisonersDilemma(strategies_list)

def main() -> None:
    f = open(tournament_path, 'w')
    f.write("")

    strategies: list[Strategy] = PD.strategies

    print("Games: ")

    # loop through the strategies so every strategy playes against each strategy
    for i in range(len(strategies)):
        for j in range(i, len(strategies)):
            strategy1: Strategy = PD.strategies[i]
            strategy2: Strategy = PD.strategies[j]
            playIPD(strategy1, strategy2)

    # sort the list of strategies based on the points
    print("\nResults: ")

    strategies.sort(reverse=True)
    for index, strategy in enumerate(strategies):
        print(f"{index + 1}. {strategy.name : <{spacing}} {strategy.points : >5}pts")

    # print results in csv file
    printResultsInBarPlot(strategies)

    # Change to the R script's directory
    os.chdir(r_script_dir)
    subprocess.call("Rscript ../data/results.r", shell=True)
    # Return to original directory
    os.chdir(original_dir)


# play the Iterated Prisoner's Dilemma
def playIPD(strategy1: Strategy, strategy2: Strategy):

    printTournamentHeader(strategy1, strategy2)

    strategy1.reset()
    strategy2.reset()
    for i in range(rounds):
        print(f"[{i+1}/{rounds}]\r{strategy1.name} vs. {strategy2.name} ", end='', flush=True)
        playCPD(strategy1, strategy2, i)
    printInTournament("\n")    
    print()


# play one game of Continuous Prisoner's Dilemma
def playCPD(strategy1, strategy2, round):
    move1: float = strategy1.make_move(round=round)
    move2: float = strategy2.make_move(round=round)

    # get the results of the payoff matrix
    result1, result2 = PD.award(move1, move2)

    # updating the strategy
    strategy1.update(move1, move2, result1)
    strategy2.update(move2, move1, result2)

    # print the results in the 'tournament.txt' file
    printInTournament(f"{result1 : ^{spacing}} | {result2 : ^{spacing}}\n")

# print in file
def printTournamentHeader(strategy1: Strategy, strategy2: Strategy) -> None:
    f = open(tournament_path, 'a')
    f.write(f"{strategy1.name : ^{spacing}} | {strategy2.name : ^{spacing}}\n")
    f.write((2 * spacing + 3) * '-')
    f.write('\n')

# print results
def printInTournament(content: str = ""):
    f = open(tournament_path, 'a')
    f.write(content)

# for r to do statistics
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
