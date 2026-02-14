#!/usr/bin/env python3
"""
HTTP Client Tool - Modern Insomnia-like interface
Split view: Headers (left) + JSON Body (right)
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import subprocess
import json
import threading
from datetime import datetime
import re

class HTTPClient(ttkb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        
        self.title("🚀 HTTP Client Pro")
        self.geometry("1000x750")
        self.minsize(900, 650)
        
        # Variables
        self.method_var = tk.StringVar(value="GET")
        self.content_type_var = tk.StringVar(value="application/json")
        self.body_type_var = tk.StringVar(value="JSON")
        self.auth_type_var = tk.StringVar(value="None")
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttkb.Frame(self, padding=10)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # ========== TOP SECTION ==========
        top_frame = ttkb.Frame(main_frame, bootstyle="secondary")
        top_frame.pack(fill=X, pady=(0, 8))
        
        request_frame = ttkb.Frame(top_frame, padding=10)
        request_frame.pack(fill=X)
        
        self.method_menu = ttkb.Combobox(
            request_frame,
            values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            textvariable=self.method_var,
            width=10,
            state="readonly",
            bootstyle="primary",
            font=("Segoe UI", 10, "bold")
        )
        self.method_menu.pack(side=LEFT, padx=(0, 8))
        
        self.url_entry = ttkb.Entry(
            request_frame,
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        self.url_entry.insert(0, "https://jsonplaceholder.typicode.com/posts/1")
        self.url_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 8))
        
        self.send_button = ttkb.Button(
            request_frame,
            text="SEND ⚡",
            command=self.send_request,
            bootstyle="success",
            width=10
        )
        self.send_button.pack(side=LEFT)
        
        # ========== MIDDLE SECTION ==========
        middle_frame = ttkb.Frame(main_frame)
        middle_frame.pack(fill=X, pady=(0, 8))
        
        self.notebook = ttkb.Notebook(middle_frame, bootstyle="secondary")
        self.notebook.pack(fill=X, padx=5, pady=5)
        
        # HEADERS TAB
        headers_tab = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(headers_tab, text="Headers")
        
        ct_frame = ttkb.Frame(headers_tab)
        ct_frame.pack(fill=X, pady=(0, 8))
        
        ttkb.Label(ct_frame, text="Content-Type:", font=("Segoe UI", 9)).pack(side=LEFT, padx=(0, 8))
        
        self.content_type_menu = ttkb.Combobox(
            ct_frame,
            values=[
                "application/json",
                "application/xml",
                "application/x-www-form-urlencoded",
                "multipart/form-data",
                "text/plain",
                "text/html"
            ],
            textvariable=self.content_type_var,
            width=30,
            state="readonly",
            bootstyle="secondary",
            font=("Segoe UI", 9)
        )
        self.content_type_menu.pack(side=LEFT)
        
        ttkb.Label(headers_tab, text="Custom Headers:", font=("Segoe UI", 9)).pack(anchor=W, pady=(5, 3))
        
        headers_frame = ttkb.Frame(headers_tab)
        headers_frame.pack(fill=BOTH, expand=YES)
        
        self.headers_text = tk.Text(
            headers_frame,
            height=3,
            font=("Consolas", 9),
            bg="#2b2b2b",
            fg="#d4d4d4",
            insertbackground="white",
            relief=FLAT,
            padx=8,
            pady=6
        )
        headers_scrollbar = ttkb.Scrollbar(headers_frame, command=self.headers_text.yview)
        self.headers_text.configure(yscrollcommand=headers_scrollbar.set)
        
        self.headers_text.pack(side=LEFT, fill=BOTH, expand=YES)
        headers_scrollbar.pack(side=RIGHT, fill=Y)
        
        self.headers_text.insert("1.0", "Authorization: Bearer your_token_here")
        
        # BODY TAB
        body_tab = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(body_tab, text="Body")
        
        body_type_frame = ttkb.Frame(body_tab)
        body_type_frame.pack(fill=X, pady=(0, 8))
        
        for body_type in ["JSON", "Raw", "Form"]:
            ttkb.Radiobutton(
                body_type_frame,
                text=body_type,
                variable=self.body_type_var,
                value=body_type,
                bootstyle="secondary"
            ).pack(side=LEFT, padx=8)
        
        format_btn = ttkb.Button(
            body_type_frame,
            text="Format",
            command=self.format_json,
            bootstyle="info-outline",
            width=8
        )
        format_btn.pack(side=RIGHT)
        
        body_frame = ttkb.Frame(body_tab)
        body_frame.pack(fill=BOTH, expand=YES)
        
        self.body_text = tk.Text(
            body_frame,
            height=4,
            font=("Consolas", 9),
            bg="#2b2b2b",
            fg="#d4d4d4",
            insertbackground="white",
            relief=FLAT,
            padx=8,
            pady=6
        )
        body_scrollbar = ttkb.Scrollbar(body_frame, command=self.body_text.yview)
        self.body_text.configure(yscrollcommand=body_scrollbar.set)
        
        self.body_text.pack(side=LEFT, fill=BOTH, expand=YES)
        body_scrollbar.pack(side=RIGHT, fill=Y)
        
        default_body = '{"name": "John", "email": "john@example.com"}'
        self.body_text.insert("1.0", default_body)
        
        # AUTH TAB
        auth_tab = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(auth_tab, text="Auth")
        
        auth_type_frame = ttkb.Frame(auth_tab)
        auth_type_frame.pack(fill=X, pady=(0, 10))
        
        ttkb.Label(auth_type_frame, text="Type:", font=("Segoe UI", 9)).pack(side=LEFT, padx=(0, 8))
        
        auth_menu = ttkb.Combobox(
            auth_type_frame,
            values=["None", "Bearer Token", "Basic Auth", "API Key"],
            textvariable=self.auth_type_var,
            width=15,
            state="readonly",
            bootstyle="secondary",
            font=("Segoe UI", 9)
        )
        auth_menu.pack(side=LEFT)
        
        ttkb.Label(auth_tab, text="Token/Username:", font=("Segoe UI", 9)).pack(anchor=W, pady=(5, 3))
        self.auth_field1 = ttkb.Entry(auth_tab, font=("Segoe UI", 9), bootstyle="secondary")
        self.auth_field1.pack(fill=X, pady=(0, 8))
        
        ttkb.Label(auth_tab, text="Password:", font=("Segoe UI", 9)).pack(anchor=W, pady=(5, 3))
        self.auth_field2 = ttkb.Entry(auth_tab, show="*", font=("Segoe UI", 9), bootstyle="secondary")
        self.auth_field2.pack(fill=X)
        
        # PARAMS TAB
        params_tab = ttkb.Frame(self.notebook, padding=10)
        self.notebook.add(params_tab, text="Params")
        
        ttkb.Label(params_tab, text="Query Params (key=value):", font=("Segoe UI", 9)).pack(anchor=W, pady=(0, 3))
        
        params_frame = ttkb.Frame(params_tab)
        params_frame.pack(fill=BOTH, expand=YES)
        
        self.params_text = tk.Text(
            params_frame,
            height=3,
            font=("Consolas", 9),
            bg="#2b2b2b",
            fg="#d4d4d4",
            insertbackground="white",
            relief=FLAT,
            padx=8,
            pady=6
        )
        params_scrollbar = ttkb.Scrollbar(params_frame, command=self.params_text.yview)
        self.params_text.configure(yscrollcommand=params_scrollbar.set)
        
        self.params_text.pack(side=LEFT, fill=BOTH, expand=YES)
        params_scrollbar.pack(side=RIGHT, fill=Y)
        
        self.params_text.insert("1.0", "page=1\nlimit=10")
        
        # ========== BOTTOM SECTION (SPLIT VIEW!) ==========
        bottom_frame = ttkb.Frame(main_frame, bootstyle="dark")
        bottom_frame.pack(fill=BOTH, expand=YES)
        
        # Header
        terminal_header = ttkb.Frame(bottom_frame, bootstyle="secondary", padding=8)
        terminal_header.pack(fill=X)
        
        ttkb.Label(
            terminal_header,
            text="⚡ Response",
            font=("Segoe UI", 11, "bold"),
            bootstyle="inverse-secondary"
        ).pack(side=LEFT, padx=(5, 0))
        
        self.status_label = ttkb.Label(
            terminal_header,
            text="● Ready",
            font=("Segoe UI", 9),
            bootstyle="inverse-secondary"
        )
        self.status_label.pack(side=LEFT, padx=12)
        
        clear_btn = ttkb.Button(
            terminal_header,
            text="Clear",
            command=self.clear_terminal,
            bootstyle="secondary",
            width=8
        )
        clear_btn.pack(side=RIGHT, padx=5)
        
        # SPLIT VIEW: Headers (left) + JSON Body (right)
        split_container = ttkb.Frame(bottom_frame)
        split_container.pack(fill=BOTH, expand=YES, padx=8, pady=(0, 8))
        
        # LEFT: Headers & Status
        left_frame = ttkb.Frame(split_container, bootstyle="dark")
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 4))
        
        ttkb.Label(
            left_frame,
            text="Headers & Status",
            font=("Segoe UI", 9, "bold"),
            bootstyle="inverse-dark"
        ).pack(fill=X, padx=5, pady=(5, 3))
        
        headers_display_frame = ttkb.Frame(left_frame)
        headers_display_frame.pack(fill=BOTH, expand=YES)
        
        self.headers_display = tk.Text(
            headers_display_frame,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#cccccc",
            insertbackground="white",
            relief=FLAT,
            padx=10,
            pady=8,
            wrap=tk.WORD
        )
        headers_scrollbar = ttkb.Scrollbar(headers_display_frame, command=self.headers_display.yview)
        self.headers_display.configure(yscrollcommand=headers_scrollbar.set)
        
        self.headers_display.pack(side=LEFT, fill=BOTH, expand=YES)
        headers_scrollbar.pack(side=RIGHT, fill=Y)
        
        # RIGHT: JSON Body
        right_frame = ttkb.Frame(split_container, bootstyle="dark")
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(4, 0))
        
        ttkb.Label(
            right_frame,
            text="Response Body (JSON)",
            font=("Segoe UI", 9, "bold"),
            bootstyle="inverse-dark"
        ).pack(fill=X, padx=5, pady=(5, 3))
        
        json_display_frame = ttkb.Frame(right_frame)
        json_display_frame.pack(fill=BOTH, expand=YES)
        
        self.json_display = tk.Text(
            json_display_frame,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#9cdcfe",
            insertbackground="white",
            relief=FLAT,
            padx=10,
            pady=8,
            wrap=tk.WORD
        )
        json_scrollbar = ttkb.Scrollbar(json_display_frame, command=self.json_display.yview)
        self.json_display.configure(yscrollcommand=json_scrollbar.set)
        
        self.json_display.pack(side=LEFT, fill=BOTH, expand=YES)
        json_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Configure tags
        for widget in [self.headers_display, self.json_display]:
            widget.tag_config("blue", foreground="#569cd6")
            widget.tag_config("green", foreground="#4ec9b0")
            widget.tag_config("yellow", foreground="#dcdcaa")
            widget.tag_config("red", foreground="#f48771")
            widget.tag_config("orange", foreground="#ce9178")
            widget.tag_config("gray", foreground="#808080")
            widget.tag_config("white", foreground="#d4d4d4")
            widget.tag_config("json", foreground="#9cdcfe")
            widget.tag_config("bold", font=("Consolas", 10, "bold"))
        
        # Welcome
        self.print_headers("Ready to send requests\n", "blue")
        self.print_json("JSON response will appear here...\n", "gray")
        
    def print_headers(self, text, color="white", style=""):
        """Print to headers display"""
        tags = [color]
        if style:
            tags.append(style)
        self.headers_display.insert(tk.END, text, tuple(tags))
        self.headers_display.see(tk.END)
        
    def print_json(self, text, color="json", style=""):
        """Print to JSON display"""
        tags = [color]
        if style:
            tags.append(style)
        self.json_display.insert(tk.END, text, tuple(tags))
        self.json_display.see(tk.END)
        
    def clear_terminal(self):
        """Clear both displays"""
        self.headers_display.delete("1.0", tk.END)
        self.json_display.delete("1.0", tk.END)
        
    def format_json(self):
        """Format JSON in body editor"""
        try:
            content = self.body_text.get("1.0", tk.END).strip()
            parsed = json.loads(content)
            formatted = json.dumps(parsed, indent=2)
            self.body_text.delete("1.0", tk.END)
            self.body_text.insert("1.0", formatted)
        except json.JSONDecodeError as e:
            self.print_headers(f"✗ JSON error: {str(e)}\n", "red")
            
    def build_curl_command(self):
        """Build curl command"""
        method = self.method_var.get()
        url = self.url_entry.get().strip()
        
        if not url:
            raise ValueError("URL is required")
            
        cmd = ["curl", "-i", "-X", method]
        cmd.extend(["-H", f"Content-Type: {self.content_type_var.get()}"])
        
        custom_headers = self.headers_text.get("1.0", tk.END).strip()
        if custom_headers:
            for line in custom_headers.split("\n"):
                line = line.strip()
                if line and ":" in line:
                    cmd.extend(["-H", line])
        
        auth_type = self.auth_type_var.get()
        if auth_type == "Bearer Token":
            token = self.auth_field1.get().strip()
            if token:
                cmd.extend(["-H", f"Authorization: Bearer {token}"])
        elif auth_type == "Basic Auth":
            username = self.auth_field1.get().strip()
            password = self.auth_field2.get().strip()
            if username:
                cmd.extend(["-u", f"{username}:{password}"])
        elif auth_type == "API Key":
            api_key = self.auth_field1.get().strip()
            if api_key:
                cmd.extend(["-H", f"X-API-Key: {api_key}"])
        
        if method in ["POST", "PUT", "PATCH"]:
            body = self.body_text.get("1.0", tk.END).strip()
            if body:
                cmd.extend(["-d", body])
        
        params = self.params_text.get("1.0", tk.END).strip()
        if params:
            param_list = []
            for line in params.split("\n"):
                line = line.strip()
                if line and "=" in line:
                    param_list.append(line)
            if param_list:
                if "?" in url:
                    url += "&" + "&".join(param_list)
                else:
                    url += "?" + "&".join(param_list)
        
        cmd.append(url)
        return cmd
        
    def send_request(self):
        """Send request in thread"""
        thread = threading.Thread(target=self._send_request_thread, daemon=True)
        thread.start()
        
    def _send_request_thread(self):
        """Execute curl and display results"""
        try:
            self.send_button.configure(state="disabled", text="SENDING...")
            self.status_label.configure(text="● Sending...", bootstyle="warning")
            
            # Clear
            self.headers_display.delete("1.0", tk.END)
            self.json_display.delete("1.0", tk.END)
            
            cmd = self.build_curl_command()
            
            # Display request info
            self.print_headers(f"REQUEST - {datetime.now().strftime('%H:%M:%S')}\n", "blue", "bold")
            self.print_headers("─" * 45 + "\n", "gray")
            self.print_headers(f"{self.method_var.get()} {self.url_entry.get()}\n\n", "yellow")
            
            # Execute
            start_time = datetime.now()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            output = result.stdout if result.stdout else result.stderr
            
            # MELHOR PARSING - tenta vários separadores
            body_part = ""
            headers_part = output
            
            # Tenta separar por diferentes padrões
            for separator in ["\r\n\r\n", "\n\n", "\r\r"]:
                if separator in output:
                    parts = output.split(separator, 1)
                    headers_part = parts[0]
                    body_part = parts[1] if len(parts) > 1 else ""
                    break
            
            # Extract status
            status_match = re.search(r'HTTP/[\d.]+ (\d+)', headers_part)
            status_code = int(status_match.group(1)) if status_match else 0
            
            # Display headers
            self.print_headers("\nRESPONSE\n", "blue", "bold")
            self.print_headers("─" * 45 + "\n", "gray")
            
            if status_code:
                color = "green" if 200 <= status_code < 300 else "red" if status_code >= 400 else "orange"
                self.print_headers(f"Status: ", "gray")
                self.print_headers(f"{status_code}\n", color, "bold")
                self.print_headers(f"Time: {duration:.3f}s\n\n", "gray")
            
            self.print_headers("Headers:\n", "yellow")
            header_lines = [h for h in headers_part.split("\n") if h.strip()]
            for line in header_lines[:8]:  # Mostra mais headers
                if line.strip():
                    self.print_headers(f"{line}\n", "gray")
            if len(header_lines) > 8:
                self.print_headers(f"... ({len(header_lines) - 8} more)\n", "gray")
            
            self.print_headers(f"\n✓ Completed in {duration:.3f}s\n", "green")
            
            # Display body (JSON)
            if body_part.strip():
                try:
                    json_body = json.loads(body_part)
                    formatted_body = json.dumps(json_body, indent=2, ensure_ascii=False)
                    self.print_json(formatted_body + "\n", "json")
                except:
                    # Se não for JSON, mostra como texto
                    self.print_json(body_part + "\n", "white")
            else:
                self.print_json("(No body in response)\n", "gray")
            
            # Update status
            status_text = f"● {status_code}" if status_code else "● Complete"
            status_style = "success" if 200 <= status_code < 300 else "danger" if status_code >= 400 else "warning"
            self.status_label.configure(text=status_text, bootstyle=status_style)
            
        except subprocess.TimeoutExpired:
            self.print_headers("\n✗ Request timeout (30s)\n", "red")
            self.status_label.configure(text="● Timeout", bootstyle="danger")
        except Exception as e:
            self.print_headers(f"\n✗ Error: {str(e)}\n", "red")
            self.print_json(f"Error details:\n{str(e)}\n", "red")
            self.status_label.configure(text="● Error", bootstyle="danger")
        finally:
            self.send_button.configure(state="normal", text="SEND ⚡")
            self.update()

if __name__ == "__main__":
    app = HTTPClient()
    app.mainloop()
