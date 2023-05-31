alias setup_problem='python3 ~/Programming/Competitive-Programming-Scripts/setup_problem.py\
 -problem_file a.cpp ~/Programming/Templates/template_multitest.cpp\
 -problem_file debug.h ~/Programming/Templates/debug.h\
 -problem_file .vscode ~/Programming/Codeforces/.vscode\
 -selenium'

alias fast_setup_problem='python3 ~/Programming/Competitive-Programming-Scripts/setup_problem.py\
 -problem_file a.cpp ~/Programming/Templates/template_multitest.cpp\
 -problem_file debug.h ~/Programming/Templates/debug.h\
 -problem_file .vscode ~/Programming/Codeforces/.vscode'

alias setup_contest='python3 ~/Programming/Competitive-Programming-Scripts/setup_contest.py\
 -problem_file a.cpp ~/Programming/Templates/template_multitest.cpp\
 -problem_file debug.h ~/Programming/Templates/debug.h\
 -contest_file .vscode ~/Programming/Codeforces/.vscode\
 -selenium'

alias fast_setup_contest='python3 ~/Programming/Competitive-Programming-Scripts/setup_contest.py\
 -problem_file a.cpp ~/Programming/Templates/template_multitest.cpp\
 -problem_file debug.h ~/Programming/Templates/debug.h\
 -contest_file .vscode ~/Programming/Codeforces/.vscode'

alias drun='python3 ~/Programming/Competitive-Programming-Scripts/test.py -exec'

alias cmpl='python3 ~/Programming/Competitive-Programming-Scripts/test.py\
 -compiler g++-12 -compile_flags DLOCAL g std=c++20 D_GLIBCXX_DEBUG Wall Wextra -cmpl -exec'

alias bld='python3 ~/Programming/Competitive-Programming-Scripts/test.py\
 -compiler g++-12 -compile_flags DLOCAL g std=c++20 D_GLIBCXX_DEBUG Wall Wextra -exec'

alias fcmpl='python3 ~/Programming/Competitive-Programming-Scripts/test.py\
 -compiler g++-12 -compile_flags DLOCAL O2 std=c++20 -cmpl -exec'

alias fbld='python3 ~/Programming/Competitive-Programming-Scripts/test.py\
 -compiler g++-12 -compile_flags DLOCAL O2 std=c++20 -exec'
