from numba import njit

@njit()
def silicon_reaction(is_add, curr_counter, prev_counter, curr_farr, prev_farr, Si_num):
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

    elif curr_counter >= 2 * Si_num:
        prev_farr = 1
        curr_counter = Si_num
        prev_counter = Si_num

    return curr_counter, prev_counter, curr_farr, prev_farr