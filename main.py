from customtkinter import *
from win11toast import notify
import winsound

app = CTk()
app.title('Project: Timer')
AppFont = ('Roboto', 15)

# Замена иконки ---------------------------------------------------------------------------------------
def icon_set():
    if get_appearance_mode() == 'Dark': app.wm_iconbitmap(default="icon_for_dark.ico")
    if get_appearance_mode() == 'Light': app.wm_iconbitmap(default="icon_for_light.ico")
icon_set()

app.resizable(False, False)

# Полезные источники ---------------------------------------------------------------------------------------

# metanit.com/python/tkinter
# customtkinter.tomschimansky.com/documentation

# Размещение окна по центру экрана ---------------------------------------------------------------------------------------
# 1. Определяем размеры окна
window_width = 350
window_height = 550
app.geometry(f"{window_width}x{window_height}")

# 2. Получаем размеры экрана
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
# 3. Вычисляем координаты для центрирования
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)

# 4. Применяем позиционирование
app.geometry(f"+{int(x_coordinate)}+{int(y_coordinate)}")


# Переключатель выбора темы ---------------------------------------------------------------------------------------
# Создаю фрейм для помещения виджетов и даю вес колоннам грида для растяжения по всей области
ThemeFrame = CTkFrame(app)
ThemeFrame.columnconfigure(index = [i for i in range(2)], weight = 1)
# Текст
ThemeText = CTkLabel(ThemeFrame, text='Тема приложения', font=AppFont)
ThemeText.grid(row=0, column=0, padx = 10, pady = 5, sticky = W)
# Свитчер тем
def ButtonThemeChange(theme):
    if theme == 'Светлая': set_appearance_mode("light")
    if theme == 'Темная': set_appearance_mode("dark")
    # if theme == 'Система': set_appearance_mode("system")
    icon_set()

ThemeButton = CTkSegmentedButton(ThemeFrame, values=['Светлая', 'Темная'], command=ButtonThemeChange, font=AppFont)
ThemeButton.set('Светлая')
set_appearance_mode("light")
ThemeButton.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = E)

ThemeFrame.pack(padx=10, pady=10, fill=X)


#Создание окна таймера ---------------------------------------------------------------------------------------
TimerSelectFrame = CTkFrame(app)
# Создание фреймов указателя времени
SecondsFrame = CTkFrame(TimerSelectFrame)
MinutesFrame = CTkFrame(TimerSelectFrame)
HoursFrame = CTkFrame(TimerSelectFrame)

TimerSelectFrame.columnconfigure(index = [i for i in range(3)], weight = 1, uniform='column')
# Переменные таймера
selected_seconds = 0
selected_minutes = 0
selected_hours = 0
# Создание и размещение текста в фреймы
HoursText = CTkLabel(HoursFrame, text=f'{selected_hours} ч', font=AppFont)
MinutesText = CTkLabel(MinutesFrame, text=f'{selected_minutes} мин', font=AppFont)
SecondsText = CTkLabel(SecondsFrame, text=f'{selected_seconds} с', font=AppFont)
HoursText.pack(padx = 2, pady = 4, fill = BOTH)
MinutesText.pack(padx = 2, pady = 4,fill = BOTH)
SecondsText.pack(padx = 2, pady = 4,fill = BOTH)
# Поизиционировние фреймов в гриды
SecondsFrame.grid(row = 0, column = 2, padx = (0,5), pady = 5, sticky = NSEW)
MinutesFrame.grid(row = 0, column = 1, padx = (0,5), pady = 5, sticky = NSEW)
HoursFrame.grid(row = 0, column = 0, padx = 5, pady = 5,  sticky = NSEW)

TimerSelectFrame.pack(padx=20, pady=(12,10), fill = X)

# События на колесо мыши + функции ---------------------------------------------------------------------------------------
def AddSeconds(event):
    global selected_seconds
    if event.delta < 0: selected_seconds -= 1
    elif event.delta > 0: selected_seconds += 1
    if selected_seconds < 0: selected_seconds = 60
    elif selected_seconds > 60: selected_seconds = 0
    SecondsText.configure(text=f'{selected_seconds} с')  # Через Var не удалось

def AddMinutes(event):
    global selected_minutes
    if event.delta < 0: selected_minutes -= 1
    elif event.delta > 0: selected_minutes += 1
    if selected_minutes < 0: selected_minutes = 60
    elif selected_minutes > 60: selected_minutes = 0
    MinutesText.configure(text=f'{selected_minutes} мин')

def AddHours(event):
    global selected_hours
    if event.delta < 0: selected_hours -= 1
    elif event.delta > 0: selected_hours += 1
    if selected_hours < 0: selected_hours = 23
    if selected_hours > 23: selected_hours = 0
    HoursText.configure(text=f'{selected_hours} ч')

SecondsText.bind("<MouseWheel>", AddSeconds)
MinutesText.bind("<MouseWheel>", AddMinutes)
HoursText.bind("<MouseWheel>", AddHours)

# Поле ввода названия таймера ---------------------------------------------------------------------------------------
TimerNameFrame = CTkFrame(TimerSelectFrame)
TimerNameText = CTkLabel(TimerNameFrame, text='Название', font=AppFont)
TimerNameEntry = CTkEntry(TimerNameFrame, placeholder_text='Таймер', fg_color='transparent', justify=RIGHT, font=AppFont, border_color="")

TimerNameFrame.columnconfigure(index = [i for i in range(3)], weight = 1, uniform='column')

TimerNameFrame.grid(row=1, column=0, columnspan=3, sticky = NSEW, padx=5, pady=(0, 5))
TimerNameText.grid(row=0, column=0, padx=5, pady=4)
TimerNameEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=4, sticky=NSEW)

# Кнопка добавления таймера + reset_selected ---------------------------------------------------------------------------------------
TimerFrame = CTkFrame(app)

TimerFrame.columnconfigure(index = [i for i in range(3)], weight = 1, uniform='column')
# Функция обновления текста в выборе времени таймера
def UpdateSelectedTime():
    SecondsText.configure(text=f'{selected_seconds} с')
    MinutesText.configure(text=f'{selected_minutes} мин')
    HoursText.configure(text=f'{selected_hours} ч')

def ResetSelection():
    global selected_hours, selected_minutes, selected_seconds
    selected_hours = selected_minutes = selected_seconds = 0
    UpdateSelectedTime()
    TimerNameEntry.delete(0,END)
# Функция подсчета общего времени для таймера
total_time = 0
def solve_total_time(selected_seconds, selected_minutes, selected_hours):
    global total_time
    total_time = selected_seconds + selected_minutes*60 + selected_hours*3600
    return total_time
# Новый скроллабл фрейм для таймеров
scrollable_frame = CTkScrollableFrame(app, fg_color="transparent")

def StopSound(): winsound.PlaySound("notification.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
# Функция добавления таймеров

def AddTimer():
    solved_to_seconds = IntVar(value=solve_total_time(selected_seconds, selected_minutes, selected_hours))
    if solved_to_seconds.get() == 0: return
    
    frame = CTkFrame(scrollable_frame, corner_radius=10)
    #frame.columnconfigure(index = [i for i in range(2)], weight = 2, uniform='column')
    frame.columnconfigure(index = 0, weight = 22, uniform='column')
    frame.columnconfigure(index = 1, weight = 1, uniform='column')
    frame.rowconfigure(index = 0, weight = 0)
    frame.rowconfigure(index = 1, weight = 0)

    MMSS_text = CTkLabel(frame, text="", font=('Roboto', 30))
    timer_name = CTkLabel(frame, text=TimerNameEntry.get() if TimerNameEntry.get() else f'{selected_minutes+selected_hours*60} мин {selected_seconds} с', font=AppFont)
    TimerDeleteButton = CTkButton(frame, text='|', corner_radius=0, hover_color="#8D0000", fg_color="#BB0000", command=lambda: (winsound.PlaySound(None, winsound.SND_PURGE), MMSS_text.destroy(), frame.destroy(), TimerDeleteButton.destroy()))

    if len(TimerNameEntry.get()) > 25:
        timer_name.configure(text=TimerNameEntry.get()[:25]+'…')

    frame.pack(fill="x", padx=5, pady=5)
    MMSS_text.grid(row=0, column=0, sticky=W, padx=10, pady=(4,0))
    timer_name.grid(row=1, column=0, sticky=W, padx=10, pady=(0,4))
    TimerDeleteButton.grid(row=0, column=1, rowspan=2, sticky=NSEW)

    def update_timer():
        seconds = solved_to_seconds.get()

        if seconds > 0:
            minutes = seconds // 60
            sec = seconds % 60
            formatted_text = f"{minutes:02d}:{sec:02d}"
            MMSS_text.configure(text=formatted_text)

            solved_to_seconds.set(seconds - 1)
            MMSS_text.after(1000, update_timer)
        else:
            MMSS_text.configure(text="00:00", text_color = 'red')
            notify(f'Таймер "{timer_name.cget("text")}" подошёл к концу', 'Удалите таймер для отключения звукового уведомления')    # TODO on_click=StopSound
            winsound.PlaySound("notification.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    update_timer()
    
    

# Кнопки
AddTimerButton = CTkButton(TimerFrame, text='+', command=AddTimer, font=AppFont)
ResetTimerSelectButton = CTkButton(TimerFrame ,text='Сбросить значения', command=ResetSelection, font=AppFont, fg_color='grey', hover_color="#5C5C5C")

ResetTimerSelectButton.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=5, pady=5)
AddTimerButton.grid(row=0, column=2, sticky = NSEW,  padx=5, pady=5, ipady=1)

TimerFrame.pack(fill=X, padx=20)

scrollable_frame.pack(fill=BOTH, padx=10, pady=10, expand=True)     # Frame pack ток щас делается после кнопок для корректного отображения

# научица бы не парица па пустикам, не балеть с утра па панидельникам и от таво што не нравица ни мучица

app.mainloop()