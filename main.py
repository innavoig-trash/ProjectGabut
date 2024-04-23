import random
import tkinter
from tkinter import messagebox
from tkinter import ttk
from tkinter import END, BOTH
from os.path import join


class App:
    def __init__(self, data: dict) -> None:
        # set attributes
        self.data = data
        self.max = max([len(word) for words in self.data.values() for word in words])
        print(self.max)

        # Create the main window
        self.window = tkinter.Tk()
        self.window.title('Hangman')
        self.window.minsize(width=400, height=200)
        self.window.resizable(False, False)

        # setting icon
        self.window.iconbitmap('assets/icon.ico')

        # create main frame
        self.frame = ttk.Frame(self.window)
        self.frame.pack()

        # list of hangman images
        self.images = [tkinter.PhotoImage(file=join('assets', f'hangman-{index}.png')) for index in range(1, 12)]

    def run(self) -> None:
        # change to default screen
        self.welcome()

        # run the main loop
        self.window.mainloop()

    def welcome(self) -> None:
        # create frame
        self.frame.destroy()
        self.frame = ttk.Frame(self.window)

        # set padding for frame
        self.frame.propagate(False)
        self.frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # create header label
        self.header = ttk.Label(self.frame, text='Welcome To Hangman!', font=('Open Sans', 13, 'bold'))
        self.header.grid(row=0, column=0, sticky='nsew', columnspan=2, padx=10, pady=(0, 20))

        # crate label to choose difficulty
        ttk.Label(self.frame, text='Choose Difficulty').grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))

        # create button for each difficulty
        for index, difficulty in enumerate(self.data.keys()):
            button = ttk.Button(self.frame, text=difficulty, command=lambda key=difficulty: self.game(key), width=60)
            button.grid(row=2 + index, column=0, sticky='nsew', padx=10, pady=(0, 5), ipadx=10, ipady=5)

        # exit button
        self.back = ttk.Button(self.frame, text='exit', command=self.window.destroy, width=60)
        self.back.grid(row=2 + len(self.data), column=0, sticky='nsew', padx=10, pady=(0, 10), ipadx=5, ipady=5)

    def game(self, difficulty: str) -> None:
        # create frame
        self.frame.destroy()
        self.frame = ttk.Frame(self.window)

        # set padding for frame
        self.frame.propagate(False)
        self.frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # get random word from dictionary
        self.word = random.choice(list(self.data[difficulty])).lower()

        # create a set to store guessed letters
        self.guessed = set()

        # store wrong guesses
        self.wrong = 0

        # create header label in left top of frame
        self.header = ttk.Label(self.frame, text='Play Hangman!', font=('Open Sans', 13, 'bold'))
        self.header.grid(row=0, column=0, sticky='nsew', padx=10, pady=(0, 20))

        # back button on the left top of frame
        self.back = ttk.Button(self.frame, text='back', command=self.welcome, width=3)
        self.back.grid(row=0, column=self.max - 1, sticky='nsew', padx=10, pady=(0, 20), ipadx=5, ipady=5)

        # create a canvas to draw hangman
        self.canvas = tkinter.Canvas(self.frame, width=400, height=300, background='white')
        self.canvas.grid(row=1, column=0, sticky='nsew', columnspan=self.max, padx=10, pady=(0, 10))

        # draw hangman image in canvass
        self.draw(self.canvas)

        # create a empry button to show the word
        self.display(self.frame, row=2)

        # create keyboards button with qwerty layout
        self.keyboards(self.frame, row=3)

    def keyboards(self, frame: ttk.Frame, row: int) -> None:
        # initialize layout position for each line and keys
        keyboard = [ttk.Frame(frame) for _ in range(3)]
        keys = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

        # place keyboard on the frame
        for index, line in enumerate(keyboard):
            line.grid(row=index + row, column=0, columnspan=self.max, padx=10)

        # place keys on the keyboard
        for index, line in enumerate(keyboard):
            for row, letter in enumerate(keys[index]):
                # check if the letter is in the word
                if letter not in self.guessed:
                    button = ttk.Button(line, text=letter, command=lambda letter=letter: self.guess(letter), width=2)
                else:
                    button = ttk.Button(line, text=letter, state='disabled', width=2)
                button.grid(row=0, column=row, padx=1, pady=2 if index < 2 else (2, 10), ipadx=8, ipady=5)

    def display(self, frame: ttk.Frame, row: int) -> None:
        # initialize layout position
        placeholder = ttk.Frame(frame)
        placeholder.grid(row=row, column=0, columnspan=self.max, padx=10, pady=(0, 10))

        # place placeholder on the frame
        for index, letter in enumerate(self.word):
            # check if the letter is in the word
            if letter not in self.guessed:
                button = ttk.Button(placeholder, text='_', command=lambda letter=letter: self.guess(letter), width=2)
            else:
                button = ttk.Button(placeholder, text=letter, width=2)
            button.grid(row=0, column=index, padx=1, pady=2, ipadx=8, ipady=5)

    def draw(self, canvas: tkinter.Canvas) -> None:
        # draw image based on the number of wrong guesses
        canvas.create_image(200, 150, image=self.images[self.wrong])

    def is_winning(self) -> bool:
        # check if every letter in the word is guessed
        return all(letter in self.guessed for letter in self.word)

    def guess(self, letter: str) -> None:
        # add letter to guessed set
        self.guessed.add(letter)
        self.keyboards(self.frame, row=3)

        # check if letter is in the word
        if letter not in self.word:
            self.wrong += 1
            self.draw(self.canvas)
        else:
            self.display(self.frame, row=2)

        # check if the game is over
        if self.wrong == len(self.images) - 1:
            messagebox.showinfo('Game Over', 'Too bad, you lose', parent=self.window)
            self.welcome()

        # check if the game is won
        if self.is_winning():
            messagebox.showinfo('Congratulation', 'Congratulation You Win!', parent=self.window)
            self.welcome()


def main() -> None:

    # set difficulties
    DIFFICULTIES = ['easy', 'medium', 'hard']

    # read data from txt file
    data = dict()
    for difficulty in DIFFICULTIES:
        with open(f'{difficulty}.txt', 'r') as file:
            data[difficulty] = file.read().splitlines()

    # create app
    app = App(data)

    # run app
    app.run()


if __name__ == '__main__':
    main()
