## clean_analytics.rpy
## Экран аналитики компетенций и совместимости со специальностями проекта «Чистый берег» (14+)

init python:
    def analytics_start_role(spec_id):
        clean_state.set_specialty(spec_id)
        tasks = clean_state.get_tasks_for_specialty(spec_id)
        if tasks:
            first_incomplete = next((t for t in tasks if not t.completed), tasks[0])
            clean_state.start_role_mission(first_incomplete.id)
        renpy.show_screen("clean_role_mission_screen")
        renpy.restart_interaction()

screen clean_analytics_screen():
    tag clean_screen
    add Solid("#060d19")

    # Фоновое мягкое сияние
    add Solid("#0b1c3630"):
        xsize 1920
        ysize 1080

    $ ca = clean_state.career_analytics
    $ top_p = ca.get_top_profile()
    $ top_spec_id = ca.recommended_spec_id
    $ top_spec = clean_state.get_specialty_by_id(top_spec_id)
    $ top_aff = ca.get_affinity(top_spec_id)

    # ЦЕНТРАЛЬНЫЙ КОНТЕЙНЕР
    frame:
        xalign 0.5
        ypos 30
        xsize 1380
        ysize 1020
        background Frame(Solid("#09172c"), 16, 16)
        padding (36, 26)

        vbox:
            spacing 16
            xfill True

            # ВЕРХНИЙ ХЕДЕР
            hbox:
                xfill True
                yalign 0.5

                vbox:
                    spacing 2
                    text "📊 АНАЛИТИКА КОМПЕТЕНЦИЙ И ПРОФИЛЬ УЧАСТНИКА (14+)":
                        size 22
                        color "#ffffff"
                        bold True
                    text "Оценка профессиональных склонностей, точности решения задач и рекомендации для реальной карьеры":
                        size 12
                        color "#94a3b8"

                hbox:
                    spacing 12
                    yalign 0.5

                    button:
                        action Show("role_selection_entry_screen")
                        background Frame(Solid("#1e293b"), 10, 10)
                        hover_background Frame(Solid("#334155"), 10, 10)
                        padding (18, 8)
                        text "← К выбору ролей":
                            size 13
                            color "#cbd5e1"
                            bold True

                    if clean_state.all_specialties_completed():
                        button:
                            action Show("clean_certificate_screen")
                            background Frame(Solid("#d97706"), 10, 10)
                            hover_background Frame(Solid("#f59e0b"), 10, 10)
                            padding (18, 8)
                            text "🏆 К сертификату →":
                                size 13
                                color "#ffffff"
                                bold True

            # Разделитель
            frame:
                background Solid("#1e293b")
                xfill True
                ysize 2

            # БЛОК 1: ТОП-СПЕЦИАЛИЗАЦИЯ И СУПЕРСИЛА УЧАСТНИКА
            frame:
                background Frame(Solid("#0d213f"), 12, 12)
                padding (22, 18)
                xfill True

                hbox:
                    spacing 24
                    yalign 0.5

                    # Иконка и процент совместимости
                    vbox:
                        xsize 160
                        spacing 6
                        xalign 0.5
                        yalign 0.5

                        frame:
                            background Frame(Solid("#071224"), 14, 14)
                            padding (14, 10)
                            xalign 0.5
                            text "[top_spec.icon]":
                                size 44
                                xalign 0.5

                        frame:
                            background Frame(Solid(top_p["accent"]), 12, 12)
                            padding (10, 4)
                            xalign 0.5
                            text "[top_aff]% СОВПАДЕНИЕ":
                                size 11
                                color "#041122"
                                bold True
                                xalign 0.5

                    # Описание профиля и карьеры
                    vbox:
                        spacing 6
                        xsize 1100

                        hbox:
                            spacing 10
                            yalign 0.5
                            text "🌟 ТВОЯ ГЛАВНАЯ СПЕЦИАЛИЗАЦИЯ:":
                                size 13
                                color "#f59e0b"
                                bold True
                            frame:
                                background Frame(Solid("#1e293b"), 8, 8)
                                padding (8, 3)
                                text "[top_p['badge']]":
                                    size 11
                                    color "#38bdf8"
                                    bold True

                        text "[top_p['title']]":
                            size 21
                            color "#ffffff"
                            bold True

                        text "[top_p['traits']]":
                            size 13
                            color "#e2e8f0"
                            line_spacing 2

                        frame:
                            background Solid("#081528")
                            padding (12, 8)
                            xfill True
                            vbox:
                                spacing 4
                                text "💼 Профессии в будущем: [top_p['careers']]":
                                    size 12
                                    color "#00e6b8"
                                text "🎓 Где учиться: [top_p['study_majors']]":
                                    size 12
                                    color "#93c5fd"

            # БЛОК 2: СЕТКА СОВМЕСТИМОСТИ ПО ВСЕМ 6 СПЕЦИАЛЬНОСТЯМ
            vbox:
                spacing 8
                xfill True

                text "📈 КАРТА СОВМЕСТИМОСТИ ПО ВСЕМ 6 НАПРАВЛЕНИЯМ:":
                    size 13
                    color "#94a3b8"
                    bold True

                grid 2 3:
                    spacing 12
                    xfill True

                    for sp in clean_state.specialties:
                        $ aff = ca.get_affinity(sp.id)
                        $ is_top = (sp.id == top_spec_id)
                        $ sp_tasks_done = clean_state.get_completed_tasks_count(sp.id)
                        $ sp_tasks_correct = clean_state.get_correct_tasks_count(sp.id)
                        $ is_done = clean_state.is_specialty_completed(sp.id)

                        frame:
                            background Frame(Solid("#0c1c33" if not is_top else "#0f2648"), 10, 10)
                            padding (16, 12)
                            xsize 645
                            ysize 110

                            vbox:
                                spacing 6
                                xfill True

                                # Заголовок карточки
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "[sp.icon]":
                                            size 18
                                            yalign 0.5
                                        text "[sp.name]":
                                            size 14
                                            color ("#00e6b8" if is_top else "#ffffff")
                                            bold True
                                            yalign 0.5
                                        if is_top:
                                            frame:
                                                background Frame(Solid("#d97706"), 8, 8)
                                                padding (6, 2)
                                                text "★ ТОП-1":
                                                    size 9
                                                    color "#ffffff"
                                                    bold True

                                    # Процент совместимости
                                    text "[aff]%":
                                        size 16
                                        color ("#00e6b8" if aff >= 80 else ("#38bdf8" if aff >= 65 else "#94a3b8"))
                                        bold True
                                        yalign 0.5

                                # Прогресс-бар совместимости
                                frame:
                                    background Solid("#1e293b")
                                    xfill True
                                    ysize 8
                                    padding (0, 0)
                                    frame:
                                        background Solid("#00e6b8" if is_top else ("#38bdf8" if aff >= 70 else "#64748b"))
                                        xsize int(613 * (aff / 100.0))
                                        ysize 8

                                # Статус решения боевых задач
                                hbox:
                                    xfill True
                                    yalign 0.5

                                    if is_done:
                                        text "✔ 3/3 задач сдано (Направление освоено, верно: [sp_tasks_correct])":
                                            size 11
                                            color "#4ade80"
                                    elif sp_tasks_done > 0:
                                        text "⚡ Решено [sp_tasks_done]/3 задач (Верно: [sp_tasks_correct])":
                                            size 11
                                            color "#f59e0b"
                                    else:
                                        text "○ Миссии еще не начаты (0/3 задач)":
                                            size 11
                                            color "#64748b"

                                    if not is_done:
                                        $ btn_title = "Продолжить задачи (" + str(sp_tasks_done) + "/3) →" if sp_tasks_done > 0 else "Начать миссии →"
                                        textbutton btn_title:
                                            action Function(analytics_start_role, sp.id)
                                            text_size 11
                                            text_color ("#00e6b8" if sp_tasks_done > 0 else "#38bdf8")
                                            text_hover_color "#ffffff"
                                            yalign 0.5

            # НИЖНЯЯ ПАНЕЛЬ ДЕЙСТВИЙ
            hbox:
                spacing 16
                xalign 0.5
                yalign 0.5

                button:
                    action Show("clean_prologue_screen")
                    background Frame(Solid("#1e293b"), 10, 10)
                    hover_background Frame(Solid("#334155"), 10, 10)
                    padding (24, 12)
                    text "🔄 Пройти тест профориентации заново":
                        size 13
                        color "#94a3b8"

                button:
                    action Show("role_selection_entry_screen")
                    background Frame(Solid("#00e6b8"), 12, 12)
                    hover_background Frame(Solid("#38bdf8"), 12, 12)
                    padding (36, 12)
                    hbox:
                        spacing 8
                        yalign 0.5
                        text "🚀":
                            size 18
                            yalign 0.5
                        text "ПЕРЕЙТИ К ВЫБОРУ РОЛИ В ШТАБЕ →":
                            size 14
                            color "#041122"
                            bold True
                            yalign 0.5
