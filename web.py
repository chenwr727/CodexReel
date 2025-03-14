import datetime
import json
import os

import pandas as pd
import requests
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from utils.config import config
from utils.url import parse_url


class TaskAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def create_task(self, name: str) -> requests.Response:
        url = f"{self.base_url}/v1/tasks"
        return requests.post(url, json={"name": name})

    def get_task_status(self, task_id: str) -> requests.Response:
        url = f"{self.base_url}/v1/tasks/{task_id}"
        return requests.get(url)

    def get_task_list(self, task_date: datetime.date) -> requests.Response:
        url = f"{self.base_url}/v1/tasks/list/{task_date}"
        return requests.get(url)

    def cancel_task(self, task_id: str) -> requests.Response:
        url = f"{self.base_url}/v1/tasks/{task_id}/cancel"
        return requests.post(url)

    def get_queue_status(self) -> requests.Response:
        url = f"{self.base_url}/v1/tasks/queue/status"
        return requests.get(url)


@st.cache_data(ttl="4h")
def get_hot_list():
    url = "https://api.vvhan.com/api/hotlist/all"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception:
        return []


def init_session_state():
    if "current_task_name" not in st.session_state:
        st.session_state.current_task_name = None


def format_task_data(tasks: list) -> pd.DataFrame:
    if not tasks:
        return pd.DataFrame()
    df = pd.DataFrame(tasks)
    df["create_time"] = pd.to_datetime(df["create_time"]).dt.strftime("%Y-%m-%d %H:%M:%S")
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


def load_authenticator() -> stauth.Authenticate:
    with open("auth.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        credentials=config["credentials"],
        cookie_name=config["cookie"]["name"],
        key=config["cookie"]["key"],
        cookie_expiry_days=config["cookie"]["expiry_days"],
    )

    return authenticator


def handle_authentication(authenticator: stauth.Authenticate) -> bool:
    try:
        authenticator.login()

        if not st.session_state["authentication_status"]:
            st.error("Username/password is incorrect")
            return False
        elif st.session_state["authentication_status"] is None:
            st.warning("Please enter your username and password")
            return False

        return True

    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False


def main():
    st.set_page_config(page_title="Task Management System", layout="wide")
    init_session_state()

    authenticator = load_authenticator()
    if not handle_authentication(authenticator):
        return

    tab1, tab2 = st.tabs(["Task List", "Create Task"])

    with tab1:
        task_date = st.date_input("Select Date", datetime.date.today())

        if task_date:
            response = api_client.get_task_list(task_date)
            if response.status_code == 200:
                df = format_task_data(response.json())
                if not df.empty:
                    event = st.dataframe(
                        df,
                        hide_index=True,
                        use_container_width=True,
                        on_select="rerun",
                        selection_mode="single-row",
                        column_config={"name": st.column_config.LinkColumn(validate=r"^https?://.+$")},
                    )
                    if event.selection["rows"]:
                        task_data = df.iloc[event.selection["rows"][0]].to_dict()
                        task_id = task_data["id"]

                        if st.button("Check Status"):
                            response = api_client.get_task_status(task_id)
                            if response.status_code == 200:
                                task_data = response.json()

                        st.markdown("### Task Information")
                        st.json(task_data)

                        folder = parse_url("", int(task_id))
                        file_json = os.path.join(folder, "_script.json")
                        if os.path.exists(file_json):
                            expander = st.expander("See dialogue")
                            with open(file_json, "r", encoding="utf-8") as f:
                                json_data = json.load(f)
                                expander.json(json_data)

                        if task_data["result"]:
                            if task_data["status"] == "completed":
                                if os.path.exists(task_data["result"]):
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

                        if st.button("Rerun Task"):
                            response = api_client.create_task(task_data["name"])
                            if response.status_code == 200:
                                st.success("Task rerun successfully!")
                            else:
                                st.error("Failed to rerun task")

                        if st.button("Cancel Task"):
                            response = api_client.cancel_task(task_id)
                            if response.status_code == 200:
                                st.success("Task has been canceled")
                            else:
                                st.error("Failed to cancel task")
                else:
                    st.info("No task records for the selected date")
            else:
                st.error("Failed to retrieve task list")

    with tab2:
        hot_list = get_hot_list()
        if hot_list:
            st.subheader("Hot List")
            hot_dict = {data["name"]: data["data"] for data in hot_list["data"]}
            selected_hot = st.selectbox("Select Hot List", hot_dict.keys())
            selected_hot_data = hot_dict[selected_hot]
            df = pd.DataFrame(selected_hot_data, columns=["index", "title", "hot", "url"])
            df["title"] = df["url"] + "#" + df["title"]
            df.drop(columns=["url"], inplace=True)
            event = st.dataframe(
                df,
                height=(len(df) + 1) * 35 + 3,
                hide_index=True,
                use_container_width=True,
                on_select="rerun",
                selection_mode="single-row",
                column_config={"title": st.column_config.LinkColumn(display_text=r"#(.*?)$")},
            )
            if event.selection["rows"]:
                row = df.iloc[event.selection["rows"][0]]
                url = row["title"].split("#")[0]
                st.session_state.current_task_name = url
            else:
                st.session_state.current_task_name = None

        st.subheader("Create New Task")
        with st.form("create_task_form"):
            task_name = st.text_input("Task Name", value=st.session_state.current_task_name or "")
            submitted = st.form_submit_button("Create Task")
            if submitted and task_name:
                response = api_client.create_task(task_name)
                if response.status_code == 200:
                    st.success("Task created successfully!")
                    data = response.json()
                    st.json(data)
                    st.session_state.current_task_name = task_name
                else:
                    st.error("Failed to create task")


base_url = f"http://localhost:{config.api.app_port}"
api_client = TaskAPIClient(base_url)

if __name__ == "__main__":
    main()
