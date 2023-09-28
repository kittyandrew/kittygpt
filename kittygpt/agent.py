from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from typing import Callable
from pathlib import Path
import traceback
import datetime
import json
import os

from .basic import execute_bash, finish
from .command import Command


class Agent:
    def __init__(self, openai_key = None, model_name = "gpt-4", temperature = 0, prompts_dir = Path("prompts")):
        self.token = openai_key or os.environ["OPENAI_API_KEY"]
        self.model = model_name
        self.temperature = temperature
        self.prompts_dir = prompts_dir

        self.commands = [Command(execute_bash), Command(finish, terminating=True)]
        self.commands_map = {cmd.name: cmd for cmd in self.commands}

        self.history = []

    def add_command(self, func: Callable, terminating: bool = False):
        cmd = Command(func, terminating)
        self.commands.insert(-1, cmd)
        self.commands_map[cmd.name] = cmd

    def cook_commands(self):
        instructions = []
        for i, cmd in enumerate(self.commands):
            params = ", ".join(f"{aname}: {atype}" for aname, atype in cmd.annotations.items())
            instructions.append(f"{i+1}. {cmd.name}: {cmd.doc}. Params: ({params})")
        return "\n".join(instructions)

    def cook_chain(self):
        with open(self.prompts_dir / "prompt.txt") as f:  prompt = f.read().strip(" \r\t\n")
        with open(self.prompts_dir / "output.txt") as f:  output_fmt = f.read().strip(" \r\t\n")
        with open(self.prompts_dir / "trigger.txt") as f: trigger = f.read().strip(" \r\t\n")

        current_date = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S %p")
        date_prompt = f"The current time and date is {current_date}"
        messages = [SystemMessagePromptTemplate.from_template(prompt), SystemMessage(content=date_prompt)]

        for message in self.history:
            if message["type"] == "ai":       messages.append(AIMessage(content=message["text"]))
            elif message["type"] == "user":   messages.append(HumanMessage(content=message["text"]))
            elif message["type"] == "system": messages.append(SystemMessage(content=message["text"]))
            else: raise NotImplementedError(f"Unexpected message: {message}")

        messages.extend([SystemMessage(content=output_fmt), HumanMessage(content=trigger)])

        model = ChatOpenAI(model=self.model, temperature=self.temperature, openai_api_key=self.token, request_timeout=60)
        chain = LLMChain(llm=model, prompt=ChatPromptTemplate.from_messages(messages))
        return chain

    def run(self, goal: str, max_cycles: int = 10, autonomous: bool = False, debug: bool = False):
        cycles_left = max_cycles
        while cycles_left:
            chain = self.cook_chain()
            if debug: print(chain.prompt.format(goal=goal, commands=self.cook_commands()))
            answer = chain.run(goal=goal, commands=self.cook_commands())
            self.history.append({"type": "ai", "text": answer})

            answer_data = json.loads(answer)
            cname, cargs = answer_data["command"]["name"], answer_data["command"]["args"]
            tool = self.commands_map[cname]

            if not tool.terminating: print("Command is about to be executed:", answer_data["command"])
            if not tool.terminating and not autonomous: input("Press anything once to continue... ")

            try:
                output = tool(**cargs)
                self.history.append({"type": "system", "text": f"Command {cname} returned: {output}"})
                if tool.terminating: return output
            except Exception:
                self.history.append({"type": "system", "text": f"Command {cname} failed: {traceback.format_exc()}"})

            cycles_left -= 1
        raise Exception(f"Ran out of cycles! (max_cycles = {max_cycles})")
