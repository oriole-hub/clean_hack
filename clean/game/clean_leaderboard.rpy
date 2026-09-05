## clean_leaderboard.rpy
## Экран рейтинга и таблицы лидеров (Этап 8)

screen clean_leaderboard_screen():
    tag clean_screen
    add Solid("#070f1e")

    use clean_top_bar(active_tab="rating")

    $ player_pts = clean_state.gis_mgr.player_points if clean_state.gis_mgr.player_points > 0 else 1248
    $ player_time = clean_state.gis_mgr.total_time_str if clean_state.gis_mgr.total_time_str != "00:00" else "01:18"
    $ player_spec_label = clean_state.active_specialty.icon + " " + clean_state.active_specialty.name
    $ all_ranks = clean_state.leaderboard.get_all(player_pts=player_pts, player_time=player_time, player_specialty=player_spec_label)

    vbox:
        xalign 0.5
        ypos 110
        spacing 20
        xsize 1300

        # ВЕРХНИЙ БАННЕР ИГРОКА (Этап 8: «🥇 1 248 очков. Ты вошёл в топ-10%.»)
        frame:
            background Frame(Solid("#0e1e38"), 12, 12)
            padding (35, 20)
            xfill True

            hbox:
                spacing 35
                yalign 0.5

                vbox:
                    spacing 5
                    text "ВАШ ТЕКУЩИЙ РЕЗУЛЬТАТ:":
                        size 14
                        color "#94a3b8"
                        bold True
                    text "🥇 [player_pts] очков":
                        size 36
                        color "#00e6b8"
                        bold True

                # Разделитель
                add Solid("#1e293b"):
                    xsize 2
                    ysize 70

                vbox:
                    spacing 4
                    text "СТАТУС КВАЛИФИКАЦИИ:":
                        size 14
                        color "#94a3b8"
                    text "Ты вошёл в топ-10% исследователей!":
                        size 22
                        color "#f59e0b"
                        bold True

                add Solid("#1e293b"):
                    xsize 2
                    ysize 70

                hbox:
                    spacing 30
                    vbox:
                        text "Время:":
                            size 14
                            color "#94a3b8"
                        text "[player_time]":
                            size 20
                            color "#ffffff"
                            bold True
                    vbox:
                        text "Точность:":
                            size 14
                            color "#94a3b8"
                        text "92%":
                            size 20
                            color "#38bdf8"
                            bold True
                    vbox:
                        text "Ранг:":
                            size 14
                            color "#94a3b8"
                        text "#3 в регионе":
                            size 20
                            color "#22c55e"
                            bold True

        # ТАБЛИЦА ЛИДЕРОВ
        frame:
            background Frame(Solid("#0a162a"), 10, 10)
            padding (25, 20)
            xfill True

            vbox:
                spacing 12

                # Заголовок таблицы
                hbox:
                    xfill True
                    text "МЕСТО / ИГРОК":
                        size 14
                        color "#64748b"
                        xsize 480
                        bold True
                    text "ОЧКИ":
                        size 14
                        color "#64748b"
                        xsize 200
                        bold True
                    text "ЛУЧШЕЕ ВРЕМЯ":
                        size 14
                        color "#64748b"
                        xsize 220
                        bold True
                    text "ТОЧНОСТЬ":
                        size 14
                        color "#64748b"
                        xsize 180
                        bold True

                add Solid("#1e293b"):
                    xsize 1250
                    ysize 2

                # Строки таблицы
                for item in all_ranks[:7]:
                    $ row_bg = "#132847" if item.is_player else "#0d1a30"
                    $ text_col = "#00e6b8" if item.is_player else "#ffffff"
                    frame:
                        background Frame(Solid(row_bg), 6, 6)
                        padding (15, 12)
                        xfill True

                        hbox:
                            xfill True
                            hbox:
                                xsize 480
                                spacing 15
                                if item.rank == 1:
                                    text "🥇":
                                        size 20
                                elif item.rank == 2:
                                    text "🥈":
                                        size 20
                                elif item.rank == 3:
                                    text "🥉":
                                        size 20
                                else:
                                    text "[item.rank]":
                                        size 18
                                        color "#94a3b8"
                                        xsize 25

                                vbox:
                                    spacing 2
                                    text "[item.name]":
                                        size 17
                                        color text_col
                                        bold item.is_player
                                    text "[item.specialty]":
                                        size 12
                                        color "#38bdf8"

                            text "[item.points] XP":
                                size 18
                                color "#38bdf8"
                                bold True
                                xsize 200

                            text "[item.time_str]":
                                size 17
                                color "#cbd5e1"
                                xsize 220

                            text "[item.accuracy]":
                                size 17
                                color "#22c55e"
                                bold True
                                xsize 180

        # Кнопки внизу
        hbox:
            spacing 20
            xalign 0.5
            textbutton "← Пройти тренажер заново":
                text_size 16
                text_color "#cbd5e1"
                background Frame(Solid("#1e293b"), 6, 6)
                xpadding 25
                ypadding 12
                action [Function(clean_state.gis_mgr.start_game), Show("gis_play_screen")]

            textbutton "Перейти к Челленджам Чистого берега →":
                text_size 16
                text_color "#070f1e"
                text_bold True
                background Frame(Solid("#00e6b8"), 6, 6)
                hover_background Frame(Solid("#38bdf8"), 6, 6)
                xpadding 30
                ypadding 12
                action Show("challenge_catalog_screen")
