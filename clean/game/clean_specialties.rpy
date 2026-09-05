## clean_specialties.rpy
## Раздел 6 профильных специальностей и ролевых задач проекта «Чистый берег»

init python:
    def select_specialty_action(spec_id):
        clean_state.set_specialty(spec_id)
        clean_state.specialties_filter_id = spec_id
        renpy.restart_interaction()

    def select_specialty_filter_action(spec_id):
        clean_state.specialties_filter_id = spec_id
        renpy.restart_interaction()

    def set_specialties_subtab_action(tab_name):
        clean_state.specialties_subtab = tab_name
        renpy.restart_interaction()

    def start_mission_from_hub(task_id):
        clean_state.start_role_mission(task_id)
        renpy.show_screen("clean_role_mission_screen")
        renpy.restart_interaction()

    def quiz_answer_click(chosen_spec_id):
        clean_state.quiz_result_id = chosen_spec_id
        clean_state.set_specialty(chosen_spec_id)
        clean_state.specialties_filter_id = chosen_spec_id
        clean_state.specialties_subtab = "tasks"
        renpy.restart_interaction()

screen clean_specialties_screen():
    tag clean_screen
    add Solid("#070f1e")

    use clean_top_bar(active_tab="specialties")

    $ cur_spec = clean_state.active_specialty
    $ filter_id = clean_state.specialties_filter_id
    $ current_filtered_spec = clean_state.get_specialty_by_id(filter_id)
    $ completed_in_active = clean_state.get_completed_tasks_count(cur_spec.id)

    vbox:
        xalign 0.5
        ypos 95
        spacing 12
        xsize 1400

        # 1. ВЕРХНИЙ БАННЕР ТЕКУЩЕЙ СПЕЦИАЛЬНОСТИ И ПРОГРЕССА
        frame:
            background Frame(Solid("#0e1e38"), 10, 10)
            padding (25, 14)
            xfill True

            hbox:
                spacing 20
                yalign 0.5

                text "[cur_spec.icon]":
                    size 38
                    yalign 0.5

                vbox:
                    spacing 3
                    hbox:
                        spacing 10
                        text "ВАШ ПРОФИЛЬ В ПРОЕКТЕ:":
                            size 12
                            color "#00e6b8"
                            bold True
                        frame:
                            background Solid("#166534")
                            padding (6, 2)
                            text "АКТИВЕН":
                                size 11
                                color "#bbf7d0"
                                bold True
                        frame:
                            background Solid("#1e293b")
                            padding (6, 2)
                            text "Выполнено задач роли: [completed_in_active] из 3":
                                size 11
                                color "#f59e0b"
                                bold True

                    text "[cur_spec.name] ([cur_spec.short_title])":
                        size 22
                        color "#ffffff"
                        bold True

                    text "[cur_spec.role_desc]":
                        size 13
                        color "#94a3b8"

                # Блок активного инструмента
                frame:
                    background Solid("#091426")
                    padding (14, 8)
                    xsize 390
                    yalign 0.5
                    vbox:
                        spacing 3
                        text "РАБОЧИЙ ИНСТРУМЕНТ:":
                            size 11
                            color "#f59e0b"
                            bold True
                        text "⚡ [cur_spec.tool_name]":
                            size 13
                            color "#38bdf8"
                            bold True
                        text "[cur_spec.tool_desc]":
                            size 11
                            color "#cbd5e1"

        # 2. ВКЛАДКИ РАЗДЕЛА: [🎯 Задачи ролей (18)] | [👥 Каталог 6 ролей] | [❓ Тест профориентации]
        hbox:
            spacing 10
            xfill True

            $ subtab = clean_state.specialties_subtab

            textbutton "🎯 ПРАКТИЧЕСКИЕ ЗАДАЧИ И МИССИИ РОЛЕЙ (18)":
                text_size 14
                text_bold True
                text_color ("#ffffff" if subtab == "tasks" else "#94a3b8")
                background Frame(Solid("#1e40af" if subtab == "tasks" else "#0f1f38"), 6, 6)
                hover_background Frame(Solid("#2563eb"), 6, 6)
                xpadding 25
                ypadding 10
                action Function(set_specialties_subtab_action, "tasks")

            textbutton "👥 КАТАЛОГ 6 СПЕЦИАЛЬНОСТЕЙ":
                text_size 14
                text_bold True
                text_color ("#ffffff" if subtab == "roles" else "#94a3b8")
                background Frame(Solid("#1e40af" if subtab == "roles" else "#0f1f38"), 6, 6)
                hover_background Frame(Solid("#2563eb"), 6, 6)
                xpadding 25
                ypadding 10
                action Function(set_specialties_subtab_action, "roles")

            textbutton "❓ ЭКСПРЕСС-ТЕСТ ПРОФОРИЕНТАЦИИ":
                text_size 14
                text_bold True
                text_color ("#ffffff" if subtab == "quiz" else "#94a3b8")
                background Frame(Solid("#1e40af" if subtab == "quiz" else "#0f1f38"), 6, 6)
                hover_background Frame(Solid("#2563eb"), 6, 6)
                xpadding 25
                ypadding 10
                action Function(set_specialties_subtab_action, "quiz")


        # 3. ОСНОВНОЙ КОНТЕНТ В ЗАВИСИМОСТИ ОТ ВКЛАДКИ
        if subtab == "tasks":
            # --- ВКЛАДКА 1: ЗАДАЧИ И МИССИИ ПО РОЛЯМ ---
            vbox:
                spacing 10

                # Горизонтальный фильтр по 6 ролям
                hbox:
                    spacing 8
                    for sp in clean_state.specialties:
                        $ is_f = (sp.id == filter_id)
                        $ count_done = clean_state.get_completed_tasks_count(sp.id)
                        textbutton ("[sp.icon] [sp.short_title] (" + str(count_done) + "/3)"):
                            text_size 13
                            text_bold is_f
                            text_color ("#ffffff" if is_f else "#94a3b8")
                            background Frame(Solid("#00e6b8" if is_f else "#10223d"), 5, 5)
                            hover_background Frame(Solid("#38bdf8"), 5, 5)
                            xpadding 14
                            ypadding 8
                            action Function(select_specialty_filter_action, sp.id)

                # Шапка выбранной специальности в фильтре
                $ f_spec = clean_state.get_specialty_by_id(filter_id)

                frame:
                    background Solid("#0a1527")
                    padding (16, 8)
                    xfill True
                    hbox:
                        spacing 15
                        yalign 0.5
                        text "[f_spec.icon] Практические миссии: [f_spec.name]":
                            size 16
                            color "#00e6b8"
                            bold True
                        text "•":
                            size 14
                            color "#64748b"
                        text "[f_spec.tasks_desc]":
                            size 12
                            color "#cbd5e1"
                            yalign 0.5

                # Список 3 задач для выбранной специальности
                $ cur_tasks = clean_state.get_tasks_for_specialty(filter_id)

                hbox:
                    spacing 15
                    for t_item in cur_tasks:
                        frame:
                            background Frame(Solid("#102647" if t_item.completed else "#0c1a30"), 8, 8)
                            padding (20, 16)
                            xsize 450
                            yminimum 450

                            vbox:
                                spacing 8

                                # Бейджи сложности и очков
                                hbox:
                                    spacing 8
                                    frame:
                                        background Solid("#1e293b")
                                        padding (6, 3)
                                        text "[t_item.difficulty]":
                                            size 11
                                            color "#f59e0b"
                                            bold True
                                    frame:
                                        background Solid("#14532d")
                                        padding (6, 3)
                                        text "+[t_item.reward_xp] XP":
                                            size 11
                                            color "#86efac"
                                            bold True
                                    if t_item.completed:
                                        frame:
                                            background Solid("#166534")
                                            padding (6, 3)
                                            text "✔ ВЫПОЛНЕНО":
                                                size 11
                                                color "#bbf7d0"
                                                bold True

                                # Заголовок задачи
                                text "[t_item.title]":
                                    size 16
                                    color "#ffffff"
                                    bold True
                                    line_spacing 2

                                # Сценарий
                                text "[t_item.scenario]":
                                    size 12
                                    color "#cbd5e1"
                                    line_spacing 2

                                # Цель
                                frame:
                                    background Solid("#081224")
                                    padding (10, 8)
                                    xfill True
                                    vbox:
                                        spacing 3
                                        text "ЦЕЛЬ:":
                                            size 10
                                            color "#38bdf8"
                                            bold True
                                        text "[t_item.goal]":
                                            size 11
                                            color "#e2e8f0"
                                            line_spacing 2

                                # Стек
                                text "Стек: [t_item.tech_stack]":
                                    size 11
                                    color "#93c5fd"

                                null height 4

                                # Кнопка запуска миссии
                                if t_item.completed:
                                    textbutton "✔ Пройти снова (+XP) →":
                                        text_size 13
                                        text_color "#bbf7d0"
                                        background Frame(Solid("#166534"), 5, 5)
                                        hover_background Frame(Solid("#22c55e"), 5, 5)
                                        xfill True
                                        ypadding 9
                                        action Function(start_mission_from_hub, t_item.id)
                                else:
                                    textbutton "▶ Выполнить задачу →":
                                        text_size 13
                                        text_bold True
                                        text_color "#ffffff"
                                        background Frame(Solid("#00e6b8"), 5, 5)
                                        hover_background Frame(Solid("#38bdf8"), 5, 5)
                                        xfill True
                                        ypadding 9
                                        action Function(start_mission_from_hub, t_item.id)


        elif subtab == "roles":
            # --- ВКЛАДКА 2: КАТАЛОГ 6 СПЕЦИАЛЬНОСТЕЙ ---
            viewport:
                scrollbars "vertical"
                mousewheel True
                ysize 530

                vbox:
                    spacing 15

                    # Строка 1: ДЗЗ, GIS, ML
                    hbox:
                        spacing 15
                        for spec in clean_state.specialties[:3]:
                            $ is_active = (spec.id == cur_spec.id)
                            $ done_cnt = clean_state.get_completed_tasks_count(spec.id)
                            frame:
                                background Frame(Solid("#102647" if is_active else "#0c1a30"), 8, 8)
                                padding (20, 16)
                                xsize 450
                                ysize 255

                                vbox:
                                    spacing 8
                                    hbox:
                                        spacing 12
                                        text "[spec.icon]":
                                            size 28
                                        vbox:
                                            text "[spec.name]":
                                                size 18
                                                color ("#00e6b8" if is_active else "#ffffff")
                                                bold True
                                            text "[spec.short_title] • Задач сдано: [done_cnt]/3":
                                                size 12
                                                color "#94a3b8"

                                    text "[spec.tasks_desc]":
                                        size 12
                                        color "#cbd5e1"
                                        line_spacing 2
                                        ysize 65

                                    frame:
                                        background Solid("#07101f")
                                        padding (8, 4)
                                        xfill True
                                        text "Стек: [spec.tech_stack]":
                                            size 11
                                            color "#38bdf8"

                                    hbox:
                                        spacing 8
                                        if is_active:
                                            frame:
                                                background Solid("#15803d")
                                                padding (8, 6)
                                                xsize 210
                                                text "✔ Активная роль":
                                                    size 12
                                                    color "#ffffff"
                                                    bold True
                                                    xalign 0.5
                                        else:
                                            textbutton "Выбрать роль →":
                                                text_size 12
                                                text_color "#cbd5e1"
                                                background Frame(Solid("#1e293b"), 4, 4)
                                                hover_background Frame(Solid("#00e6b8"), 4, 4)
                                                xsize 210
                                                ypadding 6
                                                action Function(select_specialty_action, spec.id)

                                        textbutton "Задачи роли (3) →":
                                            text_size 12
                                            text_color "#38bdf8"
                                            background Frame(Solid("#132847"), 4, 4)
                                            hover_background Frame(Solid("#2563eb"), 4, 4)
                                            xsize 200
                                            ypadding 6
                                            action [Function(select_specialty_filter_action, spec.id), Function(set_specialties_subtab_action, "tasks")]

                    # Строка 2: Эколог, БПЛА, Координатор
                    hbox:
                        spacing 15
                        for spec in clean_state.specialties[3:]:
                            $ is_active = (spec.id == cur_spec.id)
                            $ done_cnt = clean_state.get_completed_tasks_count(spec.id)
                            frame:
                                background Frame(Solid("#102647" if is_active else "#0c1a30"), 8, 8)
                                padding (20, 16)
                                xsize 450
                                ysize 255

                                vbox:
                                    spacing 8
                                    hbox:
                                        spacing 12
                                        text "[spec.icon]":
                                            size 28
                                        vbox:
                                            text "[spec.name]":
                                                size 18
                                                color ("#00e6b8" if is_active else "#ffffff")
                                                bold True
                                            text "[spec.short_title] • Задач сдано: [done_cnt]/3":
                                                size 12
                                                color "#94a3b8"

                                    text "[spec.tasks_desc]":
                                        size 12
                                        color "#cbd5e1"
                                        line_spacing 2
                                        ysize 65

                                    frame:
                                        background Solid("#07101f")
                                        padding (8, 4)
                                        xfill True
                                        text "Стек: [spec.tech_stack]":
                                            size 11
                                            color "#38bdf8"

                                    hbox:
                                        spacing 8
                                        if is_active:
                                            frame:
                                                background Solid("#15803d")
                                                padding (8, 6)
                                                xsize 210
                                                text "✔ Активная роль":
                                                    size 12
                                                    color "#ffffff"
                                                    bold True
                                                    xalign 0.5
                                        else:
                                            textbutton "Выбрать роль →":
                                                text_size 12
                                                text_color "#cbd5e1"
                                                background Frame(Solid("#1e293b"), 4, 4)
                                                hover_background Frame(Solid("#00e6b8"), 4, 4)
                                                xsize 210
                                                ypadding 6
                                                action Function(select_specialty_action, spec.id)

                                        textbutton "Задачи роли (3) →":
                                            text_size 12
                                            text_color "#38bdf8"
                                            background Frame(Solid("#132847"), 4, 4)
                                            hover_background Frame(Solid("#2563eb"), 4, 4)
                                            xsize 200
                                            ypadding 6
                                            action [Function(select_specialty_filter_action, spec.id), Function(set_specialties_subtab_action, "tasks")]


        elif subtab == "quiz":
            # --- ВКЛАДКА 3: ЭКСПРЕСС-ТЕСТ ПРОФОРИЕНТАЦИИ ---
            frame:
                background Frame(Solid("#0e1e38"), 8, 8)
                padding (30, 24)
                xfill True

                vbox:
                    spacing 16
                    hbox:
                        spacing 15
                        text "🎯 ЭКСПРЕСС-ТЕСТ: КАКАЯ СПЕЦИАЛЬНОСТЬ ТЕБЕ ПОДХОДИТ?":
                            size 18
                            color "#f59e0b"
                            bold True
                        text "Кликни на утверждение, которое тебе ближе всего — роль и задачи активируются сразу:":
                            size 13
                            color "#94a3b8"
                            yalign 0.5

                    grid 3 2:
                        spacing 12
                        xfill True

                        textbutton "🛰️ «Люблю космические снимки и глобальный масштаб»":
                            text_size 13
                            background Frame(Solid("#132847"), 5, 5)
                            hover_background Frame(Solid("#00e6b8"), 5, 5)
                            ypadding 12
                            action Function(quiz_answer_click, "dzz")

                        textbutton "🗺️ «Обожаю карты, координаты и пространственные слои»":
                            text_size 13
                            background Frame(Solid("#132847"), 5, 5)
                            hover_background Frame(Solid("#00e6b8"), 5, 5)
                            ypadding 12
                            action Function(quiz_answer_click, "gis")

                        textbutton "🧠 «Хочу обучать нейросети и автоматизировать детекцию»":
                            text_size 13
                            background Frame(Solid("#132847"), 5, 5)
                            hover_background Frame(Solid("#00e6b8"), 5, 5)
                            ypadding 12
                            action Function(quiz_answer_click, "ml")

                        textbutton "🌿 «Хочу изучать влияние отходов на животных и флору»":
                            text_size 13
                            background Frame(Solid("#132847"), 5, 5)
                            hover_background Frame(Solid("#00e6b8"), 5, 5)
                            ypadding 12
                            action Function(quiz_answer_click, "ecologist")

                        textbutton "🚁 «Хочу пилотировать дроны и делать детальную съемку»":
                            text_size 13
                            background Frame(Solid("#132847"), 5, 5)
                            hover_background Frame(Solid("#00e6b8"), 5, 5)
                            ypadding 12
                            action Function(quiz_answer_click, "uav")

                        textbutton "🤝 «Хочу работать с людьми и организовывать акции»":
                            text_size 13
                            background Frame(Solid("#132847"), 5, 5)
                            hover_background Frame(Solid("#00e6b8"), 5, 5)
                            ypadding 12
                            action Function(quiz_answer_click, "volunteer_coord")
