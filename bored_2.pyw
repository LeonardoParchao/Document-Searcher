import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading

def search_web_documents(query=None, domain=None, tld=None, url_text=None, num_results=1000, start_date=None, end_date=None, file_type=None, language=None, progress_callback=None, proxy=None, search_engine="Google"):
    search_components = []
    
    if tld:
        search_components.append(f"site:.{tld}")
    
    if domain:
        search_components.append(f"site:{domain}")
    
    if query:
        search_components.append(query)
    
    if url_text:
        search_components.append(f"inurl:{url_text}")
    
    if file_type == "All":
        search_components.append("(filetype:pdf OR filetype:doc OR filetype:docx)")
    elif file_type:
        search_components.append(f"filetype:{file_type.lower()}")
    
    if start_date and end_date:
        search_components.append(f"daterange:{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}")
    elif start_date:
        search_components.append(f"after:{start_date.strftime('%Y-%m-%d')}")
    elif end_date:
        search_components.append(f"before:{end_date.strftime('%Y-%m-%d')}")
    
    search_query = " ".join(search_components)
    
    if search_engine == "Google":
        search_url = f"https://www.google.com/search?q={search_query}&num={num_results}"
        if language and language != "Any":
            search_url += f"&lr=lang_{language}"
    elif search_engine == "Bing":
        search_url = f"https://www.bing.com/search?q={search_query}&count={num_results}"
        if language and language != "Any":
            search_url += f"&setlang={language}"
    elif search_engine == "DuckDuckGo":
        search_url = f"https://html.duckduckgo.com/html/?q={search_query}"
    elif search_engine == "Yandex":
        search_url = f"https://yandex.com/search/?text={search_query}&numdoc={num_results}"
        if language and language != "Any":
            search_url += f"&lang={language}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    proxies = None
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy
        }
    
    try:
        response = requests.get(search_url, headers=headers, proxies=proxies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        document_links = []
        
        if search_engine == "Google":
            results = soup.find_all('div', class_='yuRUbf')
        elif search_engine == "Bing":
            results = soup.find_all('li', class_='b_algo')
        elif search_engine == "DuckDuckGo":
            results = soup.find_all('div', class_='links_main')
        elif search_engine == "Yandex":
            results = soup.find_all('li', class_='serp-item')
        
        total_results = len(results)
        
        for i, result in enumerate(results):
            if search_engine == "Google":
                link = result.find('a')['href']
            elif search_engine == "Bing":
                link = result.find('a')['href']
            elif search_engine == "DuckDuckGo":
                link = result.find('a', class_='result__a')['href']
            elif search_engine == "Yandex":
                link = result.find('a', class_='link')['href']
            
            if file_type == "All":
                if re.search(r'\.(pdf|doc|docx)$', link, re.IGNORECASE):
                    document_links.append(link)
            elif file_type:
                if re.search(rf'\.{file_type.lower()}$', link, re.IGNORECASE):
                    document_links.append(link)
            else:
                document_links.append(link)
            
            if progress_callback:
                progress_callback(i + 1, total_results)
        
        return document_links
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def update_progress(current, total):
    progress = int((current / total) * 100)
    progress_bar['value'] = progress
    status_label.config(text=f"Searching... {current}/{total} ({progress}%)")
    root.update_idletasks()

def on_clear():
    query_entry.delete(0, tk.END)
    domain_entry.delete(0, tk.END)
    tld_entry.delete(0, tk.END)
    url_text_entry.delete(0, tk.END)
    start_date_entry.delete(0, tk.END)
    end_date_entry.delete(0, tk.END)
    file_type_combobox.set("All")
    language_combobox.set("Any")
    search_engine_combobox.set("Google")
    proxy_entry.delete(0, tk.END)
    result_listbox.delete(0, tk.END)
    progress_bar['value'] = 0
    status_label.config(text="Cleared")


def on_search():
    query = query_entry.get().strip()
    domain = domain_entry.get().strip()
    tld = tld_entry.get().strip()
    url_text = url_text_entry.get().strip()
    start_date_str = start_date_entry.get().strip()
    end_date_str = end_date_entry.get().strip()
    file_type = file_type_combobox.get()
    language = language_combobox.get()
    proxy = proxy_entry.get().strip()
    search_engine = search_engine_combobox.get()

    if not query and not domain and not tld and not url_text:
        messagebox.showwarning("Input Error", "Please enter a search query, a domain, a TLD, a URL text, or a combination of these.")
        return
    
    start_date = None
    end_date = None

    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning("Date Error", "Please enter the start date in DD-MM-YYYY format.")
            return

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning("Date Error", "Please enter the end date in DD-MM-YYYY format.")
            return

    if start_date and end_date and start_date > end_date:
        messagebox.showwarning("Date Error", "Start date must be before or equal to end date.")
        return

    progress_bar['value'] = 0
    status_label.config(text="Preparing search...")
    search_button.config(state=tk.DISABLED)

    def search_thread():
        results = search_web_documents(query, domain, tld, url_text, start_date=start_date, end_date=end_date,
                                       file_type=file_type, language=language, progress_callback=update_progress,
                                       proxy=proxy, search_engine=search_engine)
        
        result_listbox.delete(0, tk.END)  # Clear previous results

        if results:
            for link in results:
                result_listbox.insert(tk.END, link)
        else:
            result_listbox.insert(tk.END, "No documents found.")
        
        progress_bar['value'] = 100
        status_label.config(text="Search completed!")
        search_button.config(state=tk.NORMAL)

    threading.Thread(target=search_thread, daemon=True).start()

def show_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{widget.winfo_rootx() + 20}+{widget.winfo_rooty() + 20}")
    label = ttk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1, padding=5)
    label.pack()
    
    def hide_tooltip(event):
        tooltip.destroy()
    
    widget.bind('<Leave>', hide_tooltip)

def on_listbox_click(event):
    selected = result_listbox.curselection()
    if selected:
        link = result_listbox.get(selected[0])
        if link.startswith("http"):
            import webbrowser
            webbrowser.open(link)

def create_gui():
    global root, progress_bar, status_label, search_button, result_listbox

    root = tk.Tk()
    root.title("Web Document Search")

    # Configure grid weights for responsiveness
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=0)

    # Main Frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, columnspan=2, rowspan=5, sticky="nsew")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=2)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_rowconfigure(4, weight=0)

    # Group search criteria fields in one frame
    criteria_frame = ttk.Labelframe(main_frame, text="Search Criteria", padding="10")
    criteria_frame.grid(row=0, column=0, sticky="ew")

    ttk.Label(criteria_frame, text="Top-Level Domain (optional):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    global tld_entry
    tld_entry = ttk.Entry(criteria_frame, width=50)
    tld_entry.grid(row=0, column=1, padx=5, pady=5)
    tld_entry.insert(0, "e.g., com, org")

    ttk.Label(criteria_frame, text="Domain (optional):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    global domain_entry
    domain_entry = ttk.Entry(criteria_frame, width=50)
    domain_entry.grid(row=1, column=1, padx=5, pady=5)
    domain_entry.insert(0, "e.g., example.com")

    ttk.Label(criteria_frame, text="Search Query (optional):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    global query_entry
    query_entry = ttk.Entry(criteria_frame, width=50)
    query_entry.grid(row=2, column=1, padx=5, pady=5)
    query_entry.insert(0, "Enter keywords")

    ttk.Label(criteria_frame, text="URL Text (optional):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    global url_text_entry
    url_text_entry = ttk.Entry(criteria_frame, width=50)
    url_text_entry.grid(row=3, column=1, padx=5, pady=5)
    url_text_entry.insert(0, "Text in URL")

    # Date Filter Frame
    date_frame = ttk.Labelframe(main_frame, text="Date Filters", padding="10")
    date_frame.grid(row=1, column=0, sticky="ew")

    ttk.Label(date_frame, text="Start Date (DD-MM-YYYY):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    global start_date_entry
    start_date_entry = ttk.Entry(date_frame, width=50)
    start_date_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(date_frame, text="End Date (DD-MM-YYYY):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    global end_date_entry
    end_date_entry = ttk.Entry(date_frame, width=50)
    end_date_entry.grid(row=1, column=1, padx=5, pady=5)

    # Options Frame
    options_frame = ttk.Labelframe(main_frame, text="Search Options", padding="10")
    options_frame.grid(row=2, column=0, sticky="ew")

    ttk.Label(options_frame, text="File Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    global file_type_combobox
    file_type_combobox = ttk.Combobox(options_frame, values=["All", "PDF", "DOC", "DOCX"], width=47)
    file_type_combobox.set("All")
    file_type_combobox.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(options_frame, text="Language:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    global language_combobox
    language_combobox = ttk.Combobox(options_frame, values=["Any", "en", "fr", "de", "es", "it", "pt", "ru", "zh-CN", "ja"], width=47)
    language_combobox.set("Any")
    language_combobox.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(options_frame, text="Search Engine:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    global search_engine_combobox
    search_engine_combobox = ttk.Combobox(options_frame, values=["Google", "Bing", "DuckDuckGo"], width=47)
    search_engine_combobox.set("Google")
    search_engine_combobox.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(options_frame, text="Proxy (optional):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    global proxy_entry
    proxy_entry = ttk.Entry(options_frame, width=50)
    proxy_entry.grid(row=3, column=1, padx=5, pady=5)
    proxy_entry.insert(0, "http://proxy.example.com:8080")

    # Results Frame
    result_frame = ttk.Labelframe(main_frame, text="Search Results", padding="10")
    result_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

    result_frame.grid_rowconfigure(0, weight=1)
    result_frame.grid_columnconfigure(0, weight=1)

    global result_listbox
    result_listbox = tk.Listbox(result_frame, height=25, width=50)
    result_listbox.grid(row=0, column=0, sticky="nsew")
    result_listbox.bind("<Double-Button-1>", on_listbox_click)

    result_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_listbox.yview)
    result_scrollbar.grid(row=0, column=1, sticky="ns")
    result_listbox.config(yscrollcommand=result_scrollbar.set)

    # Search Button
    search_button = ttk.Button(main_frame, text="Search", command=on_search)
    search_button.grid(row=3, column=0, pady=10)

    # Progress Bar and Status
    progress_frame = ttk.Frame(main_frame, padding="10")
    progress_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

    progress_frame.grid_rowconfigure(0, weight=1)
    progress_frame.grid_columnconfigure(0, weight=1)

    global progress_bar
    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
    progress_bar.pack(fill="x", expand=True, pady=5)

    global status_label
    status_label = ttk.Label(progress_frame, text="Ready")
    status_label.pack(anchor="w")

    # Clear Button
    clear_button = ttk.Button(options_frame, text="Clear", command=on_clear)
    clear_button.grid(row=4, column=0, padx=5, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()