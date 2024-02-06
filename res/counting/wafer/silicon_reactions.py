from numba import njit

@njit()
def silicon_reaction(is_add, curr_counter, prev_counter, curr_farr, prev_farr, Ns):
    # Основное вещество (идёт активная реакция)
    if is_add:
        curr_counter += 1
        # print("Села")
    else:
        curr_counter -= 1
        # print("Выбила")
    if curr_counter <= 0:
        curr_farr = 0
        curr_counter = 0

    elif curr_counter >= 2 * Ns[0]:
        prev_farr = 1
        curr_counter = Ns[0]
        prev_counter = Ns[0]

    return curr_counter, prev_counter, curr_farr, prev_farr