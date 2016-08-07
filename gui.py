import tkFileDialog
import Tkinter as tk
from PIL import ImageTk, Image

def make_tk_image(imagepath):
    """
    Opens and reads in an image to display in tk widgets. Using for example
        img=make_tk_image(imagepath)
        label=tk.Label(foo,img=image)
    """
    return ImageTk.PhotoImage(Image.open(imagepath))


root = tk.Tk()
frame = tk.Frame(root)
frame.pack(side='left',expand=1,fill='both')

picdisplay = tk.Frame(root)
picdisplay.pack(side='right',expand=1,fill='both')
styledisplay = tk.LabelFrame(picdisplay,text='Style')
contentdisplay = tk.LabelFrame(picdisplay,text='Content',padx=3)
styledisplay.pack()
contentdisplay.pack()
tk.Label(styledisplay,text='foo').pack()
tk.Label(contentdisplay,text='foo').pack()


class FileChooser(tk.Frame):
    def __init__(self, master, label="FileChooser", op='open'):
        tk.Frame.__init__(self, master=master)
        self.label = tk.Label(self, text=label)
        self.entry_var = tk.StringVar(self)
        self.entry = tk.Entry(self, textvariable=self.entry_var, text='Entry')
        self.choice_button = tk.Button(self, text='^', command=self.on_button)
        self.label.pack(side='left')
        self.entry.pack(side='left',fill='x',expand='true')
        self.choice_button.pack(side='left')
        self.op = op

    def on_button(self):
        if self.op == 'open':
            chosen = tkFileDialog.askopenfilename()
        elif self.op == 'saveas':
            chosen = tkFileDialog.asksaveasfilename()
        if chosen != '':
            self.entry.delete(0, tk.END)
            self.entry.insert(0, chosen)


class ModelChooser(tk.Frame):
    def __init__(self, master, label='Model Choice',
                 models=("vgg19", "vgg16", "googlenet", "caffenet")):
        tk.Frame.__init__(self, master=master)
        # label
        self.label = tk.Label(self, text=label)
        # model choice dropdown
        self._models = models
        self.model_choice_var = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.model_choice_var, *self._models)
        # pack
        self.label.pack(side='left')
        self.dropdown.pack(side='right',expand=1,fill='x')
    def get(self):
        return self.model_choice_var.get()

class IntOptionChooser(tk.Frame):
    def __init__(self,master,label='IntOptionChooser',default=None):
        tk.Frame.__init__(self, master=master)
        # label
        self.label = tk.Label(self, text=label)
        # entry
        self.entryvar = tk.StringVar(self)
        self.entry = tk.Entry(self, textvariable=self.entryvar)
        # pack
        self.label.pack(side='left',fill='x')
        self.entry.pack(side='right',fill='x')
        if default:
            self.entryvar.set(str(default))

    def get(self):
        return self.entryvar.get()


if __name__ == '__main__':
    # File Selectors
    style = FileChooser(frame, label="Style Image Filename", op="open")
    content = FileChooser(frame, label="Content Image Filename", op="open")
    output = FileChooser(frame, label="Output Image Filename", op="saveas")
    # Model chooser
    model_chooser = ModelChooser(frame)
    # Calibrations
    ratio = IntOptionChooser(frame,label="Style/Content Ratio (int,default:1e4)",default=1e4)
    num_iters = IntOptionChooser(frame,label="Number of Iterations (int,default:512)",default=512)
    max_image_length = IntOptionChooser(frame,label="Max Image Length (int,default:512)",default=512)

    # Confirm, Cancel Buttons
    def confirm():
        command_list = ["python", "style.py",
                        "-s", style.entry.get(),
                        "-c", content.entry.get(),
                        "-o", output.entry.get(),
                        "-m", model_chooser.get(),
                        "-r", ratio.get(),
                        "-n", num_iters.get(),
                        "-l", max_image_length.get(),
                        "-g", "-1"
                        ]
        print(" ".join(command_list))
    confirm_button = tk.Button(frame, text='Ok', command=confirm, bg='green')
    cancel_button = tk.Button(frame, text='Cancel', command=root.destroy, bg='red')

    # Pack Everything
    style.pack(side='top',fill='x',expand='true')
    content.pack(side='top',fill='x',expand='true')
    output.pack(side='top',fill='x',expand='true')
    model_chooser.pack(side='top',fill='x',expand='true')
    ratio.pack(side='top',fill='x',expand='true')
    num_iters.pack(side='top',fill='x',expand='true')
    max_image_length.pack(side='top',fill='x',expand='true')
    confirm_button.pack()
    cancel_button.pack()

    # Run the program
    root.mainloop()