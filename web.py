"""
streamlit run web.py --server.port 8000
"""

import datetime
from datetime import date

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from utils.config import load_config

config = load_config()


class TaskAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def create_task(self, name: str) -> requests.Response:
        url = f"{self.base_url}/v1/tasks"
        return requests.post(url, json={"name": name})

    def get_task_status(self, task_id: str) -> requests.Response:
        url = f"{self.base_url}/v1/tasks/{task_id}"
        return requests.get(url)

    def get_task_list(self, task_date: date) -> requests.Response:
        url = f"{self.base_url}/v1/tasks/list/{task_date}"
        return requests.get(url)

    def cancel_task(self, task_id: str) -> requests.Response:
        url = f"{self.base_url}/v1/tasks/{task_id}/cancel"
        return requests.post(url)

    def get_queue_status(self) -> requests.Response:
        url = f"{self.base_url}/v1/tasks/queue/status"
        return requests.get(url)


def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "current_task" not in st.session_state:
        st.session_state.current_task = None


def format_task_data(tasks: list) -> pd.DataFrame:
    if not tasks:
        return pd.DataFrame()
    df = pd.DataFrame(tasks)
    df["create_time"] = pd.to_datetime(df["create_time"]).dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return df


def render_task_status(status: str) -> str:
    colors = {
        "pending": "blue",
        "running": "orange",
        "completed": "green",
        "failed": "red",
        "timeout": "gray",
    }
    return f":{colors.get(status, 'black')}[{status}]"


def main():
    st.set_page_config(page_title="Task Management System", layout="wide")
    init_session_state()

    if not st.session_state.authenticated:
        password = st.text_input(
            "Please input the passwrd", type="password", placeholder="Enter Password"
        )
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password!")
        return

    tab1, tab2, tab3 = st.tabs(["Task List", "Create Task", "Task Details"])

    with tab1:
        st.subheader("Task List")
        col1, col2 = st.columns([2, 1])
        with col1:
            task_date = st.date_input("Select Date", datetime.date.today())
        with col2:
            if st.button("Refresh"):
                st.rerun()

        if task_date:
            response = api_client.get_task_list(task_date)
            if response.status_code == 200:
                df = format_task_data(response.json())
                if not df.empty:
                    st.dataframe(df, use_container_width=True)

                    fig = px.pie(df, names="status", title="Task Status Distribution")
                    st.plotly_chart(fig)
                else:
                    st.info("No task records for the selected date")
            else:
                st.error("Failed to retrieve task list")

    with tab2:
        st.subheader("Create New Task")
        with st.form("create_task_form"):
            task_name = st.text_input("Task Name")
            submitted = st.form_submit_button("Create Task")
            if submitted and task_name:
                response = api_client.create_task(task_name)
                if response.status_code == 200:
                    st.success(f"Task created successfully!")
                    data = response.json()
                    st.json(data)
                    st.session_state.current_task = data["id"]
                else:
                    st.error("Failed to create task")

    with tab3:
        st.subheader("Task Details")
        task_id = st.text_input("Task ID", value=st.session_state.current_task or "")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Check Status"):
                if task_id:
                    response = api_client.get_task_status(task_id)
                    if response.status_code == 200:
                        task_data = response.json()
                        st.markdown("### Task Information")
                        st.markdown(
                            f"- **Status**: {render_task_status(task_data['status'])}"
                        )
                        st.markdown(f"- **Created Time**: {task_data['create_time']}")
                        if task_data["result"]:
                            st.markdown("### Task Result")
                            if task_data["status"] == "completed":
                                st.markdown("### Task Result")
                                st.video(task_data["result"])
                                with open(task_data["result"], "rb") as f:
                                    st.download_button(
                                        label="Download Video",
                                        data=f,
                                        file_name=f"{task_data['id']}.mp4",
                                        mime="video/mp4",
                                    )
                            else:
                                st.markdown(f"```{task_data['result']}```")
                    else:
                        st.error("Failed to retrieve task status")
                else:
                    st.warning("Please enter a Task ID")

        with col2:
            if st.button("Cancel Task"):
                if task_id:
                    response = api_client.cancel_task(task_id)
                    if response.status_code == 200:
                        st.success("Task has been canceled")
                    else:
                        st.error("Failed to cancel task")
                else:
                    st.warning("Please enter a Task ID")


base_url = f"http://localhost:{config['api']['app_port']}"
api_client = TaskAPIClient(base_url)
ADMIN_PASSWORD = config["web"]["password"]

if __name__ == "__main__":
    main()
