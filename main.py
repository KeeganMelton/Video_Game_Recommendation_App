import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# reads in "data_set.csv"
df = pd.read_csv(r"data_set.csv", header=0)

# updates to reflect user input
ui_input = {'platform_xbox_one': [0],
            'platform_xbox_series': [0],
            'platform_ps4': [0],
            'platform_ps5': [0],
            'platform_nintendo_switch': [0],
            'genre_fighting': [0],
            'genre_shooter': [0],
            'genre_platform': [0],
            'genre_puzzle': [0],
            'genre_racing': [0],
            'genre_rpg': [0],
            'genre_simulator': [0],
            'genre_sport': [0],
            'genre_tactical': [0],
            'genre_adventure': [0],
            'genre_indie': [0],
            'genre_arcade': [0],
            'esrb_e': [1],
            'esrb_e10': [1],
            'esrb_t': [0],
            'esrb_m': [0],
            'rating': [None]}


# used as command for 'for_me_button'
# asks user age range, platform, and game genre
def for_me():
    global user_age
    global user_platform
    global questionNum
    global user_genre

    # used to align label frames
    questionNum = 0

    # clears previous selections for a fresh start
    reset()

    # age range label and radio buttons
    # age range correlates with ESRB ratings
    age_question_frame = ttk.LabelFrame(user_info_frame, text="What is your age range?")
    age_question_frame.grid(column=0, row=questionNum, columnspan=2, padx=30, pady=5, sticky=tk.W)
    age = ["12 & Under", "13-16", "17+"]
    user_age = tk.StringVar()
    questionNum += 1
    for option in range(3):
        age_rb = tk.Radiobutton(age_question_frame, text=age[option], variable=user_age,
                                value=age[option], tristatevalue="Blank")
        age_rb.grid(column=option, row=0, sticky=tk.W)

    # Gaming Platform label and radio buttons
    platform_question_frame = ttk.LabelFrame(user_info_frame, text="What Console do you play on?")
    platform_question_frame.grid(column=0, row=questionNum, columnspan=2, padx=30, pady=5, sticky=tk.W)
    platform = ["Xbox One", "Xbox Series X|S", "Playstation 4", "Playstation 5", "Nintendo Switch"]
    user_platform = tk.StringVar()
    row = 0
    questionNum += 1
    for option in range(5):
        if option % 2 == 0:
            row += 1
        platform_rb = tk.Radiobutton(platform_question_frame, text=platform[option],
                                     variable=user_platform, value=platform[option],
                                     tristatevalue="Blank")
        platform_rb.grid(column=option % 2, row=row, sticky=tk.W)

    # Game genre label and radio buttons
    genre_question_frame = ttk.LabelFrame(user_info_frame, text="What type of games do you like?")
    genre_question_frame.grid(column=0, row=questionNum, columnspan=2, padx=30, pady=5, sticky=tk.W)
    genre = ["Fighting", "Shooter", "Platform", "Puzzle", "Racing", "RPG",
             "Simulator", "Sport", "Tactical", "Adventure", "Indie", "Arcade"]
    user_genre = tk.StringVar()
    row = 0
    questionNum += 1
    for option in range(12):
        if option % 3 == 0:
            row += 1
        genre_rb = tk.Radiobutton(genre_question_frame, text=genre[option],
                                  variable=user_genre, value=genre[option],
                                  tristatevalue="Blank")
        genre_rb.grid(column=option % 3, row=row, sticky=tk.W)

    # Buttons to clear selections and save choices
    reset_button = tk.Button(user_info_frame, text="Clear Choices", command=reset)
    reset_button.grid(column=0, row=questionNum, padx=30, sticky=tk.W)
    save_button = tk.Button(user_info_frame, text="Show Recommendation", command=save_user_choices)
    save_button.grid(column=1, row=questionNum, padx=30, sticky=tk.W)


# used as a command for 'for_someone_else_button'
# asks user for age range of recipient and platform
def for_someone_else():
    global user_age
    global user_platform
    global questionNum
    questionNum = 0

    # clears previous selections for a fresh start
    reset()

    # age range label and radio buttons
    # age range correlates with ESRB ratings
    age_question_frame = ttk.LabelFrame(user_info_frame, text="What is your age range of the game recipient?")
    age_question_frame.grid(column=0, row=questionNum, columnspan=2, padx=30, pady=5, sticky=tk.W)
    age = ["12 & Under", "13-16", "17+"]
    user_age = tk.StringVar()
    questionNum += 1
    for option in range(3):
        age_rb = tk.Radiobutton(age_question_frame, text=age[option], variable=user_age,
                                value=age[option], tristatevalue="Blank")
        age_rb.grid(column=option, row=0, sticky=tk.W)

    # Gaming Platform label and radio buttons
    platform_question_frame = ttk.LabelFrame(user_info_frame, text="Console:")
    platform_question_frame.grid(column=0, row=questionNum, columnspan=2, padx=30, pady=5, sticky=tk.W)
    platform = ["Xbox One", "Xbox Series X|S", "Playstation 4", "Playstation 5", "Nintendo Switch"]
    user_platform = tk.StringVar()
    row = 0
    questionNum += 1
    for option in range(5):
        if option % 2 == 0:
            row += 1
        platform_rb = tk.Radiobutton(platform_question_frame, text=platform[option],
                                     variable=user_platform, value=platform[option],
                                     tristatevalue="Blank")
        platform_rb.grid(column=option % 2, row=row, sticky=tk.W)

    # Buttons to clear selections and save choices
    reset_button = tk.Button(user_info_frame, text="Clear Choices", command=reset)
    reset_button.grid(column=0, row=questionNum, padx=30, sticky=tk.W)
    save_button = tk.Button(user_info_frame, text="Show Recommendation", command=save_user_choices)
    save_button.grid(column=1, row=questionNum, padx=30, sticky=tk.W)


# used as command for 'save_button'
# updates 'ui_input' based on user selections
def save_user_choices():
    global user_input

    # reset ui_input
    for key in ui_input:
        ui_input[key][0] = 0
    ui_input['esrb_e'][0] = 1
    ui_input['esrb_e10'][0] = 1

    if user_age.get() == "":
        messagebox.showinfo("Age Not Selected", "Please select an age range")
        return
    if user_age.get() == "13-16":
        ui_input['esrb_t'][0] = 1

    if user_age.get() == "17+":
        ui_input['esrb_t'][0] = 1
        ui_input['esrb_m'][0] = 1

    if user_platform.get() == "":
        messagebox.showinfo("Console Not Selected", "Please select a game console")
        return

    if user_platform.get() == "Xbox One":
        ui_input['platform_xbox_one'][0] = 1

    elif user_platform.get() == "Xbox Series X|S":
        ui_input['platform_xbox_series'][0] = 1

    elif user_platform.get() == "Playstation 4":
        ui_input['platform_ps4'][0] = 1

    elif user_platform.get() == "Playstation 5":
        ui_input['platform_ps5'][0] = 1

    elif user_platform.get() == "Nintendo Switch":
        ui_input['platform_nintendo_switch'][0] = 1

    if user_genre.get() == "Fighting":
        ui_input['genre_fighting'][0] = 1

    elif user_genre.get() == "Shooter":
        ui_input['genre_shooter'][0] = 1

    elif user_genre.get() == "Platform":
        ui_input['genre_platform'][0] = 1

    elif user_genre.get() == "Puzzle":
        ui_input['genre_puzzle'][0] = 1

    elif user_genre.get() == "Racing":
        ui_input['genre_racing'][0] = 1

    elif user_genre.get() == "RPG":
        ui_input['genre_rpg'][0] = 1

    elif user_genre.get() == "Simulator":
        ui_input['genre_simulator'][0] = 1

    elif user_genre.get() == "Sport":
        ui_input['genre_sport'][0] = 1

    elif user_genre.get() == "Tactical":
        ui_input['genre_tactical'][0] = 1

    elif user_genre.get() == "Adventure":
        ui_input['genre_adventure'][0] = 1

    elif user_genre.get() == "Indie":
        ui_input['genre_indie'][0] = 1

    elif user_genre.get() == "Arcade":
        ui_input['genre_arcade'][0] = 1

    user_input = pd.DataFrame(ui_input)
    show_recommendations()


# called at the end of save_user_choices()
# Creates a data frame to reflect user choices
# Classification decision tree is used on the new data frame to recommend games
# Information from those games is gathered and used for pie charts
# Recommendations are presented to the user
# Genre and ESRB pie charts are presented to the user
def show_recommendations():
    global recommended
    global user_input
    global recommendation_label
    # used to align labelFrames
    row = 0

    # new data frame based on user input
    user_input_df = df[
        (df['platform_xbox_one'] >= user_input['platform_xbox_one'][0]) &
        (df['platform_xbox_series'] >= user_input['platform_xbox_series'][0]) &
        (df['platform_ps4'] >= user_input['platform_ps4'][0]) &
        (df['platform_ps5'] >= user_input['platform_ps5'][0]) &
        (df['platform_nintendo_switch'] >= user_input['platform_nintendo_switch'][0]) &
        (df['genre_fighting'] >= user_input['genre_fighting'][0]) &
        (df['genre_shooter'] >= user_input['genre_shooter'][0]) &
        (df['genre_platform'] >= user_input['genre_platform'][0]) &
        (df['genre_puzzle'] >= user_input['genre_puzzle'][0]) &
        (df['genre_racing'] >= user_input['genre_racing'][0]) &
        (df['genre_rpg'] >= user_input['genre_rpg'][0]) &
        (df['genre_simulator'] >= user_input['genre_simulator'][0]) &
        (df['genre_sport'] >= user_input['genre_sport'][0]) &
        (df['genre_tactical'] >= user_input['genre_tactical'][0]) &
        (df['genre_adventure'] >= user_input['genre_adventure'][0]) &
        (df['genre_indie'] >= user_input['genre_indie'][0]) &
        (df['genre_arcade'] >= user_input['genre_arcade'][0]) &
        (df['esrb_e'] <= user_input['esrb_e'][0]) &
        (df['esrb_e10'] <= user_input['esrb_e10'][0]) &
        (df['esrb_t'] <= user_input['esrb_t'][0]) &
        (df['esrb_m'] <= user_input['esrb_m'][0])
        ].sort_values(by='rating', ascending=False)

    # labels for pie charts
    genre_pie_chart_labels = {'genre_fighting': 'Fighting',
                              'genre_shooter': 'Shooter',
                              'genre_platform': 'Platform',
                              'genre_puzzle': 'Puzzle',
                              'genre_racing': 'Racing',
                              'genre_rpg': 'RPG',
                              'genre_simulator': 'Simulator',
                              'genre_sport': 'Sport',
                              'genre_tactical': 'Tactical',
                              'genre_adventure': 'Adventure',
                              'genre_indie': 'Indie',
                              'genre_arcade': 'Arcade'}

    esrb_pie_chart_labels = {'esrb_e': 'E',
                             'esrb_e10': 'E10',
                             'esrb_t': 'T',
                             'esrb_m': 'M'}

    # Sets X and y for classification tree
    X = user_input_df.drop(columns=["name"])
    y = user_input_df["name"]

    # test and train split for classification tree
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=76)

    # Classification Tree
    classTree = DecisionTreeClassifier()
    classTree.fit(X_train, y_train)
    y_pred = classTree.predict(X)

    # Gets top 5 recommendations
    recommended = classTree.predict(X)[:5]

    # Gets top 5 from the scv file to use for graphs
    top_5_games = df[df['name'].isin(recommended)]

    # totals genre and esrb count for graphs
    genre_count = top_5_games[:5].sum()[6:18]
    esrb_count = top_5_games[:5].sum()[18:22]

    # Removes 0 counts for the graph
    genre_pie_data = {genre_pie_chart_labels.get(label, label): count for label, count in genre_count.items() if
                      count > 0}
    esrb_pie_data = {esrb_pie_chart_labels.get(label, label): count for label, count in esrb_count.items() if count > 0}

    # Genre and ESRB graphs
    fig1, ax1 = plt.subplots(figsize=(3, 2))
    fig2, ax2 = plt.subplots(figsize=(2.25, 2))
    ax1.pie(genre_pie_data.values(), labels=genre_pie_data.keys(), startangle=90, radius=.1)
    ax1.axis('equal')
    ax2.pie(esrb_pie_data.values(), labels=esrb_pie_data.keys(), startangle=90, radius=.1)
    ax2.axis('equal')

    # Displays recommendations and pie charts to the user
    show_recommendations_frame = ttk.LabelFrame(recommendations_frame, text="Here are your recommendations")
    show_recommendations_frame.grid(column=0, row=1, columnspan=2, padx=30, pady=10, sticky=tk.W)

    show_pie_data = ttk.LabelFrame(recommendations_frame,
                                         text="Genre and ESRB Ratings Across Your Recommendations")
    show_pie_data.grid(column=0, row=2, padx=30, pady=10)

    accuracy = accuracy_score(y, y_pred) * 100

    accuracy_label = tk.Label(show_recommendations_frame, text="Recommendation Accuracy: " +
                                                               str(round(accuracy, 2)) + '%')
    accuracy_label.grid(column=0, row=row, sticky=tk.W)
    row += 1

    for game in range(5):
        recommendation_label = tk.Label(show_recommendations_frame, text=recommended[game])
        recommendation_label.grid(column=0, row=row, sticky=tk.W)
        row += 1

    genre_graph_label = tk.Label(show_pie_data, text="Genres")
    genre_graph_label.grid(column=0, row=row)

    genre_graph_label = tk.Label(show_pie_data, text="ESRB Ratings")
    genre_graph_label.grid(column=1, row=row)

    row += 1

    genre_canvas = FigureCanvasTkAgg(fig1, master=show_pie_data)
    genre_canvas_widget = genre_canvas.get_tk_widget()
    genre_canvas_widget.grid(column=0, row=row, padx=5, pady=5, sticky=tk.NSEW)

    esrb_canvas = FigureCanvasTkAgg(fig2, master=show_pie_data)
    esrb_canvas_widget = esrb_canvas.get_tk_widget()
    esrb_canvas_widget.grid(column=1, row=row, padx=5, pady=5, sticky=tk.NSEW)
    return

# clears information
def reset():
    global user_age
    global user_platform
    global user_genre
    for widgets in user_info_frame.winfo_children():
        widgets.destroy()
    for widgets in recommendations_frame.winfo_children():
        widgets.destroy()
    user_age = tk.StringVar()
    user_platform = tk.StringVar()
    user_genre = tk.StringVar()

    # reset ui_input
    for key in ui_input:
        ui_input[key][0] = 0
    ui_input['esrb_e'][0] = 1
    ui_input['esrb_e10'][0] = 1

# closes application
def close():
    window.destroy()


# Main Window
window = tk.Tk()
window.title("Game Recommendations")
window.geometry("600x900")
window.protocol("WM_DELETE_WINDOW", close)

# variables
user_age = tk.StringVar()
user_platform = tk.StringVar()
user_genre = tk.StringVar()
questionNum = 0
recommended = None
user_input = None
recommendation_label = None

# Labels
welcome_label = tk.Label(window, text="Game Recommendations", font="bold")
welcome_label.grid(column=0, row=0, columnspan=2, padx=10, pady=10)
first_question_frame = ttk.LabelFrame(window, text="Are you looking for a game for you, or someone else?")
first_question_frame.grid(column=0, row=1, columnspan=2, padx=150, pady=10)

# Buttons
for_me_button = tk.Button(first_question_frame, text="For Me", command=for_me)
for_me_button.grid(column=0, row=0, padx=10, pady=10, ipadx=25)
for_someone_else_button = tk.Button(first_question_frame, text="For Someone Else", command=for_someone_else)
for_someone_else_button.grid(column=1, row=0, padx=10, pady=5, ipadx=25, sticky=tk.E)

user_info_frame = ttk.Frame(window)
user_info_frame.grid(column=0, row=2, sticky=tk.W)

recommendations_frame = ttk.Frame(window)
recommendations_frame.grid(column=0, row=3, sticky=tk.W)

window.mainloop()