import re
from ply import lex, yacc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Lexer:
    def __init__(self):
        self.reservada_keywords = ['if', 'else', 'while', 'for', 'int', 'float', 'Cadena', 'print', 'end']
        self.Simboloss = ['=', '==', '!=', '<', '>', '<=', '>=', '(', ')', '{', '}', ';', ',', '"', "'", '[', ']', '%']
        self.token_patterns = [
            ('Cadena', r'"(?:[^"\\]|\\.)*"'),
            ('VARIABLE', r'\$\w+'),
            ('Numero', r'\d+(\.?\d+)?'),
            ('reservada', '|'.join(r'\b' + re.escape(keyword) + r'\b' for keyword in self.reservada_keywords)),
            ('Identificador', r'[A-Za-z_][A-Za-z0-9_]*'),
            ('Operadores', r'[+\-*/]'),
            ('Simbolos', '|'.join(map(re.escape, self.Simboloss))),
            ('SPACE', r'\s+'),
        ]
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns)
        self.token_pattern = re.compile(self.token_regex)

    def tokenize(self, text):
        tokens = []
        position = 0
        while position < len(text):
            match = self.token_pattern.match(text, position)
            if match:
                token_type = match.lastgroup
                if token_type != 'SPACE':
                    token_value = match.group(token_type)
                    tokens.append((token_type, token_value))
                position = match.end()
            else:
                position += 1
        return tokens

class LexerApp:
    def __init__(self):
        self.windows = tk.Tk()
        self.windows.title("Analizador Léxico y Sintatico")
        self.windows.geometry("1000x720")

        self.text_label = tk.Label(text="Ingrese texto a analizar", height=2)
        self.text_label.pack()

        self.text_label = tk.Label(text="Luis Antonio Castro Gutiérrez\n 6 M\nUniversidad Autónoma de Chiapas", height=3)
        self.text_label.pack(side="bottom", pady=40)

        self.text_input = tk.Text(self.windows, height=10, width=50)
        self.text_input.insert("1.0",
                            'for i in (0..9)\n  if i % 2 == 0\n     print i.to_s + " es par\\n" \n else\n    print i.to_s + " no es par\\n"\n  end\nend')
        self.text_input.pack()

        # Color
        self.text_input.tag_configure("highlight", background="#fdfd96")

        self.button_frame = tk.Frame(self.windows)
        self.button_frame.pack()

        self.analyze_button = tk.Button(self.button_frame, text="Analizar", command=self.analyze_text)
        self.analyze_button.pack(side="left", padx=10)

        self.clean_button = tk.Button(self.button_frame, text="Limpiar", command=self.clean_text)
        self.clean_button.pack(side="left", padx=10)

        self.tree = ttk.Treeview(self.windows, columns=("Linea", "Token", "Valor", "Reservada", "Cadena", "Identificador", "Símbolo", "Operadores", "Numero"))
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("Linea", text="Linea")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Reservada", text="Reservada")
        self.tree.heading("Cadena", text="Cadena")
        self.tree.heading("Identificador", text="Identificador")
        self.tree.heading("Símbolo", text="Símbolo")
        self.tree.heading("Operadores", text="Operadores")
        self.tree.heading("Numero", text="Numero")

        self.tree.column("Linea", anchor="center")
        self.tree.column("Token", anchor="center")
        self.tree.column("Valor", anchor="center")
        self.tree.column("Reservada", anchor="center")
        self.tree.column("Cadena", anchor="center")
        self.tree.column("Identificador", anchor="center")
        self.tree.column("Símbolo", anchor="center")
        self.tree.column("Operadores", anchor="center")
        self.tree.column("Numero", anchor="center")
        self.tree.pack()

        self.count_tree = ttk.Treeview(self.windows, columns=("Objeto", "Cantidad"), show="headings")
        self.count_tree.heading("Objeto", text="Objeto")
        self.count_tree.heading("Cantidad", text="Cantidad")
        self.count_tree.column("Objeto", width=200, minwidth=100, anchor="center")
        self.count_tree.column("Cantidad", width=200, minwidth=100, anchor="center")
        self.count_tree.pack(pady=10)

    def analyze_text(self):
        lexer = Lexer()
        text = self.text_input.get("1.0", "end")
        lines = text.split('\n')
        tokens_by_line = [lexer.tokenize(line) for line in lines]

        self.tree.delete(*self.tree.get_children())
        self.count_tree.delete(*self.count_tree.get_children())

        count_tokens = {
            'Cadena': 0,
            'reservada': 0,
            'Numero': 0,
            'Identificador': 0,
            'Simbolos': 0,
            'Operadores': 0
        }

        count_elements = {
            ';': 0,
            '(': 0,
            ')': 0,
            '{': 0,
            '}': 0,
            '[': 0,
            ']': 0
        }

        for line_number, line_tokens in enumerate(tokens_by_line, start=1):
            for token_type, token_value in line_tokens:
                row_data = [line_number, token_type, token_value, "", "", "", "", "", ""]
                if token_type == 'reservada':
                    if token_value in lexer.reservada_keywords:
                        row_data[3] = "x"
                        count_tokens['reservada'] += 1
                elif token_type == 'Identificador':
                    row_data[5] = "x"
                    count_tokens['Identificador'] += 1
                elif token_type == 'Simbolos':
                    row_data[6] = "x"
                    count_tokens['Simbolos'] += 1
                    if token_value in count_elements:
                        count_elements[token_value] += 1
                elif token_type == 'Cadena':
                    row_data[4] = "x"
                    count_tokens['Cadena'] += 1
                elif token_type == 'Operadores':
                    row_data[7] = "x"
                    count_tokens['Operadores'] += 1
                elif token_type == 'Numero':
                    row_data[8] = "x"
                    count_tokens['Numero'] += 1

                self.tree.insert("", "end", values=row_data)

        for element, count in count_elements.items():
            self.count_tree.insert("", "end", values=(element, count))

        for token_type, count in count_tokens.items():
            self.count_tree.insert("", "end", values=(token_type, count))

        # Ahora realiza el análisis sintáctico
        self.parse_code(text)

    def clean_text(self):
        self.text_input.delete("1.0", "end")
        self.tree.delete(*self.tree.get_children())
        self.count_tree.delete(*self.count_tree.get_children())

    def run(self):
        self.windows.mainloop()

    tokens = (
        'FOR',
        'IF',
        'ELSE',
        'ID',
        'NUM',
        'STRING',
        'PLUS',
        'SEMICOLON',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'DOT',
        'EQUALS',
        'LEQ',
        'NOTEQ',
    )

    t_PLUS = r'\+'
    t_SEMICOLON = r';'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_DOT = r'\.'
    t_EQUALS = r'='
    t_LEQ = r'<='
    t_NOTEQ = r'!='

    def t_STRING(t):
        r'\".*?\"'
        t.value = t.value[1:-1]
        return t

    def t_ID(t):
        r'[a-zA-Z#%_][a-zA-Z0-9#%_]*'
        if t.value == 'for':
            t.type = 'FOR'
        elif t.value == 'if':
            t.type = 'IF'
        elif t.value == 'else':
            t.type = 'ELSE'
        return t

    def t_NUM(t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_ignore = ' \t\n'

    def t_error(t):
        app.error_message(f"Token desconocido '{t.value[0]}'", t.lineno)
        t.lexer.skip(1)

    lexer = lex.lex()

    def p_for_loop(p):
        '''for_loop : FOR ID ID  LPAREN NUM DOT DOT NUM RPAREN IF ID ID NUM EQUALS EQUALS NUM ID ID DOT ID PLUS STRING ELSE ID ID DOT ID PLUS STRING ID ID'''
        pass

    def p_error(p):
        if p:
            app.error_message(f"Error de sintaxis en '{p.value}'", p.lineno)
        else:
            # Replace the following line with appropriate error handling or reference
            app.error_message("Error de sintaxis: final inesperado del código",
                              len(app.text_input.get("1.0", "end-1c").split('\n')))

    parser = yacc.yacc()

    def lex_analyzer(self, code):
        self.lexer.input(code)
        tokens = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            tokens.append((token.lineno, token.type, token.value))
        return tokens

    def parse_code(self, code):
        try:
            self.parser.parse(code, lexer=self.lexer)
        except Exception as e:
            line_number = getattr(e, 'lineno', -1)
            if line_number == -1 and hasattr(self.lexer, 'lineno'):
                line_number = self.lexer.lineno
            self.error_message(str(e), line_number)

    def error_message(self, message, line_number):
        messagebox.showerror("Error de sintaxis", f"{message}\nEn la línea {line_number}")

    def process_code(self):
        code = self.text_input.get("1.0", "end-1c")
        tokens = self.lex_analyzer(code)
        for token in tokens:
            line_number, token_type, token_value = token
            print(f"Línea ->: {token_type} -> {token_value}")
        self.parse_code(code)

app = LexerApp()
app.run()
