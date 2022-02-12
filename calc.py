import tkinter as tk

LIGHT_GREY = '#F5F5F5'
LABEL_COLOR = '#25265E'
WHITE = '#FFF'
OFF_WHITE = '#F8FAFF'
LIGHT_BLUE = '#CCEDFF'
SMALL_FONT = ('Arial', 16)
LARGE_FONT = ('Arial', 40, 'bold')
DIGITS_FONT_STYLE = ('Arial', 24, 'bold')
DEFAULT_FONT = ('Arial', 20)


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x660")
        self.window.resizable(0, 0)
        self.window.title('Calculator')

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.current_expression = ''
        self.total_expression = ''
        self.total_label, self.current_label = self.create_label_expressions()

        self.digits = {
            '7': (1, 1), '8': (1, 2), '9': (1, 3),
            '4': (2, 1), '5': (2, 2), '6': (2, 3),
            '1': (3, 1), '2': (3, 2), '3': (3, 3),
            '0': (4, 2), '.': (4, 1),
        }
        self.operators = {'/': '\u00F7', '*': '\u00D7', '-': '-', '+': '+'}

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digits()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_square_root_button()
        self.bind_keys()

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GREY)
        frame.pack(expand=True, fill='both')
        return frame

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')
        return frame

    def create_label_expressions(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GREY,
                               fg=LABEL_COLOR, padx=18, font=SMALL_FONT)
        total_label.pack(expand=True, fill='both')
        current_label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GREY,
                                 fg=LABEL_COLOR, padx=15, font=LARGE_FONT)
        current_label.pack(expand=True, fill='both')
        return total_label, current_label

    def create_digits(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=digit, bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operators.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def create_clear_button(self):
        clear_button = tk.Button(self.buttons_frame, text='C', bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT,
                                 borderwidth=0, command=self.clear)
        clear_button.grid(row=0, column=1, sticky=tk.NSEW)

    def create_equals_button(self):
        equals_button = tk.Button(self.buttons_frame, text='=', bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT,
                                  borderwidth=0, command=self.evaluate)
        equals_button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_square_button(self):
        clear_button = tk.Button(self.buttons_frame, text='x\u00b2', bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT,
                                 borderwidth=0, command=self.square)
        clear_button.grid(row=0, column=2, sticky=tk.NSEW)

    def create_square_root_button(self):
        clear_button = tk.Button(self.buttons_frame, text='\u221ax', bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT,
                                 borderwidth=0, command=self.square_root)
        clear_button.grid(row=0, column=3, sticky=tk.NSEW)

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operators.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_current_label(self):
        self.current_label.config(text=self.current_expression[:10])

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_current_label()

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ''
        self.update_total_label()
        self.update_current_label()

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ''

        except Exception:
            self.current_expression = 'Error'
        finally:
            self.update_current_label()

    def clear(self):
        self.total_expression = ''
        self.current_expression = ''
        self.update_total_label()
        self.update_current_label()

    def square(self):
        self.current_expression = str(eval(f'{self.current_expression}**2'))
        self.update_current_label()

    def square_root(self):
        self.current_expression = str(eval(f'{self.current_expression}**0.5'))
        self.update_current_label()

    def bind_keys(self):
        self.window.bind('<Return>', lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operators:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    calc = Calculator()
    calc.run()
