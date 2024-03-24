alias setup_problem='python3 ~/Programming/Competitive-Programming-Scripts/setup_problem.py\
 -problem_file a.cpp ~/Programming/Algorithm-Library/template_multitest.cpp\
 -problem_file debug.h ~/Programming/Algorithm-Library/debug.h\
 -problem_file .vscode ~/Programming/Codeforces/.vscode\
 -selenium'

alias fast_setup_problem='python3 ~/Programming/Competitive-Programming-Scripts/setup_problem.py\
 -problem_file a.cpp ~/Programming/Algorithm-Library/template_multitest.cpp\
 -problem_file debug.h ~/Programming/Algorithm-Library/debug.h\
 -problem_file .vscode ~/Programming/Codeforces/.vscode'

alias setup_contest='python3 ~/Programming/Competitive-Programming-Scripts/setup_contest.py\
 -problem_file a.cpp ~/Programming/Algorithm-Library/template_multitest.cpp\
 -problem_file debug.h ~/Programming/Algorithm-Library/debug.h\
 -contest_file .vscode ~/Programming/Codeforces/.vscode\
 -selenium'

alias fast_setup_contest='python3 ~/Programming/Competitive-Programming-Scripts/setup_contest.py\
 -problem_file a.cpp ~/Programming/Algorithm-Library/template_multitest.cpp\
 -problem_file debug.h ~/Programming/Algorithm-Library/debug.h\
 -contest_file .vscode ~/Programming/Codeforces/.vscode'

alias drun='python3 ~/Programming/Competitive-Programming-Scripts/test.py'

alias cmpl='python3 ~/Programming/Competitive-Programming-Scripts/test.py\
 -compiler clang++ -flags DLOCAL g std=c++20 D_GLIBCXX_DEBUG Wall Wextra fsanitize=address,undefined,bounds -cmpl'

alias bld='python3 ~/Programming/Competitive-Programming-Scripts/test.py\
 -flags DLOCAL g std=c++20 D_GLIBCXX_DEBUG Wall Wextra fsanitize=address,undefined,bounds -compiler clang++'

alias fcmpl='python3 ~/Programming/Competitive-Programming-Scripts/test.py\
 -compiler clang++ -flags DLOCAL O2 std=c++20 -cmpl'

alias fbld='python3 ~/Programming/Competitive-Programming-Scripts/test.py\
 -flags DLOCAL O2 std=c++20 -compiler clang++'

alias stress_test='python3 ~/Programming/Competitive-Programming-Scripts/stress_test.py'

alias interact='python3 ~/Programming/Competitive-Programming-Scripts/interact.py'
