import getpass
import json

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from spade_llm import ChatAgent

console = Console()


def display_response(message: str, sender: str = "Tool Assistant", **metadata):
    """
    Display agent messages in rich panels, with optional metadata.
    Confidence values are color-coded automatically.
    """

    # Header with sender
    header = Text(f"🗨️  {sender}", style="bold cyan")

    # Main message
    message_text = Text(message, style="white")

    # Metadata panel
    metadata_panel = None
    if metadata:
        table = Table.grid(expand=True)
        table.add_column(justify="right", style="bold magenta")
        table.add_column(justify="left", style="white")

        for key, value in metadata.items():
            # Pretty-print JSON structures
            if isinstance(value, dict):
                value = json.dumps(value, indent=2)

            # Color confidence values
            if "confidence" in key.lower():
                try:
                    conf = float(value)
                    if conf >= 0.6:
                        style = "bold green"
                    elif conf >= 0.3:
                        style = "bold yellow"
                    else:
                        style = "bold red"
                    value = Text(f"{value:.3f}", style=style)
                except Exception:
                    pass  # fallback to default if not float

            table.add_row(str(key), str(value))

        metadata_panel = Panel(table, title="📌 Metadata", box=box.ROUNDED, style="dim")

    # Compose full panel
    if metadata_panel:
        console.print(
            Panel.fit(
                Panel(message_text, title=header, box=box.ROUNDED, style="green"),
                metadata_panel,
                box=box.SQUARE,
            )
        )
    else:
        console.print(Panel(message_text, title=header, box=box.ROUNDED, style="green"))


def init_chat_agent(xmpp_server):
    chat_agent = ChatAgent(
        jid=f"user@{xmpp_server}",
        password=getpass.getpass("Chat agent password: "),
        target_agent_jid=f"tool_assistant@{xmpp_server}",
        display_callback=display_response,
    )
    return chat_agent
