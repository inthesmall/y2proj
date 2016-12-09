#!/bin/bash
while getopts :masptcd: testvar; do
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
		p)
			echo "run physics"
			p=true
			;;
		t)
			echo "run timing test"
			t=true
			;;
		c)
			echo "run conservation test"
			c=true
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
elif [ "$p" = true ]; then
		if [ "$d" = true ]; then
		echo "ran physics with debug $debug"
		python testing.py p d $debug >> test.$(date +%Y%m%d%H%M).log 2>&1
	else
		echo "ran physics with no debug"
		python testing.py p >> test.$(date +%Y%m%d%H%M).log 2>&1
	fi
elif [ "$t" = true ]; then
	if [ "$d" = true ]; then
		echo "ran timing with debug $debug"
		python testing.py t d $debug >> test.$(date +%Y%m%d%H%M).log 2>&1
	else
		echo "ran timing with no debug"
		python testing.py t >> test.$(date +%Y%m%d%H%M).log 2>&1
	fi
elif [ "$c" = true ]; then
	if [ "$d" = true ]; then
		echo "ran conservation with debug $debug"
		python testing.py c d $debug >> test.$(date +%Y%m%d%H%M).log 2>&1
	else
		echo "ran conservation with no debug"
		python testing.py c >> test.$(date +%Y%m%d%H%M).log 2>&1
	fi
elif [ "$d" = true ]; then
	echo "ran with debug $debug"
	python testing.py d $debug >> test.$(date +%Y%m%d%H%M).log 2>&1
else
	echo "ran with no args"
	python testing.py >> test.$(date +%Y%m%d%H%M).log 2>&1
fi
