## clean_oopt.rpy
## Кабинет сотрудника ООПТ (Особо охраняемой природной территории)

init python:
    def oopt_select_report(rep):
        clean_state.selected_map_report = rep
        renpy.restart_interaction()

    def oopt_approve(rep_id):
        clean_state.approve_report_by_id(rep_id)
        renpy.restart_interaction()

    def oopt_reject(rep_id):
        clean_state.reject_report_by_id(rep_id)
        renpy.restart_interaction()

    def oopt_create_and_publish():
        clean_state.add_created_challenge()
        clean_state.oopt_active_tab = "promo"
        renpy.restart_interaction()

## ГЛАВНЫЙ ЭКРАН КАБИНЕТА ООПТ
screen oopt_cabinet_screen():
    tag clean_screen
    add Solid("#070f1e")

    use clean_top_bar(active_tab="oopt")

    $ stats = clean_state.oopt_stats
    $ cur_tab = clean_state.oopt_active_tab

    vbox:
        xalign 0.5
        ypos 100
        spacing 15
        xsize 1400

        # ВЕРХНЯЯ ШАПКА: СТАТИСТИКА И ТЕРРИТОРИЯ (Этап 3: Участников: 126, Заданий: 98, Фото: 241, Подтверждено: 87)
        frame:
            background Frame(Solid("#0e1e38"), 10, 10)
            padding (30, 18)
            xfill True

            hbox:
                xfill True
                yalign 0.5

                # Информация о ведомстве
                vbox:
                    spacing 4
                    text "КАБИНЕТ ОПЕРАТОРА ООПТ":
                        size 13
                        color "#00e6b8"
                        bold True
                    text "Национальный парк «Куршская коса»":
                        size 22
                        color "#ffffff"
                        bold True
                    text "Подведомственная площадь: 6 621 га • Акватория: 14 500 га":
                        size 13
                        color "#94a3b8"

                # 4 ключевые метрики (Этап 3)
                hbox:
                    spacing 25
                    vbox:
                        text "[stats.participants]":
                            style "clean_stat_number"
                            xalign 0.5
                        text "Участников":
                            style "clean_stat_label"
                            xalign 0.5

                    add Solid("#1e293b"):
                        xsize 2
                        ysize 50

                    vbox:
                        text "[stats.tasks_completed]":
                            style "clean_stat_number"
                            color "#38bdf8"
                            xalign 0.5
                        text "Заданий выполнено":
                            style "clean_stat_label"
                            xalign 0.5

                    add Solid("#1e293b"):
                        xsize 2
                        ysize 50

                    vbox:
                        text "[stats.photos_count]":
                            style "clean_stat_number"
                            color "#f59e0b"
                            xalign 0.5
                        text "Фотографий":
                            style "clean_stat_label"
                            xalign 0.5

                    add Solid("#1e293b"):
                        xsize 2
                        ysize 50

                    vbox:
                        text "[stats.approved_count]":
                            style "clean_stat_number"
                            color "#22c55e"
                            xalign 0.5
                        text "Подтверждено":
                            style "clean_stat_label"
                            xalign 0.5

        # НАВИГАЦИОННЫЕ ВКЛАДКИ КАБИНЕТА
        hbox:
            spacing 12
            textbutton "🗺️ Общая карта результатов":
                text_size 15
                text_bold True
                text_color ("#ffffff" if cur_tab == "map" else "#94a3b8")
                background Frame(Solid("#132847" if cur_tab == "map" else "#0c1a30"), 6, 6)
                xpadding 20
                ypadding 10
                action [SetField(clean_state, "oopt_active_tab", "map")]

            textbutton "📋 Входящие отчеты (Модерация)":
                text_size 15
                text_bold True
                text_color ("#ffffff" if cur_tab == "moderation" else "#94a3b8")
                background Frame(Solid("#132847" if cur_tab == "moderation" else "#0c1a30"), 6, 6)
                xpadding 20
                ypadding 10
                action [SetField(clean_state, "oopt_active_tab", "moderation")]

            textbutton "➕ Создать задание":
                text_size 15
                text_bold True
                text_color ("#ffffff" if cur_tab == "create" else "#94a3b8")
                background Frame(Solid("#132847" if cur_tab == "create" else "#0c1a30"), 6, 6)
                xpadding 20
                ypadding 10
                action [SetField(clean_state, "oopt_active_tab", "create")]

            textbutton "📢 Публикация и QR-код":
                text_size 15
                text_bold True
                text_color ("#ffffff" if cur_tab == "promo" else "#94a3b8")
                background Frame(Solid("#132847" if cur_tab == "promo" else "#0c1a30"), 6, 6)
                xpadding 20
                ypadding 10
                action [SetField(clean_state, "oopt_active_tab", "promo")]

            textbutton "👥 Штаб 6 Специальностей":
                text_size 15
                text_bold True
                text_color ("#ffffff" if cur_tab == "team" else "#94a3b8")
                background Frame(Solid("#132847" if cur_tab == "team" else "#0c1a30"), 6, 6)
                xpadding 18
                ypadding 10
                action [SetField(clean_state, "oopt_active_tab", "team")]

        # ОСНОВНОЙ КОНТЕНТ ВКЛАДОК
        frame:
            background Frame(Solid("#0a162a"), 10, 10)
            padding (25, 20)
            xfill True
            ysize 650

            # -------------------------------------------------------------
            # ВКЛАДКА 1: ОБЩАЯ КАРТА РЕЗУЛЬТАТОВ (Этап 4)
            # Участники → Точки наблюдений → Фото → Типы загрязнения → Общая карта
            # -------------------------------------------------------------
            if cur_tab == "map" or cur_tab == "stats":
                hbox:
                    spacing 20

                    # Левая часть: Интерактивная карта с точками наблюдений (880x600)
                    frame:
                        xsize 880
                        ysize 600
                        background Solid("#000000")
                        padding (0, 0)

                        add "images/ui/oopt_map_bg.png":
                            xsize 880
                            ysize 600

                        # Точки наблюдений участников на карте
                        # Точка 1 (Пластик)
                        button:
                            pos (410, 220)
                            xsize 36
                            ysize 36
                            background None
                            add "images/ui/map_pin.png":
                                zoom 0.8
                            action Function(oopt_select_report, clean_state.reports[0])

                        # Точка 2 (Сети)
                        button:
                            pos (550, 160)
                            xsize 36
                            ysize 36
                            background None
                            add "images/ui/map_pin.png":
                                zoom 0.8
                            action Function(oopt_select_report, clean_state.reports[1])

                        # Точка 3 (Покрышки)
                        button:
                            pos (370, 390)
                            xsize 36
                            ysize 36
                            background None
                            add "images/ui/map_pin.png":
                                zoom 0.8
                            action Function(oopt_select_report, clean_state.reports[2])

                        # Точка 4 (Металл)
                        button:
                            pos (510, 310)
                            xsize 36
                            ysize 36
                            background None
                            add "images/ui/map_pin.png":
                                zoom 0.8
                            action Function(oopt_select_report, clean_state.reports[3])

                        # Легенда карты
                        frame:
                            xpos 15
                            ypos 15
                            background Solid("#091426eb")
                            padding (12, 10)
                            vbox:
                                spacing 4
                                text "ГИС СЛОЙ: НАБЛЮДЕНИЯ УЧАСТНИКОВ":
                                    size 12
                                    color "#38bdf8"
                                    bold True
                                text "🔴 Точки полевых отчетов (Кликните для деталей)":
                                    size 11
                                    color "#e2e8f0"
                                text "🟡 Границы особо охраняемой зоны":
                                    size 11
                                    color "#f59e0b"

                    # Правая часть: Карточка выбранной точки наблюдения
                    vbox:
                        spacing 15
                        xsize 440

                        if clean_state.selected_map_report is not None:
                            $ rep = clean_state.selected_map_report
                            frame:
                                background Frame(Solid("#0e1e38"), 8, 8)
                                padding (20, 15)
                                xfill True

                                vbox:
                                    spacing 10
                                    hbox:
                                        xfill True
                                        text "ОТЧЕТ НАБЛЮДАТЕЛЯ":
                                            size 13
                                            color "#00e6b8"
                                            bold True
                                        if rep.status == "approved":
                                            text "ПОДТВЕРЖДЕНО":
                                                size 12
                                                color "#22c55e"
                                                bold True
                                        else:
                                            text "НА ПРОВЕРКЕ":
                                                size 12
                                                color "#f59e0b"
                                                bold True

                                    add rep.photo_path:
                                        xsize 400
                                        ysize 220

                                    text "[rep.category]":
                                        size 18
                                        color "#ffffff"
                                        bold True

                                    text "📍 [rep.location_name]":
                                        size 14
                                        color "#38bdf8"

                                    text "Координаты: [rep.lat], [rep.lon]":
                                        size 13
                                        color "#94a3b8"

                                    text "Автор: [rep.user_name]  •  [rep.timestamp]":
                                        size 12
                                        color "#64748b"

                                    text "«[rep.comment]»":
                                        size 13
                                        color "#cbd5e1"

                                    null height 5

                                    if rep.status != "approved":
                                        hbox:
                                            spacing 10
                                            textbutton "Подтвердить (+100 XP) ✔":
                                                text_size 13
                                                text_bold True
                                                background Frame(Solid("#15803d"), 4, 4)
                                                xpadding 15
                                                ypadding 8
                                                action Function(oopt_approve, rep.id)

                                            textbutton "Отклонить ✖":
                                                text_size 13
                                                background Frame(Solid("#7f1d1d"), 4, 4)
                                                xpadding 15
                                                ypadding 8
                                                action Function(oopt_reject, rep.id)
                        else:
                            frame:
                                background Frame(Solid("#0e1e38"), 8, 8)
                                padding (20, 20)
                                xfill True
                                vbox:
                                    spacing 10
                                    text "КАРТОЧКА ОБЪЕКТА":
                                        size 14
                                        color "#94a3b8"
                                        bold True
                                    text "Кликните на любой красный маркер на ГИС-карте слева, чтобы просмотреть фотографию, тип загрязнения и верифицировать данные волонтера.":
                                        size 14
                                        color "#cbd5e1"
                                        line_spacing 4

            # -------------------------------------------------------------
            # ВКЛАДКА 2: СПИСОК ВХОДЯЩИХ ОТЧЕТОВ (Модерация)
            # -------------------------------------------------------------
            elif cur_tab == "moderation":
                vbox:
                    spacing 12
                    text "РЕЕСТР ПОЛЕВЫХ ОТЧЕТОВ УЧАСТНИКОВ НА ВЕРИФИКАЦИЮ":
                        size 18
                        color "#ffffff"
                        bold True

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        ysize 530

                        vbox:
                            spacing 10
                            for rep in clean_state.reports:
                                frame:
                                    background Frame(Solid("#0e1e38"), 6, 6)
                                    padding (15, 12)
                                    xfill True

                                    hbox:
                                        spacing 20
                                        yalign 0.5

                                        add rep.photo_path:
                                            xsize 120
                                            ysize 80

                                        vbox:
                                            spacing 3
                                            xsize 600
                                            text "[rep.category]  •  [rep.location_name]":
                                                size 16
                                                color "#38bdf8"
                                                bold True
                                            text "Участник: [rep.user_name]  •  [rep.lat], [rep.lon]  •  [rep.timestamp]":
                                                size 13
                                                color "#94a3b8"
                                            text "«[rep.comment]»":
                                                size 13
                                                color "#e2e8f0"

                                        vbox:
                                            spacing 8
                                            xalign 1.0
                                            if rep.status == "approved":
                                                frame:
                                                    background Solid("#166534")
                                                    padding (8, 4)
                                                    text "ПОДТВЕРЖДЕНО":
                                                        size 12
                                                        color "#bbf7d0"
                                            else:
                                                hbox:
                                                    spacing 8
                                                    textbutton "Одобрить":
                                                        text_size 13
                                                        text_bold True
                                                        background Frame(Solid("#15803d"), 4, 4)
                                                        xpadding 15
                                                        ypadding 8
                                                        action Function(oopt_approve, rep.id)
                                                    textbutton "Отклонить":
                                                        text_size 13
                                                        background Frame(Solid("#7f1d1d"), 4, 4)
                                                        xpadding 15
                                                        ypadding 8
                                                        action Function(oopt_reject, rep.id)

            # -------------------------------------------------------------
            # ВКЛАДКА 3: СОЗДАНИЕ ЧЕЛЛЕНДЖА (Этап 1: Форма)
            # Название, Описание, Территория, Даты, Участники, Тип, Награда
            # -------------------------------------------------------------
            elif cur_tab == "create":
                vbox:
                    spacing 15
                    xalign 0.5
                    xsize 900

                    text "СОЗДАНИЕ НОВОГО ЧЕЛЛЕНДЖА МОНИТОРИНГА ООПТ":
                        size 22
                        color "#00e6b8"
                        bold True
                        xalign 0.5

                    grid 2 4:
                        spacing 15
                        xfill True

                        # Поле 1: Название
                        vbox:
                            text "Название задания:":
                                size 14
                                color "#94a3b8"
                            input:
                                value FieldInputValue(clean_state, "new_task_title")
                                length 50
                                size 16
                                color "#ffffff"

                        # Поле 2: Территория
                        vbox:
                            text "Территория ООПТ:":
                                size 14
                                color "#94a3b8"
                            input:
                                value FieldInputValue(clean_state, "new_task_territory")
                                length 40
                                size 16
                                color "#ffffff"

                        # Поле 3: Описание
                        vbox:
                            text "Описание задачи:":
                                size 14
                                color "#94a3b8"
                            input:
                                value FieldInputValue(clean_state, "new_task_desc")
                                length 70
                                size 16
                                color "#ffffff"

                        # Поле 4: Тип задания
                        vbox:
                            text "Тип задания:":
                                size 14
                                color "#94a3b8"
                            input:
                                value FieldInputValue(clean_state, "new_task_type")
                                length 35
                                size 16
                                color "#ffffff"

                        # Поле 5: Дата начала
                        vbox:
                            text "Дата начала:":
                                size 14
                                color "#94a3b8"
                            input:
                                value FieldInputValue(clean_state, "new_task_start")
                                length 15
                                size 16
                                color "#ffffff"

                        # Поле 6: Дата окончания
                        vbox:
                            text "Дата окончания:":
                                size 14
                                color "#94a3b8"
                            input:
                                value FieldInputValue(clean_state, "new_task_end")
                                length 15
                                size 16
                                color "#ffffff"

                        # Поле 7: Количество участников
                        vbox:
                            text "Лимит участников:":
                                size 14
                                color "#94a3b8"
                            input:
                                value FieldInputValue(clean_state, "new_task_max_users")
                                length 10
                                size 16
                                color "#ffffff"

                        # Поле 8: Награда
                        vbox:
                            text "Награда (XP):":
                                size 14
                                color "#94a3b8"
                            input:
                                value FieldInputValue(clean_state, "new_task_reward")
                                length 10
                                size 16
                                color "#ffffff"

                    null height 15

                    textbutton "Опубликовать челлендж в системе →":
                        text_size 18
                        text_bold True
                        text_color "#070f1e"
                        background Frame(Solid("#00e6b8"), 8, 8)
                        hover_background Frame(Solid("#38bdf8"), 8, 8)
                        xpadding 40
                        ypadding 12
                        xalign 0.5
                        action Function(oopt_create_and_publish)

            # -------------------------------------------------------------
            # ВКЛАДКА 4: ПУБЛИКАЦИЯ И ПРОМО (Этап 2)
            # Web-ссылка, QR-код, Карточка для соцсетей
            # -------------------------------------------------------------
            elif cur_tab == "promo":
                $ last_ch = clean_state.challenges[-1]
                vbox:
                    spacing 15
                    xalign 0.5

                    text "ПАКЕТ МАТЕРИАЛОВ ДЛЯ ПУБЛИКАЦИИ И РАСПРОСТРАНЕНИЯ":
                        size 22
                        color "#00e6b8"
                        bold True
                        xalign 0.5

                    hbox:
                        spacing 40
                        xalign 0.5

                        # Блок 1: QR-код и Web-ссылка
                        frame:
                            background Frame(Solid("#0e1e38"), 8, 8)
                            padding (25, 20)
                            xsize 420
                            vbox:
                                spacing 12
                                xalign 0.5
                                text "QR-КОД ДЛЯ СТЕНДОВ И БУКЛЕТОВ:":
                                    size 14
                                    color "#38bdf8"
                                    bold True

                                add "images/ui/qr_code.png":
                                    xsize 190
                                    ysize 190
                                    xalign 0.5

                                text "Ссылка на страницу челленджа:":
                                    size 12
                                    color "#94a3b8"

                                frame:
                                    background Solid("#07101f")
                                    padding (10, 6)
                                    xfill True
                                    text "https://clean-coast.ru/c/[last_ch.id]":
                                        size 12
                                        color "#00e6b8"

                                text "Разместите на сайте ООПТ, инфостенде экотропы или визит-центра":
                                    size 12
                                    color "#cbd5e1"
                                    text_align 0.5

                        # Блок 2: Карточка для социальных сетей
                        frame:
                            background Frame(Solid("#0e1e38"), 8, 8)
                            padding (25, 20)
                            xsize 680
                            vbox:
                                spacing 12
                                text "КАРТОЧКА ДЛЯ СОЦИАЛЬНЫХ СЕТЕЙ (VK, TELEGRAM):":
                                    size 14
                                    color "#38bdf8"
                                    bold True

                                frame:
                                    xsize 630
                                    ysize 280
                                    background Frame(Solid("#102644"), 6, 6)
                                    padding (0, 0)

                                    add "images/ui/promo_card.png":
                                        xsize 630
                                        ysize 280
                                        fit "cover"
                                    add Solid("#071224d0"):
                                        xsize 630
                                        ysize 280

                                    vbox:
                                        xpos 25
                                        ypos 20
                                        spacing 8
                                        frame:
                                            background Solid("#00e6b8")
                                            padding (8, 4)
                                            text "ЧИСТЫЙ БЕРЕГ  •  ЧЕЛЛЕНДЖ ООПТ":
                                                size 11
                                                color "#070f1e"
                                                bold True
                                        text "[last_ch.title]":
                                            size 20
                                            color "#ffffff"
                                            bold True
                                        text "Территория: [last_ch.territory]":
                                            size 14
                                            color "#38bdf8"
                                        text "[last_ch.description]":
                                            size 13
                                            color "#cbd5e1"
                                        null height 6
                                        text "Присоединяйся к мониторингу: набери очки и помоги заповедной зоне!":
                                            size 12
                                            color "#f59e0b"
                                            bold True

                                hbox:
                                    spacing 15
                                    textbutton "Скачать графическую карточку":
                                        text_size 13
                                        background Frame(Solid("#1e293b"), 4, 4)
                                        xpadding 15
                                        ypadding 8
                                        action Notify("Карточка сохранена для публикации в соцсетях!")
                                    textbutton "Скопировать ссылку анонса":
                                        text_size 13
                                        background Frame(Solid("#1e293b"), 4, 4)
                                        xpadding 15
                                        ypadding 8
                                        action Notify("Ссылка скопирована в буфер!")

            # -------------------------------------------------------------
            # ВКЛАДКА 5: ШТАБ 6 СПЕЦИАЛЬНОСТЕЙ ООПТ
            # -------------------------------------------------------------
            elif cur_tab == "team":
                vbox:
                    spacing 14
                    xalign 0.5
                    xsize 1320

                    text "МЕЖДИСЦИПЛИНАРНЫЙ ШТАБ МОНИТОРИНГА И ОХРАНЫ ПОБЕРЕЖЬЯ":
                        size 20
                        color "#00e6b8"
                        bold True
                        xalign 0.5

                    # Схема взаимодействия
                    frame:
                        background Frame(Solid("#0e1e38"), 8, 8)
                        padding (18, 12)
                        xfill True
                        hbox:
                            spacing 8
                            xalign 0.5
                            for s_icon, s_name in [("🛰️", "ДЗЗ (Космос)"), ("→", ""), ("🚁", "БПЛА (Воздух)"), ("→", ""), ("🧠", "ML (AI-Детекция)"), ("→", ""), ("🗺️", "ГИС (Слои)"), ("→", ""), ("🌿", "Эколог (Ущерб)"), ("→", ""), ("🤝", "Координатор (Действие)")]:
                                if s_name:
                                    frame:
                                        background Solid("#132847")
                                        padding (8, 4)
                                        text "[s_icon] [s_name]":
                                            size 12
                                            color "#00e6b8"
                                            bold True
                                else:
                                    text "[s_icon]":
                                        size 14
                                        color "#94a3b8"
                                        yalign 0.5

                    # Сетка 6 специалистов
                    grid 3 2:
                        spacing 12
                        xfill True
                        for sp in clean_state.specialties:
                            $ sp_done = clean_state.get_completed_tasks_count(sp.id)
                            frame:
                                background Frame(Solid("#102647"), 6, 6)
                                padding (14, 10)
                                vbox:
                                    spacing 5
                                    hbox:
                                        spacing 10
                                        text "[sp.icon]":
                                            size 22
                                        vbox:
                                            text "[sp.name]":
                                                size 15
                                                color "#ffffff"
                                                bold True
                                            text "[sp.short_title] • Задач сдано: [sp_done]/3":
                                                size 11
                                                color "#38bdf8"
                                    text "[sp.role_desc]":
                                        size 12
                                        color "#cbd5e1"
                                        line_spacing 2
                                    frame:
                                        background Solid("#07101f")
                                        padding (6, 3)
                                        xfill True
                                        text "Инструмент: [sp.tool_name]":
                                            size 10
                                            color "#f59e0b"

                                    textbutton "▶ Задачи специалиста (3) →":
                                        text_size 11
                                        text_color "#00e6b8"
                                        background Frame(Solid("#08172c"), 4, 4)
                                        hover_background Frame(Solid("#13365e"), 4, 4)
                                        xfill True
                                        ypadding 5
                                        action [Function(clean_state.set_specialty, sp.id), Show("clean_role_mission_screen")]
