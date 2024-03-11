
# example() goes through a single contest of length t (user input)
# with t bets (so i = 0, ..., t) of specified size (user input)
# on either A or B (user input)
# by one of C, D, F, or G (user input).
# at the end the total winnings of each of C, D, F, G are printed,
# and if the user elects for verbose printing lots more too.
# example(shortcut) skips the user inputs to print the final calculations.
def example(shortcut = None):
    print("Token names are A and B, people names are C, D, F, and G.")
    print()

    ns = [0, 0]
    vs = [0, 0]
    rolling_winnings = {"C" : 0, "D" : 0, "F" : 0, "G" : 0}
    
    if shortcut is None:
        #Ask to see how much to print
        verboseness = input("Verbose output? T or F: ")
        while verboseness not in ["T", "F"]:
            verboseness = input("Verbose output? T or F: ")
    else:
        verboseness = shortcut["verboseness"]
    verbose = True if verboseness == "T" else False
    print()
    
    if shortcut is None:
        # Ask for number of time steps in the example
        t = int(input("Number of time steps for illustrative purposes: "))
    else:
        t = shortcut["t"]

    print("Betting period.")
    print()
    if shortcut is None:
        events = []
        for i in range(t):
            print()
            print(f"Time step {i}.")
            # Ask for i-th bet
            bettor = input("Who's betting: ")
            while bettor not in ["C", "D", "F", "G"]:
                print("(Something wrong w bettor name --- try again.)")        
                bettor = input("Who's betting: ")
            which_token = input("Which token: ")
            while which_token not in ["A", "B"]:
                print("(Something wrong w token name --- try again.)")
                which_token = input("Which token: ")
            token_index = 0 if which_token == "A" else 1
            opposite_index = 1 - token_index
            bet = float(input("How many tokens: "))
            vs[0] = float(input("Current value of one A token: "))
            vs[1] = float(input("Current value of one B token: "))
            bet_coefficient = (vs[token_index] * bet) * (1 + ns[opposite_index] * vs[opposite_index]) / (1 + ns[token_index] * vs[token_index])
            ns[token_index] += bet
            events.append((bettor, token_index, bet, bet_coefficient))
            if verbose:
                print((bettor, token_index, bet, bet_coefficient))
        if verbose:
            print()
    else:
        events = shortcut["events"]
        for i in range(t):
            bettor, token_index, bet, bet_coefficient = events[i]
            opposite_index = 1 - token_index
            ns[token_index] += bet
            if verbose:
                print((bettor, token_index, bet, bet_coefficient))
        if verbose:
            print()


    if shortcut is None:
        # Ask for final values
        vs[0] = float(input("Final value of one A token: "))
        vs[1] = float(input("Final value of one B token: "))
        print()
    else:
        vs[0] = shortcut["final_vs"][0]
        vs[1] = shortcut["final_vs"][1]

    winner = 0 if ns[0] * vs[0] >= ns[1] * vs[1] else 1
    loser = 1 - winner
    print(f"Contest over! The winner is { {0 : "A", 1 : "B"}[winner] }.")
    print()

    total_bet_coefficient = 0
    for i in range(t):
        bettor, token_index, bet, bet_coefficient = events[i]
        if token_index == winner:
            total_bet_coefficient += bet_coefficient

    for i in range(t):
        bettor, token_index, bet, bet_coefficient = events[i]
        if token_index == winner:
            rolling_winnings[bettor] += 0.98 * (bet * vs[winner])
            rolling_winnings[bettor] += 0.98 * (bet_coefficient / total_bet_coefficient) * (ns[loser] * vs[loser])
            if verbose:
                print(f"{ {"C" : "Charlie", "D" : "David", "F" : "Frank", "G" : "George"}[bettor] } wins {0.98} * {bet} = {0.98 * bet} of { {0 : "A", 1 : "B"}[winner] },", end = "")
                print(f"\n     and {0.98} * {bet_coefficient} / {total_bet_coefficient} * ({ns[loser]}) = {0.98 * (bet_coefficient / total_bet_coefficient) * ns[loser]} of { {0 : "A", 1 : "B"}[loser] }.", end = "\n")
                print()

    print(f"Charlie gets {rolling_winnings["C"]} SOL,")
    print(f"David gets {rolling_winnings["D"]} SOL.")        
    print(f"Frank gets {rolling_winnings["F"]} SOL.")        
    print(f"George gets {rolling_winnings["G"]} SOL.")

if __name__ == "__main__":
    # the example in the Google doc:
    print("\n\n--- Google doc example. ---\n")
    example(
        shortcut = {
            "verboseness" : "T",
            "t" : 4,
            "events" : [
                ["C", 0, 4, 4],
                ["D", 1, 3, 30],
                ["F", 0, 2, 3.818],
                ["G", 1, 3.5, 9.545]
            ],
            "final_vs" : [1.5, 1.5],
            })
    # a user-input example:
    print("\n\n--- User-input example. ---\n")
    example()
