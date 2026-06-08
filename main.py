import streamlit as st
import queue
import time
import cv2
import sys
import threading
import os

# Add the parent directory to sys.path to allow imports from SafeGuardAI package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SafeGuardAI import config
from SafeGuardAI.capture.producer import VideoProducer
from SafeGuardAI.analysis.consumer import VideoConsumer
from SafeGuardAI.core.metrics import MetricsManager
from SafeGuardAI.ui import dashboard

# Streamlit Page Config - Moved inside main to avoid context errors on raw run
# st.set_page_config(layout="wide", page_title="SafeGuard AI")

@st.cache_resource
def start_system():
    # Queues
    frame_queue = queue.Queue(maxsize=2)
    result_queue = queue.Queue(maxsize=2)
    
    # Metrics
    metrics_manager = MetricsManager()
    
    # Threads
    # Only start threads once; st.cache_resource handles singleton behavior
    producer = VideoProducer(frame_queue)
    producer.start()
    
    consumer = VideoConsumer(frame_queue, result_queue, metrics_manager) 
    consumer.start()
    
    return producer, consumer, result_queue, metrics_manager

def main():
    st.set_page_config(layout="wide", page_title="SafeGuard AI")
    st.markdown("""
        <style>
        .css-18e3th9 {
            padding-top: 0rem;
        }
        .block-container {
            padding-top: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Live Monitor", "Customer Registration"])
    
    # Start system in background (always running for now)
    producer, consumer, result_queue, metrics_manager = start_system()

    if page == "Live Monitor":
        from SafeGuardAI.ui import dashboard
        dashboard.render(result_queue, metrics_manager)
    
    elif page == "Customer Registration":
        from SafeGuardAI.ui import customer_form
        customer_form.render()

if __name__ == "__main__":
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    import sys
    import os

    # Check if we are running inside Streamlit
    if get_script_run_ctx():
        main()
    else:
        # Not in streamlit, relaunch
        print("Launching Streamlit...")
        os.execvp("streamlit", ["streamlit", "run", os.path.abspath(__file__)] + sys.argv[1:])


