## clean_gis_game.rpy
## Интерактивный симулятор ДЗЗ и ГИС-анализа побережья

init python:
    def gis_handle_image_click():
        mx, my = renpy.get_mouse_pos()
        # Положение снимка на экране: x=320, y=100
        img_x = 320
        img_y = 100
        zoom = clean_state.gis_mgr.zoom_level
        lx = int((mx - img_x) / zoom)
        ly = int((my - img_y) / zoom)
        lx = max(0, min(1280, lx))
        ly = max(0, min(720, ly))
        clean_state.gis_mgr.last_click = (lx, ly)
        renpy.restart_interaction()

    def gis_proceed_next():
        clean_state.gis_mgr.next_task()
        if clean_state.gis_mgr.game_finished:
            renpy.show_screen("gis_result_screen")
        else:
            renpy.show_screen("gis_play_screen")
        renpy.restart_interaction()

    def gis_confirm_selection():
        if clean_state.gis_mgr.last_click:
            lx, ly = clean_state.gis_mgr.last_click
            clean_state.gis_mgr.register_click(lx, ly)
            clean_state.unlock_achievement("ach_scout")
            renpy.restart_interaction()

    def gis_select_zone(zone_letter):
        clean_state.gis_mgr.selected_zone = zone_letter
        if zone_letter == "A":
            clean_state.gis_mgr.last_click = (320, 180)
        elif zone_letter == "B":
            clean_state.gis_mgr.last_click = (1050, 160)
        elif zone_letter == "C":
            clean_state.gis_mgr.last_click = (320, 540)
        elif zone_letter == "D":
            clean_state.gis_mgr.last_click = (960, 540)
        renpy.restart_interaction()

## ЭКРАН 1: СТАРТОВЫЙ БРИФИНГ
screen gis_briefing_screen():
    tag clean_screen
    add Solid("#070f1e")
    
    use clean_top_bar(active_tab="gis")

    $ cur_spec = clean_state.active_specialty

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1060
        ysize 670
        background Frame(Solid("#0e1e38"), 14, 14)
        padding (36, 26)

        vbox:
            spacing 14
            xalign 0.5
            yalign 0.5

            # ШАПКА БРИФИНГА: АДАПТИРУЕТСЯ ПОД ВЫБРАННУЮ РОЛЬ
            hbox:
                spacing 18
                xalign 0.5
                yalign 0.5
                frame:
                    background Frame(Solid("#081426"), 8, 8)
                    padding (14, 12)
                    text "[cur_spec.icon]":
                        size 38
                        yalign 0.5
                vbox:
                    spacing 2
                    frame:
                        background Frame("images/ui/rounded/pill_chip.png", 18, 18)
                        padding (12, 4)
                        text "ИНСТРУКТАЖ СПЕЦИАЛИСТА: [cur_spec.name]":
                            size 11
                            color "#00e6b8"
                            bold True
                    text "Добро пожаловать в систему экомониторинга!":
                        size 23
                        color "#ffffff"
                        bold True
                    text "[cur_spec.role_desc]":
                        size 13
                        color "#94a3b8"

            # ПЛАШКА ЗАКРЕПЛЕННОГО ИНСТРУМЕНТА РОЛИ
            frame:
                background Solid("#08152b")
                padding (16, 10)
                xfill True
                hbox:
                    spacing 14
                    yalign 0.5
                    text "⚡":
                        size 20
                        yalign 0.5
                    vbox:
                        spacing 2
                        text "Ваш рабочий инструмент роли: «[cur_spec.tool_name]»":
                            size 13
                            color "#f59e0b"
                            bold True
                        text "[cur_spec.tool_desc]":
                            size 11
                            color "#cbd5e1"
                    null width 10
                    textbutton "Сменить роль":
                        text_size 12
                        text_color "#38bdf8"
                        background Frame(Solid("#132847"), 4, 4)
                        hover_background Frame(Solid("#1e40af"), 4, 4)
                        xpadding 12
                        ypadding 6
                        yalign 0.5
                        action Show("role_selection_entry_screen")

            # ДВА ПОНЯТНЫХ НАПРАВЛЕНИЯ РАБОТЫ (КАРТОЧКИ ВЫБОРА)
            hbox:
                spacing 16
                xalign 0.5

                # КАРТОЧКА 1: ТРЕНАЖЕР СНИМКОВ ПОБЕРЕЖЬЯ
                frame:
                    xsize 480
                    ysize 255
                    background Frame(Solid("#09162a"), 10, 10)
                    padding (20, 16)
                    vbox:
                        spacing 8
                        hbox:
                            spacing 10
                            text "🛰️":
                                size 22
                            vbox:
                                text "ТРЕНАЖЕР СНИМКОВ (3 УРОВНЯ)":
                                    size 14
                                    color "#38bdf8"
                                    bold True
                                text "Поиск загрязнений на карте побережья":
                                    size 11
                                    color "#64748b"

                        text "Исследуйте спутниковые снимки, найдите подозрительное пятно кликом мыши и проверьте точность с помощью вашего инструмента («[cur_spec.short_title]»).":
                            size 12
                            color "#cbd5e1"
                            line_spacing 3

                        frame:
                            background Solid("#06101e")
                            padding (8, 5)
                            xfill True
                            text "🎯 Инструмент роли встроен в интерфейс тренажера":
                                size 10
                                color "#00e6b8"

                        null height 2

                        textbutton "Начать в тренажере снимков →":
                            text_size 14
                            text_bold True
                            text_color "#041122"
                            xfill True
                            background Frame(Solid("#00e6b8"), 6, 6)
                            hover_background Frame(Solid("#38bdf8"), 6, 6)
                            ypadding 10
                            action [Function(clean_state.gis_mgr.start_game), Show("gis_play_screen")]

                # КАРТОЧКА 2: ПРАКТИЧЕСКИЕ ЗАДАЧИ РОЛИ
                frame:
                    xsize 480
                    ysize 255
                    background Frame(Solid("#09162a"), 10, 10)
                    padding (20, 16)
                    vbox:
                        spacing 8
                        hbox:
                            spacing 10
                            text "[cur_spec.icon]":
                                size 22
                            vbox:
                                text "МИССИИ СПЕЦИАЛЬНОСТИ ([cur_spec.short_title])":
                                    size 14
                                    color "#00e6b8"
                                    bold True
                                text "3 профессиональных кейса с теорией":
                                    size 11
                                    color "#64748b"

                        text "[cur_spec.tasks_desc]":
                            size 11
                            color "#cbd5e1"
                            line_spacing 2

                        frame:
                            background Solid("#06101e")
                            padding (8, 5)
                            xfill True
                            text "🏆 Награда: до 950 XP за выполнение всех кейсов":
                                size 10
                                color "#86efac"

                        null height 2

                        textbutton "Решать задачи специальности →":
                            text_size 14
                            text_bold True
                            text_color "#ffffff"
                            xfill True
                            background Frame(Solid("#1e40af"), 6, 6)
                            hover_background Frame(Solid("#2563eb"), 6, 6)
                            ypadding 10
                            action [Function(clean_state.set_specialty, cur_spec.id), Show("clean_role_mission_screen")]

            # НИЖНЯЯ ССЫЛКА НАВИГАЦИИ
            textbutton "← Вернуться к выбору специальности":
                text_size 12
                text_color "#94a3b8"
                text_hover_color "#38bdf8"
                xalign 0.5
                action Show("role_selection_entry_screen")

## ЭКРАН 2: ИНТЕРАКТИВНЫЙ СНИМОК И ВЫБОР ОБЛАСТИ
screen gis_play_screen():
    tag clean_screen
    add Solid("#070f1e")

    $ current_task = clean_state.gis_mgr.get_current_task()
    $ zoom = clean_state.gis_mgr.zoom_level

    use clean_top_bar(active_tab="gis")

    # ЛЕВАЯ ПАНЕЛЬ: ЗАДАНИЕ И ИНСТРУМЕНТЫ (300px)
    frame:
        xpos 25
        ypos 100
        xsize 280
        ysize 880
        background Frame(Solid("#0c1a30"), 10, 10)
        padding (20, 20)

        vbox:
            spacing 15

            # Заголовок уровня
            text "[current_task.title]":
                size 20
                color "#38bdf8"
                bold True

            # Сложность и координаты
            hbox:
                spacing 8
                frame:
                    background Solid("#1e293b")
                    padding (8, 4)
                    text "[current_task.difficulty]":
                        size 13
                        color "#f59e0b"
                        bold True
                $ cur_lvl_num = clean_state.gis_mgr.current_index + 1
                frame:
                    background Solid("#1e293b")
                    padding (8, 4)
                    text "Уровень [cur_lvl_num] из 3":
                        size 13
                        color "#94a3b8"

            null height 5

            # Координаты снимка
            vbox:
                spacing 2
                text "Координаты центра:":
                    size 13
                    color "#64748b"
                text "[current_task.coordinates]":
                    size 14
                    color "#00e6b8"
                    bold True

            # Описание задачи
            text "[current_task.description]":
                size 15
                color "#cbd5e1"
                line_spacing 4

            null height 10

            # ПАНЕЛЬ УПРАВЛЕНИЯ В ЗАВИСИМОСТИ ОТ УРОВНЯ
            if current_task.level_type == 2:
                # Режим сравнения снимков
                text "ВРЕМЕННОЙ АНАЛИЗ:":
                    size 13
                    color "#f59e0b"
                    bold True
                hbox:
                    spacing 8
                    textbutton "ДО":
                        text_size 14
                        text_bold True
                        background Frame(Solid("#22c55e" if clean_state.gis_mgr.view_mode == "BEFORE" else "#1e293b"), 6, 6)
                        xpadding 20
                        ypadding 8
                        action [SetField(clean_state.gis_mgr, "view_mode", "BEFORE")]
                    textbutton "ПОСЛЕ (Текущий)":
                        text_size 14
                        text_bold True
                        background Frame(Solid("#ef4444" if clean_state.gis_mgr.view_mode == "AFTER" else "#1e293b"), 6, 6)
                        xpadding 20
                        ypadding 8
                        action [SetField(clean_state.gis_mgr, "view_mode", "AFTER")]

            elif current_task.level_type == 3:
                # Режим мульти-сектора
                text "ВЫБОР КРИТИЧЕСКОГО СЕКТОРА:":
                    size 13
                    color "#f59e0b"
                    bold True
                grid 2 2:
                    spacing 6
                    textbutton "Сектор A":
                        text_size 14
                        background Frame(Solid("#00e6b8" if clean_state.gis_mgr.selected_zone == "A" else "#1e293b"), 4, 4)
                        xpadding 15
                        ypadding 8
                        action Function(gis_select_zone, "A")
                    textbutton "Сектор B":
                        text_size 14
                        background Frame(Solid("#00e6b8" if clean_state.gis_mgr.selected_zone == "B" else "#1e293b"), 4, 4)
                        xpadding 15
                        ypadding 8
                        action Function(gis_select_zone, "B")
                    textbutton "Сектор C":
                        text_size 14
                        background Frame(Solid("#00e6b8" if clean_state.gis_mgr.selected_zone == "C" else "#1e293b"), 4, 4)
                        xpadding 15
                        ypadding 8
                        action Function(gis_select_zone, "C")
                    textbutton "Сектор D":
                        text_size 14
                        background Frame(Solid("#00e6b8" if clean_state.gis_mgr.selected_zone == "D" else "#1e293b"), 4, 4)
                        xpadding 15
                        ypadding 8
                        action Function(gis_select_zone, "D")

            null height 10

            # МАСШТАБИРОВАНИЕ
            text "МАСШТАБ (ZOOM):":
                size 13
                color "#64748b"
                bold True
            hbox:
                spacing 6
                textbutton "1.0x":
                    text_size 13
                    background Frame(Solid("#00e6b8" if zoom == 1.0 else "#1e293b"), 4, 4)
                    xpadding 12
                    ypadding 6
                    action [SetField(clean_state.gis_mgr, "zoom_level", 1.0)]
                textbutton "1.5x":
                    text_size 13
                    background Frame(Solid("#00e6b8" if zoom == 1.5 else "#1e293b"), 4, 4)
                    xpadding 12
                    ypadding 6
                    action [SetField(clean_state.gis_mgr, "zoom_level", 1.5)]
                textbutton "2.0x":
                    text_size 13
                    background Frame(Solid("#00e6b8" if zoom == 2.0 else "#1e293b"), 4, 4)
                    xpadding 12
                    ypadding 6
                    action [SetField(clean_state.gis_mgr, "zoom_level", 2.0)]

            null height 10

            # ИНСТРУМЕНТ СПЕЦИАЛЬНОСТИ
            $ cur_spec = clean_state.active_specialty
            vbox:
                spacing 3
                text "[cur_spec.icon] ИНСТРУМЕНТ [cur_spec.short_title]:":
                    size 12
                    color "#00e6b8"
                    bold True
                textbutton ("[cur_spec.icon] " + ("Отключить" if clean_state.specialty_tool_active else "Активировать")):
                    text_size 12
                    text_bold True
                    text_color "#ffffff"
                    background Frame(Solid("#166534" if clean_state.specialty_tool_active else "#1e293b"), 4, 4)
                    hover_background Frame(Solid("#00e6b8"), 4, 4)
                    xfill True
                    ypadding 6
                    action Function(clean_state.toggle_specialty_tool)
                text "[cur_spec.tool_name]":
                    size 11
                    color "#94a3b8"

                textbutton "🎯 Миссии роли ([cur_spec.short_title]) →":
                    text_size 11
                    text_bold True
                    text_color "#38bdf8"
                    background Frame(Solid("#102647"), 4, 4)
                    hover_background Frame(Solid("#1e40af"), 4, 4)
                    xfill True
                    ypadding 5
                    action [Function(clean_state.set_specialty, cur_spec.id), Show("clean_role_mission_screen")]

            null height 10

            # КНОПКА ОСНОВНОГО ДЕЙСТВИЯ (ШАГИ 1 -> 2 -> 3)
            if clean_state.gis_mgr.last_result is None:
                if clean_state.gis_mgr.last_click is not None:
                    textbutton "✔ Подтвердить выбор":
                        text_size 16
                        text_bold True
                        text_color "#041122"
                        background Frame(Solid("#00e6b8"), 8, 8)
                        hover_background Frame(Solid("#38bdf8"), 8, 8)
                        xfill True
                        ypadding 13
                        action Function(gis_confirm_selection)
                else:
                    frame:
                        background Solid("#101c30")
                        xfill True
                        padding (10, 12)
                        text "1️⃣ Сначала кликните по карте":
                            size 12
                            color "#94a3b8"
                            text_align 0.5
                            xalign 0.5
            else:
                # Результат уже получен
                $ next_lvl_num = cur_lvl_num + 1
                if next_lvl_num <= 3:
                    textbutton "Следующий снимок (Уровень [next_lvl_num]) →":
                        text_size 14
                        text_bold True
                        text_color "#ffffff"
                        background Frame(Solid("#16a34a"), 8, 8)
                        hover_background Frame(Solid("#22c55e"), 8, 8)
                        xfill True
                        ypadding 13
                        action Function(gis_proceed_next)
                else:
                    textbutton "Завершить и итоги →":
                        text_size 15
                        text_bold True
                        text_color "#ffffff"
                        background Frame(Solid("#16a34a"), 8, 8)
                        hover_background Frame(Solid("#22c55e"), 8, 8)
                        xfill True
                        ypadding 13
                        action Function(gis_proceed_next)

            null height 15
            # Текущие очки
            hbox:
                spacing 10
                text "Счет:":
                    size 16
                    color "#94a3b8"
                text "[clean_state.gis_mgr.player_points] XP":
                    size 18
                    color "#00e6b8"
                    bold True

    # ЦЕНТРАЛЬНО-ПРАВАЯ ОБЛАСТЬ: СНИМОК И ИНТЕРАКТИВНОЕ ПОЛЕ (1280x720)
    # Позиция: x=320, y=100
    frame:
        xpos 320
        ypos 100
        xsize 1280
        ysize 720
        background Solid("#000000")
        padding (0, 0)

        # 1. Сам снимок
        if current_task.level_type == 2 and clean_state.gis_mgr.view_mode == "BEFORE":
            add current_task.image:
                fit "cover"
                zoom zoom
        elif current_task.level_type == 2 and clean_state.gis_mgr.view_mode == "AFTER":
            add current_task.image_after:
                fit "cover"
                zoom zoom
        else:
            add current_task.image:
                fit "cover"
                zoom zoom

        # 2. Невидимая интерактивная кнопка клика поверх снимка
        if clean_state.gis_mgr.last_result is None:
            button:
                xfill True
                yfill True
                background Solid("#00000001")
                focus_mask None
                action Function(gis_handle_image_click)

        # 3. Маркер клика игрока
        if clean_state.gis_mgr.last_click is not None:
            $ clk_x = int(clean_state.gis_mgr.last_click[0] * zoom)
            $ clk_y = int(clean_state.gis_mgr.last_click[1] * zoom)
            # Перекрестие
            add Solid("#38bdf8"):
                pos (clk_x - 18, clk_y - 2)
                xsize 36
                ysize 4
            add Solid("#38bdf8"):
                pos (clk_x - 2, clk_y - 18)
                xsize 4
                ysize 36
            # Пульсирующий маркер
            add Solid("#00e6b840"):
                pos (clk_x - 22, clk_y - 22)
                xsize 44
                ysize 44
                at radar_pulse

        # 4. Если результат получен: показываем истинную область поражения
        if clean_state.gis_mgr.last_result is not None:
            $ tgt_x = int(current_task.target_x * zoom)
            $ tgt_y = int(current_task.target_y * zoom)
            $ rad = int(current_task.hit_radius * zoom)

            # Контур истинного загрязнения
            add Solid("#22c55e50"):
                pos (tgt_x - rad, tgt_y - rad)
                xsize (rad * 2)
                ysize (rad * 2)
                at radar_pulse

            # Подпись к области
            frame:
                pos (tgt_x - 80, tgt_y + rad + 10)
                background Solid("#0f172ae0")
                padding (8, 4)
                text "ОЧАГ ЗАГРЯЗНЕНИЯ":
                    size 12
        # 5. Оверлей специального инструмента роли
        if clean_state.specialty_tool_active:
            $ t_x = int(current_task.target_x * zoom)
            $ t_y = int(current_task.target_y * zoom)

            if clean_state.active_specialty.id == "ml":
                # ML / AI Bounding Box
                frame:
                    pos (t_x - 70, t_y - 70)
                    xsize 140
                    ysize 140
                    background Frame(Solid("#22c55e40"), 2, 2)
                    padding (0, 0)
                frame:
                    pos (t_x - 70, t_y - 95)
                    background Solid("#15803df0")
                    padding (6, 2)
                    text "🧠 YOLOv8: Marine Debris (94.2%)":
                        size 11
                        color "#ffffff"
                        bold True

            elif clean_state.active_specialty.id == "gis":
                # GIS буферная зона
                add Solid("#f59e0b25"):
                    pos (t_x - 110, t_y - 110)
                    xsize 220
                    ysize 220
                    at radar_pulse
                frame:
                    pos (t_x - 110, t_y - 135)
                    background Solid("#091426ea")
                    padding (6, 2)
                    text "🗺️ GIS: Буфер R=250м • Площадь ~1.4 га":
                        size 11
                        color "#f59e0b"
                        bold True

            elif clean_state.active_specialty.id == "dzz":
                # Спектральный фильтр NDWI
                add Solid("#00e6b830"):
                    pos (t_x - 80, t_y - 80)
                    xsize 160
                    ysize 160
                    at radar_pulse
                frame:
                    pos (t_x - 80, t_y - 105)
                    background Solid("#091426ea")
                    padding (6, 2)
                    text "🛰️ NDWI: Аномалия спектра в ИК":
                        size 11
                        color "#00e6b8"
                        bold True

            elif clean_state.active_specialty.id == "ecologist":
                # Экологический паспорт риска
                frame:
                    pos (t_x - 90, t_y - 115)
                    background Solid("#7f1d1dea")
                    padding (8, 4)
                    text "🌿 ЭКО-РИСК: IV класс • Угроза фауне":
                        size 11
                        color "#fca5a5"
                        bold True

            elif clean_state.active_specialty.id == "uav":
                # БПЛА ортофото режим
                frame:
                    pos (t_x - 90, t_y - 115)
                    background Solid("#0284c7ea")
                    padding (8, 4)
                    text "🚁 БПЛА GSD: 2.1 см/пикс • Высота 120м":
                        size 11
                        color "#bae6fd"
                        bold True

            elif clean_state.active_specialty.id == "volunteer_coord":
                # Наряд волонтерам
                frame:
                    pos (t_x - 90, t_y - 115)
                    background Solid("#6b21a8ea")
                    padding (8, 4)
                    text "🤝 Наряд №14: Группа 6 чел. готова":
                        size 11
                        color "#e9d5ff"
                        bold True

        # Верхний динамический гид-инструкция прямо на снимке
        if clean_state.gis_mgr.last_result is None:
            if clean_state.gis_mgr.last_click is None:
                frame:
                    pos (15, 15)
                    background Solid("#071224e8")
                    padding (14, 8)
                    hbox:
                        spacing 8
                        yalign 0.5
                        text "👆":
                            size 16
                            yalign 0.5
                        text "ШАГ 1: Кликните мышью по подозрительному участку на снимке":
                            size 13
                            color "#38bdf8"
                            bold True
            else:
                $ cur_clk_x = clean_state.gis_mgr.last_click[0]
                $ cur_clk_y = clean_state.gis_mgr.last_click[1]
                frame:
                    pos (15, 15)
                    background Solid("#064e3be8")
                    padding (14, 8)
                    hbox:
                        spacing 8
                        yalign 0.5
                        text "📍":
                            size 16
                            yalign 0.5
                        text "ТОЧКА ВЫБРАНА (X=[cur_clk_x], Y=[cur_clk_y]) ➔ ШАГ 2: Нажмите «Подтвердить выбор» слева":
                            size 13
                            color "#86efac"
                            bold True
        else:
            frame:
                pos (15, 15)
                background Solid("#0c2340e8")
                padding (14, 8)
                hbox:
                    spacing 8
                    yalign 0.5
                    text "✔":
                        size 16
                        color "#00e6b8"
                        yalign 0.5
                    text "АНАЛИЗ ЗАВЕРШЕН. Ознакомьтесь с отчетом внизу и перейдите к следующему заданию":
                        size 13
                        color "#ffffff"
                        bold True

        if clean_state.gis_mgr.last_click is not None:
            $ cur_clk_x = clean_state.gis_mgr.last_click[0]
            $ cur_clk_y = clean_state.gis_mgr.last_click[1]
            frame:
                xpos 15
                ypos 665
                background Solid("#091426cc")
                padding (10, 6)
                text "КУРСОР: X=[cur_clk_x] Y=[cur_clk_y]":
                    size 12
                    color "#00e6b8"

    # НИЖНЯЯ ПАНЕЛЬ: РЕЗУЛЬТАТ И КРАТКОЕ ОБЪЯСНЕНИЕ (ЭТАП 4 и 5)
    if clean_state.gis_mgr.last_result is not None:
        frame:
            xpos 320
            ypos 835
            xsize 1280
            ysize 145
            background Frame(Solid("#0e1e38"), 10, 10)
            padding (25, 18)
            at slide_down

            hbox:
                spacing 25
                yalign 0.5

                # Статус: Попал / почти / мимо
                if clean_state.gis_mgr.last_result == "HIT":
                    frame:
                        background Solid("#15803d")
                        padding (18, 12)
                        text "🎯 ПОПАЛ!":
                            size 24
                            color "#ffffff"
                            bold True
                elif clean_state.gis_mgr.last_result == "CLOSE":
                    frame:
                        background Solid("#d97706")
                        padding (18, 12)
                        text "⚠️ ПОЧТИ!":
                            size 24
                            color "#ffffff"
                            bold True
                else:
                    frame:
                        background Solid("#b91c1c")
                        padding (18, 12)
                        text "❌ МИМО!":
                            size 24
                            color "#ffffff"
                            bold True

                # Очки и фидбек
                vbox:
                    spacing 4
                    hbox:
                        spacing 12
                        text "+[clean_state.gis_mgr.last_score_gain] очков":
                            size 20
                            color "#00e6b8"
                            bold True
                        text "| [clean_state.gis_mgr.last_feedback]":
                            size 16
                            color "#e2e8f0"

                    # Короткое объяснение (ЭТАП 5: «Так специалисты ДЗЗ ищут изменения на больших территориях. И всё. Не превращать это в урок.»)
                    text "«[current_task.brief_explanation]»":
                        size 17
                        color "#38bdf8"
                        bold True

    # ПРАВАЯ ПАНЕЛЬ: ПОДСКАЗКИ И СПРАВКА (280px)
    frame:
        xpos 1615
        ypos 100
        xsize 280
        ysize 880
        background Frame(Solid("#0c1a30"), 10, 10)
        padding (18, 18)

        vbox:
            spacing 14

            # Заголовок блока подсказок
            hbox:
                spacing 8
                text "💡":
                    size 18
                text "КАК РАБОТАТЬ":
                    size 14
                    color "#00e6b8"
                    bold True

            # Пошаговая инструкция
            frame:
                background Solid("#071224")
                padding (12, 10)
                xfill True
                vbox:
                    spacing 8
                    text "1️⃣ Осмотрите снимок в поисках темных пятен нефтепродуктов или скоплений мусора.":
                        size 11
                        color "#cbd5e1"
                        line_spacing 2
                    text "2️⃣ Кликните мышью по аномальной точке (появится синий маркер).":
                        size 11
                        color "#cbd5e1"
                        line_spacing 2
                    text "3️⃣ Нажмите «Подтвердить выбор» на панели слева для проверки.":
                        size 11
                        color "#cbd5e1"
                        line_spacing 2

            # Блок инструмента роли
            vbox:
                spacing 4
                text "ИНСТРУМЕНТ РОЛИ:":
                    size 12
                    color "#f59e0b"
                    bold True
                frame:
                    background Solid("#071224")
                    padding (12, 10)
                    xfill True
                    vbox:
                        spacing 5
                        text "[cur_spec.icon] [cur_spec.tool_name]":
                            size 11
                            color "#38bdf8"
                            bold True
                        text "[cur_spec.tool_desc]":
                            size 10
                            color "#94a3b8"
                            line_spacing 2

            # Легенда обозначений на снимке
            vbox:
                spacing 6
                text "ЛЕГЕНДА СНИМКА:":
                    size 12
                    color "#94a3b8"
                    bold True
                hbox:
                    spacing 8
                    add Solid("#38bdf8"):
                        xsize 12
                        ysize 12
                        yalign 0.5
                    text "Ваша точка выбора":
                        size 11
                        color "#cbd5e1"
                hbox:
                    spacing 8
                    add Solid("#22c55e"):
                        xsize 12
                        ysize 12
                        yalign 0.5
                    text "Истинный очаг угрозы":
                        size 11
                        color "#cbd5e1"
                hbox:
                    spacing 8
                    add Solid("#f59e0b"):
                        xsize 12
                        ysize 12
                        yalign 0.5
                    text "Зона инструмента роли":
                        size 11
                        color "#cbd5e1"

            null height 6

            # Быстрый переход к миссиям роли
            textbutton "🎯 Миссии роли ([cur_spec.short_title]) →":
                text_size 11
                text_bold True
                text_color "#ffffff"
                background Frame(Solid("#1e40af"), 6, 6)
                hover_background Frame(Solid("#2563eb"), 6, 6)
                xfill True
                ypadding 10
                action [Function(clean_state.set_specialty, cur_spec.id), Show("clean_role_mission_screen")]

            textbutton "👥 Сменить профессию":
                text_size 11
                text_color "#94a3b8"
                text_hover_color "#38bdf8"
                xalign 0.5
                action Show("role_selection_entry_screen")

## ЭКРАН 3: ФИНАЛЬНЫЙ РЕЗУЛЬТАТ (ЭТАП 7)
screen gis_result_screen():
    tag clean_screen
    add Solid("#070f1e")
    use clean_top_bar(active_tab="gis")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 980
        ysize 640
        background Frame(Solid("#0e1e38"), 12, 12)
        padding (50, 45)
        at slide_down

        vbox:
            spacing 25
            xalign 0.5

            # Заголовок
            text "ИТОГИ ДЗЗ-МОНИТОРИНГА":
                size 30
                color "#00e6b8"
                bold True
                xalign 0.5

            # Результат пользователя (Этап 7: «Ты обнаружил 8 из 10 проблемных участков»)
            frame:
                background Solid("#091426")
                padding (30, 25)
                xfill True
                vbox:
                    spacing 15
                    xalign 0.5
                    $ hits_estimate = int(clean_state.gis_mgr.hits_count * 3)
                    text "Ты обнаружил [hits_estimate] из 10 проблемных участков на побережье.":
                        size 24
                        color "#ffffff"
                        bold True
                        xalign 0.5
                    text "Набрано очков: [clean_state.gis_mgr.player_points] XP  •  Время: [clean_state.gis_mgr.total_time_str]":
                        size 18
                        color "#38bdf8"
                        xalign 0.5

            # Ключевой посыл проекта
            frame:
                background Solid("#132644")
                padding (25, 20)
                xfill True
                vbox:
                    spacing 10
                    text "«Этим занимаются специалисты ДЗЗ и GIS в “Чистом береге”.»":
                        size 22
                        color "#f59e0b"
                        bold True
                        xalign 0.5
                    text "Данные космических спутников и БПЛА объединяются с полевыми наблюдениями волонтеров для оперативного реагирования и защиты природных территорий.":
                        size 16
                        color "#cbd5e1"
                        text_align 0.5

            null height 10

            # Кнопки действий: CTA (Этап 7: «Посмотреть, как это работает →») и Рейтинг
            hbox:
                spacing 25
                xalign 0.5
                textbutton "Посмотреть рейтинг (Топ-10%) 🏆":
                    text_size 18
                    text_bold True
                    text_color "#ffffff"
                    background Frame(Solid("#1e293b"), 8, 8)
                    hover_background Frame(Solid("#334155"), 8, 8)
                    xpadding 30
                    ypadding 14
                    action Show("clean_leaderboard_screen")

                textbutton "Посмотреть, как это работает →":
                    text_size 20
                    text_bold True
                    text_color "#070f1e"
                    background Frame(Solid("#00e6b8"), 8, 8)
                    hover_background Frame(Solid("#38bdf8"), 8, 8)
                    xpadding 40
                    ypadding 14
                    action Show("challenge_catalog_screen")
