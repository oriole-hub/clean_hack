## clean_certificate.rpy
## Финальный наградной сертификат за полное прохождение всех 6 специальностей
## Включает статистику правильных и неправильных ответов в сумме и по каждому блоку

init python:
    import datetime

    def open_certificate_link():
        pass

    def download_certificate_pdf():
        pass

    def open_certificate_pdf_action():
        pass

    def reveal_certificate_folder_action():
        pass

screen clean_certificate_screen():
    tag clean_screen
    add Solid("#040913")

    # Фоновые световые акценты
    add Solid("#0b244733"):
        xsize 1920
        ysize 1080

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 14
        xsize 1200

        # ОСНОВНОЙ НАГРАДНОЙ БЛАНК СЕРТИФИКАТА
        frame:
            xalign 0.5
            xsize 1260
            background Frame(Solid("#09172c"), 16, 16)
            padding (40, 24)

            vbox:
                spacing 12
                xalign 0.5

                # 1. Шапка сертификата
                hbox:
                    xalign 0.5
                    spacing 16
                    text "⭐":
                        size 22
                        yalign 0.5
                    vbox:
                        xalign 0.5
                        spacing 2
                        text "ВСЕРОССИЙСКИЙ ПРОЕКТ ЦИФРОВОГО ЭКОМОНИТОРИНГА «ЧИСТЫЙ БЕРЕГ» (14+)":
                            size 13
                            color "#38bdf8"
                            bold True
                            xalign 0.5
                        text "ОФИЦИАЛЬНЫЙ НАГРАДНОЙ СЕРТИФИКАТ":
                            size 16
                            color "#94a3b8"
                            bold True
                            xalign 0.5
                    text "⭐":
                        size 22
                        yalign 0.5

                # Золотая разделительная линия
                frame:
                    background Solid("#f59e0b66")
                    xsize 1160
                    ysize 3
                    xalign 0.5

                # 2. ГЛАВНЫЙ НАГРАДНОЙ ТЕКСТ (НЕЙТРАЛЬНЫЙ И ПОЧЕТНЫЙ)
                text "СЕРТИФИКАТ ЭКО-ЭКСПЕРТА":
                    size 40
                    color "#f59e0b"
                    bold True
                    xalign 0.5

                text "ПОЗДРАВЛЯЕМ С УСПЕШНЫМ ЗАВЕРШЕНИЕМ ЭКСПЕДИЦИИ!":
                    size 16
                    color "#38bdf8"
                    bold True
                    xalign 0.5

                # 3. Текст поздравления и заслуг
                text "Настоящий сертификат подтверждает, что исследователь успешно освоил ВСЕ 6 профильных специальностей цифрового экологического мониторинга побережья озера Байкал и решил все 18 боевых миссий!":
                    size 14
                    color "#e2e8f0"
                    text_align 0.5
                    line_spacing 3
                    xalign 0.5
                    xsize 1100

                null height 4

                # 4. СТАТИСТИКА В КАЖДОМ БЛОКЕ (6 СПЕЦИАЛЬНОСТЕЙ)
                

                # 5. ИТОГОВАЯ СТАТИСТИКА В СУММЕ (ВСЕГО, ПРАВИЛЬНЫХ, НЕПРАВИЛЬНЫХ)
                frame:
                    xalign 0.5
                    xsize 1100
                    background Frame(Solid("#081528"), 12, 12)
                    padding (20, 8)

                    $ total_done = clean_state.get_total_completed_tasks()
                    $ total_cor = clean_state.get_total_correct_tasks()
                    $ total_incor = clean_state.get_total_incorrect_tasks()
                    $ total_all = clean_state.get_total_tasks_count()
                    $ total_acc = int((float(total_cor) / float(total_done)) * 100) if total_done > 0 else 100

                    hbox:
                        xalign 0.5
                        spacing 36

                        # Колонка 1: Опыт
                        vbox:
                            spacing 1
                            xalign 0.5
                            text "НАБРАННЫЙ ЭКО-ОПЫТ":
                                size 10
                                color "#94a3b8"
                                bold True
                                xalign 0.5
                            text "[clean_state.user_xp] XP":
                                size 20
                                color "#00e6b8"
                                bold True
                                xalign 0.5

                        frame:
                            xsize 1
                            ysize 36
                            background Solid("#1e3a5f")
                            yalign 0.5

                        # Колонка 2: Решено задач
                        vbox:
                            spacing 1
                            xalign 0.5
                            text "РЕШЕНО ЗАДАЧ":
                                size 10
                                color "#94a3b8"
                                bold True
                                xalign 0.5
                            text "[total_done] из [total_all]":
                                size 20
                                color "#38bdf8"
                                bold True
                                xalign 0.5

                        frame:
                            xsize 1
                            ysize 36
                            background Solid("#1e3a5f")
                            yalign 0.5

                        # Колонка 3: Правильных в сумме
                        vbox:
                            spacing 1
                            xalign 0.5
                            text "ПРАВИЛЬНЫХ В СУММЕ":
                                size 10
                                color "#4ade80"
                                bold True
                                xalign 0.5
                            text "✅ [total_cor] ([total_acc]%)":
                                size 20
                                color "#4ade80"
                                bold True
                                xalign 0.5

                        frame:
                            xsize 1
                            ysize 36
                            background Solid("#1e3a5f")
                            yalign 0.5

                        # Колонка 4: Неправильных в сумме
                        vbox:
                            spacing 1
                            xalign 0.5
                            text "ОШИБОК В СУММЕ":
                                size 10
                                color ("#f87171" if total_incor > 0 else "#94a3b8")
                                bold True
                                xalign 0.5
                            text ("❌ [total_incor]" if total_incor > 0 else "✓ 0"):
                                size 20
                                color ("#f87171" if total_incor > 0 else "#94a3b8")
                                bold True
                                xalign 0.5

                        frame:
                            xsize 1
                            ysize 36
                            background Solid("#1e3a5f")
                            yalign 0.5

                        # Колонка 5: Ранг
                        vbox:
                            spacing 1
                            xalign 0.5
                            text "ПРИСВОЕННЫЙ РАНГ":
                                size 10
                                color "#f59e0b"
                                bold True
                                xalign 0.5
                            text "Главный Эксперт":
                                size 18
                                color "#f59e0b"
                                bold True
                                xalign 0.5

                # 6. Регистрационные данные сертификата
                $ cert_date = datetime.datetime.now().strftime("%d.%m.%Y")
                hbox:
                    xalign 0.5
                    spacing 24
                    text "Дата выдачи: [cert_date]":
                        size 14
                        color "#64748b"
                    text "•":
                        size 14
                        color "#334155"
                    text "Регистрационный номер: CB-2026-8891":
                        size 14
                        color "#64748b"
                    text "•":
                        size 14
                        color "#334155"
                    text "Цифровой реестр проекта «Чистый берег»":
                        size 14
                        color "#64748b"

        # 7. БЛОК КНОПОК ДЕЙСТВИЙ (БЕЗ PDF, БЕЗ НАЛОЖЕНИЙ)
        vbox:
            xalign 0.5
            spacing 8

            hbox:
                xalign 0.5
                spacing 16

                # Кнопка: Аналитика профиля
                button:
                    xsize 520
                    ysize 50
                    background Frame(Solid("#059669"), 12, 12)
                    hover_background Frame(Solid("#10b981"), 12, 12)
                    padding (20, 10)
                    action Show("clean_analytics_screen")

                    hbox:
                        spacing 12
                        xalign 0.5
                        yalign 0.5
                        text "📊":
                            size 20
                            yalign 0.5
                        text "ПОДРОБНАЯ АНАЛИТИКА ПРОФИЛЯ →":
                            size 15
                            color "#ffffff"
                            bold True
                            yalign 0.5

                # Кнопка: К специальностям
                button:
                    xsize 380
                    ysize 50
                    background Frame(Solid("#0d2847"), 12, 12)
                    hover_background Frame(Solid("#1e40af"), 12, 12)
                    padding (20, 10)
                    action Show("role_selection_entry_screen")

                    hbox:
                        spacing 10
                        xalign 0.5
                        yalign 0.5
                        text "↩":
                            size 16
                            yalign 0.5
                        text "К специальностям":
                            size 15
                            color "#38bdf8"
                            bold True
                            yalign 0.5

                # Кнопка: Продолжить — перейти на сайт проекта «Чистый берег»
                button:
                    xsize 320
                    ysize 50
                    background Frame(Solid("#0369a1"), 12, 12)
                    hover_background Frame(Solid("#0284c7"), 12, 12)
                    padding (20, 10)
                    action OpenURL("https://защитиприроду.рф/chistyi-bereg#media")

                    hbox:
                        spacing 10
                        xalign 0.5
                        yalign 0.5
                        text "🌊":
                            size 18
                            yalign 0.5
                        text "ПРОДОЛЖИТЬ →":
                            size 15
                            color "#ffffff"
                            bold True
                            yalign 0.5

            text "💡 Нажмите «Продолжить», чтобы узнать больше о проекте «Чистый берег» и присоединиться к эко-экспедициям!":
                size 12
                color "#64748b"
                xalign 0.5
