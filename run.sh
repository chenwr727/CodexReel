#!/bin/bash

# Load conda environment
source /root/miniconda3/etc/profile.d/conda.sh
conda activate notebook

# Define service commands
STREAMLIT_SERVICE="streamlit run web.py"
APP_SERVICE="uvicorn app:app"

# Define ports and workers
STREAMLIT_PORT=80
APP_PORT=8000
APP_WORKERS=4

# Function to start services
start_services() {
    echo "Starting Streamlit service on port $STREAMLIT_PORT..."
    nohup $STREAMLIT_SERVICE --server.port $STREAMLIT_PORT > /dev/null 2>&1 &
    STREAMLIT_PID=$!
    echo "Streamlit service started with PID $STREAMLIT_PID."

    echo "Starting App service on port $APP_PORT..."
    nohup $APP_SERVICE --host 0.0.0.0 --port $APP_PORT --workers $APP_WORKERS > /dev/null 2>&1 &
    APP_PID=$!
    echo "App service started with PID $APP_PID."

    echo "Services started."
}

# Function to stop services
stop_services() {
    echo "Stopping Streamlit service..."
    if pgrep -f "$STREAMLIT_SERVICE" > /dev/null; then
        pkill -f "$STREAMLIT_SERVICE"
        echo "Streamlit service stopped."
    else
        echo "Streamlit service not running."
    fi

    echo "Stopping App service..."
    if pgrep -f "$APP_SERVICE" > /dev/null; then
        pkill -f "$APP_SERVICE"
        echo "App service stopped."
    else
        echo "App service not running."
    fi

    echo "Services stopped."
}

# Function to restart services
restart_services() {
    stop_services
    start_services
}

# Main script logic
case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0