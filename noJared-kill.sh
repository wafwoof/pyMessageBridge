 ps -a | grep noJared | awk '{print $1}' | xargs kill -9