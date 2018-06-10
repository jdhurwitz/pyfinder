#bash scripts/iter.sh <foldername> <filetostoreresults> <solver>
#example basch ...... test covtest --cvc
rm scripts/$2_results.txt
SOLVER=${3:-"--z3"} # use z3 by default, but cvc if provided. I assume you know what you're doing.

for file in $1/*
do

    if [[ -f $file ]] && [[ $file =~ \.py$ ]] && [[ $file != "test/filesys.py" ]] && [[ $file != "test/gcd.py" ]] && [[ $file != "fail/git.py" ]] && [[ $file != "pyfinder_tests/custom_tests/int_overflow.py" ]] && [[ $file != "cvc/strstrip.py" ]] ; then
	echo $file
	bash scripts/trycov.sh $file $SOLVER | tail -7 >> scripts/$2_results.txt
	fi
done