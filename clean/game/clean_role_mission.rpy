## clean_role_mission.rpy
## Интерактивный экран выполнения ролевых задач проекта «Чистый берег»
## Apple-style UI: чистый дизайн, мягкие цвета, крупные элементы

init python:
    def role_mission_select_opt(opt_text):
        clean_state.select_mission_option(opt_text)
        renpy.restart_interaction()

    def role_mission_submit():
        clean_state.submit_mission_choice()
        renpy.restart_interaction()

    def role_mission_finish_specialty():
        clean_state.complete_current_specialty()
        if clean_state.all_specialties_completed():
            renpy.show_screen("clean_certificate_screen")
        else:
            rem = clean_state.get_remaining_specialties()
            if rem:
                clean_state.set_specialty(rem[0].id)
            renpy.show_screen("role_selection_entry_screen")
        renpy.restart_interaction()

    def role_mission_next():
        cur_task = clean_state.active_role_mission
        tasks = clean_state.get_tasks_for_specialty(cur_task.specialty_id)
        next_t = None
        for t in tasks:
            if not t.completed and t.id != cur_task.id:
                next_t = t
                break
        if not next_t:
            for i, t in enumerate(tasks):
                if t.id == cur_task.id and i + 1 < len(tasks):
                    next_t = tasks[i + 1]
                    break
        if not next_t and tasks:
            next_t = tasks[0]
        if next_t:
            clean_state.start_role_mission(next_t.id)
        renpy.restart_interaction()

    # Обработчик клика по карте для интерактивных map-задач
    def map_click_handle(task_id, zone_id):
        clean_state.map_click_zone = zone_id
        renpy.restart_interaction()

screen clean_role_mission_screen():
    tag clean_screen
    add Solid("#0a0a0a")

    $ task = clean_state.active_role_mission
    $ spec = clean_state.active_specialty
    $ tasks_list = clean_state.get_tasks_for_specialty(task.specialty_id)

    # ═══════════════════════════════════════════════════════
    # ВЕРХНЯЯ НАВИГАЦИОННАЯ ПАНЕЛЬ (Apple-style)
    # ═══════════════════════════════════════════════════════
    frame:
        xpos 0
        ypos 0
        xsize 1920
        ysize 64
        background Solid("#141414")
        padding (24, 0)

        hbox:
            spacing 16
            yalign 0.5

            # Кнопка назад
            button:
                yalign 0.5
                background Frame(Solid("#1c1c1e"), 12, 12)
                hover_background Frame(Solid("#2c2c2e"), 12, 12)
                padding (16, 8)
                action Show("role_selection_entry_screen")
                text "← Назад":
                    size 14
                    color "#8e8e93"

            # Разделитель
            frame:
                yalign 0.5
                xsize 1
                ysize 28
                background Solid("#3a3a3c")

            # Специальность и задача
            $ task_num = tasks_list.index(task) + 1 if (task and task in tasks_list) else 1
            text "[spec.icon] [spec.name]":
                size 16
                color "#ffffff"
                bold True
                yalign 0.5

            text "Задача [task_num] из 3":
                size 14
                color "#8e8e93"
                yalign 0.5

            # Статус-бейджи
            frame:
                yalign 0.5
                background Frame(Solid("#1c1c1e"), 12, 12)
                padding (12, 6)
                text "[task.difficulty]":
                    size 12
                    color "#f59e0b"
                    bold True

            frame:
                yalign 0.5
                background Frame(Solid("#0a2e1a"), 12, 12)
                padding (12, 6)
                text "+[task.reward_xp] XP":
                    size 12
                    color "#34d399"
                    bold True

            if task.completed:
                frame:
                    yalign 0.5
                    background Frame(Solid("#064e3b"), 12, 12)
                    padding (12, 6)
                    text "✓ Сдано":
                        size 12
                        color "#6ee7b7"
                        bold True

            null width 30

            # Переключатель миссий
            hbox:
                spacing 8
                yalign 0.5
                for idx, t_item in enumerate(tasks_list):
                    $ is_current = (t_item.id == task.id)
                    $ mbg = "#0a84ff" if is_current else ("#1a3a2a" if t_item.completed else "#1c1c1e")
                    $ mfg = "#ffffff" if is_current else ("#6ee7b7" if t_item.completed else "#8e8e93")
                    button:
                        yalign 0.5
                        background Frame(Solid(mbg), 12, 12)
                        hover_background Frame(Solid("#3a3a3c"), 12, 12)
                        padding (14, 6)
                        action [Function(clean_state.start_role_mission, t_item.id), Function(renpy.restart_interaction)]
                        hbox:
                            spacing 4
                            text (str(idx + 1)):
                                size 13
                                color mfg
                                bold True
                            if t_item.completed:
                                text "✓":
                                    size 11
                                    color "#6ee7b7"

            # Кнопка гида
            null width 20
            button:
                yalign 0.5
                background Frame(Solid("#1c1c1e"), 12, 12)
                hover_background Frame(Solid("#2c2c2e"), 12, 12)
                padding (14, 8)
                action Show("mission_tutorial_modal")
                text "? Гид":
                    size 13
                    color "#f59e0b"

    # ═══════════════════════════════════════════════════════
    # ОСНОВНАЯ ОБЛАСТЬ: ЛЕВАЯ ПАНЕЛЬ + ПРАВАЯ ВИЗУАЛИЗАЦИЯ
    # ═══════════════════════════════════════════════════════

    # ЛЕВАЯ ПАНЕЛЬ — ЗАДАНИЕ И ОТВЕТЫ (Apple card style)
    frame:
        xpos 24
        ypos 80
        xsize 540
        ysize 980
        background Frame(Solid("#1c1c1e"), 16, 16)
        padding (24, 24)

        vbox:
            spacing 16

            # Заголовок задачи
            text "[task.title]":
                size 20
                color "#ffffff"
                bold True
                line_spacing 4

            # Сценарий
            frame:
                background Frame(Solid("#2c2c2e"), 12, 12)
                padding (16, 14)
                xfill True
                vbox:
                    spacing 6
                    text "Ситуация":
                        size 12
                        color "#8e8e93"
                        bold True
                    text "[task.scenario]":
                        size 14
                        color "#e5e5e7"
                        line_spacing 4

            # Цель
            frame:
                background Frame(Solid("#0a1e3a"), 12, 12)
                padding (16, 14)
                xfill True
                vbox:
                    spacing 6
                    text "Задача":
                        size 12
                        color "#0a84ff"
                        bold True
                    text "[task.goal]":
                        size 14
                        color "#ffffff"
                        bold True
                        line_spacing 4

            # Инструменты
            frame:
                background Frame(Solid("#2c2c2e"), 12, 12)
                padding (12, 10)
                xfill True
                text "[task.tech_stack]":
                    size 12
                    color "#8e8e93"

            null height 4

            # ═══════════════════════════════════════
            # БЛОК ОТВЕТОВ / РЕЗУЛЬТАТ
            # ═══════════════════════════════════════
            if clean_state.mission_status == "BRIEFING":
                text "Выберите ответ":
                    size 13
                    color "#8e8e93"
                    bold True

                vbox:
                    spacing 10
                    for opt in task.options:
                        $ is_selected = (clean_state.mission_selected_option == opt)
                        button:
                            if is_selected:
                                background Frame(Solid("#0a3d6e"), 12, 12)
                            else:
                                background Frame(Solid("#2c2c2e"), 12, 12)
                            hover_background Frame(Solid("#3a3a3c"), 12, 12)
                            padding (16, 14)
                            xfill True
                            action Function(role_mission_select_opt, opt)
                            hbox:
                                spacing 12
                                yalign 0.5
                                if is_selected:
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        ysize 20
                                        background Frame(Solid("#0a84ff"), 10, 10)
                                else:
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        ysize 20
                                        background Frame(Solid("#3a3a3c"), 10, 10)
                                text "[opt]":
                                    size 13
                                    color ("#ffffff" if is_selected else "#c7c7cc")
                                    bold is_selected
                                    line_spacing 3

                null height 6

                button:
                    xfill True
                    ysize 52
                    background Frame(Solid("#0a84ff"), 14, 14)
                    hover_background Frame(Solid("#0070e0"), 14, 14)
                    padding (16, 12)
                    action Function(role_mission_submit)
                    text "Проверить ответ":
                        size 16
                        color "#ffffff"
                        bold True
                        xalign 0.5
                        yalign 0.5

            else:
                # РЕЗУЛЬТАТ
                vbox:
                    spacing 12
                    if clean_state.mission_result_success:
                        frame:
                            background Frame(Solid("#0a2e1a"), 12, 12)
                            padding (16, 14)
                            xfill True
                            vbox:
                                spacing 4
                                text "Верно!":
                                    size 18
                                    color "#34d399"
                                    bold True
                                text "+[clean_state.mission_result_xp] XP":
                                    size 14
                                    color "#6ee7b7"
                    else:
                        frame:
                            background Frame(Solid("#3a2008"), 12, 12)
                            padding (16, 14)
                            xfill True
                            vbox:
                                spacing 4
                                text "Не совсем":
                                    size 18
                                    color "#fbbf24"
                                    bold True
                                text "+[clean_state.mission_result_xp] XP за попытку":
                                    size 14
                                    color "#fcd34d"

                    # Объяснение
                    frame:
                        background Frame(Solid("#2c2c2e"), 12, 12)
                        padding (16, 14)
                        xfill True
                        yminimum 120
                        vbox:
                            spacing 6
                            text "Объяснение":
                                size 12
                                color "#0a84ff"
                                bold True
                            text "[clean_state.mission_result_feedback]":
                                size 13
                                color "#e5e5e7"
                                line_spacing 4

                    # Навигация
                    $ all_spec_done = all(t.completed for t in tasks_list)
                    $ remaining_uncompleted = [t for t in tasks_list if not t.completed]

                    if all_spec_done:
                        button:
                            xfill True
                            ysize 52
                            background Frame(Solid("#059669"), 14, 14)
                            hover_background Frame(Solid("#10b981"), 14, 14)
                            padding (16, 12)
                            action Function(role_mission_finish_specialty)
                            text "Завершить специальность ✓":
                                size 16
                                color "#ffffff"
                                bold True
                                xalign 0.5
                                yalign 0.5
                    elif remaining_uncompleted:
                        $ next_unc = remaining_uncompleted[0]
                        $ next_num = tasks_list.index(next_unc) + 1
                        button:
                            xfill True
                            ysize 52
                            background Frame(Solid("#0a84ff"), 14, 14)
                            hover_background Frame(Solid("#0070e0"), 14, 14)
                            padding (16, 12)
                            action Function(role_mission_next)
                            text "Задача №[next_num] →":
                                size 16
                                color "#ffffff"
                                bold True
                                xalign 0.5
                                yalign 0.5
                    else:
                        button:
                            xfill True
                            ysize 52
                            background Frame(Solid("#0a84ff"), 14, 14)
                            hover_background Frame(Solid("#0070e0"), 14, 14)
                            padding (16, 12)
                            action Function(role_mission_next)
                            text "Далее →":
                                size 16
                                color "#ffffff"
                                bold True
                                xalign 0.5
                                yalign 0.5


    # ═══════════════════════════════════════════════════════
    # ПРАВАЯ ПАНЕЛЬ — ВИЗУАЛИЗАЦИЯ (Apple card)
    # ═══════════════════════════════════════════════════════
    frame:
        xpos 580
        ypos 80
        xsize 1316
        ysize 980
        background Frame(Solid("#1c1c1e"), 16, 16)
        padding (12, 12)

        vbox:
            spacing 8

            # Мини-хедер инструмента
            frame:
                background Frame(Solid("#2c2c2e"), 12, 12)
                padding (16, 8)
                xfill True
                hbox:
                    spacing 12
                    yalign 0.5
                    text "[spec.icon] [spec.tool_name]":
                        size 14
                        color "#ffffff"
                        bold True

                    if task.specialty_id == "dzz":
                        text "Sentinel-2 MSI • 10м":
                            size 12
                            color "#8e8e93"
                    elif task.specialty_id == "gis":
                        text "WGS 84 / UTM 34N":
                            size 12
                            color "#8e8e93"
                    elif task.specialty_id == "ml":
                        text "YOLOv8 • PyTorch":
                            size 12
                            color "#8e8e93"
                    elif task.specialty_id == "ecologist":
                        text "Экоаудит ФККО":
                            size 12
                            color "#8e8e93"
                    elif task.specialty_id == "uav":
                        text "Pixhawk • GSD 2 см/пикс":
                            size 12
                            color "#8e8e93"
                    elif task.specialty_id == "volunteer_coord":
                        text "Citizen Science":
                            size 12
                            color "#8e8e93"

            # ВИЗУАЛИЗАТОР
            frame:
                background Solid("#000000")
                xfill True
                ysize 920
                padding (0, 0)

                # ═══════════════════════════════════════
                # 1. ДЗЗ
                # ═══════════════════════════════════════

                # ДЗЗ-1 — ИНТЕРАКТИВНАЯ КАРТА (map-click для выбора области аномалии)
                if task.id == "dzz_1":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    # Интерактивные кликабельные зоны — пользователь тыкает на область аномалии
                    # Зона нефтяного шлейфа (правильная)
                    button:
                        pos (250, 240)
                        xsize 320
                        ysize 370
                        background Solid("#00000000")
                        hover_background Solid("#0a84ff15")
                        action Function(map_click_handle, "dzz_1", "oil_slick")

                    # Зона чистой воды (неправильная)
                    button:
                        pos (700, 100)
                        xsize 400
                        ysize 300
                        background Solid("#00000000")
                        hover_background Solid("#0a84ff15")
                        action Function(map_click_handle, "dzz_1", "clean_water")

                    # Зона берега (неправильная)
                    button:
                        pos (100, 700)
                        xsize 500
                        ysize 200
                        background Solid("#00000000")
                        hover_background Solid("#0a84ff15")
                        action Function(map_click_handle, "dzz_1", "coastline")

                    # Пульсирующий контур шлейфа
                    $ mcz = getattr(clean_state, "map_click_zone", None)
                    if mcz == "oil_slick":
                        add Solid("#34d39940"):
                            pos (250, 240)
                            xsize 320
                            ysize 370
                            at radar_pulse
                        frame:
                            pos (250, 210)
                            background Frame(Solid("#0a2e1a"), 8, 8)
                            padding (12, 6)
                            text "✓ Нефтяной шлейф обнаружен!":
                                size 13
                                color "#34d399"
                                bold True
                    elif mcz == "clean_water":
                        add Solid("#ef444440"):
                            pos (700, 100)
                            xsize 400
                            ysize 300
                        frame:
                            pos (700, 70)
                            background Frame(Solid("#3a1008"), 8, 8)
                            padding (12, 6)
                            text "✗ Это не вода":
                                size 13
                                color "#fca5a5"
                                bold True
                    elif mcz == "coastline":
                        add Solid("#ef444440"):
                            pos (100, 700)
                            xsize 500
                            ysize 200
                        frame:
                            pos (100, 670)
                            background Frame(Solid("#3a1008"), 8, 8)
                            padding (12, 6)
                            text "✗ Это береговая линия":
                                size 13
                                color "#fca5a5"
                                bold True

                    # Инфо-карточка сверху
                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Sentinel-2 MSI":
                                size 12
                                color "#0a84ff"
                                bold True
                            text "Нажмите на подозрительную\nобласть на снимке":
                                size 12
                                color "#c7c7cc"
                                line_spacing 2

                    frame:
                        pos (20, 860)
                        background Frame(Solid("#1c1c1ed0"), 12, 12)
                        padding (12, 6)
                        text "55°09′14″ N, 20°51′21″ E • 10м/пикс":
                            size 11
                            color "#8e8e93"


                # ДЗЗ-2: Сравнение До и После
                elif task.id == "dzz_2":
                    hbox:
                        spacing 8
                        xalign 0.5
                        yalign 0.5
                        frame:
                            xsize 630
                            ysize 910
                            padding (0, 0)
                            background Solid("#050c17")
                            add im.Scale("images/satellite/level2_before.png", 630, 910)
                            frame:
                                pos (12, 12)
                                background Frame(Solid("#1c1c1ef0"), 10, 10)
                                padding (12, 6)
                                text "До шторма (15.08)":
                                    size 13
                                    color "#0a84ff"
                                    bold True

                        frame:
                            xsize 630
                            ysize 910
                            padding (0, 0)
                            background Solid("#050c17")
                            add im.Scale("images/satellite/level2_after.png", 630, 910)
                            frame:
                                pos (12, 12)
                                background Frame(Solid("#1c1c1ef0"), 10, 10)
                                padding (12, 6)
                                text "После шторма (20.08)":
                                    size 13
                                    color "#f59e0b"
                                    bold True

                            add Solid("#f59e0b30"):
                                pos (220, 360)
                                xsize 260
                                ysize 200
                                at radar_pulse

                            frame:
                                pos (180, 330)
                                background Frame(Solid("#3a2008f0"), 8, 8)
                                padding (10, 6)
                                text "+1.2 га новых отходов":
                                    size 12
                                    color "#fbbf24"
                                    bold True


                # ДЗЗ-3: Калибровка NDWI
                elif task.id == "dzz_3":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    add Solid("#ef444425"):
                        pos (750, 600)
                        xsize 50
                        ysize 50
                    frame:
                        pos (750, 570)
                        background Frame(Solid("#3a1008f0"), 8, 8)
                        padding (8, 4)
                        text "Шум отсечен (NDWI < +0.15)":
                            size 11
                            color "#fca5a5"
                            bold True

                    add Solid("#34d39930"):
                        pos (300, 290)
                        xsize 280
                        ysize 210
                        at radar_pulse
                    frame:
                        pos (300, 260)
                        background Frame(Solid("#0a2e1af0"), 8, 8)
                        padding (10, 6)
                        text "Загрязнение (NDWI > +0.15)":
                            size 12
                            color "#34d399"
                            bold True

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Калибровка NDWI":
                                size 13
                                color "#0a84ff"
                                bold True
                            text "NDWI < 0.00 — суша\n0.00–0.15 — пена (шум)\n> +0.15 — загрязнение":
                                size 11
                                color "#c7c7cc"
                                line_spacing 3

                # ═══════════════════════════════════════
                # 2. GIS
                # ═══════════════════════════════════════

                # ГИС-1 — ИНТЕРАКТИВНАЯ КАРТА (клик по области буфера)
                elif task.id == "gis_1":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    # Кликабельная зона: охранный буфер 250м (правильная)
                    button:
                        pos (420, 190)
                        xsize 400
                        ysize 400
                        background Solid("#00000000")
                        hover_background Solid("#f59e0b12")
                        action Function(map_click_handle, "gis_1", "buffer_250")

                    # Кликабельная зона: далеко от парка
                    button:
                        pos (50, 500)
                        xsize 300
                        ysize 300
                        background Solid("#00000000")
                        hover_background Solid("#0a84ff10")
                        action Function(map_click_handle, "gis_1", "outside")

                    $ mcz_gis = getattr(clean_state, "map_click_zone", None)
                    if mcz_gis == "buffer_250":
                        add Solid("#f59e0b25"):
                            pos (420, 190)
                            xsize 400
                            ysize 400
                            at radar_pulse
                        frame:
                            pos (420, 160)
                            background Frame(Solid("#3a2008f0"), 8, 8)
                            padding (12, 6)
                            text "✓ Охранная зона R=250м":
                                size 13
                                color "#fbbf24"
                                bold True
                        frame:
                            pos (520, 360)
                            background Frame(Solid("#3a1008f0"), 8, 8)
                            padding (8, 4)
                            text "⚠ Свалка внутри зоны!":
                                size 11
                                color "#fca5a5"
                                bold True
                    elif mcz_gis == "outside":
                        frame:
                            pos (50, 470)
                            background Frame(Solid("#1c1c1ef0"), 8, 8)
                            padding (12, 6)
                            text "Эта область вне охранной зоны":
                                size 12
                                color "#8e8e93"

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Векторные слои QGIS":
                                size 13
                                color "#0a84ff"
                                bold True
                            text "Нажмите на охранную зону\nна карте заповедника":
                                size 12
                                color "#c7c7cc"
                                line_spacing 2


                # ГИС-2: Площадь полигона
                elif task.id == "gis_2":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    frame:
                        pos (100, 100)
                        xsize 900
                        ysize 700
                        background Frame(Solid("#34d39920"), 3, 3)

                    frame:
                        pos (460, 220)
                        background Frame(Solid("#1c1c1ef0"), 8, 8)
                        padding (10, 6)
                        text "↔ 140 м":
                            size 13
                            color "#34d399"
                            bold True

                    frame:
                        pos (890, 400)
                        background Frame(Solid("#1c1c1ef0"), 8, 8)
                        padding (10, 6)
                        text "↕ 100 м":
                            size 13
                            color "#34d399"
                            bold True

                    frame:
                        pos (440, 400)
                        background Frame(Solid("#0a2e1af0"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Площадь":
                                size 12
                                color "#6ee7b7"
                            text "1.40 га":
                                size 24
                                color "#ffffff"
                                bold True
                            text "140м × 100м = 14 000 м²":
                                size 11
                                color "#c7c7cc"

                # ГИС-3: Секторы — ИНТЕРАКТИВНАЯ КАРТА (клик по секторам)
                elif task.id == "gis_3":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    # 4 кликабельных сектора
                    button:
                        pos (100, 80)
                        xsize 530
                        ysize 380
                        background Solid("#00000000")
                        hover_background Solid("#0a84ff10")
                        action Function(map_click_handle, "gis_3", "A")

                    button:
                        pos (650, 80)
                        xsize 530
                        ysize 380
                        background Solid("#00000000")
                        hover_background Solid("#ef444415")
                        action Function(map_click_handle, "gis_3", "B")

                    button:
                        pos (100, 480)
                        xsize 530
                        ysize 380
                        background Solid("#00000000")
                        hover_background Solid("#0a84ff10")
                        action Function(map_click_handle, "gis_3", "C")

                    button:
                        pos (650, 480)
                        xsize 530
                        ysize 380
                        background Solid("#00000000")
                        hover_background Solid("#0a84ff10")
                        action Function(map_click_handle, "gis_3", "D")

                    $ mcz_sec = getattr(clean_state, "map_click_zone", None)

                    # Лейблы секторов
                    frame:
                        pos (280, 240)
                        background Frame(Solid("#1c1c1eea"), 8, 8)
                        padding (10, 6)
                        text ("✓ Сектор A (Мыс)" if mcz_sec == "A" else "Сектор A (Мыс)"):
                            size 12
                            color ("#fca5a5" if mcz_sec == "A" else "#8e8e93")

                    if mcz_sec == "B":
                        add Solid("#ef444430"):
                            pos (650, 80)
                            xsize 530
                            ysize 380
                            at radar_pulse
                    frame:
                        pos (780, 200)
                        background Frame(Solid(("#3a1008f0" if mcz_sec == "B" else "#1c1c1eea")), 8, 8)
                        padding (10, 6)
                        vbox:
                            spacing 2
                            text ("✓ Сектор B — УГРОЗА!" if mcz_sec == "B" else "Сектор B (Залив)"):
                                size 13
                                color ("#ef4444" if mcz_sec == "B" else "#8e8e93")
                                bold (mcz_sec == "B")
                            if mcz_sec == "B":
                                text "Течение сносит 72% мусора сюда":
                                    size 11
                                    color "#fca5a5"

                    frame:
                        pos (280, 620)
                        background Frame(Solid("#1c1c1eea"), 8, 8)
                        padding (10, 6)
                        text ("✓ Сектор C" if mcz_sec == "C" else "Сектор C (Гряда)"):
                            size 12
                            color ("#fca5a5" if mcz_sec == "C" else "#8e8e93")

                    frame:
                        pos (780, 620)
                        background Frame(Solid("#1c1c1eea"), 8, 8)
                        padding (10, 6)
                        text ("✓ Сектор D" if mcz_sec == "D" else "Сектор D (Дюны)"):
                            size 12
                            color ("#fca5a5" if mcz_sec == "D" else "#8e8e93")

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Выберите сектор":
                                size 13
                                color "#0a84ff"
                                bold True
                            text "Нажмите на самый\nопасный сектор карты":
                                size 12
                                color "#c7c7cc"
                                line_spacing 2

                # ═══════════════════════════════════════
                # 3. ML
                # ═══════════════════════════════════════

                # МЛ-1: ИНТЕРАКТИВНАЯ — клик по детекции нейросети
                elif task.id == "ml_1":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    # Кликабельная детекция: пластик (правильная)
                    button:
                        pos (400, 220)
                        xsize 260
                        ysize 300
                        background Frame(Solid("#34d39930"), 3, 3)
                        hover_background Frame(Solid("#34d39950"), 3, 3)
                        action Function(map_click_handle, "ml_1", "plastic_real")
                    frame:
                        pos (400, 188)
                        background Frame(Solid("#0a2e1af0"), 8, 8)
                        padding (8, 4)
                        text "plastic_bottle (0.94)":
                            size 11
                            color "#34d399"
                            bold True

                    # Кликабельная детекция: ещё мусор
                    button:
                        pos (700, 280)
                        xsize 280
                        ysize 260
                        background Frame(Solid("#34d39930"), 3, 3)
                        hover_background Frame(Solid("#34d39950"), 3, 3)
                        action Function(map_click_handle, "ml_1", "canister_real")
                    frame:
                        pos (700, 248)
                        background Frame(Solid("#0a2e1af0"), 8, 8)
                        padding (8, 4)
                        text "plastic_canister (0.88)":
                            size 11
                            color "#34d399"
                            bold True

                    # Ложное срабатывание: пена
                    button:
                        pos (260, 480)
                        xsize 200
                        ysize 150
                        background Frame(Solid("#ef444420"), 2, 2)
                        hover_background Frame(Solid("#ef444440"), 2, 2)
                        action Function(map_click_handle, "ml_1", "foam_false")
                    frame:
                        pos (260, 450)
                        background Frame(Solid("#3a1008f0"), 8, 8)
                        padding (6, 3)
                        text "foam (0.28 < 0.65) ✗":
                            size 10
                            color "#fca5a5"

                    $ mcz_ml = getattr(clean_state, "map_click_zone", None)
                    if mcz_ml == "plastic_real" or mcz_ml == "canister_real":
                        frame:
                            pos (20, 860)
                            background Frame(Solid("#0a2e1af0"), 12, 12)
                            padding (12, 8)
                            text "✓ Верная детекция! Conf > 0.65":
                                size 13
                                color "#34d399"
                                bold True
                    elif mcz_ml == "foam_false":
                        frame:
                            pos (20, 860)
                            background Frame(Solid("#3a1008f0"), 12, 12)
                            padding (12, 8)
                            text "✗ Это ложное срабатывание (пена)":
                                size 13
                                color "#fca5a5"
                                bold True

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "YOLOv8 Inference":
                                size 13
                                color "#34d399"
                                bold True
                            text "Нажмите на детекцию\nнейросети на снимке":
                                size 12
                                color "#c7c7cc"
                                line_spacing 2


                # МЛ-2: Разметка
                elif task.id == "ml_2":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    frame:
                        pos (360, 240)
                        xsize 560
                        ysize 440
                        background Frame(Solid("#34d39935"), 3, 3)
                    frame:
                        pos (360, 208)
                        background Frame(Solid("#0a2e1af0"), 8, 8)
                        padding (10, 5)
                        text "ghost_net (Плотный BBox)":
                            size 12
                            color "#34d399"
                            bold True

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Разметка CVAT":
                                size 13
                                color "#34d399"
                                bold True
                            text "Плотная рамка вокруг сети\nбез лишнего фона":
                                size 11
                                color "#c7c7cc"
                                line_spacing 2

                # МЛ-3: Метрики
                elif task.id == "ml_3":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    frame:
                        pos (460, 310)
                        xsize 380
                        ysize 300
                        background Frame(Solid("#34d39930"), 3, 3)
                    frame:
                        pos (460, 278)
                        background Frame(Solid("#0a2e1af0"), 8, 8)
                        padding (8, 4)
                        text "tire_waste (0.912)":
                            size 12
                            color "#34d399"
                            bold True

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Метрики модели":
                                size 13
                                color "#34d399"
                                bold True
                            text "Precision: 92.4%\nRecall: 71.2%\nmAP@0.5: 0.841":
                                size 11
                                color "#c7c7cc"
                                line_spacing 3

                # ═══════════════════════════════════════
                # 4. ЭКОЛОГ
                # ═══════════════════════════════════════

                # Эколог-1 — ИНТЕРАКТИВНАЯ: клик по бочке
                elif task.id == "ecologist_1":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    # Кликабельная бочка
                    button:
                        pos (400, 200)
                        xsize 480
                        ysize 420
                        background Solid("#00000000")
                        hover_background Solid("#ef444415")
                        action Function(map_click_handle, "ecologist_1", "barrel")

                    $ mcz_eco = getattr(clean_state, "map_click_zone", None)
                    if mcz_eco == "barrel":
                        add Solid("#ef444430"):
                            pos (400, 200)
                            xsize 480
                            ysize 420
                            at radar_pulse
                        frame:
                            pos (400, 168)
                            background Frame(Solid("#3a1008f0"), 8, 8)
                            padding (12, 6)
                            vbox:
                                spacing 2
                                text "☣ II–III класс опасности":
                                    size 14
                                    color "#fca5a5"
                                    bold True
                                text "ФККО: Отработанные масла":
                                    size 11
                                    color "#e5e5e7"

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Токсикология ФККО":
                                size 13
                                color "#ef4444"
                                bold True
                            text "Нажмите на опасный\nобъект для анализа":
                                size 12
                                color "#c7c7cc"
                                line_spacing 2


                # Эколог-2
                elif task.id == "ecologist_2":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    frame:
                        pos (380, 240)
                        xsize 560
                        ysize 420
                        background Frame(Solid("#ef444430"), 3, 3)

                    frame:
                        pos (380, 200)
                        background Frame(Solid("#3a1008f0"), 8, 8)
                        padding (12, 8)
                        vbox:
                            spacing 2
                            text "Ghost Fishing":
                                size 14
                                color "#fca5a5"
                                bold True
                            text "Кольчатая нерпа • Красная книга":
                                size 11
                                color "#e5e5e7"

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Призрачный промысел":
                                size 13
                                color "#ef4444"
                                bold True
                            text "Капрон не гниет 400+ лет\nСмертельная ловушка":
                                size 11
                                color "#c7c7cc"
                                line_spacing 2

                # Эколог-3
                elif task.id == "ecologist_3":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    frame:
                        pos (400, 240)
                        background Frame(Solid("#0a2e1af0"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 6
                            text "Биоремедиация":
                                size 14
                                color "#34d399"
                                bold True
                            text "1. Ручной сбор мазута\n2. Торфяной сорбент\n3. Посадка песколюбки":
                                size 12
                                color "#e5e5e7"
                                line_spacing 3

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Рекультивация дюн":
                                size 13
                                color "#34d399"
                                bold True
                            text "Бульдозеры запрещены\nТолько щадящие методы":
                                size 11
                                color "#c7c7cc"
                                line_spacing 2

                # ═══════════════════════════════════════
                # 5. БПЛА
                # ═══════════════════════════════════════

                # БПЛА-1 — ИНТЕРАКТИВНАЯ: клик по зоне полёта
                elif task.id == "uav_1":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    # Полетная сетка
                    button:
                        pos (300, 180)
                        xsize 700
                        ysize 450
                        background Solid("#0a84ff12")
                        hover_background Solid("#0a84ff25")
                        action Function(map_click_handle, "uav_1", "flight_grid")

                    $ mcz_uav = getattr(clean_state, "map_click_zone", None)
                    if mcz_uav == "flight_grid":
                        add Solid("#0a84ff20"):
                            pos (300, 180)
                            xsize 700
                            ysize 450
                            at radar_pulse
                        frame:
                            pos (300, 145)
                            background Frame(Solid("#0a1e3af0"), 8, 8)
                            padding (12, 6)
                            text "✓ Полетная сетка: 75% / 70% перекрытие":
                                size 13
                                color "#0a84ff"
                                bold True

                    frame:
                        pos (350, 240)
                        background Frame(Solid("#1c1c1eea"), 8, 8)
                        padding (10, 6)
                        text "WP1 → WP2 → WP3 → WP4\nWP8 ← WP7 ← WP6 ← WP5":
                            size 11
                            color "#93c5fd"
                            line_spacing 3

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Mission Planner":
                                size 13
                                color "#0a84ff"
                                bold True
                            text "Нажмите на зону полётной\nсетки для проверки":
                                size 12
                                color "#c7c7cc"
                                line_spacing 2


                # БПЛА-2: GSD
                elif task.id == "uav_2":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    frame:
                        pos (500, 300)
                        xsize 280
                        ysize 280
                        background Frame(Solid("#34d39925"), 2, 2)
                    frame:
                        pos (500, 268)
                        background Frame(Solid("#0a2e1af0"), 8, 8)
                        padding (10, 6)
                        text "GSD = 1.95 см/пикс":
                            size 12
                            color "#34d399"
                            bold True

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Телеметрия БПЛА":
                                size 13
                                color "#0a84ff"
                                bold True
                            text "Высота: 85м AGL\nСенсор: 24мм, 20МП":
                                size 11
                                color "#c7c7cc"
                                line_spacing 3

                # БПЛА-3: Метеоокно
                elif task.id == "uav_3":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    add Solid("#ef444425"):
                        pos (420, 220)
                        xsize 480
                        ysize 320
                        at radar_pulse

                    frame:
                        pos (420, 186)
                        background Frame(Solid("#3a1008f0"), 12, 12)
                        padding (14, 10)
                        vbox:
                            spacing 4
                            text "ВЫЛЕТ ОТЛОЖЕН":
                                size 16
                                color "#fca5a5"
                                bold True
                            text "Ветер 14.2 м/с (лимит 10 м/с)\nАКБ: 65% • Дальность: 2.8 км":
                                size 12
                                color "#e5e5e7"
                                line_spacing 2

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Предполётный чек-лист":
                                size 13
                                color "#ef4444"
                                bold True
                            text "Безопасность превыше всего\nЖдём улучшения погоды":
                                size 11
                                color "#c7c7cc"
                                line_spacing 2

                # ═══════════════════════════════════════
                # 6. КООРДИНАТОР
                # ═══════════════════════════════════════

                # Координатор-1 — ИНТЕРАКТИВНАЯ: клик по участкам берега
                elif task.id == "coordinator_1":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    # 4 кликабельных участка — бригады по 200м
                    button:
                        pos (80, 300)
                        xsize 260
                        ysize 350
                        background Solid("#00000000")
                        hover_background Solid("#c084fc15")
                        action Function(map_click_handle, "coord_1", "team_1")

                    button:
                        pos (360, 300)
                        xsize 260
                        ysize 350
                        background Solid("#00000000")
                        hover_background Solid("#c084fc15")
                        action Function(map_click_handle, "coord_1", "team_2")

                    button:
                        pos (640, 300)
                        xsize 260
                        ysize 350
                        background Solid("#00000000")
                        hover_background Solid("#c084fc15")
                        action Function(map_click_handle, "coord_1", "team_3")

                    button:
                        pos (920, 300)
                        xsize 260
                        ysize 350
                        background Solid("#00000000")
                        hover_background Solid("#c084fc15")
                        action Function(map_click_handle, "coord_1", "team_4")

                    $ mcz_co = getattr(clean_state, "map_click_zone", None)
                    if mcz_co and mcz_co.startswith("team_"):
                        $ team_n = mcz_co.replace("team_", "")
                        frame:
                            pos (400, 250)
                            background Frame(Solid("#2d1854f0"), 12, 12)
                            padding (16, 12)
                            vbox:
                                spacing 4
                                text "Бригада " + team_n + " • 200м берега":
                                    size 14
                                    color "#c084fc"
                                    bold True
                                text "4-5 волонтеров • 25 мешков\nПерчатки • Аптечка • Вода":
                                    size 12
                                    color "#e5e5e7"
                                    line_spacing 2

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Тактическая карта":
                                size 13
                                color "#c084fc"
                                bold True
                            text "Нажмите на участок\nдля распределения бригады":
                                size 12
                                color "#c7c7cc"
                                line_spacing 2


                # Координатор-2
                elif task.id == "coordinator_2":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    frame:
                        pos (420, 260)
                        background Frame(Solid("#1c1c1ef0"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 6
                            text "Сигнал #148":
                                size 14
                                color "#0a84ff"
                                bold True
                            text "Аноним: «Нашёл страшный мусор»\nСтатус: Требует проверки\nДействие: Запрос геоточки":
                                size 12
                                color "#e5e5e7"
                                line_spacing 3

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Модерация Citizen Science":
                                size 13
                                color "#c084fc"
                                bold True
                            text "Верифицируем сигнал\nперед выездом бригады":
                                size 11
                                color "#c7c7cc"
                                line_spacing 2

                # Координатор-3
                elif task.id == "coordinator_3":
                    frame:
                        xsize 1280
                        ysize 910
                        xalign 0.5
                        yalign 0.5
                        padding (0, 0)
                        background Solid("#050c17")
                        if task.image:
                            add im.Scale(task.image, 1280, 910)

                    frame:
                        pos (380, 240)
                        background Frame(Solid("#0a2e1af0"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 6
                            text "Zero Waste":
                                size 15
                                color "#34d399"
                                bold True
                            text "ПЭТ → Грануляция\nАлюминий → Переплавка\nШины → Пиролиз\nБатарейки → Демеркуризация":
                                size 12
                                color "#e5e5e7"
                                line_spacing 3

                    frame:
                        pos (20, 20)
                        background Frame(Solid("#1c1c1eea"), 12, 12)
                        padding (16, 12)
                        vbox:
                            spacing 4
                            text "Логистика переработки":
                                size 13
                                color "#34d399"
                                bold True
                            text "100% рециклинг\nНичего на свалку":
                                size 11
                                color "#c7c7cc"
                                line_spacing 2

                # Запасной
                else:
                    if task.image:
                        add task.image:
                            xalign 0.5
                            yalign 0.5
                            zoom 1.05

## ─────────────────────────────────────────────────────────
## МОДАЛЬНЫЙ ГИД (Apple-style)
## ─────────────────────────────────────────────────────────
screen mission_tutorial_modal():
    modal True
    tag clean_modal

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 860
        background Frame(Solid("#1c1c1e"), 20, 20)
        padding (32, 28)

        vbox:
            spacing 20
            xalign 0.5

            # Заголовок
            vbox:
                spacing 4
                xalign 0.5
                text "Как проходить миссию":
                    size 24
                    color "#ffffff"
                    bold True
                    xalign 0.5
                text "Краткий гид по интерфейсу":
                    size 14
                    color "#8e8e93"
                    xalign 0.5

            frame:
                background Solid("#3a3a3c")
                xfill True
                ysize 1

            # Карточки 2x2
            grid 2 2:
                spacing 14
                xalign 0.5

                frame:
                    xsize 390
                    yminimum 130
                    background Frame(Solid("#2c2c2e"), 12, 12)
                    padding (16, 14)
                    vbox:
                        spacing 6
                        text "1. Прочитай задание":
                            size 14
                            color "#0a84ff"
                            bold True
                        text "Слева описана ситуация и цель.\nИзучи контекст перед ответом.":
                            size 12
                            color "#c7c7cc"
                            line_spacing 3

                frame:
                    xsize 390
                    yminimum 130
                    background Frame(Solid("#2c2c2e"), 12, 12)
                    padding (16, 14)
                    vbox:
                        spacing 6
                        text "2. Изучи визуализацию":
                            size 14
                            color "#34d399"
                            bold True
                        text "Справа — снимки, карты и данные.\nНажимай на интерактивные области.":
                            size 12
                            color "#c7c7cc"
                            line_spacing 3

                frame:
                    xsize 390
                    yminimum 130
                    background Frame(Solid("#2c2c2e"), 12, 12)
                    padding (16, 14)
                    vbox:
                        spacing 6
                        text "3. Выбери ответ":
                            size 14
                            color "#f59e0b"
                            bold True
                        text "Внизу слева — варианты ответа.\nВыбери и нажми «Проверить».":
                            size 12
                            color "#c7c7cc"
                            line_spacing 3

                frame:
                    xsize 390
                    yminimum 130
                    background Frame(Solid("#2c2c2e"), 12, 12)
                    padding (16, 14)
                    vbox:
                        spacing 6
                        text "4. Переключай миссии":
                            size 14
                            color "#c084fc"
                            bold True
                        text "Вверху — кнопки 1, 2, 3 для\nпереключения между задачами.":
                            size 12
                            color "#c7c7cc"
                            line_spacing 3

            # Кнопка старта
            button:
                xalign 0.5
                xsize 340
                ysize 50
                background Frame(Solid("#0a84ff"), 14, 14)
                hover_background Frame(Solid("#0070e0"), 14, 14)
                padding (16, 10)
                action [SetField(clean_state, "mission_guide_shown", True), Hide("mission_tutorial_modal")]

                text "Понятно, начать!":
                    size 16
                    color "#ffffff"
                    bold True
                    xalign 0.5
                    yalign 0.5
