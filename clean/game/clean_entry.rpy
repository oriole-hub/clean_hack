## clean_entry.rpy
## Стартовый экран выбора профессии исследователя при входе в «Чистый берег»
## Интуитивный интерфейс: выбор роли -> краткая сводка -> боевые задачи без права на ошибку

init python:
    # Визуальные метаданные для каждой из 6 ролей (используются оптимизированные превью 294x132)
    role_visual_data = {
        "dzz": {
            "image": "images/ui/cards/card_dzz.png",
            "tag1": "🛰️ Sentinel-2",
            "tag2": "🌈 NDWI / ИК",
            "accent": "#00e6b8"
        },
        "gis": {
            "image": "images/ui/cards/card_gis.png",
            "tag1": "🗺️ Слои ООПТ",
            "tag2": "📐 Буфер 250м",
            "accent": "#38bdf8"
        },
        "ml": {
            "image": "images/ui/cards/card_ml.png",
            "tag1": "🧠 YOLOv8 AI",
            "tag2": "🎯 Детекция мусора",
            "accent": "#4ade80"
        },
        "ecologist": {
            "image": "images/ui/cards/card_ecologist.png",
            "tag1": "🌿 Паспорт ФККО",
            "tag2": "🦭 Фауна побережий",
            "accent": "#f87171"
        },
        "uav": {
            "image": "images/ui/cards/card_uav.png",
            "tag1": "🚁 Аэросъемка БПЛА",
            "tag2": "📷 GSD 2 см/пикс",
            "accent": "#38bdf8"
        },
        "volunteer_coord": {
            "image": "images/ui/cards/card_volunteer_coord.png",
            "tag1": "🤝 Экодесант",
            "tag2": "♻️ Zero Waste",
            "accent": "#c084fc"
        }
    }

    def entry_select_role(spec_id):
        if clean_state.is_specialty_completed(spec_id):
            return
        clean_state.set_specialty(spec_id)
        clean_state.specialties_filter_id = spec_id
        clean_state.selected_preview_spec = spec_id
        renpy.restart_interaction()

    def entry_close_preview():
        clean_state.selected_preview_spec = None
        renpy.restart_interaction()

    def start_chosen_specialty_missions(spec_id):
        clean_state.set_specialty(spec_id)
        clean_state.selected_preview_spec = None
        tasks = clean_state.get_tasks_for_specialty(spec_id)
        if tasks:
            first_incomplete = next((t for t in tasks if not t.completed), tasks[0])
            clean_state.start_role_mission(first_incomplete.id)
        renpy.show_screen("clean_role_mission_screen")
        if not clean_state.mission_guide_shown:
            renpy.show_screen("mission_tutorial_modal")
        renpy.restart_interaction()

screen role_selection_entry_screen():
    tag clean_screen
    add Solid("#060d19")

    # Фоновое сияние
    add Solid("#0b1c3625"):
        xsize 1920
        ysize 1080

    python:
        # Автоматически переключаем активную специальность на незавершенную, если текущая уже пройдена
        if clean_state.is_specialty_completed(clean_state.active_specialty.id):
            rem = clean_state.get_remaining_specialties()
            if rem:
                clean_state.set_specialty(rem[0].id)

    $ cur_spec = clean_state.active_specialty
    $ completed_count = len(clean_state.completed_specialties)
    $ total_tasks_done = clean_state.get_total_completed_tasks()
    $ total_tasks_cnt = clean_state.get_total_tasks_count()
    $ all_done = clean_state.all_specialties_completed()

    vbox:
        xalign 0.5
        ypos 30
        spacing 8
        xsize 1020

        # ВЕРХНИЙ БЛОК: ЗАГОЛОВОК И ПРОГРЕСС
        vbox:
            xalign 0.5
            spacing 4

            hbox:
                xalign 0.5
                spacing 14
                yalign 0.5

                if all_done:
                    frame:
                        background Frame("images/ui/rounded/pill_active.png", 18, 18)
                        padding (20, 6)
                        text "🏆 ВСЕ 18 ЗАДАЧ И 6 СПЕЦИАЛЬНОСТЕЙ УСПЕШНО ЗАВЕРШЕНЫ!":
                            size 13
                            color "#ffffff"
                            bold True
                else:
                    frame:
                        background Frame("images/ui/rounded/pill_chip.png", 18, 18)
                        padding (16, 5)
                        text "🌊 ПРОГРЕСС: [total_tasks_done] ИЗ [total_tasks_cnt] ЗАДАЧ ВЫПОЛНЕНО • [completed_count] ИЗ 6 СПЕЦИАЛЬНОСТЕЙ":
                            size 12
                            color "#00e6b8"
                            bold True

                button:
                    action Show("clean_prologue_screen")
                    background Frame(Solid("#1e293b"), 14, 14)
                    hover_background Frame(Solid("#334155"), 14, 14)
                    padding (12, 5)
                    text "📖 Пролог":
                        size 12
                        color "#38bdf8"
                        bold True

                button:
                    action Show("clean_analytics_screen")
                    background Frame(Solid("#0d2847"), 14, 14)
                    hover_background Frame(Solid("#1e40af"), 14, 14)
                    padding (12, 5)
                    text "📊 Аналитика профиля":
                        size 12
                        color "#cbd5e1"
                        bold True

                button:
                    action Show("clean_certificate_screen")
                    background Frame(Solid("#064e3b"), 14, 14)
                    hover_background Frame(Solid("#059669"), 14, 14)
                    padding (12, 5)
                    text "🏆 Сертификат":
                        size 12
                        color "#34d399"
                        bold True

            text "ВЫБЕРИТЕ ВАШУ РОЛЬ В ПРОЕКТЕ":
                size 28
                color "#ffffff"
                bold True
                xalign 0.5

            if all_done:
                text "Вы завершили все направления мониторинга! Ваш наградной сертификат готов к выдаче:":
                    size 14
                    color "#f59e0b"
                    xalign 0.5
            else:
                text "Кликните на специальность для краткой сводки ее задач. Пройденные роли блокируются:":
                    size 14
                    color "#94a3b8"
                    xalign 0.5

        null height 2

        # СЕТКА ИЗ 6 КОМПАКТНЫХ СКРУГЛЕННЫХ КАРТОЧЕК (3x2)
        grid 3 2:
            spacing 18
            xalign 0.5

            for sp in clean_state.specialties:
                $ is_done = clean_state.is_specialty_completed(sp.id)
                $ is_active = (sp.id == cur_spec.id and not is_done)
                $ sp_tasks_done = clean_state.get_completed_tasks_count(sp.id)
                $ sp_tasks_total = len(clean_state.get_tasks_for_specialty(sp.id))
                $ vdata = role_visual_data.get(sp.id, {"image": "images/ui/cards/card_dzz.png", "tag1": sp.short_title, "tag2": sp.tool_name, "accent": "#00e6b8"})
                $ card_img = vdata["image"]

                # Карточка роли (заблокированная или интерактивная)
                button:
                    action (NullAction() if is_done else Function(entry_select_role, sp.id))
                    focus_mask None
                    if is_done:
                        background Frame(Solid("#08111e"), 24, 24)
                    elif is_active:
                        background Frame("images/ui/rounded/card_active_v2.png", 24, 24)
                        hover_background Frame("images/ui/rounded/card_active_v2.png", 24, 24)
                    else:
                        background Frame("images/ui/rounded/card_idle_v2.png", 24, 24)
                        hover_background Frame("images/ui/rounded/card_hover_v2.png", 24, 24)
                    padding (12, 12)
                    xsize 318
                    ysize 310

                    vbox:
                        spacing 6

                        # 1. Графический баннер снимка
                        frame:
                            xsize 294
                            ysize 132
                            padding (0, 0)
                            background Solid("#050c17")

                            # Фото / растр
                            add card_img:
                                xsize 294
                                ysize 132
                                fit "cover"

                            # Затемнение для заблокированных
                            if is_done:
                                add Solid("#030712dd"):
                                    xsize 294
                                    ysize 132
                            else:
                                add Solid("#071224cc"):
                                    yalign 1.0
                                    xsize 294
                                    ysize 46

                            # Иконка роли
                            frame:
                                pos (8, 8)
                                background Frame("images/ui/rounded/pill_chip.png", 18, 18)
                                padding (8, 4)
                                text "[sp.icon]":
                                    size 22

                            # Статусный бейдж
                            $ is_rec = (sp.id == clean_state.career_analytics.recommended_spec_id)
                            if is_done:
                                frame:
                                    xalign 0.96
                                    ypos 8
                                    background Frame(Solid("#1e293b"), 18, 18)
                                    padding (8, 4)
                                    text "🔒 ЗАБЛОКИРОВАНО":
                                        size 10
                                        color "#94a3b8"
                                        bold True
                            elif is_rec:
                                frame:
                                    xalign 0.96
                                    ypos 8
                                    background Frame(Solid("#d97706"), 18, 18)
                                    padding (8, 4)
                                    text "★ РЕКОМЕНДОВАНО":
                                        size 10
                                        color "#ffffff"
                                        bold True
                            elif is_active:
                                frame:
                                    xalign 0.96
                                    ypos 8
                                    background Frame("images/ui/rounded/pill_active.png", 18, 18)
                                    padding (8, 4)
                                    text "★ ВЫБРАНО":
                                        size 10
                                        color "#ffffff"
                                        bold True

                            # Заголовок роли поверх баннера
                            vbox:
                                pos (10, 88)
                                spacing 1
                                text "[sp.name]":
                                    size 15
                                    color ("#64748b" if is_done else ("#00e6b8" if is_active else "#ffffff"))
                                    bold True
                                text "[sp.short_title]":
                                    size 11
                                    color ("#475569" if is_done else "#38bdf8")
                                    bold True

                        # 2. Краткая суть профессии и прогресс задач
                        frame:
                            background Solid("#00000000")
                            padding (2, 0)
                            xfill True
                            ysize 36
                            if is_done:
                                text "✓ Сдано [sp_tasks_done]/[sp_tasks_total] задач • Специальность завершена":
                                    size 10
                                    color "#22c55e"
                                    line_spacing 1
                                    text_align 0.5
                                    xalign 0.5
                            elif sp_tasks_done > 0:
                                text "⚡ Решено [sp_tasks_done] из [sp_tasks_total] задач • [sp.role_desc]":
                                    size 10
                                    color "#f59e0b"
                                    line_spacing 1
                                    text_align 0.5
                                    xalign 0.5
                            else:
                                text "[sp.role_desc]":
                                    size 10
                                    color "#cbd5e1"
                                    line_spacing 1
                                    text_align 0.5
                                    xalign 0.5

                        # 3. Плашка закрепленного инструмента
                        frame:
                            background Frame("images/ui/rounded/pill_chip.png", 18, 18)
                            padding (10, 5)
                            xfill True
                            hbox:
                                spacing 6
                                yalign 0.5
                                text ("🔒" if is_done else "⚡"):
                                    size 11
                                    yalign 0.5
                                text "[sp.tool_name]":
                                    size 10
                                    color ("#64748b" if is_done else "#f59e0b")
                                    bold True

                        null height 1

                        # 4. Нижний индикатор выбора роли со счётчиком задач
                        if is_done:
                            frame:
                                background Frame(Solid("#1e293b"), 18, 18)
                                padding (8, 6)
                                xfill True
                                text "🔒 ПРОЙДЕНО ([sp_tasks_done]/[sp_tasks_total] СДАНО)":
                                    size 11
                                    color "#64748b"
                                    bold True
                                    xalign 0.5
                        elif is_active:
                            frame:
                                background Frame("images/ui/rounded/pill_active.png", 18, 18)
                                padding (8, 6)
                                xfill True
                                text ("★ ВЫБРАНО: СДАТЬ МИССИИ ([sp_tasks_done]/[sp_tasks_total])" if sp_tasks_done > 0 else "★ ВЫБРАНО (СВОДКА И ЗАДАЧИ)"):
                                    size 11
                                    color "#ffffff"
                                    bold True
                                    xalign 0.5
                        elif sp_tasks_done > 0:
                            frame:
                                background Frame(Solid("#1e3a5f"), 18, 18)
                                padding (8, 6)
                                xfill True
                                text "⚡ В ПРОЦЕССЕ ([sp_tasks_done]/[sp_tasks_total] СДАНО)":
                                    size 11
                                    color "#38bdf8"
                                    bold True
                                    xalign 0.5
                        else:
                            frame:
                                background Frame("images/ui/rounded/pill_chip.png", 18, 18)
                                padding (8, 6)
                                xfill True
                                text "Кликните для сводки и старта (0/[sp_tasks_total])":
                                    size 11
                                    color "#94a3b8"
                                    xalign 0.5

    # НИЖНЯЯ КНОПКА ДЕЙСТВИЯ
    vbox:
        xalign 0.5
        ypos 880
        spacing 8

        if all_done:
            # Если все 6 специальностей завершены - кнопка получения сертификата
            button:
                xalign 0.5
                xsize 840
                ysize 84
                background Frame(Solid("#d97706"), 38, 38)
                hover_background Frame(Solid("#f59e0b"), 38, 38)
                padding (45, 18)
                focus_mask None
                action Show("clean_certificate_screen")

                hbox:
                    spacing 16
                    xalign 0.5
                    yalign 0.5
                    text "🏆":
                        size 32
                        yalign 0.5
                    text "ПОЛУЧИТЬ НАГРАДНОЙ СЕРТИФИКАТ ЭКСПЕРТА →":
                        size 22
                        color "#ffffff"
                        bold True
                        yalign 0.5

            text "🎉 Вы успешно завершили все 6 ролей! Нажмите для открытия официального сертификата.":
                size 12
                color "#f59e0b"
                xalign 0.5

        else:
            # Кнопка прямого перехода к миссиям выбранной специальности
            $ spec_title_upper = cur_spec.name.upper()
            $ cur_spec_done = clean_state.get_completed_tasks_count(cur_spec.id)
            $ cur_spec_total = len(clean_state.get_tasks_for_specialty(cur_spec.id))
            button:
                xalign 0.5
                xsize 880
                ysize 72
                background Frame("images/ui/rounded/btn_cta_large_idle.png", 38, 38)
                hover_background Frame("images/ui/rounded/btn_cta_large_hover.png", 38, 38)
                padding (24, 12)
                focus_mask None
                action Function(start_chosen_specialty_missions, cur_spec.id)

                hbox:
                    spacing 14
                    xalign 0.5
                    yalign 0.5
                    text "🚀":
                        size 26
                        yalign 0.5
                    if cur_spec_done > 0:
                        text "ПРОДОЛЖИТЬ ЗАДАЧИ: [spec_title_upper] ([cur_spec_done]/[cur_spec_total]) →":
                            size 17
                            color "#041122"
                            bold True
                            yalign 0.5
                    else:
                        text "ПЕРЕЙТИ К ЗАДАЧАМ: [spec_title_upper] →":
                            size 18
                            color "#041122"
                            bold True
                            yalign 0.5


            text "💡 При выборе специальности открывается краткая сводка ее задач, после чего сразу начинаются 3 миссии.":
                size 12
                color "#64748b"
                xalign 0.5

    # МОДАЛЬНОЕ ОКНО: КРАТКАЯ СВОДКА СПЕЦИАЛЬНОСТИ ПЕРЕД ЗАДАЧАМИ
    if clean_state.selected_preview_spec:
        $ p_spec = clean_state.get_specialty_by_id(clean_state.selected_preview_spec)
        $ p_vdata = role_visual_data.get(p_spec.id, {"image": "images/ui/cards/card_dzz.png", "tag1": p_spec.short_title, "tag2": p_spec.tool_name, "accent": "#00e6b8"})

        # Полупрозрачная подложка затемнения
        button:
            background Solid("#000000c8")
            action Function(entry_close_preview)
            xfill True
            yfill True

        # Центральная карточка сводки (динамическая высота, исключающая перекрытие кнопками)
        frame:
            xalign 0.5
            yalign 0.5
            xsize 940
            background Frame(Solid("#09172c"), 16, 16)
            padding (28, 18)

            vbox:
                spacing 8
                xalign 0.5

                # 1. Заголовок модального окна
                hbox:
                    spacing 14
                    yalign 0.5
                    text "[p_spec.icon]":
                        size 30
                        yalign 0.5
                    vbox:
                        spacing 2
                        text "[p_spec.name]":
                            size 20
                            color "#ffffff"
                            bold True
                        text "КРАТКАЯ СВОДКА РОЛИ • [p_spec.short_title]":
                            size 12
                            color "#38bdf8"
                            bold True

                    null width 40

                    # Кнопка закрытия
                    textbutton "✕ Закрыть":
                        action Function(entry_close_preview)
                        text_size 13
                        text_color "#94a3b8"
                        xalign 1.0
                        yalign 0.5

                # Линия
                frame:
                    background Solid("#1e293b")
                    xsize 884
                    ysize 2

                # 2. Графический баннер и суть роли
                hbox:
                    spacing 16
                    frame:
                        xsize 320
                        ysize 120
                        padding (0, 0)
                        background Solid("#040913")
                        add p_vdata["image"]:
                            xsize 320
                            ysize 120

                    frame:
                        xsize 548
                        ysize 120
                        background Frame(Solid("#0f223d"), 8, 8)
                        padding (14, 10)
                        vbox:
                            spacing 4
                            text "📋 ЧТО ДЕЛАЕТ ЭТА СПЕЦИАЛЬНОСТЬ:":
                                size 11
                                color "#00e6b8"
                                bold True
                            text "[p_spec.role_desc]":
                                size 12
                                color "#f8fafc"
                                line_spacing 2

                # 3. Боевые задачи роли
                frame:
                    xsize 884
                    background Frame(Solid("#0b1e35"), 8, 8)
                    padding (14, 10)
                    vbox:
                        spacing 3
                        text "🎯 ЧЕМ ПРЕДСТОИТ ЗАНИМАТЬСЯ (3 БОЕВЫЕ МИССИИ):":
                            size 11
                            color "#38bdf8"
                            bold True
                        text "[p_spec.tasks_desc]":
                            size 12
                            color "#cbd5e1"
                            line_spacing 2

                # 4. Инструментарий и стек
                frame:
                    xsize 884
                    background Frame(Solid("#0b1e35"), 8, 8)
                    padding (14, 8)
                    vbox:
                        spacing 3
                        hbox:
                            spacing 8
                            text "⚡ Инструмент роли:":
                                size 11
                                color "#f59e0b"
                                bold True
                            text "[p_spec.tool_name]":
                                size 11
                                color "#ffffff"
                                bold True
                        text "[p_spec.tool_desc]":
                            size 11
                            color "#94a3b8"

                # 5. Предупреждение о строгих правилах (без перепрохождения)
                frame:
                    xsize 884
                    background Frame(Solid("#450a0a"), 8, 8)
                    padding (14, 8)
                    hbox:
                        spacing 10
                        yalign 0.5
                        text "⚠️":
                            size 18
                            yalign 0.5
                        text "⚡ ПРАВИЛА ЭКСПЕДИЦИИ (14+): Задачи решаются с первой попытки без права на ошибку! Пройдешь все 3 задачи — специальность зафиксируется.":
                            size 11
                            color "#fca5a5"
                            bold True
                            line_spacing 1

                null height 2

                # 6. Кнопки запуска (свободное размещение без наложений на текст)
                $ p_done = clean_state.get_completed_tasks_count(p_spec.id)
                hbox:
                    xalign 0.5
                    spacing 16

                    button:
                        xsize 560
                        ysize 52
                        background Frame(Solid("#00e6b8"), 10, 10)
                        hover_background Frame(Solid("#38bdf8"), 10, 10)
                        padding (16, 10)
                        action Function(start_chosen_specialty_missions, p_spec.id)

                        hbox:
                            spacing 10
                            xalign 0.5
                            yalign 0.5
                            text "🚀":
                                size 20
                                yalign 0.5
                            if p_done > 0:
                                text "ПРОДОЛЖИТЬ ЗАДАЧИ ([p_done]/3 СДАНО) →":
                                    size 15
                                    color "#041122"
                                    bold True
                                    yalign 0.5
                            else:
                                text "ПРИСТУПИТЬ К ЗАДАЧАМ (3 МИССИИ) →":
                                    size 15
                                    color "#041122"
                                    bold True
                                    yalign 0.5

                    button:
                        xsize 308
                        ysize 52
                        background Frame(Solid("#1e293b"), 10, 10)
                        hover_background Frame(Solid("#334155"), 10, 10)
                        padding (16, 10)
                        action Function(entry_close_preview)

                        text "✕ Выбрать другую роль":
                            size 13
                            color "#94a3b8"
                            xalign 0.5
                            yalign 0.5

