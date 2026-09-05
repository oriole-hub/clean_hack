## clean_challenge.rpy
## Челлендж Чистого берега — интерфейс участника и мастера фиксации

init python:
    def start_challenge_wizard(ch):
        clean_state.selected_challenge = ch
        clean_state.wizard_step = 1
        renpy.show_screen("challenge_wizard_screen")
        renpy.restart_interaction()

    def wizard_set_photo(p_path, default_cat):
        clean_state.new_report_photo = p_path
        clean_state.new_report_category = default_cat
        clean_state.wizard_step = 3
        renpy.restart_interaction()

    def wizard_set_category(cat_name):
        clean_state.new_report_category = cat_name
        clean_state.wizard_step = 4
        renpy.restart_interaction()

    def wizard_map_click():
        mx, my = renpy.get_mouse_pos()
        # Преобразуем координаты клика по карте в геокоординаты
        calc_lat = 55.1000 + (720 - (my - 220)) * 0.00015
        calc_lon = 20.8000 + (mx - 480) * 0.00018
        clean_state.new_report_lat = "{:.4f}° N".format(calc_lat)
        clean_state.new_report_lon = "{:.4f}° E".format(calc_lon)
        renpy.restart_interaction()

    def complete_and_submit_report():
        clean_state.submit_user_report()
        renpy.show_screen("challenge_reward_screen")
        renpy.restart_interaction()

## ЭКРАН 1: КАТАЛОГ ЧЕЛЛЕНДЖЕЙ (Этап 1 и 2)
screen challenge_catalog_screen():
    tag clean_screen
    add Solid("#070f1e")

    use clean_top_bar(active_tab="challenge")

    vbox:
        xalign 0.5
        ypos 105
        spacing 20
        xsize 1400

        # ЗАГОЛОВОК
        hbox:
            spacing 20
            vbox:
                text "🔥 АКТИВНЫЕ ЗАДАНИЯ":
                    size 28
                    color "#ffffff"
                    bold True
                text "Выбирай задание, исследуй береговую линию и отправляй данные для защиты природы":
                    size 16
                    color "#94a3b8"

        # СПИСОК КАРТОЧЕК ЧЕЛЛЕНДЖЕЙ
        for ch in clean_state.challenges:
            frame:
                background Frame(Solid("#0e1e38"), 10, 10)
                padding (30, 22)
                xfill True

                hbox:
                    spacing 30
                    yalign 0.5

                    # Иконка / бейдж
                    add "images/ui/badge_scout.png":
                        yalign 0.5

                    # Основной контент
                    vbox:
                        spacing 6
                        xsize 800

                        text "[ch.title]":
                            size 22
                            color "#38bdf8"
                            bold True

                        text "[ch.description]":
                            size 15
                            color "#cbd5e1"
                            line_spacing 3

                        null height 4

                        # Метаданные (Этап 2: срок, сложность, место, награда, кто организатор)
                        hbox:
                            spacing 18
                            frame:
                                background Solid("#1e293b")
                                padding (8, 4)
                                text "📅 [ch.deadline]":
                                    size 13
                                    color "#94a3b8"
                            frame:
                                background Solid("#1e293b")
                                padding (8, 4)
                                text "📍 [ch.location]":
                                    size 13
                                    color "#94a3b8"
                            frame:
                                background Solid("#1e293b")
                                padding (8, 4)
                                text "🏛 [ch.organizer]":
                                    size 13
                                    color "#60a5fa"
                            frame:
                                background Solid("#1e293b")
                                padding (8, 4)
                                text "⚡ [ch.difficulty]":
                                    size 13
                                    color "#f59e0b"

                    # Награда и кнопка участия
                    vbox:
                        spacing 12
                        xalign 1.0
                        yalign 0.5

                        text "+[ch.reward_xp] XP":
                            size 26
                            color "#00e6b8"
                            bold True
                            xalign 0.5

                        textbutton "Участвовать →":
                            text_size 16
                            text_bold True
                            text_color "#070f1e"
                            background Frame(Solid("#00e6b8"), 6, 6)
                            hover_background Frame(Solid("#38bdf8"), 6, 6)
                            xpadding 25
                            ypadding 10
                            action Function(start_challenge_wizard, ch)

## ЭКРАН 2: ПОШАГОВОЕ ВЫПОЛНЕНИЕ (ЭТАП 3 И 4)
screen challenge_wizard_screen():
    tag clean_screen
    add Solid("#070f1e")

    use clean_top_bar(active_tab="challenge")

    $ step = clean_state.wizard_step

    vbox:
        xalign 0.5
        ypos 100
        spacing 15
        xsize 1350

        # ИНДИКАТОР ШАГОВ (Этап 3: 1. Найди, 2. Фото, 3. Категория, 4. Точка, 5. Отправь)
        frame:
            background Frame(Solid("#0e1e38"), 8, 8)
            padding (25, 15)
            xfill True

            hbox:
                spacing 35
                xalign 0.5

                for idx, step_name in [(1, "1. Найди участок"), (2, "2. Сделай фото"), (3, "3. Тип мусора"), (4, "4. Отметь точку"), (5, "5. Отправка")]:
                    $ is_active = (idx == step)
                    $ is_done = (idx < step)
                    $ num_col = "#00e6b8" if is_active else ("#22c55e" if is_done else "#64748b")
                    hbox:
                        spacing 8
                        text "[step_name]":
                            size 15
                            color num_col
                            bold is_active

        # КОНТЕНТ ШАГА
        frame:
            background Frame(Solid("#0c1a30"), 10, 10)
            padding (35, 25)
            xfill True
            ysize 670

            # ШАГ 1: НАЙДИ УЧАСТОК
            if step == 1:
                vbox:
                    spacing 20
                    xalign 0.5
                    yalign 0.5

                    text "ШАГ 1: ВЫХОД НА МАРШРУТ И ПОИСК ЗАГРЯЗНЕНИЯ":
                        size 22
                        color "#38bdf8"
                        bold True
                        xalign 0.5

                    frame:
                        background Solid("#07101f")
                        padding (25, 20)
                        xsize 900
                        vbox:
                            spacing 10
                            text "Задание: [clean_state.selected_challenge.title]":
                                size 18
                                color "#ffffff"
                                bold True
                            text "Район мониторинга: [clean_state.selected_challenge.location]":
                                size 16
                                color "#00e6b8"
                            text "Вам необходимо обследовать береговую полосу и зафиксировать любые несанкционированные скопления антропогенных отходов.":
                                size 15
                                color "#cbd5e1"

                    textbutton "Участок найден! Перейти к фотосъемке →":
                        text_size 18
                        text_bold True
                        text_color "#070f1e"
                        background Frame(Solid("#00e6b8"), 8, 8)
                        hover_background Frame(Solid("#38bdf8"), 8, 8)
                        xpadding 35
                        ypadding 14
                        xalign 0.5
                        action [SetField(clean_state, "wizard_step", 2)]

            # ШАГ 2: СДЕЛАЙ ФОТО (Интерфейс камеры / выбора снимка)
            elif step == 2:
                vbox:
                    spacing 15
                    xalign 0.5

                    text "ШАГ 2: ФОТОФИКСАЦИЯ НАХОДКИ (КАМЕРА СМАРТФОНА)":
                        size 22
                        color "#38bdf8"
                        bold True
                        xalign 0.5

                    text "Сделайте четкий снимок найденных отходов или выберите из галереи инспекции:":
                        size 16
                        color "#94a3b8"
                        xalign 0.5

                    hbox:
                        spacing 20
                        xalign 0.5

                        vbox:
                            spacing 8
                            add "images/challenge/photo_plastic.png":
                                xsize 240
                                ysize 135
                                fit "cover"
                            textbutton "Пластик и бутылки":
                                text_size 14
                                xfill True
                                background Frame(Solid("#1e293b"), 4, 4)
                                hover_background Frame(Solid("#00e6b8"), 4, 4)
                                action Function(wizard_set_photo, "images/challenge/photo_plastic.png", "Пластик / ПЭТ")

                        vbox:
                            spacing 8
                            add "images/challenge/photo_ghostnet.png":
                                xsize 240
                                ysize 135
                                fit "cover"
                            textbutton "Рыболовные сети":
                                text_size 14
                                xfill True
                                background Frame(Solid("#1e293b"), 4, 4)
                                hover_background Frame(Solid("#00e6b8"), 4, 4)
                                action Function(wizard_set_photo, "images/challenge/photo_ghostnet.png", "Сети и снасти (Ghost Gear)")

                        vbox:
                            spacing 8
                            add "images/challenge/photo_tires.png":
                                xsize 240
                                ysize 135
                                fit "cover"
                            textbutton "Старые покрышки":
                                text_size 14
                                xfill True
                                background Frame(Solid("#1e293b"), 4, 4)
                                hover_background Frame(Solid("#00e6b8"), 4, 4)
                                action Function(wizard_set_photo, "images/challenge/photo_tires.png", "Покрышки / Резина")

                        vbox:
                            spacing 8
                            add "images/challenge/photo_metal.png":
                                xsize 240
                                ysize 135
                                fit "cover"
                            textbutton "Металл и бочки":
                                text_size 14
                                xfill True
                                background Frame(Solid("#1e293b"), 4, 4)
                                hover_background Frame(Solid("#00e6b8"), 4, 4)
                                action Function(wizard_set_photo, "images/challenge/photo_metal.png", "Металл / Бочки")

            # ШАГ 3: ОПРЕДЕЛИ ТИП МУСОРА
            elif step == 3:
                vbox:
                    spacing 20
                    xalign 0.5
                    yalign 0.5

                    text "ШАГ 3: ОПРЕДЕЛЕНИЕ КАТЕГОРИИ ЗАГРЯЗНЕНИЯ":
                        size 22
                        color "#38bdf8"
                        bold True
                        xalign 0.5

                    hbox:
                        spacing 40
                        xalign 0.5
                        add clean_state.new_report_photo:
                            xsize 320
                            ysize 180
                            fit "cover"

                        vbox:
                            spacing 10
                            text "Выберите тип материала для протокола мониторинга:":
                                size 16
                                color "#cbd5e1"

                            for cat in ["Пластик / ПЭТ упаковка", "Сети и снасти (Ghost Gear)", "Покрышки / Резина", "Металл / Техногенный лом", "Нефтепродукты / ГСМ"]:
                                textbutton "[cat]":
                                    text_size 16
                                    background Frame(Solid("#00e6b8" if clean_state.new_report_category.startswith(cat[:7]) else "#1e293b"), 6, 6)
                                    hover_background Frame(Solid("#38bdf8"), 6, 6)
                                    xsize 380
                                    ypadding 10
                                    action Function(wizard_set_category, cat)

            # ШАГ 4: ОТМЕТЬ ТОЧКУ НА КАРТЕ
            elif step == 4:
                vbox:
                    spacing 15
                    xalign 0.5

                    text "ШАГ 4: ГЕОЛОКАЦИЯ И МАРКЕР НА КАРТЕ":
                        size 22
                        color "#38bdf8"
                        bold True
                        xalign 0.5

                    hbox:
                        spacing 25
                        xalign 0.5

                        # Интерактивная карта клика
                        frame:
                            xsize 720
                            ysize 400
                            background Solid("#000000")
                            padding (0, 0)
                            add "images/ui/oopt_map_bg.png":
                                xsize 720
                                ysize 400
                                fit "cover"

                            button:
                                xfill True
                                yfill True
                                background None
                                action Function(wizard_map_click)

                            # Пин на карте
                            add "images/ui/map_pin.png":
                                pos (340, 180)
                                at marker_pop

                        # Правая панель координат
                        vbox:
                            spacing 15
                            xsize 380

                            frame:
                                background Solid("#07101f")
                                padding (18, 15)
                                xfill True
                                vbox:
                                    spacing 6
                                    text "ТЕКУЩИЕ КООРДИНАТЫ:":
                                        size 14
                                        color "#94a3b8"
                                        bold True
                                    text "[clean_state.new_report_lat]":
                                        size 20
                                        color "#00e6b8"
                                        bold True
                                    text "[clean_state.new_report_lon]":
                                        size 20
                                        color "#00e6b8"
                                        bold True
                                    null height 5
                                    text "Кликните по карте для уточнения позиции":
                                        size 12
                                        color "#64748b"

                            textbutton "Координаты подтверждены →":
                                text_size 16
                                text_bold True
                                text_color "#070f1e"
                                background Frame(Solid("#00e6b8"), 6, 6)
                                hover_background Frame(Solid("#38bdf8"), 6, 6)
                                xfill True
                                ypadding 12
                                action [SetField(clean_state, "wizard_step", 5)]

            # ШАГ 5: ОТПРАВЬ РЕЗУЛЬТАТ
            elif step == 5:
                vbox:
                    spacing 20
                    xalign 0.5
                    yalign 0.5

                    text "ШАГ 5: ПРОВЕРКА ДАННЫХ И ОТПРАВКА НА МОДЕРАЦИЮ":
                        size 22
                        color "#38bdf8"
                        bold True
                        xalign 0.5

                    frame:
                        background Solid("#07101f")
                        padding (25, 20)
                        xsize 850
                        hbox:
                            spacing 25
                            add clean_state.new_report_photo:
                                xsize 200
                                ysize 112
                                fit "cover"
                            vbox:
                                spacing 8
                                text "Челлендж: [clean_state.selected_challenge.title]":
                                    size 16
                                    color "#ffffff"
                                    bold True
                                text "Категория: [clean_state.new_report_category]":
                                    size 15
                                    color "#00e6b8"
                                text "Координаты: [clean_state.new_report_lat], [clean_state.new_report_lon]":
                                    size 14
                                    color "#94a3b8"
                                text "Комментарий: [clean_state.new_report_comment]":
                                    size 14
                                    color "#cbd5e1"

                    hbox:
                        spacing 20
                        xalign 0.5
                        textbutton "← Назад":
                            text_size 16
                            background Frame(Solid("#1e293b"), 6, 6)
                            xpadding 25
                            ypadding 12
                            action [SetField(clean_state, "wizard_step", 4)]

                        textbutton "Отправить результат на проверку 🚀":
                            text_size 18
                            text_bold True
                            text_color "#070f1e"
                            background Frame(Solid("#00e6b8"), 8, 8)
                            hover_background Frame(Solid("#38bdf8"), 8, 8)
                            xpadding 35
                            ypadding 12
                            action Function(complete_and_submit_report)

## ЭКРАН 3: НАГРАДА И ПЕРЕХОД К МЕРОПРИЯТИЯМ (ЭТАП 6 И 7)
screen challenge_reward_screen():
    tag clean_screen
    add Solid("#070f1e")

    use clean_top_bar(active_tab="challenge")

    vbox:
        xalign 0.5
        ypos 100
        spacing 20
        xsize 1350

        # БАННЕР НАГРАДЫ (Этап 6: +100 очков и достижения)
        frame:
            background Frame(Solid("#0e1e38"), 12, 12)
            padding (35, 20)
            xfill True
            at slide_down

            hbox:
                spacing 30
                yalign 0.5

                add "images/ui/badge_first.png":
                    yalign 0.5

                vbox:
                    spacing 4
                    text "ОТЧЕТ ПРИНЯТ НА МОДЕРАЦИЮ!":
                        size 16
                        color "#00e6b8"
                        bold True
                    text "+100 очков начислено":
                        size 32
                        color "#ffffff"
                        bold True
                    text "Статус: На первичной верификации сотрудником ООПТ":
                        size 14
                        color "#f59e0b"

                add Solid("#1e293b"):
                    xsize 2
                    ysize 80

                # Список полученных достижений
                vbox:
                    spacing 6
                    text "РАЗБЛОКИРОВАНЫ ДОСТИЖЕНИЯ:":
                        size 13
                        color "#94a3b8"
                        bold True
                    hbox:
                        spacing 12
                        frame:
                            background Solid("#132847")
                            padding (10, 6)
                            text "🏅 Первое исследование":
                                size 14
                                color "#ffd700"
                        frame:
                            background Solid("#132847")
                            padding (10, 6)
                            text "🔍 Экоразведчик":
                                size 14
                                color "#00e6b8"

        # ЭТАП 7: ПЕРЕХОД К РЕАЛЬНОМУ МЕРОПРИЯТИЮ
        # «Хочешь сделать больше?» → ближайшие мероприятия «Чистого берега».
        # Цифровой челлендж → Первое действие → Интерес → Реальное мероприятие
        vbox:
            spacing 12

            hbox:
                spacing 15
                text "ХОЧЕШЬ СДЕЛАТЬ БОЛЬШЕ?":
                    size 24
                    color "#38bdf8"
                    bold True
                text "→ Ближайшие экспедиции и субботники «Чистого берега»":
                    size 18
                    color "#94a3b8"
                    yalign 0.5

            hbox:
                spacing 20
                for evt in clean_state.real_events:
                    frame:
                        background Frame(Solid("#0c1a30"), 10, 10)
                        padding (25, 20)
                        xsize 430
                        ysize 260

                        vbox:
                            spacing 8
                            frame:
                                background Solid("#166534")
                                padding (8, 4)
                                text "[evt.status]":
                                    size 12
                                    color "#bbf7d0"
                                    bold True

                            text "[evt.title]":
                                size 18
                                color "#ffffff"
                                bold True

                            text "📅 [evt.date]":
                                size 14
                                color "#00e6b8"

                            text "📍 [evt.place]":
                                size 13
                                color "#94a3b8"

                            text "[evt.desc]":
                                size 13
                                color "#cbd5e1"
                                line_spacing 2

                            null height 6
                            textbutton "Записаться волонтером →":
                                text_size 14
                                text_color "#38bdf8"
                                text_bold True
                                action Show("event_signup_modal", evt=evt)

        # Кнопка возврата в каталог
        textbutton "← Вернуться к списку заданий":
            text_size 16
            text_color "#cbd5e1"
            background Frame(Solid("#1e293b"), 6, 6)
            xpadding 25
            ypadding 10
            xalign 0.5
            action Show("challenge_catalog_screen")

## ВСПЛЫВАЮЩЕЕ ОКНО ЗАПИСИ НА МЕРОПРИЯТИЕ
screen event_signup_modal(evt):
    modal True
    add Solid("#000000b0")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 650
        ysize 400
        background Frame(Solid("#0e1e38"), 12, 12)
        padding (35, 30)

        vbox:
            spacing 15
            xalign 0.5

            text "ЗАПИСЬ НА МЕРОПРИЯТИЕ":
                size 22
                color "#00e6b8"
                bold True
                xalign 0.5

            text "[evt.title]":
                size 18
                color "#ffffff"
                bold True
                text_align 0.5

            text "Дата: [evt.date]\nМесто сбора: [evt.place]\n\nВы зарегистрированы в волонтерскую команду проекта «Чистый берег»! Координатор свяжется с вами в Telegram за 3 дня до старта.":
                size 15
                color "#cbd5e1"
                line_spacing 4

            null height 15

            textbutton "Отлично, буду участвовать! 👍":
                text_size 16
                text_bold True
                text_color "#070f1e"
                background Frame(Solid("#00e6b8"), 6, 6)
                hover_background Frame(Solid("#38bdf8"), 6, 6)
                xpadding 30
                ypadding 12
                xalign 0.5
                action Hide("event_signup_modal")
