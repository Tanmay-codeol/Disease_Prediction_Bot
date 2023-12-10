import pandas as pd
from tkinter import *
from tkinter import ttk
import predictor


dis_df = pd.read_csv('./data.csv', index_col='disease')

df = pd.read_csv("./disease_symptoms_weight.csv",
                 index_col='Disease').iloc[:, 1:-1]

sympts = df.columns.tolist()

sevrty = pd.read_csv("symptom_severity.csv", index_col="Symptom")
sevrty.sort_index(inplace=True)


shown_list = list(map(lambda x: x.replace("_", " "), sympts))
shown_list = list(map(lambda x: "   "+x, shown_list))

real_in_sympt_lst = []

txt_state = 0


def weightadder(lst: list):

    if len(lst) < 3:
        dis_err("to_few_symptoms")
        return

    # input_symptoms = lst
    input_symptoms = lst

    input_symptoms_list = []

    for s in sympts:
        if s in input_symptoms:
            weight = sevrty.loc[s, "weight"]
            input_symptoms_list.append(weight)
        else:
            input_symptoms_list.append(0)

    return input_symptoms_list


def add_symptom():
    sympt = sympts[sympt_list.curselection()[0]]

    real_in_sympt_lst.append(sympt)

    global txt_state

    if txt_state:
        show_to_user = sympt.replace("_", " ")
        txt.insert(END, ", "+show_to_user)
    else:
        show_to_user = sympt.replace("_", " ")
        txt.insert(END, show_to_user)
        txt_state = 1


def clear_txt():
    txt.delete('1.0', END)
    global txt_state
    txt_state = 0

    real_in_sympt_lst.clear()


def dis_err(err_type):

    if err_type == "to_few_symptoms":
        dis_name.config(text="Please Enter at least 3 Symptoms")


def predict_dis():

    input_sympts_lst = weightadder(real_in_sympt_lst)
    disease = predictor.predict(input_sympts_lst).lower()

    print(f"\nDisease - {disease}\n")

    dis_name.config(text=disease.upper())

    out = dis_df.loc[disease]

    about_dis.config(state='normal')
    about_dis.delete("1.0", END)
    about_dis.insert("1.0", 'Discription :\n\n')
    about_dis.insert("3.0", out['description'])
    about_dis.config(state='disabled')

    precautions = out['precautions'].split(",")

    precau.config(state='normal')
    precau.delete("1.0", END)
    precau.insert("1.0", "Precautions :\n\n")
    for i, preco in enumerate(precautions):
        precau.insert(str(2*i+3)+".0", str(i+1) + ") " + preco.lstrip()+"\n\n")
    precau.config(state='disabled')


if __name__ == "__main__":

    light_blue = "#17C3B2"
    blue = "#44D8D6"
    bg_color_brrr = "#ebebde"
    fore = "#4f4747"

    root = Tk()

    root.attributes('-fullscreen', True)

    s = ttk.Style()
    s.configure('new.TFrame', background="#343A40")

    content = ttk.Frame(root, padding=(10, 10, 10, 10))
    content.config(style="new.TFrame")
    frame = Frame(content)

    body_font = "Consolas"

    root.option_add("*font", body_font)
    root['bg'] = "black"

    title = Label(content, text="Disease Prediction Bot", width=47,
                  height=2, background="grey", font="Dyuthi 18", bg="#343A40", foreground=blue)

    about = Button(content, text="People can interact with the bot just like they\n do with another human and through a series of queries,\n chatbot will identify the symptoms of the user and thereby,\n predicts the disease and recommends treatment.",
                   width=45, height=6, background=bg_color_brrr,  activebackground=light_blue, foreground=fore, font="Dyuthi 20")

    add_sympt = Button(content, text="Add Symptom", command=add_symptom, width=39, height=2,
                       font="Dyuthi 23", background=bg_color_brrr,  activebackground=light_blue, foreground=fore)

    sl = StringVar()
    sl.set(shown_list)

    sympt_list = Listbox(content, listvariable=sl,
                         width=57, height=14, font=body_font, background=bg_color_brrr, selectbackground=light_blue, foreground=fore)

    txt = Text(content, width=49, height=3.2, padx=15,
               pady=15, font=body_font, background=bg_color_brrr, foreground=fore)

    clear = Button(content, text="clear", command=clear_txt,
                   width=10, height=1, background=bg_color_brrr,  activebackground=light_blue, foreground=fore, font="Dyuthi 18")

    do_predict = Button(content, text="Click to Predict", command=predict_dis,
                        width=31, height=4, background=bg_color_brrr,  activebackground=light_blue, foreground=fore, font="Dyuthi 30")

    dis_name = Label(content, text="Disease Name will occur here", width=38, height=2,
                     background=bg_color_brrr,  activebackground=light_blue, foreground=fore, font="Dyuthi 25")

    about_dis = Text(content, width=25, height=19,
                     wrap='word', padx=15, pady=15, font=body_font, spacing2=5, background=bg_color_brrr, foreground=fore)
    about_dis.insert("1.0", "About Disease")
    about_dis.config(state='disabled')

    precau = Text(content, width=24, height=19, wrap='word',
                  padx=15, pady=15, font=body_font, background=bg_color_brrr,  foreground=fore)
    precau.insert("1.0", "Precaution of Disease")
    precau.config(state='disabled')

    title.grid(column=0, row=0, columnspan=4)
    about.grid(column=0, row=1, columnspan=2)
    add_sympt.grid(column=0, row=2, columnspan=2)
    sympt_list.grid(column=0, row=3, columnspan=2)
    txt.grid(column=0, row=4, columnspan=2)
    clear.grid(column=0, row=5, columnspan=2)
    do_predict.grid(column=2, row=1, columnspan=2)
    dis_name.grid(column=2, row=2, columnspan=2)
    about_dis.grid(column=2, row=3, rowspan=3)
    precau.grid(column=3, row=3, rowspan=3)

    content.grid(column=0, row=0)

    root.mainloop()
