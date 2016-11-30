#!/bin/bash
while getopts :masd: testvar; do
	case $testvar in
		m)
			echo "run main"
			m=true
			;;
		a)
			echo "run anim"
			a=true
			;;
		s)
			echo "run small"
			s=true
			;;
		d)
			echo "debug level $OPTARG"
			debug=$OPTARG
			d=true

			;;
		\?)
			echo "Invalid option -$OPTARG" 1>&2
			;;
	esac
done
if [ "$m" = true ]; then
	if [ "$d" = true ]; then
		echo "ran main with debug $debug"
		python testing.py m d $debug >> test.$(date +%Y%m%d%H%M).log 2>&1
	else
		echo "ran main with no debug"
		python testing.py m >> test.$(date +%Y%m%d%H%M).log 2>&1
	fi
elif [ "$a" = true ]; then
	if [ "$d" = true ]; then
		echo "ran anim with debug $debug"
		python testing.py a d $debug >> test.$(date +%Y%m%d%H%M).log 2>&1
	else
		echo "ran anim with no debug"
		python testing.py a >> test.$(date +%Y%m%d%H%M).log 2>&1
	fi
elif [ "$s" = true ]; then
		if [ "$d" = true ]; then
		echo "ran small with debug $debug"
		python testing.py s d $debug >> test.$(date +%Y%m%d%H%M).log 2>&1
	else
		echo "ran small with no debug"
		python testing.py s >> test.$(date +%Y%m%d%H%M).log 2>&1
	fi
elif [ "$d" = true ]; then
	echo "ran with debug $debug"
	python testing.py d $debug >> test.$(date +%Y%m%d%H%M).log 2>&1
else
	echo "ran with no args"
	python testing.py >> test.$(date +%Y%m%d%H%M).log 2>&1
fi
