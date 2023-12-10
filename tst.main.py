import pickle
import pandas as pd
from tkinter import *
from tkinter import ttk

with open('./classifire.pkl', 'rb') as file:
    model = pickle.load(file, errors='ignore')

dis_df = pd.read_csv('./data.csv', index_col='disease')

df = pd.read_csv("./disease_symptoms_weight.csv", index_col='Disease').iloc[:, 1:]
symp_dcptn = pd.read_csv("./Symptom-description.csv", index_col='Symptom')



related_sympts = pd.read_csv('./related_symptoms.csv', index_col="symptom1")


sympts = df.columns.tolist()
shown_list=list(map(lambda x:x.replace("_", " "),sympts))
shown_list=list(map(lambda x: "   "+x,shown_list))



sevrty = pd.read_csv("symptom_severity.csv", index_col="Symptom")

# def Convert(string):
#     li = list(string.split(" "))
#     return li
  

real_in_sympt_lst = []
 

def predict(data: list):

    lst = pd.DataFrame(data).transpose()
    col = df.columns.tolist()
    lst.columns = col
    data = lst

    prediction = model.predict(data)[0]

    return prediction


def weightadder(lst:list):

    # filtered_list = sen.split(" ")[:-1]

    filtered_list = lst
    input_symptoms = filtered_list

    rsi = related_sympts.index.tolist()

    for i in filtered_list:
        if i in rsi:
            input_symptoms.append(related_sympts.loc[i, 'symptom2'])
    
    lst = []

    for s in sympts:
        if s in input_symptoms:
            weight = sevrty.loc[i, "weight"]
            lst.append(weight)
        else:
            lst.append(0)

    return lst


def add_symptom():
    sympt = sympts[sympt_list.curselection()[0]]

    real_in_sympt_lst.append(sympt)

    show_to_user = sympt.replace("_", " ")
    txt.insert(END, show_to_user+", ")


    Simp_tom_des.config(text=symp_dcptn.loc[sympt,"Description"] )



def clear_txt():
    txt.delete('1.0', END)


def predict_dis():
    # sen = txt.get("1.0", END)
    
    input_sympts_lst = weightadder(real_in_sympt_lst)
    disease = predict(input_sympts_lst)

    dis_name.config(text=disease.upper())

    out = dis_df.loc[disease]

    about_dis.config(state='normal')
    about_dis.delete("1.0", END)
    about_dis.insert("1.0", 'Discription :\n\n')
    about_dis.insert("3.0", out['discription'])
    about_dis.config(state='disabled')

    precautions = out['precautions'].split(",")

    precau.config(state='normal')
    precau.delete("1.0", END)
    precau.insert("1.0", "Precautions :\n\n")
    for i, preco in enumerate(precautions):
        precau.insert(str(2*i+3)+".0", str(i+1) + ") " + preco.lstrip()+"\n\n")
    precau.config(state='disabled')

    real_in_sympt_lst.clear()

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

    body_font = "Dyuthi 15"

    root.option_add("*font", body_font)
    root['bg'] = "black"

    title = Label(content, text="Disease Prediction Bot", width=47,
                  height=2, background="grey", font="Dyuthi 40", bg="#343A40", foreground=blue)

    about = Button(content, text="This is about our project",
                   width=60, height=8, font=body_font, background=bg_color_brrr,  activebackground=light_blue, foreground=fore)

    Simp_tom_des = Label(content, text="Symptom description",
                   width=21, height=17, font=body_font, background=bg_color_brrr,  activebackground=light_blue, foreground=fore,justify=CENTER)

    add_sympt = Button(content, text="Add Symptom",
                       command=add_symptom, width=36, height=2, font=body_font, background=bg_color_brrr,  activebackground=light_blue, foreground=fore)

    var2 = StringVar()

    var2.set(shown_list)
    sympt_list = Listbox(content, listvariable=var2,
                         width=38, height=14, font=body_font, background=bg_color_brrr, selectbackground=light_blue, foreground=fore)

    txt = Text(content, width=60, height=5, padx=15,
               pady=15, font=body_font, background=bg_color_brrr, foreground=fore)

    clear = Button(content, text="clear", command=clear_txt,
                   width=60, height=1, font=body_font, background=bg_color_brrr,  activebackground=light_blue, foreground=fore)

    do_predict = Button(content, text="Image", command=predict_dis,
                        width=60, height=8, background=bg_color_brrr,  activebackground=light_blue, foreground=fore)

    dis_name = Label(content, text="Disease Name will occur here", width=62, height=3,
                     background=bg_color_brrr,  activebackground=light_blue, foreground=fore)

    about_dis = Text(content, width=29, height=22,
                     wrap='word', padx=15, pady=15, font=body_font, spacing2=5, background=bg_color_brrr, foreground=fore)
    about_dis.insert("1.0", "About Disease")
    about_dis.config(state='disabled')

    precau = Text(content, width=28, height=22, wrap='word',
                  padx=15, pady=15, font=body_font, background=bg_color_brrr,  foreground=fore)
    precau.insert("1.0", "Precaution of Disease")
    precau.config(state='disabled')

    title.grid(column=0, row=0, columnspan=4)
    about.grid(column=0, row=1, columnspan=2)
    Simp_tom_des.grid(column=0, row=2, rowspan=2)
    add_sympt.grid(column=1, row=2)
    sympt_list.grid(column=1, row=3)
    txt.grid(column=0, row=4, columnspan=2)
    clear.grid(column=0, row=5, columnspan=2)
    do_predict.grid(column=2, row=1, columnspan=2)
    dis_name.grid(column=2, row=2, columnspan=2)
    about_dis.grid(column=2, row=3, rowspan=3)
    precau.grid(column=3, row=3, rowspan=3)

    content.grid(column=0, row=0)

    root.mainloop()
