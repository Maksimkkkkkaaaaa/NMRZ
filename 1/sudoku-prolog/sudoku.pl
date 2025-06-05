:- encoding(utf8).
:- use_module(library(clpfd)).

solve_sudoku(Rows) :-
    length(Rows, 9),
    maplist(same_length(Rows), Rows),
    append(Rows, Vs), Vs ins 1..9,

    maplist(all_distinct, Rows),
    transpose(Rows, Columns),
    maplist(all_distinct, Columns),

    Rows = [R1,R2,R3,R4,R5,R6,R7,R8,R9],
    blocks(R1, R2, R3),
    blocks(R4, R5, R6),
    blocks(R7, R8, R9),

    labeling([ff], Vs).  % first_fail: быстро находит одно решение

blocks([], [], []).
blocks([A,B,C|T1], [D,E,F|T2], [G,H,I|T3]) :-
    all_distinct([A,B,C,D,E,F,G,H,I]),
    blocks(T1, T2, T3).

new_sudoku(SolutionRows) :-
    length(R1, 9), length(R2, 9), length(R3, 9),
    length(R4, 9), length(R5, 9), length(R6, 9),
    length(R7, 9), length(R8, 9), length(R9, 9),
    SolutionRows = [R1,R2,R3,R4,R5,R6,R7,R8,R9],
    solve_sudoku(SolutionRows).

mask_template([
    [1,0,0,  0,1,0,  0,0,1],
    [0,1,0,  1,0,1,  0,1,0],
    [0,0,1,  0,1,0,  1,0,0],

    [0,1,0,  1,0,1,  0,1,0],
    [1,0,0,  0,1,0,  0,0,1],
    [0,0,1,  0,1,0,  1,0,0],

    [0,1,0,  1,0,1,  0,1,0],
    [1,0,0,  0,1,0,  0,0,1],
    [0,0,1,  0,1,0,  1,0,0]
]).

apply_mask([], [], []).
apply_mask([FullRow|FRs], [MaskRow|MRs], [PuzzleRow|PRs]) :-
    apply_mask_row(FullRow, MaskRow, PuzzleRow),
    apply_mask(FRs, MRs, PRs).

apply_mask_row([], [], []).
apply_mask_row([V|Vs], [1|Ms], [V|Ps]) :- 
    apply_mask_row(Vs, Ms, Ps).
apply_mask_row([_|Vs], [0|Ms], [0|Ps]) :- 
    apply_mask_row(Vs, Ms, Ps).

run_sudoku :-
    new_sudoku(Full),

    mask_template(Mask),

    apply_mask(Full, Mask, Puzzle),

    nl, write('Игровое поле ( . = пустая клетка, цифры — рандомные подсказки ):'), nl,
    maplist(print_row_puzzle, Puzzle), nl,

    write('Решение (полная сетка):'), nl,
    maplist(print_row_solution, Full), nl.

print_row_puzzle(Row) :-
    maplist(write_cell_puzzle, Row), nl.

write_cell_puzzle(0) :- write('. ').
write_cell_puzzle(N) :- N \= 0, write(N), write(' ').

print_row_solution(Row) :-
    maplist(write_cell_solution, Row), nl.

write_cell_solution(N) :- write(N), write(' ').

:- initialization(run_sudoku, main).
