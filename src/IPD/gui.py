from .main import run_simulation
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2Tk
from tkinter import Tk, Frame, IntVar, Button, Label, Menu, Canvas, Entry, TclError, BOTH, TOP, E, S, messagebox, ttk, DoubleVar
import matplotlib
matplotlib.use('TkAgg')


class SimulationGUI(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=BOTH)
        self.config(bg=bg['default'])

        self.header = Frame(self)
        self.graph_frame = Frame(self)
        self.footer = Frame(self)

        self.header.grid(row=0, column=0, columnspan=2)
        self.graph_frame.grid(row=1, column=1)
        self.footer.grid(row=2, column=0, columnspan=2)

        self.curr_row = 0

        self.init_settings()
        self.init_graph()
        self.init_menu()
        self.init_decor()

    def init_settings(self):
        self.setting_frame_top = Frame(self)
        self.setting_book = ttk.Notebook(self.setting_frame_top)
        self.setting_book.grid()
        self.setting_frame_mainsub = Frame(self)
        self.setting_frame_pop = Frame(self)
        self.setting_book.add(self.setting_frame_mainsub, text="Settings")
        self.setting_book.add(self.setting_frame_pop, text="Population")
        self.setting_frame_top.grid(row=1, column=0)
        self.init_strats()
        self.init_params()
        # self.init_presets()
        self.init_setting_buttons()

    def init_setting_buttons(self):

        self.setting_button_frame = Frame(self.setting_frame_top)
        self.clear_button = Button(self.setting_button_frame, text='Clear',
                                   font=fonts['sub_button'], height=2,
                                   command=self.reset)
        self.clear_button.grid(row=0, column=0)
        self.execute_button = Button(self.setting_button_frame, text='Execute',
                                     font=fonts['main_button'], height=2,
                                     command=self.confirm, bg='blue')
        self.execute_button.grid(row=0, column=1)
        self.setting_button_frame.grid(row=self.curr_row, column=0)
        self.curr_row += 1

    def init_strats(self):
        self.coop_strats = {
            'Kantian': IntVar(),
            'Tit for Tat': IntVar(),
            'Tit for 2 Tats': IntVar(),
            'Grudger': IntVar(),
        }
        self.self_strats = {
            'Defector': IntVar(),
            'Wary Tit for Tat': IntVar(),
            'Mean Tit for Tat': IntVar(),
            'Conniver': IntVar(),
            'Tester': IntVar(),
            'Grofman': IntVar()
        }
        self.neut_strats = {
            'Random': IntVar(),
        }
        self.all_strats = {
            'Cooperative strategies': self.coop_strats,
            'Mean strategies': self.self_strats,
            'Neutral strategies': self.neut_strats
        }
        Label(self.setting_frame_pop, text="Initial Profile",
              font=fonts['header'], height=2).grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for strategy_type in self.all_strats:
            Label(self.setting_frame_pop, text=strategy_type, font=fonts['sub_header'],
                  padx=15, width=15).grid(row=self.curr_row)
            self.curr_row += 1
            for strategy in self.all_strats[strategy_type]:
                self.all_strats[strategy_type][strategy].set(10)
                Label(self.setting_frame_pop, text=strategy + ' -', font=fonts['text'],
                      width=15, anchor=E).\
                    grid(row=self.curr_row, column=0)
                Entry(self.setting_frame_pop, width=entry_width, justify='right',
                      textvariable=self.all_strats[strategy_type][strategy]).\
                    grid(row=self.curr_row, column=1)
                self.curr_row += 1

    def init_params(self):
        self.param = {
            'Rounds': IntVar(),
            'Generations': IntVar(), 
            'Noise': DoubleVar()
        }
        self.param['Rounds'].set(10)
        self.param['Generations'].set(35)
        self.param['Noise'].set(0.1)

        Label(self.setting_frame_mainsub, text="Simulation settings",
              font=fonts['sub_header'], height=2, width=15, anchor=S).\
            grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for param in self.param:
            Label(self.setting_frame_mainsub, text=param + " -", width=12,
                  anchor=E).grid(row=self.curr_row, column=0)
            Entry(self.setting_frame_mainsub, width=entry_width, justify='right',
                  textvariable=self.param[param]).\
                grid(row=self.curr_row, column=1)
            self.curr_row += 1

    def init_presets(self):
        diverse = {
            # just make a function that changes all values to n.
        }
        defectors_among_kantians = {
            'Defector': 3,
            'Kantian': 97
        }
        tft_among_defectors = {
            'Tit for Tat': 3,
            'Defector': 97
        }
        all_presets = {
            'Defectors among Kantians': [defectors_among_kantians, None],
            'TFT among Defectors': [tft_among_defectors, None]
        }
        self.presets_frame = Frame(self.setting_frame_mainsub)
        Label(self.presets_frame, text="Presets",
              font=fonts['sub_header']).\
            grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for preset in all_presets:
            all_presets[preset][1] = Button(self.presets_frame, text='select',
                                            font=fonts['sub_button'],
                                            command=self.select_preset(preset))
            all_presets[preset][1].grid(row=self.curr_row, column=0)
            Label(self.presets_frame, text=preset).\
                grid(row=self.curr_row, column=1)
            self.curr_row += 1
        self.presets_frame.grid()

    def init_graph(self):
        self.fig = Figure(figsize=(8, 5.25), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.plot_filler()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        toolbar.update()
        self.canvas._tkcanvas.pack()

    def init_menu(self):
        main_menu = Menu(self.parent)
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(
            label='Execute', accelerator='Cmd+E', command=self.execute_plot)
        main_menu.add_cascade(label='File', menu=file_menu)
        self.parent.config(menu=main_menu)

    def init_decor(self):
        self.header.config(bg=bg['decor1'])
        self.footer.config(bg=bg['decor1'])
        top_canvas = Canvas(
            self.header, bg=bg['decor1'], height=25, width=1094)
        top_canvas.grid(row=0, column=0)
        bot_canvas = Canvas(
            self.footer, bg=bg['decor1'], height=25, width=1094)
        bot_canvas.grid(row=0, column=0)

    def set_graph_params(self):
        self.f.set_title("Population distibution with respect to time")
        self.f.set_xlabel("Generation")
        self.f.set_ylabel("Population density [%]")
        self.f.set_xbound(lower=0, upper=self.param['Generations'].get())
        self.f.set_ybound(lower=-5, upper=110)

    def plot_filler(self):
        self.fig.clear()
        self.f = self.fig.add_subplot(111)
        self.f.plot()
        self.set_graph_params()
        self.canvas.draw()

    def reset(self):
        response = messagebox.askquestion("Confirmation",
                                          "Are you sure you would like to "
                                          "reset simulation variables?")
        if response == 'yes':
            self.plot_filler()
            for strat_list in self.all_strats:
                for strat in self.all_strats[strat_list]:
                    self.all_strats[strat_list][strat].set(0)

    def compile_profile(self):
        profile = {}
        for strategy_type in self.all_strats:
            for strategy in self.all_strats[strategy_type]:
                try:
                    var = self.all_strats[strategy_type][strategy].get()
                except TclError:
                    messagebox.showerror("Warning",
                                         "Inputted values are invalid. Please try again.")
                    return
                if var > 0:
                    profile[strategy] = var
        return profile

    def confirm(self):
        response = messagebox.askquestion("Confirmation",
                                          "Are you sure you would like to "
                                          "execute this simulation?")
        if response == 'yes':

            self.execute_plot()

    def execute_plot(self):
        result = run_simulation(self.compile_profile(),
                                self.param['Generations'].get(),
                                self.param['Rounds'].get(), 
                                self.param["Noise"].get())
        self.fig.clear()
        x_axis = result.pop('gens')
        self.f = self.fig.add_subplot(111)
        for strat in result:
            self.f.plot(x_axis, result[strat], label=strat)
        self.set_graph_params()
        self.f.legend()
        self.canvas.draw()

    def quit_app(self):
        self.parent.quit()

    def select_preset(self, preset):
        pass


def run_gui():
    root = Tk()
    root.title("IPD Simulation")
    root.geometry("1100x631")
    root.resizable(False, False)
    ipd = SimulationGUI(root)
    root.mainloop()


fonts = {
    'header': 'Calibri 19 bold',
    'sub_header': 'Calibri 16 bold italic',
    'text': 'Calibri 14',
    'main_button': 'Calibri 14 italic',
    'sub_button': 'Calibri 12'
}

bg = {
    'default': '#DCDCDC',
    'main_button': '#435440',
    'decor1': '#1569C7',
    'test3': '#ffff66',
    'test4': '#7a1018',
    'test5': '#e8db1e'
}

entry_width = 4


if __name__ == '__main__':
    run_gui()
