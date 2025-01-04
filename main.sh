
PORT=8888
PID=$(lsof -ti :$PORT)

if [ -n "$PID" ]; then
    echo "Killing process $PID running on port $PORT..."
    kill -9 $PID
else
    echo "No process is running on port $PORT."
fi

python3 src/main.py
cd public && python -m http.server 8888
