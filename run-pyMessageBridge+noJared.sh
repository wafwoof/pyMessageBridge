echo "Running pyMessageBridge + noJared..."
echo ""
echo "This may ask for your credentials to kill port 8000 (the first time)."
echo "If you are alarmed; feel free to check the commands in this script."
sudo lsof -t -i tcp:8000 | xargs kill -9
ps -a | grep noJared | awk '{print $1}' | xargs kill -9

python3 noJared/noJared.py &
python3 -m uvicorn server:app &