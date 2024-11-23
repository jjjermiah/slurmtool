from textual.app import App, ComposeResult
from textual.widgets import DataTable, Button, Footer, Label, ProgressBar
from textual.scroll_view import ScrollView
from textual.containers import Container
from textual.reactive import reactive
from textual.events import Key
from textual.widgets import Welcome

from .slurm_jobs import JobList

import asyncio 

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]

class TableApp(App):

    def compose(self) -> ComposeResult:
        yield Label("Do you love Textual?")
        yield Button("Exit", name="exit_button", variant = "primary")
        yield Button("Refresh", name="refresh_button", variant = "primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)

app = TableApp()
if __name__ == "__main__":
    reply = app.run()
    print(reply)
    
# class JobTableApp(App):
#     selected_job = reactive(None)



# if __name__ == "__main__":
    sacctJobs = JobList.initialize()
    
#     filtered = [job for job in sacctJobs.jobs if not '.' in job.JobID] 
#     JobTableApp(jobs=filtered).run()