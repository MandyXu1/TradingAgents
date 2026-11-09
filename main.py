import os
import sys
from dotenv import load_dotenv

# Must execute this before importing other project modules
# to ensure environment variables are loaded correctly.
load_dotenv()

# --- New Feature: Dual Logger ---
class DualLogger:
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.err_terminal = sys.stderr
        # Open file with utf-8 encoding to prevent errors when outputting special characters
        self.log = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()  # Flush buffer immediately after each write to prevent log loss

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# Redirect standard output and standard error to the dual logger
sys.stdout = DualLogger("execution_log.txt")
sys.stderr = sys.stdout
# --------------------------------

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Copy default config; the framework will automatically read
# variables with TRADINGAGENTS_ and OPENAI_ prefixes from .env
config = DEFAULT_CONFIG.copy()

print("="*50)
print("Initializing TradingAgents framework...")
# debug=True will output the thinking process of all agents,
# which will now be written to the txt file alongside the terminal.
ta = TradingAgentsGraph(debug=True, config=config)

print("\nStarting forward propagation (Target: MSFT, Date: 2026-11-10)...")
# forward propagate
_, decision = ta.propagate("MSFT", "2026-11-10")

print("\n" + "="*50)
print("Final Decision:")
print(decision)
print("="*50)
print("Execution completed. Complete log saved to execution_log.txt")