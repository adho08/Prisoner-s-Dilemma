# import strategies from strategies directory
from strategies import *
from game import PrisonersDilemma
import csv
import subprocess
import os
import random

# initialize the strategies
AC = AlwaysCooperate()
AD = AlwaysDefect()
AD2 = AlwaysDefect()
T4T = Tit4Tat()
RND = Random()
IN = Inverse()
AVR2 = Average2()
AVR3 = Average3()
AVR5 = Average5()
NTR = Neutral()
T4TB = Tit4TatB()
UTE = Adapt()

# list of all strategies that take participate in the tournament
strategies_list = [UTE, NTR, T4TB, AD, AVR5, AC, T4T]

spacing = 20
rounds = 20

tournament_path = "./../data/tournament.txt"
results_path = "./../data/results.csv"
attributes_path = "./../data/strategies_attributes.csv"

# Store current directory
original_dir = os.getcwd()
# Get the directory of the R script
r_script_path = "../data/results.r"  # Path to R script from Python script
r_script_dir = os.path.dirname(os.path.abspath(r_script_path))
r_script_abs_path = os.path.abspath(r_script_path)
    
# initialize the game
CPD = PrisonersDilemma(strategies_list)

def main() -> None:
    f = open(tournament_path, 'w')
    f.write("")

    strategies: list[Strategy] = CPD.strategies

    print("Games: ")

    try:
        # loop through the strategies so every strategy playes against each strategy
        for i in range(len(strategies)):
            for j in range(i, len(strategies)):
                strategy1: Strategy = CPD.strategies[i]
                strategy2: Strategy = CPD.strategies[j]
                playICPD(strategy1, strategy2)

    except Exception as e:
        print(e.args[0])
        print(f"Concerned strategy: {e.args[1]}")

    else:

        # sort the list of strategies based on the points
        print("\nResults: ")

        strategies.sort(reverse=True)
        for i, strategy in enumerate(strategies):
            print(f"{i + 1}. {strategy: <{spacing}} {strategy.points : >5}pts")

        # print results in csv file
        printResultsInCSV(strategies)
        # print attributes in csv file
        printAttributesInCSV(strategies)

        # Change to the Rscript's directory
        os.chdir(r_script_dir)
        # Execute results.r in shell
        subprocess.call("Rscript results.r", shell=True)
        # Return to original directory
        os.chdir(original_dir)

        print(f"\nPrinting Plot in {r_script_abs_path}")

# play the Iterated Prisoner's Dilemma
def playICPD(strategy1: Strategy, strategy2: Strategy):

    printTournamentHeader(strategy1, strategy2)

    strategy1.reset()
    strategy2.reset()
    # play the CPD rounds times
    for i in range(rounds):
        print(f"[{i+1}/{rounds}]\r{strategy1.name} vs. {strategy2.name} ", end='', flush=True)
        playCPD(strategy1, strategy2, i)

    printInTournament("\n")    
    print()


# play one game of Continuous Prisoner's Dilemma
def playCPD(strategy1, strategy2, round):
    move1: float = strategy1.make_move(round=round)
    move2: float = strategy2.make_move(round=round)

    try:
        # get the results of the payoff matrix
        result1, result2 = CPD.award(move1, move2)
    except ValueError as e:
        # if move1 or move2 was out of range (0, 1), raise an exception
        raise Exception(e.args[0], strategy1 if e.args[1] == 'x' else strategy2)
    else:
        # updating the strategymai
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
def printResultsInCSV(strategies):
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

# for r to do statistics
def printAttributesInCSV(strategies):
    # clear the file
    f = open(attributes_path, 'w')
    f.write("")

    # write in form of dictionary the strategies and their attributes
    f = open(attributes_path, 'a')
    fieldnames: list[str] = ['strategy', 'nice', 'retaliates', 'forgiving', 'envious']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    # write the strategies and their attributes
    for strategy in strategies:
        writer.writerow({'strategy': strategy.name, 'nice': strategy.isNice, 'retaliates': strategy.retaliates, 'forgiving': strategy.isForgiving, 'envious': strategy.isEnvious})

if __name__ == '__main__':
    main()
