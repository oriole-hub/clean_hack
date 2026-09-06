## clean_prologue.rpy
## Интерактивный пролог и экспресс-тест профориентации проекта «Чистый берег» (14+)

init python:
    class PrologueManager(object):
        def __init__(self):
            self.current_slide = 0
            self.total_slides = 4
            self.quiz_step = 0 # 0, 1, 2 = вопросы; 3 = результат

        def next_slide(self):
            if self.current_slide < self.total_slides - 1:
                self.current_slide += 1
            else:
                self.finish_prologue()
            renpy.restart_interaction()

        def prev_slide(self):
            if self.current_slide > 0:
                self.current_slide -= 1
            renpy.restart_interaction()

        def set_slide(self, idx):
            if 0 <= idx < self.total_slides:
                self.current_slide = idx
            renpy.restart_interaction()

        def answer_quiz(self, spec_id):
            clean_state.career_analytics.record_quiz_answer(spec_id, 35)
            self.quiz_step += 1
            renpy.restart_interaction()

        def reset_quiz(self):
            self.quiz_step = 0
            renpy.restart_interaction()

        def finish_prologue(self):
            renpy.show_screen("role_selection_entry_screen")
            renpy.restart_interaction()

        def start_with_recommended(self):
            rec_id = clean_state.career_analytics.recommended_spec_id
            clean_state.set_specialty(rec_id)
            tasks = clean_state.get_tasks_for_specialty(rec_id)
            if tasks:
                clean_state.start_role_mission(tasks[0].id)
            renpy.show_screen("clean_role_mission_screen")
            renpy.restart_interaction()

    clean_prologue_mgr = PrologueManager()

    def prologue_go_to_roles():
        clean_prologue_mgr.finish_prologue()

screen clean_prologue_screen():
    tag clean_screen
    add Solid("#060d19")

    # Фоновое мягкое сияние
    add Solid("#0b1c3635"):
        xsize 1920
        ysize 1080

    $ cur = clean_prologue_mgr.current_slide

    # ЦЕНТРАЛЬНЫЙ КОНТЕЙНЕР
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1380
        ysize 920
        background Frame(Solid("#09172c"), 16, 16)
        padding (40, 30)

        viewport:
            scrollbars None
            draggable True
            mousewheel True
            xfill True
            yfill True

            vbox:
                spacing 18
                xfill True

            # ВЕРХНЯЯ СТРОКА: ИНДИКАТОР 4 ЭТАПОВ И КНОПКА ПРОПУСКА
            hbox:
                xfill True
                yalign 0.5

                # Индикаторы этапов
                hbox:
                    spacing 10
                    yalign 0.5

                    # Шаг 1
                    button:
                        action Function(clean_prologue_mgr.set_slide, 0)
                        background Frame(Solid("#00e6b8" if cur == 0 else ("#1e293b" if cur > 0 else "#0f223d")), 14, 14)
                        padding (12, 6)
                        text "1. ЧП на побережье":
                            size 11
                            color ("#041122" if cur == 0 else "#94a3b8")
                            bold True

                    text "→":
                        size 12
                        color "#475569"
                        yalign 0.5

                    # Шаг 2
                    button:
                        action Function(clean_prologue_mgr.set_slide, 1)
                        background Frame(Solid("#00e6b8" if cur == 1 else ("#1e293b" if cur > 1 else "#0f223d")), 14, 14)
                        padding (12, 6)
                        text "2. Технологии штаба":
                            size 11
                            color ("#041122" if cur == 1 else "#94a3b8")
                            bold True

                    text "→":
                        size 12
                        color "#475569"
                        yalign 0.5

                    # Шаг 3
                    button:
                        action Function(clean_prologue_mgr.set_slide, 2)
                        background Frame(Solid("#00e6b8" if cur == 2 else ("#1e293b" if cur > 2 else "#0f223d")), 14, 14)
                        padding (12, 6)
                        text "3. Твоя миссия":
                            size 11
                            color ("#041122" if cur == 2 else "#94a3b8")
                            bold True

                    text "→":
                        size 12
                        color "#475569"
                        yalign 0.5

                    # Шаг 4: Тест профориентации
                    button:
                        action Function(clean_prologue_mgr.set_slide, 3)
                        background Frame(Solid("#f59e0b" if cur == 3 else "#0f223d"), 14, 14)
                        padding (12, 6)
                        text "🎯 4. Тест профориентации":
                            size 11
                            color ("#041122" if cur == 3 else "#f59e0b")
                            bold True

                # Кнопка пропуска пролога
                textbutton "Пропустить в штаб ⏩":
                    action Function(prologue_go_to_roles)
                    text_size 13
                    text_color "#64748b"
                    text_hover_color "#00e6b8"
                    xalign 1.0
                    yalign 0.5

            # Разделительная линия
            frame:
                background Solid("#1e293b")
                xfill True
                ysize 2

            # =====================================================================
            # СЛАЙД 0: ЧП НА ПОБЕРЕЖЬЕ (ЧТО СЛУЧИЛОСЬ?)
            # =====================================================================
            if cur == 0:
                hbox:
                    spacing 32
                    xfill True

                    vbox:
                        spacing 12
                        xsize 540
                        frame:
                            xsize 540
                            ysize 304
                            padding (0, 0)
                            background Solid("#030712")
                            add "images/satellite/level2_after.png":
                                xsize 540
                                ysize 304
                                fit "cover"

                        frame:
                            background Frame(Solid("#450a0a"), 8, 8)
                            padding (16, 12)
                            xfill True
                            vbox:
                                spacing 4
                                text "🚨 СТАТУС: ЧРЕЗВЫЧАЙНАЯ ЭКО-СИТУАЦИЯ":
                                    size 12
                                    color "#ef4444"
                                    bold True
                                text "Штормовой прибой вынес тонны отходов в заповедную акваторию. Затронуто более 15 км берега.":
                                    size 12
                                    color "#fca5a5"
                                    line_spacing 2

                    vbox:
                        spacing 14
                        xsize 720

                        frame:
                            background Frame(Solid("#00e6b820"), 12, 12)
                            padding (12, 6)
                            text "🌊 ВВОДНЫЙ ИНСТРУКТАЖ • БАЛТИЙСКОЕ ПОБЕРЕЖЬЕ":
                                size 11
                                color "#00e6b8"
                                bold True

                        text "Шторм выбросил на заповедный берег тонны опасного мусора!":
                            size 24
                            color "#ffffff"
                            bold True
                            line_spacing 3

                        text "На днях по региону ударил мощный шторм. Волны высотой до пяти метров размыли стихийные свалки и вынесли на чистейшие песчаные косы тонны отходов.\n\nПрямо сейчас под угрозой уникальные песчаные дюны и заповедные лагуны. На берег выбросило сотни пластиковых бутылок, старые автомобильные шины, полуразрушенные бочки с мазутом и обрывки гигантских рыболовных сетей.":
                            size 14
                            color "#cbd5e1"
                            line_spacing 5

                        frame:
                            background Frame(Solid("#0f223d"), 10, 10)
                            padding (18, 14)
                            xfill True
                            vbox:
                                spacing 6
                                text "⚠️ ПОЧЕМУ ЭТО ОПАСНО ДЛЯ ЖИВОТНЫХ?":
                                    size 12
                                    color "#f59e0b"
                                    bold True
                                text "• Брошенные сети становятся «ловушками-призраками» — в них путаются и гибнут краснокнижные кольчатые нерпы и морские птицы.\n• Мазут покрывает перья птиц и отравляет планктон и рыбу.\n• Если не убрать мусор до следующего прилива, волны снова унесут его в море, превратив в ядовитый микропластик.":
                                    size 13
                                    color "#e2e8f0"
                                    line_spacing 4

            # =====================================================================
            # СЛАЙД 1: ТЕХНОЛОГИИ ШТАБА (КАК МЫ ДЕЙСТВУЕМ?)
            # =====================================================================
            elif cur == 1:
                hbox:
                    spacing 32
                    xfill True

                    vbox:
                        spacing 12
                        xsize 540
                        frame:
                            xsize 540
                            ysize 304
                            padding (0, 0)
                            background Solid("#030712")
                            add "images/satellite/level3_ortho.png":
                                xsize 540
                                ysize 304
                                fit "cover"

                        frame:
                            background Frame(Solid("#064e3b"), 8, 8)
                            padding (16, 12)
                            xfill True
                            vbox:
                                spacing 4
                                text "⚡ СИСТЕМА «ЧИСТЫЙ БЕРЕГ»: ПОЛНЫЙ ЦИКЛ":
                                    size 12
                                    color "#10b981"
                                    bold True
                                text "Космос → Аэроразведка дронами → ИИ-анализ → Интерактивные карты → Молодежный десант.":
                                    size 12
                                    color "#a7f3d0"
                                    line_spacing 2

                    vbox:
                        spacing 14
                        xsize 720

                        frame:
                            background Frame(Solid("#38bdf820"), 12, 12)
                            padding (12, 6)
                            text "🛰️ НАСТОЯЩИЙ HI-TECH НА ЗАЩИТЕ ПРИРОДЫ":
                                size 11
                                color "#38bdf8"
                                bold True

                        text "«Чистый берег» — это не просто уборка, а высокие технологии!":
                            size 24
                            color "#ffffff"
                            bold True
                            line_spacing 3

                        text "Обойти пешком сотни километров побережий невозможно. Поэтому наш штаб объединил передовые цифровые инструменты в единую умную цепочку:":
                            size 14
                            color "#cbd5e1"
                            line_spacing 4

                        vbox:
                            spacing 8
                            xfill True

                            frame:
                                background Frame(Solid("#0f223d"), 8, 8)
                                padding (14, 10)
                                hbox:
                                    spacing 12
                                    text "🛰️":
                                        size 22
                                    vbox:
                                        spacing 2
                                        text "Спутники Sentinel и Landsat":
                                            size 13
                                            color "#38bdf8"
                                            bold True
                                        text "Следят за акваторией из космоса и видят тончайшие нефтяные пленки через инфракрасные датчики.":
                                            size 12
                                            color "#94a3b8"

                            frame:
                                background Frame(Solid("#0f223d"), 8, 8)
                                padding (14, 10)
                                hbox:
                                    spacing 12
                                    text "🚁":
                                        size 22
                                    vbox:
                                        spacing 2
                                        text "Беспилотники и дроны":
                                            size 13
                                            color "#00e6b8"
                                            bold True
                                        text "Летают над скалами и песком на высоте 80м, создавая детальные ортофотопланы с точностью до 2 см на пиксель.":
                                            size 12
                                            color "#94a3b8"

                            frame:
                                background Frame(Solid("#0f223d"), 8, 8)
                                padding (14, 10)
                                hbox:
                                    spacing 12
                                    text "🧠":
                                        size 22
                                    vbox:
                                        spacing 2
                                        text "Искусственный интеллект (YOLOv8)":
                                            size 13
                                            color "#f59e0b"
                                            bold True
                                        text "Нейросеть мгновенно отсматривает тысячи кадров и обводит пластик и опасные сети рамками за доли секунды.":
                                            size 12
                                            color "#94a3b8"

            # =====================================================================
            # СЛАЙД 2: ТВОЯ МИССИЯ (ПРАВИЛА И 6 НАПРАВЛЕНИЙ)
            # =====================================================================
            elif cur == 2:
                hbox:
                    spacing 32
                    xfill True

                    vbox:
                        spacing 12
                        xsize 540
                        frame:
                            xsize 540
                            ysize 304
                            padding (0, 0)
                            background Solid("#030712")
                            add "images/challenge/photo_plastic.png":
                                xsize 540
                                ysize 304
                                fit "cover"

                        frame:
                            background Frame(Solid("#d97706"), 8, 8)
                            padding (16, 12)
                            xfill True
                            vbox:
                                spacing 4
                                text "🏆 ФИНАЛЬНАЯ НАГРАДА: СЕРТИФИКАТ ЭКСПЕРТА":
                                    size 12
                                    color "#ffffff"
                                    bold True
                                text "Успешно пройди испытания во всех 6 направлениях и получи официальный наградной сертификат эксперта!":
                                    size 12
                                    color "#fef3c7"
                                    line_spacing 2

                    vbox:
                        spacing 14
                        xsize 720

                        frame:
                            background Frame(Solid("#10b98120"), 12, 12)
                            padding (12, 6)
                            text "🎯 ТВОЯ БОЕВАЯ ЗАДАЧА В ЭКСПЕДИЦИИ":
                                size 11
                                color "#10b981"
                                bold True

                        text "Примерь на себя 6 реальных профессий будущего!":
                            size 24
                            color "#ffffff"
                            bold True
                            line_spacing 3

                        text "Ты вступаешь в команду оперативного реагирования. Тебе предстоит решить по 3 прикладные задачи в каждой из 6 специальностей:":
                            size 14
                            color "#cbd5e1"
                            line_spacing 4

                        grid 2 3:
                            spacing 8
                            xfill True

                            frame:
                                background Frame(Solid("#0f223d"), 6, 6)
                                padding (10, 8)
                                text "🛰️ Специалист ДЗЗ: найди разлив с орбиты":
                                    size 12
                                    color "#38bdf8"
                                    bold True

                            frame:
                                background Frame(Solid("#0f223d"), 6, 6)
                                padding (10, 8)
                                text "🗺️ ГИС-аналитик: рассчитай площадь свалки":
                                    size 12
                                    color "#00e6b8"
                                    bold True

                            frame:
                                background Frame(Solid("#0f223d"), 6, 6)
                                padding (10, 8)
                                text "🧠 ML-инженер: настрой зрение нейросети":
                                    size 12
                                    color "#f59e0b"
                                    bold True

                            frame:
                                background Frame(Solid("#0f223d"), 6, 6)
                                padding (10, 8)
                                text "🌿 Эколог: спаси нерпу от сетей-ловушек":
                                    size 12
                                    color "#4ade80"
                                    bold True

                            frame:
                                background Frame(Solid("#0f223d"), 6, 6)
                                padding (10, 8)
                                text "🚁 Пилот дрона: спланируй полет БПЛА":
                                    size 12
                                    color "#a855f7"
                                    bold True

                            frame:
                                background Frame(Solid("#0f223d"), 6, 6)
                                padding (10, 8)
                                text "🤝 Координатор: отправь пластик на завод":
                                    size 12
                                    color "#fb7185"
                                    bold True

                        frame:
                            background Frame(Solid("#1e1b4b"), 8, 8)
                            padding (14, 10)
                            xfill True
                            hbox:
                                spacing 10
                                yalign 0.5
                                text "⚡":
                                    size 20
                                    yalign 0.5
                                text "Правила честные и строгие: задачи выполняются без пересдач. Когда ты пройдешь все 3 задачи специальности, она блокируется, а ты переходишь к следующей.":
                                    size 12
                                    color "#c7d2fe"
                                    line_spacing 2

            # =====================================================================
            # СЛАЙД 3: ЭКСПРЕСС-ТЕСТ ПРОФОРИЕНТАЦИИ (ОПРЕДЕЛЕНИЕ ПРОФИЛЯ)
            # =====================================================================
            elif cur == 3:
                $ q_step = clean_prologue_mgr.quiz_step
                $ ca = clean_state.career_analytics
                $ rec_id = ca.recommended_spec_id
                $ rec_spec = clean_state.get_specialty_by_id(rec_id)
                $ rec_p = ca.get_top_profile()

                if q_step < 3:
                    # РЕЖИМ ВОПРОСОВ (1 из 3, 2 из 3, 3 из 3)
                    vbox:
                        spacing 14
                        xfill True

                        # Шапка вопроса
                        hbox:
                            xfill True
                            yalign 0.5
                            frame:
                                background Frame(Solid("#f59e0b25"), 12, 12)
                                padding (14, 6)
                                text "❓ ЭКСПРЕСС-ТЕСТ ПРОФОРИЕНТАЦИИ • ВОПРОС [q_step + 1] ИЗ 3":
                                    size 12
                                    color "#f59e0b"
                                    bold True

                            textbutton "Пропустить тест в каталог ⏩":
                                action Function(prologue_go_to_roles)
                                text_size 12
                                text_color "#64748b"
                                text_hover_color "#00e6b8"
                                yalign 0.5

                        # Вопрос
                        if q_step == 0:
                            text "Что тебя больше всего привлекает в исследовательской экспедиции?":
                                size 22
                                color "#ffffff"
                                bold True
                        elif q_step == 1:
                            text "Какой технологический инструмент ты хочешь освоить в первую очередь?":
                                size 22
                                color "#ffffff"
                                bold True
                        else:
                            text "В чем твоя главная сильная сторона и суперсила?":
                                size 22
                                color "#ffffff"
                                bold True

                        text "Кликни на вариант, который тебе ближе всего — мы подберем идеальную стартовую роль:":
                            size 13
                            color "#94a3b8"

                        null height 2

                        # Сетка 6 вариантов для текущего вопроса
                        grid 2 3:
                            spacing 12
                            xfill True

                            if q_step == 0:
                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "dzz")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🛰️ Смотреть на Землю из космоса и находить скрытые аномалии":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "gis")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🗺️ Работать с цифровыми картами, координатами и границами":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "ml")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🧠 Обучать нейросети и создавать искусственный интеллект":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "ecologist")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🌿 Защищать дикую природу, спасать редких животных и птиц":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "uav")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🚁 Пилотировать дроны и делать суперчеткую аэросъемку 4K":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "volunteer_coord")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🤝 Командовать десантом волонтеров и внедрять Zero Waste":
                                        size 13
                                        color "#ffffff"

                            elif q_step == 1:
                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "dzz")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🛰️ Инфракрасный спектральный фильтр спутника Sentinel":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "gis")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🗺️ Геодезический навигатор и цифровую систему QGIS":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "ml")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🧠 Нейросетевой сканер компьютерного зрения YOLOv8":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "ecologist")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🌿 Экопаспорт токсичности и снаряжение помощи фауне":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "uav")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🚁 Авиагоризонт HUD и автопилот полетных галсов дрона":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "volunteer_coord")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🤝 Тактический маршрутный лист десанта и Zero Waste план":
                                        size 13
                                        color "#ffffff"

                            else:
                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "dzz")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🛰️ Внимательность к деталям и глобальное мышление":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "gis")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🗺️ Пространственное воображение и математическая точность":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "ml")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🧠 Математическая логика и алгоритмический склад ума":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "ecologist")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🌿 Чуткость к природе, сострадание и эко-интуиция":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "uav")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🚁 Хладнокровие, быстрая реакция и любовь к технике":
                                        size 13
                                        color "#ffffff"

                                button:
                                    action Function(clean_prologue_mgr.answer_quiz, "volunteer_coord")
                                    background Frame(Solid("#0d2038"), 8, 8)
                                    hover_background Frame(Solid("#1e40af"), 8, 8)
                                    padding (18, 14)
                                    xfill True
                                    text "🤝 Лидерская харизма, энергия и организаторский талант":
                                        size 13
                                        color "#ffffff"

                else:
                    # РЕЖИМ РЕЗУЛЬТАТОВ ТЕСТА
                    vbox:
                        spacing 16
                        xfill True

                        hbox:
                            spacing 12
                            yalign 0.5
                            frame:
                                background Frame(Solid("#10b98125"), 12, 12)
                                padding (14, 6)
                                text "🏆 ТЕСТ ЗАВЕРШЕН • ТВОЙ ИДЕАЛЬНЫЙ ПРОФИЛЬ ОПРЕДЕЛЕН!":
                                    size 12
                                    color "#10b981"
                                    bold True

                        # Карточка топ-рекомендации
                        frame:
                            background Frame(Solid("#0d213f"), 12, 12)
                            padding (24, 20)
                            xfill True

                            hbox:
                                spacing 24
                                yalign 0.5

                                vbox:
                                    spacing 6
                                    xsize 140
                                    frame:
                                        background Frame(Solid("#071224"), 14, 14)
                                        padding (14, 10)
                                        xalign 0.5
                                        text "[rec_spec.icon]":
                                            size 44
                                            xalign 0.5

                                    frame:
                                        background Frame(Solid(rec_p["accent"]), 10, 10)
                                        padding (8, 4)
                                        xalign 0.5
                                        text "★ ТОП-1":
                                            size 11
                                            color "#041122"
                                            bold True
                                            xalign 0.5

                                vbox:
                                    spacing 6
                                    xsize 1120

                                    hbox:
                                        spacing 10
                                        yalign 0.5
                                        text "РЕКОМЕНДОВАННАЯ СПЕЦИАЛЬНОСТЬ ДЛЯ СТАРТА:":
                                            size 12
                                            color "#f59e0b"
                                            bold True
                                        frame:
                                            background Frame(Solid("#1e293b"), 6, 6)
                                            padding (8, 3)
                                            text "[rec_p['badge']]":
                                                size 11
                                                color "#38bdf8"
                                                bold True

                                    text "[rec_spec.name] ([rec_spec.short_title])":
                                        size 22
                                        color "#ffffff"
                                        bold True

                                    text "[rec_p['traits']]":
                                        size 13
                                        color "#cbd5e1"
                                        line_spacing 2

                                    text "💼 Карьера в будущем: [rec_p['careers']]":
                                        size 12
                                        color "#00e6b8"

                        null height 2

                        # Кнопки действия по результатам
                        hbox:
                            spacing 16
                            xalign 0.5

                            button:
                                action Function(clean_prologue_mgr.start_with_recommended)
                                background Frame(Solid("#00e6b8"), 12, 12)
                                hover_background Frame(Solid("#38bdf8"), 12, 12)
                                padding (34, 14)
                                hbox:
                                    spacing 10
                                    yalign 0.5
                                    text "🚀":
                                        size 22
                                        yalign 0.5
                                    text "НАЧАТЬ ЭКСПЕДИЦИЮ С «[rec_spec.short_title.upper()]» →":
                                        size 15
                                        color "#041122"
                                        bold True
                                        yalign 0.5

                            button:
                                action Function(prologue_go_to_roles)
                                background Frame(Solid("#1e293b"), 12, 12)
                                hover_background Frame(Solid("#334155"), 12, 12)
                                padding (26, 14)
                                text "👥 Посмотреть все 6 специальностей →":
                                    size 14
                                    color "#ffffff"
                                    bold True
                                    yalign 0.5

                            button:
                                action Function(clean_prologue_mgr.reset_quiz)
                                background Frame(Solid("#081224"), 12, 12)
                                hover_background Frame(Solid("#1e293b"), 12, 12)
                                padding (20, 14)
                                text "🔄 Пройти тест заново":
                                    size 13
                                    color "#94a3b8"
                                    yalign 0.5

            null height 6

            # НИЖНЯЯ ПАНЕЛЬ НАВИГАЦИИ СЛАЙДЕРА
            hbox:
                xfill True
                yalign 0.5

                # Кнопка назад
                if cur > 0:
                    button:
                        action Function(clean_prologue_mgr.prev_slide)
                        background Frame(Solid("#1e293b"), 12, 12)
                        hover_background Frame(Solid("#334155"), 12, 12)
                        padding (24, 12)
                        text "← Назад":
                            size 14
                            color "#cbd5e1"
                            bold True
                else:
                    null width 100

                # Центральные индикаторы-точки (4 точки)
                hbox:
                    xalign 0.5
                    spacing 10
                    yalign 0.5

                    for i in range(4):
                        button:
                            action Function(clean_prologue_mgr.set_slide, i)
                            background Solid("#00e6b8" if cur == i else "#334155")
                            xsize (28 if cur == i else 10)
                            ysize 10

                # Правая кнопка действия
                if cur == 0:
                    button:
                        action Function(clean_prologue_mgr.next_slide)
                        background Frame(Solid("#00e6b8"), 12, 12)
                        hover_background Frame(Solid("#38bdf8"), 12, 12)
                        padding (28, 12)
                        text "Далее: К технологиям штаба →":
                            size 14
                            color "#041122"
                            bold True
                elif cur == 1:
                    button:
                        action Function(clean_prologue_mgr.next_slide)
                        background Frame(Solid("#00e6b8"), 12, 12)
                        hover_background Frame(Solid("#38bdf8"), 12, 12)
                        padding (28, 12)
                        text "Далее: К твоей миссии →":
                            size 14
                            color "#041122"
                            bold True
                elif cur == 2:
                    button:
                        action Function(clean_prologue_mgr.next_slide)
                        background Frame(Solid("#f59e0b"), 12, 12)
                        hover_background Frame(Solid("#fbbf24"), 12, 12)
                        padding (28, 12)
                        hbox:
                            spacing 8
                            yalign 0.5
                            text "🎯":
                                size 18
                                yalign 0.5
                            text "ЭКСПРЕСС-ТЕСТ ПРОФОРИЕНТАЦИИ →":
                                size 14
                                color "#041122"
                                bold True
                                yalign 0.5
                else:
                    button:
                        action Function(prologue_go_to_roles)
                        background Frame(Solid("#10b981"), 12, 12)
                        hover_background Frame(Solid("#34d399"), 12, 12)
                        padding (28, 12)
                        hbox:
                            spacing 8
                            yalign 0.5
                            text "🚀":
                                size 18
                                yalign 0.5
                            text "В ШТАБ! К ВЫБОРУ РОЛИ →":
                                size 14
                                color "#041122"
                                bold True
                                yalign 0.5
