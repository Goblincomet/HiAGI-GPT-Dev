import sys
import threading
import time
from contextlib import contextmanager
from typing import Dict, Any

from ...persona.load_persona_data import load_persona_data
from ...utils.function_utils import Functions
from ...utils.storage_interface import StorageInterface


class AgentFunctions:
    agent_data: Dict[str, Any]

    functions = None
    persona_data = None
    spinner_thread = None

    def __init__(self, agent_name):
        self.spinners = []
        self.stdout_lock = threading.Lock()  # add this line

        # Initialize functions
        self.functions = Functions()

        # Initialize agent data
        self.agent_data = {
            'name': agent_name,
            'generate_text': None,
            'storage': None,
            'objective': None,
            'model': None,
            'prompts': None,
            'params': None
        }

        # Initialize agent
        self.initialize_agent(agent_name)

        # Initialize spinner
        self.spinner_running = True
        self.spinner_thread = threading.Thread(target=self._spinner_loop)

    def initialize_agent(self, agent_name):
        import configparser
        config = configparser.ConfigParser()
        config.read('Config/config.ini')

        # Load persona data
        self.persona_data = load_persona_data()
        if "HeuristicImperatives" in self.persona_data:
            self.agent_data.update(
                heuristic_imperatives=self.persona_data["HeuristicImperatives"],
            )
        self.agent_data.update(
            storage=StorageInterface(),
            objective=self.persona_data['Objective'],
            params=self.persona_data[agent_name]['Params'],
            prompts=self.persona_data[agent_name]['Prompts'],
        )
        db = self.persona_data[agent_name].get('Database')
        if db:
            self.agent_data.update(database=db)

        # Load API and Model
        language_model_api = self.persona_data[agent_name]['API']
        self.set_model_api(language_model_api)

        model = self.persona_data[agent_name]['Model']
        self.agent_data['model'] = config.get('ModelLibrary', model)

    def set_model_api(self, language_model_api):
        if language_model_api == 'oobabooga_api':
            from ...llm.oobabooga_api import generate_text
        elif language_model_api == 'openai_api':
            from ...llm.openai_api import generate_text
        else:
            raise ValueError(
                f"Unsupported Language Model API library: {language_model_api}")

        self.agent_data['generate_text'] = generate_text

    def run_llm(self, prompt):
        result = self.agent_data['generate_text'](
            prompt,
            self.agent_data['model'],
            self.agent_data['params'],
        ).strip()
        return result

    def print_task_list(self, ordered_results):
        self.functions.print_task_list(ordered_results)

    def print_result(self, result):
        self.functions.print_result(result, self.agent_data['name'])

    def _spinner_loop(self):
        # msg = f"{self.agent_data['name']}: Thinking "
        while self.spinner_running:
            for char in "|/-\\":
                # sys.stdout.write(msg + char)
                sys.stdout.write(char)
                sys.stdout.flush()
                # sys.stdout.write("\b" * (len(msg) + 1))
                sys.stdout.write("\b" * 1)
                time.sleep(0.1)

    def start_thinking(self):
        self.spinner_running = True
        self.spinner_thread = threading.Thread(target=self._spinner_loop)
        self.spinner_thread.start()

    def stop_thinking(self):
        self.spinner_running = False
        self.spinner_thread.join()

        # Clear spinner characters
        # msg = f"{self.agent_data['name']}: Thinking "
        # sys.stdout.write("\b" * len(msg + "\\"))
        sys.stdout.write("\b" * 1)

        # Write "Done." message and flush stdout
        # sys.stdout.write("\n" + msg + "- Done.\n")
        sys.stdout.write("\n")
        sys.stdout.flush()

    @contextmanager
    def thinking(self):
        try:
            self.start_thinking()
            yield
        finally:
            self.stop_thinking()
