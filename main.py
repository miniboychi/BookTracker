
import json
import os
from tkinter import *
from tkinter import ttk, messagebox

data_file = "books.json"
books = []

if os.path.exists(data_file):
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            books = json.load(f)
    except:
        books = []
else:
    books = [
        {"title": "Преступление и наказание", "author": "Ф. Достоевский", "genre": "Классика", "pages": 672},
        {"title": "Гарри Поттер и философский камень", "author": "Дж. Роулинг", "genre": "Фэнтези", "pages": 432},
        {"title": "1984", "author": "Дж. Оруэлл", "genre": "Антиутопия", "pages": 328}
    ]

def save_data():
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def refresh_table():
    for item in tree.get_children():
        tree.delete(item)
    
    filtered = books.copy()
    
    selected_genre = genre_filter.get()
    if selected_genre and selected_genre != "Все жанры":
        filtered = [b for b in filtered if b['genre'] == selected_genre]
    
    pages_value = pages_threshold.get().strip()
    if pages_value:
        try:
            threshold = int(pages_value)
            filtered = [b for b in filtered if b['pages'] > threshold]
        except:
            pass
    
    for book in filtered:
        tree.insert("", END, values=(book['title'], book['author'], book['genre'], book['pages']))
    
    status_label.config(text=f"Показано книг: {len(filtered)} из {len(books)}")

def update_genre_filter_options():
    genres = sorted(set(book['genre'] for book in books))
    genres.insert(0, "Все жанры")
    genre_filter['values'] = genres
    if not genre_filter.get():
        genre_filter.set("Все жанры")

def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages_str = pages_entry.get().strip()
    
    if not title or not author or not genre or not pages_str:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return
    
    try:
        pages = int(pages_str)
        if pages <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
        return
    
    books.append({
        "title": title,
        "author": author,
        "genre": genre,
        "pages": pages
    })
    
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    genre_entry.delete(0, END)
    pages_entry.delete(0, END)
    
    save_data()
    update_genre_filter_options()
    refresh_table()
    status_label.config(text=f"Книга '{title}' добавлена")

def delete_book():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Предупреждение", "Выберите книгу для удаления!")
        return
    
    if messagebox.askyesno("Подтверждение", "Удалить выбранную книгу?"):
        item = tree.item(selected[0])
        title = item['values'][0]
        
        for i, book in enumerate(books):
            if book['title'] == title:
                del books[i]
                break
        
        save_data()
        update_genre_filter_options()
        refresh_table()
        status_label.config(text=f"Книга '{title}' удалена")

def reset_genre_filter():
    genre_filter.set("Все жанры")
    refresh_table()

def apply_pages_filter():
    refresh_table()

def reset_all_filters():
    genre_filter.set("Все жанры")
    pages_threshold.delete(0, END)
    refresh_table()

root = Tk()
root.title("Book Tracker - Трекер прочитанных книг")
root.geometry("900x600")
root.resizable(True, True)

input_frame = LabelFrame(root, text="Добавление новой книги", padx=10, pady=10, font=("Arial", 12, "bold"))
input_frame.pack(fill="x", padx=10, pady=10)

Label(input_frame, text="Название книги:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
title_entry = Entry(input_frame, width=30, font=("Arial", 10))
title_entry.grid(row=0, column=1, padx=5, pady=5)

Label(input_frame, text="Автор:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
author_entry = Entry(input_frame, width=30, font=("Arial", 10))
author_entry.grid(row=1, column=1, padx=5, pady=5)

Label(input_frame, text="Жанр:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
genre_entry = Entry(input_frame, width=30, font=("Arial", 10))
genre_entry.grid(row=2, column=1, padx=5, pady=5)

Label(input_frame, text="Количество страниц:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
pages_entry = Entry(input_frame, width=30, font=("Arial", 10))
pages_entry.grid(row=3, column=1, padx=5, pady=5)

add_btn = Button(input_frame, text="➕ Добавить книгу", command=add_book, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
add_btn.grid(row=4, column=0, columnspan=2, pady=10)

filter_frame = LabelFrame(root, text="Фильтрация", padx=10, pady=10, font=("Arial", 12, "bold"))
filter_frame.pack(fill="x", padx=10, pady=10)

Label(filter_frame, text="Фильтр по жанру:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
genre_filter = ttk.Combobox(filter_frame, width=25, font=("Arial", 10))
genre_filter.grid(row=0, column=1, padx=5, pady=5)
genre_filter.bind("<<ComboboxSelected>>", lambda e: refresh_table())

Button(filter_frame, text="Сбросить жанр", command=reset_genre_filter, bg="#ff9800", fg="white", font=("Arial", 9)).grid(row=0, column=2, padx=5, pady=5)

Label(filter_frame, text="Страниц больше:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
pages_threshold = Entry(filter_frame, width=10, font=("Arial", 10))
pages_threshold.grid(row=1, column=1, sticky="w", padx=5, pady=5)

Button(filter_frame, text="Применить фильтр", command=apply_pages_filter, bg="#2196F3", fg="white", font=("Arial", 9)).grid(row=1, column=2, padx=5, pady=5)
Button(filter_frame, text="Сбросить все фильтры", command=reset_all_filters, bg="#f44336", fg="white", font=("Arial", 9)).grid(row=1, column=3, padx=5, pady=5)

table_frame = Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("Название", "Автор", "Жанр", "Страницы")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

tree.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

Button(root, text="🗑 Удалить выбранную книгу", command=delete_book, bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=5)

status_label = Label(root, text="Готово", bd=1, relief=SUNKEN, anchor=W, font=("Arial", 9))
status_label.pack(side=BOTTOM, fill="x")

update_genre_filter_options()
refresh_table()

root.mainloop()
