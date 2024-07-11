import customtkinter
from customtkinter import *
from tkinter import *
from tkinter import filedialog as fd
import avant
import files
import arriere


# window init
app = CTk()
app.geometry("1200x700")
app.title("Ai Assignement")
app.resizable(False, False)

# controls frame
frame = CTkFrame(app, height=500, width=370, border_width=1)
frame.place(relx=0.17, rely=0.5, anchor="center")

# output terminal
outputbox = CTkTextbox(master=app, width=760, height=650, border_width=1, state=DISABLED, font=("Helvetica", -15))
outputbox.place(relx=0.66, rely=0.5, anchor="center")

# rules module
rules_path = CTkEntry(frame, width=260, state=DISABLED)  # path entry
rules_path.place(relx=0.38, rely=0.2, anchor="center")
rules_btn = CTkButton(frame, text="Choose rules", width=50, fg_color="transparent", border_width=1,
                      command=lambda: select_file(rules_path))  # choose file button
rules_btn.place(relx=0.86, rely=0.2, anchor="center")

# facts module
facts_path = CTkEntry(frame, width=260, state=DISABLED)  # path entry
facts_path.place(relx=0.38, rely=0.3, anchor="center")
facts_btn = CTkButton(frame, text="Choose facts", width=50, fg_color="transparent", border_width=1,
                      command=lambda: select_file(facts_path))  # choose file button
facts_btn.place(relx=0.86, rely=0.3, anchor="center")

# goal checkbox module
goal_active = BooleanVar()  # goal state var
goal_checkbox = CTkCheckBox(frame, text="But", variable=goal_active, border_width=2,
                            command=lambda: toggle_goal_state())  # goal checkbox
goal_checkbox.place(relx=0.45, rely=0.45)
goal = CTkEntry(frame, width=200, height=36, state=DISABLED)  # goal entry
goal.place(relx=0.5, rely=0.55, anchor="center")

# execution module
chainage_avant_btn = CTkButton(frame, text="Chainage Avant", width=130, height=40, border_width=1,
                               command=lambda: forward_track())  # chainage avant button
chainage_avant_btn.place(relx=0.3, rely=0.75, anchor="center")

chainage_arriere_btn = CTkButton(frame, text="Chainage Arrière", width=130, height=40, border_width=1, state=DISABLED,
                                 fg_color="gray", hover=False,
                                 command=lambda: backward_track())  # chainage arriere button
chainage_arriere_btn.place(relx=0.7, rely=0.75, anchor="center")

# backtrack checkbox module
par_tentative = BooleanVar()
backtrack_mode_checkbox = CTkCheckBox(frame, text="Par tentative", variable=par_tentative, border_width=2,
                                      state=DISABLED)
backtrack_mode_checkbox.place(relx=0.7, rely=0.84, anchor="center")

# step-by-step tracking module
next_btn = CTkButton(app, text="Next", width=100, height=35, border_width=1, state=DISABLED, command=lambda: next_click())
next_btn.place(relx=0.25, rely=0.92, anchor="center")

# show all steps
step_by_step = BooleanVar()
showall_checkbox = CTkCheckBox(app, text="Show All", border_width=2, variable=step_by_step)
showall_checkbox.place(relx=0.15, rely=0.92, anchor="center")


# open file dialog and render the selected file path in the associated textfield
def select_file(container):
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Choose a file',
        initialdir='C:\\Users\\HamzaChera\\Documents\\Repos\\AI\\BF-BR',
        filetypes=filetypes)

    update_text(container, filename)


# modify and render entry text
def update_text(entry, text):
    entry.configure(state=NORMAL)
    entry.delete(0, END)
    entry.insert(0, text)
    entry.configure(state=DISABLED)


# modify and render output text
def update_output(text):
    outputbox.configure(state=NORMAL)
    outputbox.insert(END, text)
    outputbox.see(END)
    outputbox.configure(state=DISABLED)


# clears output content
def clear_output():
    outputbox.configure(state=NORMAL)
    outputbox.delete("0.0", END)
    outputbox.configure(state=DISABLED)


# toggles the usage of a goal and the associated functionalities
def toggle_goal_state():
    if goal_active.get():
        goal.configure(state=NORMAL)
        chainage_arriere_btn.configure(state=NORMAL, fg_color="#1f6aa5", hover=True)
        backtrack_mode_checkbox.configure(state=NORMAL)
    else:
        goal.configure(state=DISABLED)
        chainage_arriere_btn.configure(state=DISABLED, fg_color="gray", hover=False)
        backtrack_mode_checkbox.configure(state=DISABLED)


# retrieves textfields values (regardless of thier state)
def get_text(entry):
    entry.configure(state=NORMAL)
    text = entry.get()
    entry.configure(state=DISABLED)
    return text


# varialbe to pause execution
is_paused = customtkinter.BooleanVar(app)
is_paused.set(False)


# goes to next step uppon button click
def next_click():
    is_paused.set(False)


# pause execution after each cycle
def pause_execution():
    is_paused.set(True)
    next_btn.configure(state=NORMAL)
    showall_checkbox.configure(state=DISABLED)
    app.wait_variable(is_paused)


def buttons_state(state):
    if state:
        chainage_avant_btn.configure(state=NORMAL, fg_color="#1f6aa5", hover=True)
        chainage_arriere_btn.configure(state=NORMAL, fg_color="#1f6aa5", hover=True)
        backtrack_mode_checkbox.configure(state=NORMAL, hover=True)
        goal_checkbox.configure(state=NORMAL, hover=True)
    else:
        chainage_avant_btn.configure(state=DISABLED, fg_color="gray", hover=False)
        chainage_arriere_btn.configure(state=DISABLED, fg_color="gray", hover=False)
        backtrack_mode_checkbox.configure(state=DISABLED, hover=False)
        goal_checkbox.configure(state=DISABLED, hover=False)


# predefine path for ease of use
update_text(rules_path, "C:\\Users\\HamzaChera\\Documents\\Repos\\AI\\BF-BR\\rules5.txt")
update_text(facts_path, "C:\\Users\\HamzaChera\\Documents\\Repos\\AI\\BF-BR\\facts5.txt")


# render the steps of forward track with/without goal on display
def forward_track():
    buttons_state(False)
    facts = files.readfacts(get_text(facts_path))
    rules = files.readrules(get_text(rules_path))
    ini_rules = rules.copy()
    applicable_rules = avant.evaluate_rules(rules, facts)  # rules with premises currently in BF
    cycle = 1
    clear_output()
    update_output("+++++++++++++++  Objectif  ++++++++++++++\n\n")
    if goal_active.get():
        update_output("Le But = " + goal.get() + "\n")
    else:
        update_output("Aucun objectif specifiée!\n")

    while len(rules) > 0 and len(applicable_rules) > 0:  # do if there are still applicable rules to apply

        # display mode (step by step or all at once)
        if not step_by_step.get():
            pause_execution()

        update_output("\n\n===============   Cycle" + str(cycle) + "    ================\n\n\n")
        cycle = cycle + 1
        selected_rules = avant.select_rules(applicable_rules)  # select rules based on premise count then order of rules

        if len(applicable_rules) > 1:  # show conflicted rules if there are any
            update_output("Conflict = ")
            for rule in applicable_rules:
                update_output("[R" + str(ini_rules.index(rule)) + "] ")
        else:
            update_output("No Conflicts.")

        # apply rule (add new fact to BF and remove rule from BR)
        update_output("\n\nRunning R" + str(ini_rules.index(selected_rules[0])) + " ...")
        applied_rule, facts = avant.apply_rules(selected_rules, facts)
        rules.remove(applied_rule)
        applicable_rules = avant.evaluate_rules(rules, facts)
        update_output("\n\nBF = " + str(facts) + "\n")

        if len(rules) == 0:
            update_output("\n\n+++++++++++++++++++++++++++++++++++\n\n")
            update_output("No more rules to apply. \n\n")
        else:
            if len(applicable_rules) == 0:
                update_output("\n\n+++++++++++++++++++++++++++++++++++\n\n")
                update_output("No applicable rules. \n\n")

        if goal_active.get():  # do if the forward-tracking is goal oriented
            but = goal.get()
            if but in facts:
                update_output("\n\n+++++++++++++++++++++++++++++++++++\n\n")
                update_output("Le but est atteint. ")
                break
            else:
                if len(rules) == 0 or len(applicable_rules) == 0:
                    update_output("Le but est inaccessible ou n'existe pas. ")
    buttons_state(True)
    next_btn.configure(state=DISABLED)
    showall_checkbox.configure(state=NORMAL)


# render the steps of goal oriented backward tracking on display
def backward_track():
    buttons_state(False)
    but = goal.get()  # get the goal from the entry
    facts = files.readfacts(get_text(facts_path))  # get the BF path
    rules = files.readrules(get_text(rules_path))  # get the BR path
    toprove_stack = [but]  # stack of facts to be proved
    proved = []  # proved facts
    to_skip = []  # blocking rule (temporary stored here)
    skip_count = 0  # counter of currently blocking rules
    cycle = 1  # number of cycle

    clear_output()
    update_output("++++++++++++++  Objectif  +++++++++++++++\n\n")
    update_output("BF = " + str(facts) + "\n\n")
    update_output("But = " + but + "\n\n")
    update_output("Stack = " + str(toprove_stack) + "\n\n\n")

    while len(toprove_stack) > 0:

        # display mode (step by step or all at once)
        if not step_by_step.get():
            pause_execution()

        reaching_rules = arriere.get_reaching_rules(rules, toprove_stack[0])
        selected_rules = arriere.select_rules(reaching_rules)

        update_output("==============  Cycle " + str(cycle) + "  ================\n\n")
        cycle = cycle + 1

        if toprove_stack[0] in proved:  # do if fact is already proved
            update_output(toprove_stack[0] + " is already proved.\n\n")
            toprove_stack.pop(0)  # remove fact from to-prove stack

        else:
            if toprove_stack[0] in facts:  # do if fact is in BF
                update_output(toprove_stack[0] + " is in BF.\n\n")
                proved.append(toprove_stack[0])  # mark fact as proved
                toprove_stack.pop(0)  # remove fact from to-prove stack

            else:  # do if fact is neither already proved nor is it in BF

                if len(selected_rules) > 0:  # do if there are rules with fact as result

                    # show conflicted rules (ending on same fact + same number of premises)
                    update_output("Conflict = ")
                    for rule in reaching_rules:
                        update_output("[R" + str(rules.index(rule)) + "] ")
                    update_output("\n\n")

                    # disable blocking rules if there are any
                    if skip_count > 0:
                        skip_count = skip_count - 1
                        selected_rules.pop(0)

                    # update blocking rules list (mark current rule as blocking)
                    to_skip.clear()
                    to_skip.append(selected_rules[0])

                    # get reverse list of selected rule's conditions (for desired order)
                    conditions = selected_rules[0][1]
                    conditions.reverse()

                    # execute selected rule (replace fact with corresponding conditions in to-prove stack)
                    update_output("Running R" + str(rules.index(selected_rules[0])) + "...\n\n")
                    proved.append(toprove_stack[0])  # mark fact as proved once replaced by its corresponding conditions
                    toprove_stack.pop(0)  # remove fact from to-prove stack

                    for condition in conditions:
                        toprove_stack.insert(0, condition)

                else:  # do if there are no rules with fact as result

                    backtrack_mode = par_tentative.get()  # get backtracking mode from UI

                    if not backtrack_mode:  # if backtracking mode is "irrévocable"
                        update_output("Flow is blocked!! (No rules to apply.)\n\n\n")
                        update_output("++++++++++++++++++++++++++++++++++++++++\n\n")
                        update_output("Le But '" + but + "' n'est pas prouvé!!\n\n\n")
                        next_btn.configure(state=DISABLED)
                        buttons_state(True)
                        return None  # stop tracking

                    else:  # if backtracking mode is "par tentative" (backtrack)

                        skip_count = skip_count + 1  # increment the number of blocking rules

                        update_output("Conflict = None.\n\n")
                        update_output(str(toprove_stack[0]) + " is not proved.\n\n")

                        # roll back blocking rule (replace conditions with corresponding fact in to-prove stack)
                        to_skip[0][1].reverse()
                        for itr in range(len(to_skip[0][1])):
                            toprove_stack.pop(0)

                        # mark corresponding fact as to-prove
                        toprove_stack.insert(0, to_skip[0][0])
                        proved.remove(to_skip[0][0])

                        update_output("Back-tracking to cycle " + str(cycle - 2) + "...\n\n")

        update_output("Stack = " + str(toprove_stack) + "\n\n\n")

    update_output("++++++++++++++++++++++++++++++++++++\n\n")
    update_output("Le But '" + but + "' est prouvé!!\n\n\n")
    next_btn.configure(state=DISABLED)
    showall_checkbox.configure(state=NORMAL)
    buttons_state(True)


app.mainloop()
