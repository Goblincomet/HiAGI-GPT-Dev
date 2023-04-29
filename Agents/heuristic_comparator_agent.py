from Agents.Func.agent_functions import AgentFunctions
from Logs.logger_config import Logger

logger = Logger(name="Heuristic Comparator Agent")


class HeuristicComparatorAgent:
    agent_data = None
    agent_funcs = None
    heuristic_imperatives = "\
        1. Reduce suffering in the universe: Guiding AI systems to reduce harm, address inequalities, and alleviate pain and distress for all sentient beings, including humans, animals, and other life forms.\
        2. Increase prosperity in the universe: Encouraging AI systems to promote well-being, flourishing, and economic growth for all life forms, fostering a thriving ecosystem where all can coexist harmoniously.\
        3. Increase understanding in the universe: Inspiring AI systems, as well as humans and other life forms, to expand knowledge, foster wisdom, and facilitate better decision-making through learning and the sharing of information."

    def __init__(self):
        self.agent_funcs = AgentFunctions('HeuristicComparatorAgent')
        self.agent_data = self.agent_funcs.agent_data
        logger.set_level('debug')

    def run_agent(self, seta, setb, feedback=None):
        # This function will be the main entry point for your agent.
        setc = self.heuristic_imperatives

        # 2. Load data from storage
        data = {"seta": seta, "setb": setb, "setc": setc}

        logger.log(f"Data:\n{data}", 'debug')
        # quit()

        # 3. Get prompt formats
        prompt_formats = self.get_prompt_formats(data)

        logger.log(f"Prompt Formats:\n{prompt_formats}", 'debug')
        # quit()

        # 4. Generate prompt
        prompt = self.generate_prompt(prompt_formats, feedback)

        logger.log(f"Prompt:\n{prompt}", 'debug')
        # quit()

        # 1. Start Console Feedback
        with self.agent_funcs.thinking():
            # 5. Execute the main task of the agent
            result = self.execute_task(prompt)

        # 7. Stop Console Feedback
        self.agent_funcs.stop_thinking()

        # 6. Save the results
        # self.save_results(result)

        # 8. Print the result or any other relevant information
        self.agent_funcs.print_result(result)

        return result

    def load_data_from_storage(self):
        # Load necessary data from storage and return it as a dictionary
        pass

    def get_prompt_formats(self, data):
        # Create a dictionary of prompt formats based on the loaded data
        prompt_formats = {
            # 'SystemPrompt': {'objective': self.agent_data['objective']},
            'ContextPrompt': {'seta': data['seta'], 'setb': data['setb'], 'setc': data['setc']}
        }
        return prompt_formats
    pass

    def generate_prompt(self, prompt_formats, feedback=None):
        # Generate the prompt using prompt_formats and return it.
        # Load Prompts
        system_prompt = self.agent_data['prompts']['SystemPrompt']
        context_prompt = self.agent_data['prompts']['ContextPrompt']
        instruction_prompt = self.agent_data['prompts']['InstructionPrompt']
        # feedback_prompt = self.agent_data['prompts']['FeedbackPrompt'] if feedback != "" else ""

        # Format Prompts
        # system_prompt = system_prompt.format(**prompt_formats.get('SystemPrompt', {}))
        context_prompt = context_prompt.format(**prompt_formats.get('ContextPrompt', {}))
        # instruction_prompt = instruction_prompt.format(**prompt_formats.get('InstructionPrompt', {}))
        # feedback_prompt = feedback_prompt.format(feedback=feedback)

        prompt = [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{instruction_prompt}{context_prompt}"}
        ]

        # print(f"\nPrompt: {prompt}")
        return prompt

    def execute_task(self, prompt):
        # Execute the main task of the agent and return the result
        return self.agent_data['generate_text'](prompt, self.agent_data['model'], self.agent_data['params']).strip()

    def save_results(self, result):
        # Save the results to storage
        pass

