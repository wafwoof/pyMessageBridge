sudo lsof -t -i tcp:8000 | xargs kill -9
ps -a | grep noJared | awk '{print $1}' | xargs kill -9

python3 noJared/noJared.py &
python3 -m uvicorn server:app &