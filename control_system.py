# control_system.py

import logging
from gpt_integration import GPTIntegration
from notification import send_notification  # Ensure this function is implemented

class ControlSystem:
    """
    Manages the high-level workflow for achieving user-defined goals.
    """

    def __init__(self, goal: str):
        """
        Initializes the ControlSystem with the user's goal.

        Args:
            goal (str): The high-level goal provided by the user.
        """
        self.goal = goal
        self.execution_history = []
        self.gpt = GPTIntegration()
        logging.info(f"Initialized ControlSystem with goal: {self.goal}")

    def run(self):
        """
        Executes the entire workflow: planning, executing tasks, and evaluating results.
        """
        try:
            # Step 1: Define Goal
            self.define_goal()

            # Step 2: Planning
            self.create_plan()

            # Step 3: Executing the Plan
            self.execute_plan()

            # Step 4: Evaluation
            self.evaluate_results()

            # Step 5: Notification
            self.notify_user()

            logging.info("ControlSystem run completed successfully.")

        except Exception as e:
            logging.exception("An unexpected error occurred in ControlSystem.")
            print("An error occurred. Please check 'progress.log' for details.")

    def define_goal(self):
        """
        Defines the user's goal by communicating with GPT.
        """
        logging.info("Defining goal.")
        prompt = f"My goal is: {self.goal}\nPlease acknowledge the goal."
        response = self.gpt.send_message(prompt, model="gpt-4o-mini")
        acknowledgment = response.strip()
        logging.info(f"Goal acknowledgment: {acknowledgment}")

    def create_plan(self):
        """
        Uses GPT to create a detailed plan for achieving the goal.
        """
        logging.info("Creating plan.")
        prompt = f"My goal is: {self.goal}\nProvide a detailed step-by-step plan to achieve this goal. Answer with only the plan, without any unnecessary sentences."
        response = self.gpt.send_message(prompt, model="gpt-4o")
        self.plan = response.strip()
        logging.info(f"Plan created: {self.plan}")

    def execute_plan(self):
        """
        Executes the plan step-by-step, interacting with GPT to determine and perform each action.
        """
        logging.info("Executing the plan.")
        for i in range(10):
            next_action = self.get_next_action()
            if not next_action:
                logging.info("No further actions determined by GPT. Ending execution.")
                break

            logging.info(f"Next action: {next_action}")
            result = self.perform_action(next_action)

            # Save the result
            self.execution_history.append({
                "action": next_action,
                "result": result
            })
            logging.info(f"Result of action: {result}")

    def get_next_action(self):
        """
        Determines the next action based on the execution history by communicating with GPT.

        Returns:
            str: The next action to perform or None if the plan is complete.
        """
        history_content = "\n".join([
            f"Action: {entry['action']}\nResult: {entry['result']}"
            for entry in self.execution_history
        ])

        prompt = (
            f"Goal: {self.goal}\n"
            f"Plan: {self.plan}\n"
            f"Execution History:\n{history_content}\n"
            "Based on the above, what is the next action to take to achieve the goal? "
            "Provide a clear and concise instruction. If the goal is achieved, respond with 'Plan complete'."
        )
        response = self.gpt.send_message(prompt, model="gpt-4o-mini")
        next_action = response.strip()
        print(next_action)
        if "plan complete" in next_action.lower():
            return None
        return next_action

    def perform_action(self, action: str):
        """
        Executes the given action using GPT and captures the result.

        Args:
            action (str): The action to execute.

        Returns:
            str: The result of the action.
        """
        prompt = f"Action: {action}\nPlease perform this action and provide the result."
        response = self.gpt.send_message(prompt, model="gpt-4o-mini")
        return response

    def evaluate_results(self):
        """
        Evaluates the execution history against the goal by communicating with GPT.
        """
        logging.info("Evaluating results.")
        history_content = "\n".join([
            f"Step {idx + 1}:\nAction: {entry['action']} \nResult: {entry['result']}\n"
            for idx, entry in enumerate(self.execution_history)
        ])

        prompt = (
            f"Goal: {self.goal}\n"
            "Execution History:\n"
            f"{history_content}\n"
            "Based on the execution history, evaluate how well the goal has been met. "
            "Provide a detailed assessment."
        )
        evaluation = self.gpt.send_message(prompt, model="gpt-4o-mini")
        logging.info(f"Evaluation: {evaluation}")
        # print(f"Evaluation:\n{evaluation}")

    def notify_user(self):
        """
        Alerts the user upon completion of the workflow.
        """
        logging.info("Sending notification to user.")
        send_notification()
        logging.info("Notification sent.")
