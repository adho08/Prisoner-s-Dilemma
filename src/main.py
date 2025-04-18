# import strategies from strategies directory
from strategies import AlwaysCooperate, AlwaysDefect, Tit4Tat, Random
from game import PrisonersDilemma
import csv
import subprocess
import os

# initialize the strategies
AC = AlwaysCooperate()
AD = AlwaysDefect()
T4T = Tit4Tat()
RND = Random()

spacing = 20
rounds = 200

tournament_path = "../data/tournament.txt"
results_path = "../data/results.csv"

# Store current directory
original_dir = os.getcwd()
# Get the directory of the R script
r_script_path = "../data/results.R"  # Path to R script from Python script
r_script_dir = os.path.dirname(os.path.abspath(r_script_path))

# list of all strategies that take participate in the tournament
strategies_list = [AC, T4T, AD, RND]
    
# initialize the game
PD = PrisonersDilemma(strategies_list)

def main():
    f = open(tournament_path, 'w')
    f.write("")
    
    print("Games: ")

    # loop through the strategies so every strategy playes against each strategy
    for i in range(len(PD.strategies)):
        for j in range(i, len(PD.strategies)):
            strategy1 = PD.strategies[i]
            strategy2 = PD.strategies[j]
            playIPD(strategy1, strategy2)

    # sort the list of strategies based on the points
    print("\nResults: ")

    strategies = PD.strategies
    strategies.sort(reverse=True)
    for index, strategy in enumerate(strategies):
        print(f"{index + 1}. {strategy.name : <{spacing}} {strategy.points : >5}pts")

    # print results in csv file
    printResults(strategies)

    # Change to the R script's directory
    os.chdir(r_script_dir)
    subprocess.call("Rscript ../data/results.r", shell=True)
    # Return to original directory
    os.chdir(original_dir)


# play the Iterated Prisoner's Dilemma
def playIPD(strategy1, strategy2):

    printTournament(strategy1, strategy2)

    strategy1.reset()
    strategy2.reset()
    for i in range(rounds):
        print(f"[{i+1}/{rounds}]\r{strategy1.name} vs. {strategy2.name} ", end='', flush=True)
        playPD(strategy1, strategy2, i)
    print()


# play one game of Prisoner's Dilemma
def playPD(strategy1, strategy2, round):
    m1 = strategy1.make_move(round=round)
    m2 = strategy2.make_move(round=round)
    result = PD.award(m1, m2)

    # updating the strategy
    strategy1.update(m1, m2)
    strategy2.update(m2, m1)
    strategy1.points += result[0]
    strategy2.points += result[1]
    printTable(result[0], result[1])

# print in file
def printTournament(s1, s2):
    f = open(tournament_path, 'a')
    f.write(f"{s1.name : ^{spacing}} | {s2.name : ^{spacing}}\n")
    f.write((2 * spacing + 2) * '-')
    f.write('\n')

# print results
def printTable(r1, r2):
    f = open(tournament_path, 'a')
    f.write(f"{r1 : ^{spacing}} | {r2 : ^{spacing}}\n")

# for r to do statistics
def printResults(strategies):
    # clear the file
    f = open(results_path, 'w')
    f.write("")

    # write in form of dictionary the strategies and the points
    f = open(results_path, 'a')
    fieldnames = ['strategy', 'points']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    # write the strategies with their points
    for strategy in strategies:
        writer.writerow({'strategy': strategy.name, 'points': strategy.points})

if __name__ == '__main__':
    main()
