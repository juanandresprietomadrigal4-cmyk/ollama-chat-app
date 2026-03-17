"""
Chat Application UI Module.

Handles the Tkinter GUI for the Ollama chat client.
High cohesion: all UI logic in one module.
Low coupling: communicates with LLM client through clear interface.
"""

import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from threading import Thread
import requests
from llm_client import OllamaClient

class ChatUI:  # <--- REVISA ESTE NOMBRE
    def __init__(self, root):
        self.root = root
        # ... resto de tu código ...

class ChatMessage:
    """Represents a single chat message with metadata."""
    
    def __init__(self, role: str, text: str, response_time: float = None):
        """
        Initialize a chat message.
        
        Args:
            role: "user" or "assistant"
            text: Message content
            response_time: Response time in seconds (for assistant messages)
        """
        self.role = role
        self.text = text
        self.response_time = response_time
    
    def format_for_display(self) -> str:
        """Format message for display in chat area."""
        if self.role == "user":
            return f"[YOU]: {self.text}\n"
        else:
            time_str = f" ({self.response_time:.2f}s)" if self.response_time else ""
            return f"[BOT]{time_str}:\n{self.text}\n"


class ChatAppUI:
    """
    Main chat appUI using Tkinter.
    
    Manages:
    - Window and widget layout
    - User interactions
    - Communication with OllamaClient
    - Chat history and display
    """
    
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    WINDOW_TITLE = "Ollama Chat Client"
    
    # Color scheme
    BG_COLOR = "#f0f0f0"
    FG_COLOR = "#333333"
    USER_COLOR = "#e3f2fd"
    BOT_COLOR = "#f3e5f5"
    BUTTON_COLOR = "#2196F3"
    BUTTON_TEXT = "white"
    
    # Font sizes
    FONT_LABEL = ("Segoe UI", 10, "bold")
    FONT_TEXT = ("Segoe UI", 10)
    FONT_CHAT = ("Consolas", 9)
    
    def __init__(self):
        """Initialize the chat appUI."""
        self.root = tk.Tk()
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.configure(bg=self.BG_COLOR)
        
        # Initialize LLM client
        self.llm_client = OllamaClient()
        
        # Chat history
        self.chat_history = []
        
        # UI state
        self.is_processing = False
        
        # Build UI
        self._build_ui()
        self._check_server_connection()
    
    def _build_ui(self):
        """Build the user interface."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title = tk.Label(
            main_container,
            text="💬 Ollama Chat Client",
            font=("Segoe UI", 14, "bold"),
            bg=self.BG_COLOR,
            fg="#1565c0"
        )
        title.pack(pady=(0, 10))
        
        # Control panel
        self._build_control_panel(main_container)
        
        # Chat display area
        self._build_chat_area(main_container)
        
        # Input area
        self._build_input_area(main_container)
    
    def _build_control_panel(self, parent):
        """Build the control panel with model selector."""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Model selection
        model_label = tk.Label(
            control_frame,
            text="Select Model:",
            font=self.FONT_LABEL,
            bg=self.BG_COLOR
        )
        model_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.model_var = tk.StringVar(value=OllamaClient.DEFAULT_MODEL)
        model_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.model_var,
            values=OllamaClient.AVAILABLE_MODELS,
            state="readonly",
            width=18
        )
        model_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Server status indicator
        self.status_label = tk.Label(
            control_frame,
            text="Status: Checking...",
            font=("Segoe UI", 9),
            bg=self.BG_COLOR,
            fg="#ff9800"
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Clear history button
        clear_btn = tk.Button(
            control_frame,
            text="🗑️ Clear History",
            command=self._clear_history,
            font=self.FONT_TEXT,
            bg=self.BUTTON_COLOR,
            fg=self.BUTTON_TEXT,
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=5
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
    
    def _build_chat_area(self, parent):
        """Build the chat message display area."""
        chat_frame = ttk.Frame(parent)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Title
        chat_label = tk.Label(
            chat_frame,
            text="Chat History",
            font=self.FONT_LABEL,
            bg=self.BG_COLOR
        )
        chat_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Chat display with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=self.FONT_CHAT,
            bg="white",
            fg=self.FG_COLOR,
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=10,
            pady=10,
            height=20
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for different message types
        self.chat_display.tag_configure("user", foreground="#1565c0", font=(self.FONT_CHAT[0], self.FONT_CHAT[1], "bold"))
        self.chat_display.tag_configure("bot", foreground="#7b1fa2", font=(self.FONT_CHAT[0], self.FONT_CHAT[1], "bold"))
        self.chat_display.tag_configure("time", foreground="#666666", font=(self.FONT_CHAT[0], self.FONT_CHAT[1] - 1, "italic"))
        self.chat_display.tag_configure("error", foreground="#d32f2f")
    
    def _build_input_area(self, parent):
        """Build the user input area."""
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X)
        
        # Input label
        input_label = tk.Label(
            input_frame,
            text="Your Message:",
            font=self.FONT_LABEL,
            bg=self.BG_COLOR
        )
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Input text area
        input_sub_frame = ttk.Frame(input_frame)
        input_sub_frame.pack(fill=tk.BOTH, expand=True)
        
        self.input_text = tk.Text(
            input_sub_frame,
            height=3,
            font=self.FONT_TEXT,
            bg="white",
            fg=self.FG_COLOR,
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=10,
            pady=8
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Input scrollbar
        input_scrollbar = ttk.Scrollbar(
            input_sub_frame,
            orient=tk.VERTICAL,
            command=self.input_text.yview
        )
        input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=input_scrollbar.set)
        
        # Send button
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.send_btn = tk.Button(
            button_frame,
            text="📤 Send",
            command=self._send_message,
            font=("Segoe UI", 11, "bold"),
            bg=self.BUTTON_COLOR,
            fg=self.BUTTON_TEXT,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=8
        )
        self.send_btn.pack(side=tk.LEFT)
        
        # Bind Enter+Ctrl to send
        self.input_text.bind("<Control-Return>", lambda e: self._send_message())
    
    def _check_server_connection(self):
        """Check if Ollama server is available and update status."""
        def check():
            is_available = self.llm_client.is_available()
            if is_available:
                self.status_label.config(
                    text="✅ Server: Connected",
                    fg="#4caf50"
                )
            else:
                self.status_label.config(
                    text="❌ Server: Disconnected",
                    fg="#d32f2f"
                )
        
        thread = Thread(target=check, daemon=True)
        thread.start()
    
    def _add_message(self, message: ChatMessage):
        """
        Add a message to the chat display.
        
        Args:
            message: ChatMessage object to display
        """
        self.chat_display.config(state=tk.NORMAL)
        
        if message.role == "user":
            self.chat_display.insert(tk.END, "[YOU]: ", "user")
            self.chat_display.insert(tk.END, f"{message.text}\n")
        else:
            self.chat_display.insert(tk.END, "[BOT]: ", "bot")
            if message.response_time is not None:
                self.chat_display.insert(
                    tk.END,
                    f"({message.response_time:.2f}s) ",
                    "time"
                )
            self.chat_display.insert(tk.END, f"{message.text}\n")
        
        self.chat_display.insert(tk.END, "\n")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Store in history
        self.chat_history.append(message)
    
    def _send_message(self):
        """Send user message and get response from LLM."""
        user_input = self.input_text.get("1.0", tk.END).strip()
        
        if not user_input:
            messagebox.showwarning("Empty Message", "Please enter a message.")
            return
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Add user message to display
        user_message = ChatMessage("user", user_input)
        self._add_message(user_message)
        
        # Disable send button during processing
        self.send_btn.config(state=tk.DISABLED, text="⏳ Processing...")
        self.is_processing = True
        
        # Get response in background thread
        thread = Thread(
            target=self._get_llm_response,
            args=(user_input,),
            daemon=True
        )
        thread.start()
    
    def _get_llm_response(self, user_input: str):
        """
        Get response from LLM in background thread.
        
        Args:
            user_input: The user's message
        """
        try:
            model = self.model_var.get()
            response_text, response_time = self.llm_client.generate_response(
                user_input,
                model=model
            )
            
            # Create and add bot message
            bot_message = ChatMessage("assistant", response_text, response_time)
            self._add_message(bot_message)
        
        except requests.RequestException as e:
            error_msg = ChatMessage("assistant", f"❌ Error: {str(e)}")
            self._add_message(error_msg)
        
        except Exception as e:
            error_msg = ChatMessage("assistant", f"❌ Unexpected error: {str(e)}")
            self._add_message(error_msg)
        
        finally:
            # Re-enable send button
            self.send_btn.config(state=tk.NORMAL, text="📤 Send")
            self.is_processing = False
    
    def _clear_history(self):
        """Clear the chat history."""
        if not self.chat_history:
            messagebox.showinfo("Empty", "Chat history is already empty.")
            return
        
        response = messagebox.askyesno(
            "Clear History",
            f"Are you sure you want to clear {len(self.chat_history)} messages?"
        )
        
        if response:
            self.chat_history = []
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "Chat history cleared.")
    
    def run(self):
        """Start the appUI."""
        self.root.mainloop()
