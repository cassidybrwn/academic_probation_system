% gpa_rules.pl

% Default GPA threshold
:- dynamic default_gpa/1.
default_gpa(2.0).

% Calculate grade points earned for a single module
grade_points_earned(GradePoints, Credits, Earned) :-
    Earned is GradePoints * Credits.

% Calculate total grade points and credits for a list of modules
calculate_totals([], 0, 0).
calculate_totals([(GradePoints, Credits)|Rest], TotalPoints, TotalCredits) :-
    calculate_totals(Rest, RestPoints, RestCredits),
    grade_points_earned(GradePoints, Credits, Earned),
    TotalPoints is RestPoints + Earned,
    TotalCredits is RestCredits + Credits.

% Calculate GPA for a semester
calculate_gpa(TotalGradePoints, TotalCredits, GPA) :-
    TotalCredits > 0,
    GPA is TotalGradePoints / TotalCredits.

% Calculate cumulative GPA
calculate_cumulative_gpa(GPA1, GPA2, CGPA) :-
    CGPA is (GPA1 + GPA2) / 2.

% Check academic probation
check_academic_probation(GPA, probation) :-
    default_gpa(DefaultGPA),
    GPA < DefaultGPA, !.


check_academic_probation(_, good) :- !.
