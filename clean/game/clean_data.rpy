## clean_data.rpy
## Модели данных, специальности, состояние игры и бизнес-логика проекта «Чистый берег»

init -1 python:
    import time
    import math

    class Specialty(object):
        """
        Профильная специальность проекта «Чистый берег»:
        1. Специалист ДЗЗ
        2. GIS-специалист
        3. Мл. инженер (ML/AI)
        4. Эколог
        5. Оператор БПЛА
        6. Координатор волонтеров
        """
        def __init__(self, id, name, short_title, icon, role_desc, tasks_desc, tech_stack, tool_name, tool_desc):
            self.id = id
            self.name = name
            self.short_title = short_title
            self.icon = icon
            self.role_desc = role_desc
            self.tasks_desc = tasks_desc
            self.tech_stack = tech_stack
            self.tool_name = tool_name
            self.tool_desc = tool_desc

    class SpecialtyTask(object):
        """
        Прикладная профессиональная задача специальности:
        - id: строковый ID (напр. 'dzz_1', 'gis_2', 'ml_1')
        - specialty_id: 'dzz', 'gis', 'ml', 'ecologist', 'uav', 'volunteer_coord'
        - title: название задачи
        - difficulty: 'Базовый', 'Средний', 'Эксперт'
        - reward_xp: количество очков опыта
        - scenario: подробная вводная ситуация
        - goal: цель задачи
        - tech_stack: используемый инструментарий
        - mechanic_type: тип интерактивной механики
        - options: список вариантов ответа
        - correct_choice: правильный выбор
        - explanation: подробное объяснение методики
        - image: референсный снимок/карта/фото
        - extra_data: словарь дополнительных метаданных
        """
        def __init__(self, id, specialty_id, title, difficulty, reward_xp, 
                     scenario, goal, tech_stack, mechanic_type, 
                     options, correct_choice, explanation, 
                     image=None, extra_data=None):
            self.id = id
            self.specialty_id = specialty_id
            self.title = title
            self.difficulty = difficulty
            self.reward_xp = reward_xp
            self.scenario = scenario
            self.goal = goal
            self.tech_stack = tech_stack
            self.mechanic_type = mechanic_type
            self.options = options
            self.correct_choice = correct_choice
            self.explanation = explanation
            self.image = image
            self.extra_data = extra_data or {}
            self.completed = False
            self.last_score = 0

    class MapTask(object):
        """
        Задание для интерактивного анализа ДЗЗ/ГИС:
        - coordinates: географические координаты участка
        - image: путь к растровому снимку
        - target_x, target_y: истинные координаты центра загрязнения на снимке
        - hit_radius, close_radius: радиусы для статусов 'Попал' и 'Почти'
        - pollution_type: тип выявленного загрязнения
        - difficulty: сложность задания
        - description: контекст и описание ситуации
        - level_type: 1 (поиск на снимке), 2 (сравнение До/После), 3 (выбор приоритетной зоны)
        - image_after: для уровня 2
        - correct_zone: для уровня 3 ('A', 'B', 'C', 'D')
        """
        def __init__(self, id, title, coordinates, image, target_x, target_y, 
                     hit_radius, close_radius, pollution_type, difficulty, 
                     description, level_type=1, image_after=None, correct_zone=None,
                     brief_explanation="Так специалисты ДЗЗ ищут изменения на больших территориях."):
            self.id = id
            self.title = title
            self.coordinates = coordinates
            self.image = image
            self.target_x = target_x
            self.target_y = target_y
            self.hit_radius = hit_radius
            self.close_radius = close_radius
            self.pollution_type = pollution_type
            self.difficulty = difficulty
            self.description = description
            self.level_type = level_type
            self.image_after = image_after
            self.correct_zone = correct_zone
            self.brief_explanation = brief_explanation

        def check_target(self, click_x, click_y, chosen_zone=None):
            if self.level_type == 3:
                if chosen_zone == self.correct_zone:
                    return ("HIT", 500, 0, "Точно определен приоритетный сектор повышенного экологического риска!")
                else:
                    return ("MISS", 50, 999, "Этот сектор менее критичен. Наибольшая угроза в Секторе B!")
            
            dx = click_x - self.target_x
            dy = click_y - self.target_y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist <= self.hit_radius:
                return ("HIT", 450 + int(max(0, self.hit_radius - dist) * 2), int(dist), "Прямое попадание в очаг загрязнения!")
            elif dist <= self.close_radius:
                return ("CLOSE", 250, int(dist), "Почти в цель! Задета периферийная зона шлейфа.")
            else:
                return ("MISS", 0, int(dist), "Мимо. Загрязнение расположено на другом участке.")

    class GISGameManager(object):
        def __init__(self):
            self.tasks = [
                MapTask(
                    id="task_1",
                    title="Уровень 1. Поиск нефтяного загрязнения",
                    coordinates="55°09′14″ N, 20°51′21″ E",
                    image="images/satellite/level1_curonian.png",
                    target_x=780,
                    target_y=340,
                    hit_radius=55,
                    close_radius=110,
                    pollution_type="Нефтяное пятно / плёнка ГСМ в прибрежной акватории",
                    difficulty="Базовый",
                    description="Перед тобой спутниковый снимок Sentinel-2 побережья Куршского залива. Найди подозрительный участок с радужной пленкой или сбросом ГСМ.",
                    level_type=1,
                    brief_explanation="Так специалисты ДЗЗ ищут изменения на больших территориях."
                ),
                MapTask(
                    id="task_2",
                    title="Уровень 2. Сравнение двух снимков (До / После)",
                    coordinates="44°30′43″ N, 38°04′51″ E",
                    image="images/satellite/level2_before.png",
                    target_x=580,
                    target_y=420,
                    hit_radius=60,
                    close_radius=120,
                    pollution_type="Скопление наносного пластика и речного мусора",
                    difficulty="Средний",
                    description="Сравни снимок до шторма и текущий снимок устья реки. Переключай снимки 'До' и 'После' и отметь возникшую аномалию накопления отходов.",
                    level_type=2,
                    image_after="images/satellite/level2_after.png",
                    brief_explanation="Мультиспектральный мониторинг во времени позволяет мгновенно фиксировать динамику заторов и загрязнений."
                ),
                MapTask(
                    id="task_3",
                    title="Уровень 3. Определение приоритетного участка",
                    coordinates="55°14′02″ N, 20°58′33″ E",
                    image="images/satellite/level3_ortho.png",
                    target_x=1050,
                    target_y=160,
                    hit_radius=80,
                    close_radius=150,
                    pollution_type="Критический затор отходов у тростниковых зарослей заповедной зоны",
                    difficulty="Эксперт",
                    description="Перед тобой ортофотоплан с БПЛА, разбитый на 4 сектора (A, B, C, D). Определи, какой сектор требует первоочередного реагирования эко-служб.",
                    level_type=3,
                    correct_zone="B",
                    brief_explanation="ГИС-анализ объединяет данные съемок и карты природоохранных зон для точной расстановки приоритетов."
                )
            ]
            self.current_index = 0
            self.player_points = 0
            self.start_time = 0
            self.total_time_str = "01:18"
            self.last_click = None
            self.last_result = None
            self.last_score_gain = 0
            self.last_feedback = ""
            self.zoom_level = 1.0
            self.view_mode = "AFTER"
            self.selected_zone = "A"
            self.hits_count = 0
            self.game_finished = False

        def get_current_task(self):
            if 0 <= self.current_index < len(self.tasks):
                return self.tasks[self.current_index]
            return self.tasks[0]

        def start_game(self):
            self.current_index = 0
            self.player_points = 0
            self.hits_count = 0
            self.start_time = time.time()
            self.last_click = None
            self.last_result = None
            self.last_score_gain = 0
            self.last_feedback = ""
            self.zoom_level = 1.0
            self.view_mode = "AFTER"
            self.selected_zone = "A"
            self.game_finished = False

        def register_click(self, x, y):
            task = self.get_current_task()
            self.last_click = (int(x), int(y))
            status, score, dist, feedback = task.check_target(x, y, self.selected_zone)
            self.last_result = status
            self.last_score_gain = score
            self.last_feedback = feedback
            self.player_points += score
            if status == "HIT":
                self.hits_count += 1
            elif status == "CLOSE":
                self.hits_count += 0.7

        def next_task(self):
            self.last_click = None
            self.last_result = None
            self.last_score_gain = 0
            self.last_feedback = ""
            self.zoom_level = 1.0
            self.view_mode = "AFTER"
            self.current_index += 1
            if self.current_index >= len(self.tasks):
                self.finish_game()

        def finish_game(self):
            self.game_finished = True
            elapsed = int(time.time() - self.start_time) if self.start_time else 78
            mins = elapsed // 60
            secs = elapsed % 60
            self.total_time_str = "{:02d}:{:02d}".format(mins, secs)

    class LeaderboardEntry(object):
        def __init__(self, rank, name, specialty, points, time_str, accuracy, is_player=False):
            self.rank = rank
            self.name = name
            self.specialty = specialty
            self.points = points
            self.time_str = time_str
            self.accuracy = accuracy
            self.is_player = is_player

    class LeaderboardManager(object):
        def __init__(self):
            self.base_entries = [
                ("Анна Морозова", "🛰️ Специалист ДЗЗ", 1380, "01:12", "100%"),
                ("Илья Корчагин", "🗺️ GIS-специалист", 1290, "01:25", "95%"),
                ("Дарья Волкова", "🧠 Мл. инженер (ML/AI)", 1210, "01:40", "90%"),
                ("Максим Семенов", "🤝 Координатор волонтеров", 1120, "01:55", "85%"),
                ("Елена Кузнецова", "🌿 Эколог-инспектор ООПТ", 1040, "02:08", "80%"),
                ("Артем Белов", "🚁 Оператор БПЛА", 980, "02:22", "75%"),
                ("София Романова", "🌿 Эколог-исследователь", 910, "02:35", "70%")
            ]

        def get_all(self, player_name="Игрок", player_specialty="🛰️ Специалист ДЗЗ", player_pts=1248, player_time="01:18", player_acc="92%"):
            res = [LeaderboardEntry(0, item[0], item[1], item[2], item[3], item[4]) for item in self.base_entries]
            player_entry = LeaderboardEntry(0, player_name + " (Вы)", player_specialty, player_pts, player_time, player_acc, is_player=True)
            res.append(player_entry)
            res.sort(key=lambda e: e.points, reverse=True)
            for idx, item in enumerate(res):
                item.rank = idx + 1
            return res

    class Challenge(object):
        def __init__(self, id, title, description, deadline, difficulty, location, reward_xp, organizer, territory):
            self.id = id
            self.title = title
            self.description = description
            self.deadline = deadline
            self.difficulty = difficulty
            self.location = location
            self.reward_xp = reward_xp
            self.organizer = organizer
            self.territory = territory

    class VolunteerReport(object):
        def __init__(self, id, user_name, challenge_title, photo_path, lat, lon, location_name, category, comment, timestamp, status="pending"):
            self.id = id
            self.user_name = user_name
            self.challenge_title = challenge_title
            self.photo_path = photo_path
            self.lat = lat
            self.lon = lon
            self.location_name = location_name
            self.category = category
            self.comment = comment
            self.timestamp = timestamp
            self.status = status

    class OOPTStats(object):
        def __init__(self):
            self.participants = 126
            self.tasks_completed = 98
            self.photos_count = 241
            self.approved_count = 87

        def add_report(self):
            self.photos_count += 1
            self.tasks_completed += 1

        def approve_report(self):
            self.approved_count += 1

    class Achievement(object):
        def __init__(self, id, title, desc, icon_path, unlocked=False):
            self.id = id
            self.title = title
            self.desc = desc
            self.icon_path = icon_path
            self.unlocked = unlocked

    class CleanEvent(object):
        def __init__(self, title, date, place, desc, status):
            self.title = title
            self.date = date
            self.place = place
            self.desc = desc
            self.status = status

    class CareerAnalytics(object):
        def __init__(self):
            # Баллы интересов из вводного теста профориентации
            self.quiz_scores = {
                "dzz": 20,
                "gis": 20,
                "ml": 20,
                "ecologist": 20,
                "uav": 20,
                "volunteer_coord": 20
            }
            # Статистика решения боевых задач по специальностям
            self.task_stats = {
                "dzz": {"correct": 0, "total": 0, "xp": 0},
                "gis": {"correct": 0, "total": 0, "xp": 0},
                "ml": {"correct": 0, "total": 0, "xp": 0},
                "ecologist": {"correct": 0, "total": 0, "xp": 0},
                "uav": {"correct": 0, "total": 0, "xp": 0},
                "volunteer_coord": {"correct": 0, "total": 0, "xp": 0}
            }
            self.quiz_completed = False
            self.recommended_spec_id = "dzz"

        def record_quiz_answer(self, spec_id, points=25):
            if spec_id in self.quiz_scores:
                self.quiz_scores[spec_id] += points
            self.quiz_completed = True
            self.update_recommendation()

        def record_mission_result(self, spec_id, is_correct, xp):
            if spec_id in self.task_stats:
                st = self.task_stats[spec_id]
                st["total"] += 1
                if is_correct:
                    st["correct"] += 1
                st["xp"] += xp
            self.update_recommendation()

        def sync_with_tasks(self, tasks):
            for sp_id in self.task_stats:
                sp_tasks = [t for t in tasks if t.specialty_id == sp_id and t.completed]
                correct_cnt = sum(1 for t in sp_tasks if getattr(t, "was_correct", False))
                xp_sum = sum(getattr(t, "last_score", 0) for t in sp_tasks)
                self.task_stats[sp_id]["total"] = len(sp_tasks)
                self.task_stats[sp_id]["correct"] = correct_cnt
                self.task_stats[sp_id]["xp"] = xp_sum
            self.update_recommendation()

        def get_affinity(self, spec_id):
            q_pts = self.quiz_scores.get(spec_id, 20)
            st = self.task_stats.get(spec_id, {"correct": 0, "total": 0, "xp": 0})
            
            # Базовый процент от теста интересов (35..75%)
            base = min(75, 35 + int(q_pts * 0.75))
            
            # Вклад боевых миссий (до +25%)
            if st["total"] > 0:
                success_ratio = float(st["correct"]) / float(st["total"])
                task_bonus = int(success_ratio * 24)
                xp_bonus = min(5, int(st["xp"] / 200))
                total_pct = min(99, max(38, base + task_bonus + xp_bonus))
            else:
                total_pct = min(95, max(42, base))
            return total_pct

        def update_recommendation(self):
            best_id = "dzz"
            best_score = -1
            for sp_id in ["dzz", "gis", "ml", "ecologist", "uav", "volunteer_coord"]:
                aff = self.get_affinity(sp_id)
                if aff > best_score:
                    best_score = aff
                    best_id = sp_id
            self.recommended_spec_id = best_id

        def get_top_profile(self):
            profiles = {
                "dzz": {
                    "title": "Космический аналитик и ДЗЗ-исследователь",
                    "badge": "Глобальное зрение Земли",
                    "accent": "#38bdf8",
                    "traits": "У тебя развито системное мышление и способность видеть скрытые аномалии на космических снимках планеты.",
                    "careers": "Специалист ДЗЗ (Роскосмос, Сканэкс), аналитик спутниковых данных, климатический исследователь.",
                    "study_majors": "Аэрокосмические исследования (МИИГАиК, МГУ, НИУ ВШЭ, СПбГУ)."
                },
                "gis": {
                    "title": "Инженер пространственных геоданных и карт",
                    "badge": "Мастер цифровой картографии",
                    "accent": "#00e6b8",
                    "traits": "Твои суперсилы — математическая точность, пространственное воображение и системная работа с цифровыми слоями.",
                    "careers": "ГИС-инженер, картограф, проектировщик геопорталов, аналитик геосервисов (Яндекс Карты, 2ГИС).",
                    "study_majors": "Картография и геоинформатика (МИИГАиК, МГУ, ИТМО, ДВФУ)."
                },
                "ml": {
                    "title": "AI & Computer Vision Инженер",
                    "badge": "Архитектор искусственного интеллекта",
                    "accent": "#f59e0b",
                    "traits": "Ты мыслишь алгоритмами, понимаешь обучение нейросетей, метрики точности и машинное зрение.",
                    "careers": "ML-инженер, разработчик компьютерного зрения (Computer Vision), Data Scientist, разработчик AI для экологии.",
                    "study_majors": "Прикладная математика и ИИ (МФТИ, ВШЭ ФКН, МГТУ им. Баумана, Иннополис)."
                },
                "ecologist": {
                    "title": "Полевой эколог-эксперт и защитник фауны",
                    "badge": "Хранитель дикой природы",
                    "accent": "#4ade80",
                    "traits": "У тебя чуткая экологическая интуиция, забота о животных, знание токсикологии и готовность спасать редкие экосистемы.",
                    "careers": "Эколог национальных парков, экотоксиколог, инспектор Росприроднадзора, эксперт ООПТ.",
                    "study_majors": "Экология и природопользование (МГУ, СПбГУ, РГАУ-МСХА им. Тимирязева)."
                },
                "uav": {
                    "title": "Внешний пилот и оператор БПЛА 4K",
                    "badge": "Ас беспилотной авиации",
                    "accent": "#a855f7",
                    "traits": "Быстрая реакция, точный расчет метеоусловий, навыки аэрофотосъемки и знание беспилотной робототехники.",
                    "careers": "Внешний пилот БПЛА (Геоскан, БАС), оператор воздушного лазерного сканирования, фотограмметрист.",
                    "study_majors": "Беспилотные авиационные системы (МАИ, МГТУ ГА, БГТУ «Военмех», УГАТУ)."
                },
                "volunteer_coord": {
                    "title": "Лидер экспедиции и Zero Waste логист",
                    "badge": "Капитан эко-команды",
                    "accent": "#fb7185",
                    "traits": "Лидерские качества, стрессоустойчивость, умение организовать людей и выстроить безотходную логистику (Zero Waste).",
                    "careers": "Руководитель экспедиций, проектный менеджер эко-инициатив, координатор молодежных программ, ESG-специалист.",
                    "study_majors": "Управление проектами и природоохранный менеджмент (РАНХиГС, НИУ ВШЭ, МГИМО)."
                }
            }
            return profiles.get(self.recommended_spec_id, profiles["dzz"])

    class CleanProjectState(object):
        def __init__(self):
            self.gis_mgr = GISGameManager()
            self.leaderboard = LeaderboardManager()
            self.oopt_stats = OOPTStats()
            self.career_analytics = CareerAnalytics()
            
            # --- 6 ПРОФИЛЬНЫХ СПЕЦИАЛЬНОСТЕЙ (ПРОГРАММА 14+) ---
            self.specialties = [
                Specialty(
                    id="dzz",
                    name="Специалист ДЗЗ",
                    short_title="ДЗЗ-аналитик",
                    icon="🛰️",
                    role_desc="Космическая разведка: поиск пятен мазута и свалок на снимках с орбиты Земли",
                    tasks_desc="Смотри на побережье из космоса через спутники Sentinel и Landsat! Применяй инфракрасные фильтры, чтобы сквозь блики волн находить разливы топлива и новые завалы мусора.",
                    tech_stack="Спутники Sentinel • Landsat • Инфракрасные фильтры • Космоснимки",
                    tool_name="Спектральный фильтр (NDWI / ИК)",
                    tool_desc="Включает инфракрасный фильтр: невидимый мазут начинает ярко светиться контрастным цветом на фоне чистой воды."
                ),
                Specialty(
                    id="gis",
                    name="GIS-специалист",
                    short_title="ГИС-инженер",
                    icon="🗺️",
                    role_desc="Цифровые карты: расчет площади свалок и защита заповедных зон на геопортале",
                    tasks_desc="Работай в современной картографической системе! Вычисляй точную площадь мусорных свалок в гектарах, строй защитные буферы вокруг гнезд редких птиц и находи самые опасные секторы берега.",
                    tech_stack="Геокарты QGIS • Векторные слои • Буферные зоны • Расчет площади",
                    tool_name="Буферные зоны и расчет площади (га)",
                    tool_desc="Строит охранную зону 250м вокруг заповедника и мгновенно вычисляет площадь свалки в гектарах."
                ),
                Specialty(
                    id="ml",
                    name="Мл. инженер (ML / AI)",
                    short_title="ML-инженер",
                    icon="🧠",
                    role_desc="Искусственный интеллект: обучение нейросетей находить пластик и сети по фото",
                    tasks_desc="Научи зрение искусственного интеллекта (YOLOv8) мгновенно находить мусор! Настраивай чувствительность нейросети, обводи «сети-призраки» рамками и оценивай качество работы модели.",
                    tech_stack="Нейросети YOLOv8 • Компьютерное зрение • Разметка данных • Обучение ИИ",
                    tool_name="AI-Детекция объектов (YOLOv8)",
                    tool_desc="Запускает нейросеть: она находит мусор и обводит его зеленой рамкой (Bounding Box) с процентом уверенности."
                ),
                Specialty(
                    id="ecologist",
                    name="Эколог",
                    short_title="Эколог-эксперт",
                    icon="🌿",
                    role_desc="Защита дикой природы: спасение редких животных и оценка токсичности отходов",
                    tasks_desc="Спасай обитателей заповедника! Вызволяй балтийских нерп из смертоносных сетей-ловушек, определяй класс опасности ядовитых бочек и восстанавливай песчаные дюны без разрушительных бульдозеров.",
                    tech_stack="Экомониторинг • Красная книга • Токсичность отходов • Спасение фауны",
                    tool_name="Экопаспорт угрозы и класс риска",
                    tool_desc="Определяет класс опасности найденного мусора и подсказывает, как безопасно спасти животных."
                ),
                Specialty(
                    id="uav",
                    name="Оператор БПЛА",
                    short_title="Пилот дрона",
                    icon="🚁",
                    role_desc="Пилотирование дронов: воздушная разведка пляжей и съемка с точностью до 2 см",
                    tasks_desc="Поднимай квадрокоптер в воздух! Планируй маршрут полета «змейкой» над каменистым берегом, лови мельчайшие пластиковые пробки в камеру 4K и проверяй штормовой ветер перед взлетом.",
                    tech_stack="Квадрокоптеры • Аэрофотосъемка 4K • Полетные планы • Метеорадар",
                    tool_name="Ортофотоплан БПЛА (2 см/пикс)",
                    tool_desc="Включает режим видоискателя дрона с авиагоризонтом, высотой полета и детальным прицелом."
                ),
                Specialty(
                    id="volunteer_coord",
                    name="Координатор волонтеров",
                    short_title="Координатор",
                    icon="🤝",
                    role_desc="Эко-десант и Zero Waste: управление отрядом волонтеров и переработка отходов",
                    tasks_desc="Руководи спасательной операцией на земле! Собери команду на 800 метров пляжа, проверяй координаты тревожных сообщений от туристов и отправляй собранный пластик на завод переработки.",
                    tech_stack="Штабная координация • Мобильные группы • Zero Waste • Раздельный сбор",
                    tool_name="Наряд волонтерской группы",
                    tool_desc="Распределяет участки берега между бригадами, выдает перчатки с мешками и организует вывоз."
                )
            ]
            self.active_specialty = self.specialties[0]
            self.specialty_tool_active = False

            # --- 18 ПРИКЛАДНЫХ ЗАДАЧ ДЛЯ 6 СПЕЦИАЛЬНОСТЕЙ (ПРОГРАММА 14+) ---
            self.specialty_tasks = [
                # 🛰️ Специалист ДЗЗ
                SpecialtyTask(
                    id="dzz_1",
                    specialty_id="dzz",
                    title="Поиск масляного пятна со спутника (Sentinel-2)",
                    difficulty="Базовый",
                    reward_xp=200,
                    scenario="Космический спутник Sentinel-2 прислал свежий снимок залива. На обычной цветной фотографии нефтяное пятно почти не видно — его маскируют яркие солнечные блики на волнах. Нужно переключить каналы спутника на специальный спектральный индекс.",
                    goal="Какой режим снимка поможет четко подсветить тонкую пленку топлива на воде?",
                    tech_stack="Спутник Sentinel-2 • Водный индекс NDWI / SWIR",
                    mechanic_type="spectral_choice",
                    options=[
                        "Обычное цветное фото (RGB) — мешают солнечные блики и рябь на воде",
                        "Индекс зелени (NDVI) — показывает растения на суше, для воды не подходит",
                        "Водный ИК-индекс (NDWI / SWIR) — инфракрасный фильтр четко подсвечивает топливо",
                        "Черно-белое фото без фильтров — не различает топливо и чистую воду"
                    ],
                    correct_choice="Водный ИК-индекс (NDWI / SWIR) — инфракрасный фильтр четко подсвечивает топливо",
                    explanation="Топливо и мазут по-особенному отражают невидимые глазу инфракрасные лучи (SWIR). Спутниковый фильтр NDWI превращает незаметную глазом пленку в яркое контрастное пятно — так экологи находят даже скрытые разливы за секунды!",
                    image="images/satellite/level1_curonian.png",
                    extra_data={"badge": "Sentinel-2 MSI", "coords": "55°09′14″ N, 20°51′21″ E"}
                ),
                SpecialtyTask(
                    id="dzz_2",
                    specialty_id="dzz",
                    title="Сравнение снимков До и После шторма (Change Detection)",
                    difficulty="Средний",
                    reward_xp=300,
                    scenario="После сильного осеннего шторма река вынесла гору мусора в море. Сравни снимок побережья до шторма и через 5 дней после него, чтобы оценить масштабы возникшего затора.",
                    goal="Посмотри на снимки До и После. Что произошло на песчаной косе в устье реки?",
                    tech_stack="Landsat-8 • Сравнение До/После • Анализ изменений",
                    mechanic_type="diff_analysis",
                    options=[
                        "Появился огромный затор из пластика и бревен площадью более 1.2 га",
                        "Ничего не изменилось, коса осталась чистой",
                        "Шторм полностью смыл весь мусор в открытый океан"
                    ],
                    correct_choice="Появился огромный затор из пластика и бревен площадью более 1.2 га",
                    explanation="Сравнивая снимки До и После (метод Change Detection), спутник моментально показал яркое светлое пятно — это завал из сотен кубометров пластика, канистр и прибитых бревен, перегородивших выход в море.",
                    image="images/satellite/level2_after.png",
                    extra_data={"badge": "Landsat-8 OLI", "coords": "44°30′43″ N, 38°04′51″ E"}
                ),
                SpecialtyTask(
                    id="dzz_3",
                    specialty_id="dzz",
                    title="Калибровка водного индекса: как убрать помехи от морской пены",
                    difficulty="Эксперт",
                    reward_xp=450,
                    scenario="У самого берега волны разбиваются в белую пену, и датчик спутника иногда принимает пенные барашки за мазут. Чтобы не отправлять спасателей по ложной тревоге, нужно выставить правильный порог индекса NDWI.",
                    goal="Какой порог чувствительности оставить, чтобы видеть реальное загрязнение и не путать его с пеной?",
                    tech_stack="Калибровка датчика • Порог NDWI • Фильтрация шума",
                    mechanic_type="threshold_tuning",
                    options=[
                        "NDWI > -0.50 (Слишком слабый фильтр: захватывает песчаный берег и белую пену)",
                        "NDWI > +0.85 (Слишком жесткий фильтр: сотрет даже настоящие разливы топлива)",
                        "NDWI > +0.15 (Идеальная настройка: чистая вода отделена от пятен и суши)"
                    ],
                    correct_choice="NDWI > +0.15 (Идеальная настройка: чистая вода отделена от пятен и суши)",
                    explanation="При пороге +0.15 суша, пляж и гребни пены сразу отсекаются как фон. В поле зрения остаются только открытая вода и плавающие на ней аномалии. Ложные тревоги устранены!",
                    image="images/satellite/level1_curonian.png",
                    extra_data={"badge": "Threshold Calibration", "metric": "NDWI Cutoff"}
                ),

                # 🗺️ GIS-специалист
                SpecialtyTask(
                    id="gis_1",
                    specialty_id="gis",
                    title="Защитный буфер заповедника: попадает ли свалка в охранную зону?",
                    difficulty="Базовый",
                    reward_xp=200,
                    scenario="На границе национального парка зафиксирована стихийная свалка. По закону об охране природы вокруг колоний редких птиц и береговой полосы устанавливается защитная полоса покоя. Нужно наложить этот слой на цифровую карту.",
                    goal="Какой стандартный радиус буферной зоны покоя фауны и водоохранной полосы накладывается на карту?",
                    tech_stack="Карты QGIS • Векторный буфер • Охрана природы",
                    mechanic_type="buffer_select",
                    options=[
                        "250 метров — стандартная охранная зона покоя фауны и морского берега",
                        "50 метров — слишком мало, шум и токсины дойдут до птиц",
                        "1500 метров — зона целого биосферного полигона"
                    ],
                    correct_choice="250 метров — стандартная охранная зона покоя фауны и морского берега",
                    explanation="Буфер радиусом 250 метров вокруг гнезд орлана-белохвоста показывает: свалка лежит всего в 140 метрах! Значит, она прямо внутри зоны строгого покоя фауны, и ее нужно убрать немедленно.",
                    image="images/ui/oopt_map_bg.png",
                    extra_data={"badge": "QGIS Vector", "norm": "ВК РФ ст. 65"}
                ),
                SpecialtyTask(
                    id="gis_2",
                    specialty_id="gis",
                    title="Измерение площади мусорного полигона в гектарах",
                    difficulty="Средний",
                    reward_xp=300,
                    scenario="Пилот дрона прислал точные границы свалки: прямоугольный участок 140 метров в длину и 100 метров в ширину. Чтобы заказать нужное число мусоровозов, координатору требуется точная площадь в гектарах.",
                    goal="Сколько гектаров занимает участок размером 140м × 100м на цифровой карте?",
                    tech_stack="Геодезия • Расчет площади • Калькулятор полей",
                    mechanic_type="area_calc",
                    options=[
                        "0.14 га (1 400 кв. метров)",
                        "1.40 га (14 000 кв. метров: 140м × 100м = 14 000 кв.м = 1.4 га)",
                        "14.0 га (140 000 кв. метров)"
                    ],
                    correct_choice="1.40 га (14 000 кв. метров: 140м × 100м = 14 000 кв.м = 1.4 га)",
                    explanation="В 1 гектаре ровно 10 000 квадратных метров! Умножаем 140 м на 100 м = 14 000 кв.м. Делим на 10 000 и получаем ровно 1.4 гектара. На основе этой цифры штаб планирует логистику техники.",
                    image="images/satellite/level3_ortho.png",
                    extra_data={"badge": "UTM Zone 34N", "projection": "EPSG:32634"}
                ),
                SpecialtyTask(
                    id="gis_3",
                    specialty_id="gis",
                    title="Выбор приоритетного сектора: куда морское течение несет мусор?",
                    difficulty="Эксперт",
                    reward_xp=450,
                    scenario="Берег разбит на 4 сектора (A, B, C, D). На цифровую карту наложены слои ветра и прибрежных течений. В одном из секторов находятся заросли тростника, где нерестится рыба.",
                    goal="В каком секторе морское течение создает опасную мусорную ловушку?",
                    tech_stack="Оверлей слоев • Моделирование течений • Геоанализ",
                    mechanic_type="spatial_overlay",
                    options=[
                        "Сектор A (Открытый мыс — мусор уносит ветром в море)",
                        "Сектор C (Каменистый берег с быстрым прибоем)",
                        "Сектор D (Песчаная отмель с чистой водой)",
                        "Сектор B (Залив у тростников — течение сносит весь пластик прямо в рыбные ясли)"
                    ],
                    correct_choice="Сектор B (Залив у тростников — течение сносит весь пластик прямо в рыбные ясли)",
                    explanation="В Секторе B течение упирается в заросли тростника и образует круговорот-ловушку. Там скапливается до 70% всего плавающего мусора. Спасать этот сектор нужно в первую очередь!",
                    image="images/ui/oopt_map_bg.png",
                    extra_data={"badge": "Spatial Overlay", "layer": "Intersection"}
                ),

                # 🧠 Мл. инженер (ML / AI)
                SpecialtyTask(
                    id="ml_1",
                    specialty_id="ml",
                    title="Настройка уверенности нейросети YOLOv8 (Confidence)",
                    difficulty="Базовый",
                    reward_xp=200,
                    scenario="Мы запустили нейросеть YOLOv8 для поиска пластиковых бутылок и канистр по снимкам с дрона. Но у самого прибоя мокрые белые камни и барашки пены нейросеть ошибочно принимает за пластиковые канистры.",
                    goal="Какой порог уверенности (Confidence) задать, чтобы нейросеть перестала реагировать на пену, но находила мусор?",
                    tech_stack="Нейросеть YOLOv8 • Порог уверенности • Оптимизация ИИ",
                    mechanic_type="confidence_tune",
                    options=[
                        "Порог 0.65 — идеальный баланс: ложные срабатывания исчезли, реальный пластик найден",
                        "Порог 0.15 — слишком низкий: обведет рамками каждый пенный барашек на воде",
                        "Порог 0.98 — слишком высокий: пропустит почти весь засыпанный песком пластик"
                    ],
                    correct_choice="Порог 0.65 — идеальный баланс: ложные срабатывания исчезли, реальный пластик найден",
                    explanation="При пороге 0.65 нейросеть отсекает сомнения и шум от пены, но стабильно ловит настоящий мусор. В машинном обучении это называется балансом точности (Precision) и полноты (Recall).",
                    image="images/challenge/photo_plastic.png",
                    extra_data={"badge": "YOLOv8x-Marine", "metric": "F1: 0.89"}
                ),
                SpecialtyTask(
                    id="ml_2",
                    specialty_id="ml",
                    title="Разметка датасета: как правильно обвести рамкой сеть-призрак",
                    difficulty="Средний",
                    reward_xp=300,
                    scenario="Чтобы нейросеть научилась находить запутавшиеся рыбацкие сети, ты размечаешь обучающие фотографии — рисуешь прямоугольные рамки (Bounding Box) вокруг брошенных снастей.",
                    goal="Как правильно обвести сеть рамкой, чтобы нейросеть хорошо обучилась?",
                    tech_stack="Разметка Bounding Box • Датасет ИИ • Формат YOLO",
                    mechanic_type="bbox_annotation",
                    options=[
                        "Обвести только поплавки, а саму сеть не трогать",
                        "Сделать рамку в 2 раза шире самой сети с большим запасом пляжа",
                        "Плотно охватить все видимые края сети с минимумом лишнего песка вокруг"
                    ],
                    correct_choice="Плотно охватить все видимые края сети с минимумом лишнего песка вокруг",
                    explanation="Нейросеть учится по пикселям внутри твоей рамки! Если захватить кучу лишнего песка, алгоритм решит, что песок — это и есть сеть. Рамка должна плотно облегать объект от края до края.",
                    image="images/challenge/photo_ghostnet.png",
                    extra_data={"badge": "CVAT Annotation", "format": "YOLO Box"}
                ),
                SpecialtyTask(
                    id="ml_3",
                    specialty_id="ml",
                    title="Тестирование модели: почему нейросеть пропускает часть шин?",
                    difficulty="Эксперт",
                    reward_xp=450,
                    scenario="После проверки на 500 фотографиях нейросеть показала результаты: Точность (Precision) = 92%, Полнота (Recall) = 71%. Руководитель штаба спрашивает, что значат эти цифры.",
                    goal="Как простыми словами объяснить работу нашей модели?",
                    tech_stack="Оценка качества ИИ • Матрица ошибок • Метрики точности",
                    mechanic_type="model_eval",
                    options=[
                        "Модель работает идеально и находит 100% любого мусора на пляже",
                        "Если сеть нашла шину — она права в 92% случаев, но треть спрятанных шин пока пропускает",
                        "Нейросеть сломалась и ее нужно полностью удалить"
                    ],
                    correct_choice="Если сеть нашла шину — она права в 92% случаев, но треть спрятанных шин пока пропускает",
                    explanation="Точность 92% значит, что ложных тревог почти нет. А полнота 71% показывает, что засыпанные песком шины пока распознаются хуже. Чтобы помочь нейросети, нужно добавить в обучение больше фото полузарытых шин!",
                    image="images/challenge/photo_tires.png",
                    extra_data={"badge": "Confusion Matrix", "mAP": "mAP50: 0.84"}
                ),

                # 🌿 Эколог
                SpecialtyTask(
                    id="ecologist_1",
                    specialty_id="ecologist",
                    title="Опасная находка: определяем класс токсичности бочки с мазутом",
                    difficulty="Базовый",
                    reward_xp=200,
                    scenario="Волонтеры нашли на диком пляже ржавую пробитую бочку с черным мазутом и техническим маслом. Экологу нужно определить класс опасности отхода, чтобы вызвать спецтранспорт с химзащитой.",
                    goal="К какому классу опасности относятся старые нефтепродукты и машинные масла?",
                    tech_stack="Классификатор отходов • Паспорт токсичности • Экобезопасность",
                    mechanic_type="hazard_class",
                    options=[
                        "V класс — безопасные отходы (как сухие ветки или чистая бумага)",
                        "IV класс — малоопасный бытовой мусор",
                        "II–III класс — опасные и высокотоксичные яды для живой природы"
                    ],
                    correct_choice="II–III класс — опасные и высокотоксичные яды для живой природы",
                    explanation="Мазут и масла относятся ко II и III классам опасности! Они не растворяются, пропитывают почву на метры вглубь и смертельно ядовиты для планктона, рыбы и птиц. Их вывозят только в герметичных контейнерах.",
                    image="images/challenge/photo_metal.png",
                    extra_data={"badge": "Реестр ФККО", "law": "ФЗ №89"}
                ),
                SpecialtyTask(
                    id="ecologist_2",
                    specialty_id="ecologist",
                    title="Сети-призраки: чем брошенные снасти угрожают балтийской нерпе?",
                    difficulty="Средний",
                    reward_xp=300,
                    scenario="В прибрежной воде плавает 40-метровый обрывок капроновой сети. В этом районе охотится редкая балтийская кольчатая нерпа из Красной книги.",
                    goal="Почему экологи называют брошенные сети «призрачным промыслом» (Ghost Fishing)?",
                    tech_stack="Красная книга • Защита морских млекопитающих • Сети-призраки",
                    mechanic_type="biodiversity",
                    options=[
                        "Сеть ловит рыбу сама по себе: на приманку плывут нерпы и птицы, запутываются и гибнут годами",
                        "Сеть лежит на дне и никак не мешает животным",
                        "Сеть быстро растворяется в морской воде без вреда"
                    ],
                    correct_choice="Сеть ловит рыбу сама по себе: на приманку плывут нерпы и птицы, запутываются и гибнут годами",
                    explanation="Капрон не гниет сотни лет. Погибшая в сети рыба привлекает тюленей и бакланов — они путаются в прочных ячейках и задыхаются, не имея возможности всплыть. Извлечь сеть из воды нужно немедленно!",
                    image="images/challenge/photo_ghostnet.png",
                    extra_data={"badge": "Красная книга", "species": "Кольчатая нерпа"}
                ),
                SpecialtyTask(
                    id="ecologist_3",
                    specialty_id="ecologist",
                    title="Бережная очистка: как спасти реликтовые дюны от разрушения?",
                    difficulty="Эксперт",
                    reward_xp=450,
                    scenario="Пятно мазута выбросило на хрупкие песчаные дюны. Если загнать туда тяжелые бульдозеры, они распашут тонкий слой корней, и сильный балтийский ветер просто развеет дюны в пыль.",
                    goal="Какой щадящий план восстановления дюн должен утвердить эколог?",
                    tech_stack="Биоремедиация • Растения-песколюбы • Сохранение дюн",
                    mechanic_type="remediation",
                    options=[
                        "Срезать бульдозерами полметра песка вместе со всеми растениями",
                        "Собрать мазут вручную в перчатках, применить эко-сорбент из торфа и посадить траву-песколюбку",
                        "Залить дюны едкими химикатами прямо с вертолета"
                    ],
                    correct_choice="Собрать мазут вручную в перчатках, применить эко-сорбент из торфа и посадить траву-песколюбку",
                    explanation="Тяжелая техника уничтожит дюны навсегда. Экологи работают вручную, используют природный биосорбент и сажают траву песколюбку (Ammophila): ее мощные корни намертво связывают песок и возвращают дюну к жизни.",
                    image="images/challenge/photo_oil.png",
                    extra_data={"badge": "Биоремедиация", "plant": "Ammophila arenaria"}
                ),

                # 🚁 Оператор БПЛА
                SpecialtyTask(
                    id="uav_1",
                    specialty_id="uav",
                    title="План полета дрона: как настроить перекрытие снимков",
                    difficulty="Базовый",
                    reward_xp=200,
                    scenario="Пилот запускает дрон для создания бесшовной 3D-карты пляжа. Дрон летит галсами («змейкой») и делает снимки. Чтобы программа сшила их в одну панораму без белых дыр, кадры должны перекрывать друг друга.",
                    goal="Какое перекрытие соседних кадров (по длине и ширине) считается идеальным золотым стандартом?",
                    tech_stack="Программа полета • Перекрытие кадров • Беспилотная съемка",
                    mechanic_type="flight_plan",
                    options=[
                        "Перекрытие 30% / 20% — слишком мало, карта получится с дырами и разрывами",
                        "Перекрытие 75% продольное / 70% поперечное — идеальный стандарт качественной сшивки",
                        "Перекрытие 98% / 98% — дрон зависнет, батарея сядет на первых 10 метрах"
                    ],
                    correct_choice="Перекрытие 75% продольное / 70% поперечное — идеальный стандарт качественной сшивки",
                    explanation="При перекрытии 75% каждый камень и бутылка попадают сразу на 5-6 разных кадров с разных углов. Программа на компьютере легко находит общие точки и сшивает гигантскую карту без единой ошибки.",
                    image="images/satellite/level3_ortho.png",
                    extra_data={"badge": "Pix4D Photogrammetry", "overlap": "75% / 70%"}
                ),
                SpecialtyTask(
                    id="uav_2",
                    specialty_id="uav",
                    title="Высота полета: ищем пластиковые пробки с неба",
                    difficulty="Средний",
                    reward_xp=300,
                    scenario="Наша задача — разглядеть на песке мелкие пластиковые крышки и осколки размером всего 5 сантиметров. Камера дрона отличная (20 мегапикселей), но нужно выбрать правильную высоту полета.",
                    goal="На какой высоте запустить дрон, чтобы получить четкость картинки 2 см на один пиксель?",
                    tech_stack="Высота полета • Качество съемки (GSD) • Видоискатель",
                    mechanic_type="ortho_scan",
                    options=[
                        "Высота 350 метров — с такой высоты мелкий мусор превратится в неразличимые точки",
                        "Высота 5 метров — опасно: дрон собьет морская волна или соленые брызги",
                        "Высота 80–100 метров — идеальный баланс: захватывает широкий пляж и видит крышки от бутылок"
                    ],
                    correct_choice="Высота 80–100 метров — идеальный баланс: захватывает широкий пляж и видит крышки от бутылок",
                    explanation="На высоте 85-90 метров один пиксель фотографии равен ~2 сантиметрам земли (GSD = 1.95 см/пикс). Это позволяет отчетливо видеть даже мелкие пластиковые крышки, не рискуя разбить коптер о скалы.",
                    image="images/satellite/level3_ortho.png",
                    extra_data={"badge": "GSD Calculator", "altitude": "85m AGL"}
                ),
                SpecialtyTask(
                    id="uav_3",
                    specialty_id="uav",
                    title="Метеосводка: порыв ветра 14 м/с — взлетать или отложить?",
                    difficulty="Эксперт",
                    reward_xp=450,
                    scenario="Ты стоишь на пляже, дрон готов к старту. Но анемометр показывает порывы ветра 14.2 м/с (лимит коптера — 10 м/с). Батарея заряжена на 65%, а лететь нужно на 3 км над морем против ветра.",
                    goal="Какое грамотное командирское решение принимает пилот БПЛА?",
                    tech_stack="Безопасность полетов • Метеоминимум • Автовозврат (RTH)",
                    mechanic_type="telemetry_check",
                    options=[
                        "Отложить полет: ветер сдует дрон, а батареи не хватит на возврат домой (RTH) против шторма",
                        "Взлететь на максимальной скорости и надеяться на удачу",
                        "Снять GPS-антенну, чтобы дрон стал легче"
                    ],
                    correct_choice="Отложить полет: ветер сдует дрон, а батареи не хватит на возврат домой (RTH) против шторма",
                    explanation="Безопасность полетов превыше всего! При ветре 14 м/с дрон тратит почти всю энергию только на то, чтобы не упасть. Против ветра он просто не долетит обратно и утонет в море. Ждем летной погоды!",
                    image="images/satellite/level1_curonian.png",
                    extra_data={"badge": "Pre-flight Safety", "wind_limit": "10 m/s"}
                ),

                # 🤝 Координатор волонтеров
                SpecialtyTask(
                    id="coordinator_1",
                    specialty_id="volunteer_coord",
                    title="Тактический наряд: сколько людей и мешков нужно на 800 метров пляжа?",
                    difficulty="Базовый",
                    reward_xp=200,
                    scenario="Дрон нашел на берегу длиной 800 метров около 600 кг пластикового мусора. Координатор собирает молодежную команду на 3 часа работы. Нужно рассчитать людей, экипировку и мешки.",
                    goal="Какой расчет ресурсов идеален для слаженной и безопасной уборки?",
                    tech_stack="Штабной наряд • Экипировка волонтеров • Безопасность",
                    mechanic_type="team_dispatch",
                    options=[
                        "1 человек в шлепках с одним маленьким пакетиком",
                        "Толпа из 100 человек без перчаток, инструктажа и мешков",
                        "Команда 15–20 человек, 100 прочных мешков по 120л, защитные перчатки, аптечка и вода"
                    ],
                    correct_choice="Команда 15–20 человек, 100 прочных мешков по 120л, защитные перчатки, аптечка и вода",
                    explanation="Группа из 15-20 человек разбивается на звенья по 200 метров и спокойно собирает 600 кг за 3 часа. Главное — защита рук прочными перчатками, питьевая вода и раздельные мешки под разные типы отходов.",
                    image="images/ui/oopt_map_bg.png",
                    extra_data={"badge": "Наряд №24-ЭКО", "capacity": "20 волонтеров"}
                ),
                SpecialtyTask(
                    id="coordinator_2",
                    specialty_id="volunteer_coord",
                    title="Сигнал от туриста: проверяем координаты перед отправкой десанта",
                    difficulty="Средний",
                    reward_xp=300,
                    scenario="В эко-приложение пришло тревожное сообщение от туриста: 'Нашел кучу жуткого мусора, срочно пришлите людей!'. Но геолокация выключена, а фото сделано в темноте и смазано.",
                    goal="Что по правилам работы эко-штаба должен сделать координатор?",
                    tech_stack="Гражданская наука • Проверка координат • Связь с волонтерами",
                    mechanic_type="report_moderation",
                    options=[
                        "Связаться с автором, уточнить ориентиры/геоточку и запросить четкое фото перед выездом",
                        "Срочно отправить вертолет и всех волонтеров наугад по всему побережью",
                        "Удалить сообщение и заблокировать пользователя"
                    ],
                    correct_choice="Связаться с автором, уточнить ориентиры/геоточку и запросить четкое фото перед выездом",
                    explanation="В гражданской науке (Citizen Science) проверка данных — закон! Координатор помогает заявителю скинуть точные GPS-координаты или проверяет точку по свежим фото с дрона, чтобы волонтеры не блуждали впустую.",
                    image="images/challenge/photo_tires.png",
                    extra_data={"badge": "Citizen Science QA", "status": "Needs Verification"}
                ),
                SpecialtyTask(
                    id="coordinator_3",
                    specialty_id="volunteer_coord",
                    title="Экологичная логистика: отправляем собранный мусор на переработку",
                    difficulty="Эксперт",
                    reward_xp=450,
                    scenario="За день волонтеры собрали: 80 мешков пластиковых бутылок, 25 мешков алюминиевых банок, 12 старых покрышек и ящик опасных батареек. Главная цель проекта — замкнутый цикл (Zero Waste).",
                    goal="Как правильно распорядиться собранными отходами?",
                    tech_stack="Логистика Zero Waste • Вторичная переработка • Рециклинг",
                    mechanic_type="waste_logistics",
                    options=[
                        "Свалить все мешки в одну общую яму и закопать в песок",
                        "Раздельный вывоз: пластик и металл — на переработку, шины — в крошку, батарейки — на обезвреживание",
                        "Сжечь весь пластик на костре прямо на берегу заповедника"
                    ],
                    correct_choice="Раздельный вывоз: пластик и металл — на переработку, шины — в крошку, батарейки — на обезвреживание",
                    explanation="Принцип Zero Waste: ни один грамм не должен попасть на обычную свалку! Пластиковые бутылки станут новой одеждой и гранулами, банки — металлом, старые шины — мягким покрытием для детских площадок, а батарейки будут безопасно нейтрализованы.",
                    image="images/challenge/photo_plastic.png",
                    extra_data={"badge": "Zero Waste Logistics", "target": "100% Recycling"}
                )
            ]

            self.active_role_mission = self.specialty_tasks[0]
            self.mission_selected_option = self.specialty_tasks[0].options[0]
            self.mission_status = "BRIEFING"
            self.mission_result_success = False
            self.mission_result_feedback = ""
            self.mission_result_xp = 0
            self.specialties_filter_id = "dzz"
            self.specialties_subtab = "tasks"


            # Квиз подбора специальности
            self.quiz_step = 0
            self.quiz_answers = []
            self.quiz_result_id = None

            # Активные задания челленджа
            self.challenges = [
                Challenge(
                    id="c1",
                    title="Исследуй свой берег: найди 5 типов мусора и отметь их",
                    description="Пеший мониторинг береговой полосы. Зафиксируйте скопления отходов, определите категорию и прикрепите координаты для сводной ГИС-карты.",
                    deadline="До 15 сентября 2026",
                    difficulty="Средняя",
                    location="Куршская коса, сектор 'Морской'",
                    reward_xp=150,
                    organizer="ФГБУ «Национальный парк Куршская коса»",
                    territory="Национальный парк «Куршская коса»"
                ),
                Challenge(
                    id="c2",
                    title="Мониторинг макро- и микропластика прибоя",
                    description="Оценка загрязнения пластиковыми фрагментами и упаковкой вдоль уреза воды. Помогает оценить влияние штормовых выбросов.",
                    deadline="До 22 сентября 2026",
                    difficulty="Легкая",
                    location="Бугазская коса, ст. Благовещенская",
                    reward_xp=200,
                    organizer="АНО «Чистый берег»",
                    territory="Памятник природы «Бугазская коса»"
                ),
                Challenge(
                    id="c3",
                    title="Инспекция брошенных рыболовных сетей (Ghost Gear)",
                    description="Картирование опасных фрагментов сетей, лесок и ловушек, представляющих смертельную угрозу морским птицам и млекопитающим.",
                    deadline="До 10 сентября 2026",
                    difficulty="Высокая",
                    location="Аграханский залив",
                    reward_xp=300,
                    organizer="Государственный заповедник «Дагестанский»",
                    territory="Заповедник «Дагестанский»"
                )
            ]
            self.selected_challenge = self.challenges[0]

            # База отчетов волонтеров
            self.reports = [
                VolunteerReport(
                    id="rep_1",
                    user_name="Иван Рогов",
                    challenge_title="Исследуй свой берег: найди 5 типов мусора",
                    photo_path="images/challenge/photo_plastic.png",
                    lat="55.1482° N",
                    lon="20.8415° E",
                    location_name="Куршская коса, пляж у пос. Лесной",
                    category="Пластик / ПЭТ",
                    comment="Выброшенные пластиковые бутылки и упаковка после шторма. Очаг около 15 метров.",
                    timestamp="04.09.2026 14:32",
                    status="approved"
                ),
                VolunteerReport(
                    id="rep_2",
                    user_name="Ольга Смирнова",
                    challenge_title="Инспекция брошенных сетей",
                    photo_path="images/challenge/photo_ghostnet.png",
                    lat="55.1920° N",
                    lon="20.9110° E",
                    location_name="Мыс Острый, каменистая отмель",
                    category="Сети и снасти (Ghost Gear)",
                    comment="Обрывок капроновой сети с поплавками застрял в топляке. Требуется расчистка!",
                    timestamp="04.09.2026 16:05",
                    status="approved"
                ),
                VolunteerReport(
                    id="rep_3",
                    user_name="Денис Ковалев",
                    challenge_title="Исследуй свой берег: найди 5 типов мусора",
                    photo_path="images/challenge/photo_tires.png",
                    lat="55.1130° N",
                    lon="20.7890° E",
                    location_name="Дюнная зона близ залива",
                    category="Покрышки / Резина",
                    comment="Две грузовые автопокрышки, наполовину занесенные песком.",
                    timestamp="04.09.2026 18:20",
                    status="pending"
                ),
                VolunteerReport(
                    id="rep_4",
                    user_name="Мария Лебедева",
                    challenge_title="Мониторинг прибрежных отходов",
                    photo_path="images/challenge/photo_metal.png",
                    lat="55.1764° N",
                    lon="20.8872° E",
                    location_name="Северный мол, причал",
                    category="Металл / Бочки",
                    comment="Ржавая бочка из-под ГСМ и куски арматуры на кромке воды.",
                    timestamp="04.09.2026 19:45",
                    status="pending"
                )
            ]

            # Достижения
            self.achievements = [
                Achievement("ach_first", "Первое исследование", "Выполните первую полевую фиксацию отходов на карте", "images/ui/badge_first.png", unlocked=False),
                Achievement("ach_scout", "Экоразведчик", "Успешно обнаружьте очаг загрязнения на спутниковом снимке", "images/ui/badge_scout.png", unlocked=False),
                Achievement("ach_5tasks", "5 заданий", "Завершите серию исследовательских миссий ДЗЗ и мониторинга", "images/ui/badge_5tasks.png", unlocked=False),
                Achievement("ach_team", "Командный участник", "Ваш отчет верифицирован сотрудниками ООПТ", "images/ui/badge_team.png", unlocked=False)
            ]

            # Оффлайн мероприятия
            self.real_events = [
                CleanEvent(
                    "Большой субботник и сортировка на Куршской косе",
                    "12 сентября 2026, 10:00",
                    "Визит-центр «Музейный комплекс»",
                    "Сбор волонтеров, расчистка прибрежной полосы, раздельный сбор пластика и мастер-класс по использованию дронов.",
                    "Идет регистрация"
                ),
                CleanEvent(
                    "Байкальский эко-лагерь и БПЛА-мониторинг",
                    "18–20 сентября 2026",
                    "Остров Ольхон, Сарайский пляж",
                    "Трехдневная экспедиция с установкой фотоловушек и составлением ортофотоплана берега.",
                    "Осталось 5 мест"
                ),
                CleanEvent(
                    "Морской эко-десант «Чистые бухты»",
                    "26 сентября 2026",
                    "Владивосток, мыс Тобизина",
                    "Уборка труднодоступных скальных бухт на катерах и извлечение брошенных рыболовных снастей.",
                    "Открыта запись"
                )
            ]

            self.wizard_step = 1
            self.new_report_photo = "images/challenge/photo_plastic.png"
            self.new_report_category = "Пластик / ПЭТ"
            self.new_report_lat = "55.1520° N"
            self.new_report_lon = "20.8650° E"
            self.new_report_comment = "Обнаружено скопление пластиковых упаковок и бутылок у уреза воды."
            self.user_xp = 0

            self.new_task_title = "Осенний мониторинг тростниковых зарослей"
            self.new_task_desc = "Фиксация скопления прибитого ветром мусора в закрытых мелководных бухтах."
            self.new_task_territory = "Национальный парк «Куршская коса»"
            self.new_task_start = "10.09.2026"
            self.new_task_end = "30.09.2026"
            self.new_task_max_users = "50"
            self.new_task_type = "Картирование микропластика"
            self.new_task_reward = "250 XP"
            self.oopt_active_tab = "stats"
            self.selected_map_report = None
            self.completed_specialties = []
            self.selected_preview_spec = None
            self.certificate_downloaded = False
            self.certificate_pdf_path = ""
            self.certificate_show_modal = False
            self.certificate_html_path = ""
            self.mission_guide_shown = False
            self.map_click_zone = None

        def is_specialty_completed(self, spec_id):
            return spec_id in self.completed_specialties

        def complete_current_specialty(self):
            if self.active_specialty.id not in self.completed_specialties:
                self.completed_specialties.append(self.active_specialty.id)
                self.user_xp += 300
                self.gis_mgr.player_points += 300
                if len(self.completed_specialties) >= len(self.specialties):
                    self.unlock_achievement("ach_clean_expert")

        def all_specialties_completed(self):
            return len(self.completed_specialties) >= len(self.specialties)

        def get_remaining_specialties(self):
            return [s for s in self.specialties if s.id not in self.completed_specialties]

        def set_specialty(self, spec_id):
            for s in self.specialties:
                if s.id == spec_id:
                    self.active_specialty = s
                    self.specialties_filter_id = spec_id
                    spec_tasks = self.get_tasks_for_specialty(spec_id)
                    if spec_tasks:
                        first_incomplete = next((t for t in spec_tasks if not t.completed), spec_tasks[0])
                        self.start_role_mission(first_incomplete.id)
                    break

        def get_specialty_by_id(self, spec_id):
            for s in self.specialties:
                if s.id == spec_id:
                    return s
            return self.specialties[0]

        def get_tasks_for_specialty(self, spec_id):
            return [t for t in self.specialty_tasks if t.specialty_id == spec_id]

        def get_total_completed_tasks(self):
            return sum(1 for t in self.specialty_tasks if t.completed)

        def get_total_correct_tasks(self):
            return sum(1 for t in self.specialty_tasks if t.completed and getattr(t, "was_correct", False))

        def get_total_tasks_count(self):
            return len(self.specialty_tasks)

        def get_completed_tasks_count(self, spec_id):
            return sum(1 for t in self.specialty_tasks if t.specialty_id == spec_id and t.completed)

        def get_correct_tasks_count(self, spec_id):
            return sum(1 for t in self.specialty_tasks if t.specialty_id == spec_id and t.completed and getattr(t, "was_correct", False))

        def get_total_incorrect_tasks(self):
            return sum(1 for t in self.specialty_tasks if t.completed and not getattr(t, "was_correct", False))

        def get_incorrect_tasks_count(self, spec_id):
            return sum(1 for t in self.specialty_tasks if t.specialty_id == spec_id and t.completed and not getattr(t, "was_correct", False))

        def get_task_by_id(self, task_id):
            for t in self.specialty_tasks:
                if t.id == task_id:
                    return t
            return self.specialty_tasks[0]

        def start_role_mission(self, task_id):
            self.active_role_mission = self.get_task_by_id(task_id)
            if self.active_role_mission.completed:
                self.mission_status = "RESULT"
                self.mission_result_success = getattr(self.active_role_mission, "was_correct", True)
                self.mission_result_feedback = self.active_role_mission.explanation
                self.mission_result_xp = getattr(self.active_role_mission, "last_score", 0)
            else:
                self.mission_selected_option = self.active_role_mission.options[0] if self.active_role_mission.options else ""
                self.mission_status = "BRIEFING"
                self.mission_result_success = False
                self.mission_result_feedback = ""
                self.mission_result_xp = 0

        def select_mission_option(self, option_text):
            self.mission_selected_option = option_text

        def submit_mission_choice(self):
            task = self.active_role_mission
            if not task or task.completed:
                return
            is_correct = (self.mission_selected_option == task.correct_choice)
            self.mission_status = "RESULT"
            self.mission_result_success = is_correct
            task.completed = True
            task.was_correct = is_correct
            if is_correct:
                pts = task.reward_xp
                self.mission_result_xp = pts
                self.mission_result_feedback = task.explanation
                task.last_score = pts
                self.user_xp += pts
                self.career_analytics.record_mission_result(task.specialty_id, True, pts)
                self.unlock_achievement("ach_scout")
                self.gis_mgr.player_points += pts
                total_done = sum(1 for t in self.specialty_tasks if t.completed)
                if total_done >= 5:
                    self.unlock_achievement("ach_5tasks")
            else:
                self.mission_result_xp = 50
                task.last_score = 50
                self.career_analytics.record_mission_result(task.specialty_id, False, 50)
                self.mission_result_feedback = "Не совсем точно. Правильный ответ:\n«" + task.correct_choice + "»\n\n" + task.explanation
                self.user_xp += 50
                self.gis_mgr.player_points += 50
            self.career_analytics.sync_with_tasks(self.specialty_tasks)


        def toggle_specialty_tool(self):
            self.specialty_tool_active = not self.specialty_tool_active

        def unlock_achievement(self, ach_id):
            for a in self.achievements:
                if a.id == ach_id and not a.unlocked:
                    a.unlocked = True

        def submit_user_report(self):
            rep_id = "rep_" + str(len(self.reports) + 1)
            new_rep = VolunteerReport(
                id=rep_id,
                user_name="Вы (" + self.active_specialty.short_title + ")",
                challenge_title=self.selected_challenge.title,
                photo_path=self.new_report_photo,
                lat=self.new_report_lat,
                lon=self.new_report_lon,
                location_name=self.selected_challenge.location,
                category=self.new_report_category,
                comment=self.new_report_comment,
                timestamp="05.09.2026 10:15",
                status="pending"
            )
            self.reports.insert(0, new_rep)
            self.oopt_stats.add_report()
            self.user_xp += 100
            self.unlock_achievement("ach_first")
            if len(self.reports) >= 5:
                self.unlock_achievement("ach_5tasks")

        def approve_report_by_id(self, report_id):
            for r in self.reports:
                if r.id == report_id and r.status != "approved":
                    r.status = "approved"
                    self.oopt_stats.approve_report()
                    self.unlock_achievement("ach_team")
                    break

        def reject_report_by_id(self, report_id):
            for r in self.reports:
                if r.id == report_id:
                    r.status = "rejected"
                    break

        def add_created_challenge(self):
            c_id = "c_" + str(len(self.challenges) + 1)
            try:
                reward_val = int(self.new_task_reward.replace("XP", "").strip())
            except:
                reward_val = 200
            new_c = Challenge(
                id=c_id,
                title=self.new_task_title,
                description=self.new_task_desc,
                deadline="До " + self.new_task_end,
                difficulty="Средняя",
                location=self.new_task_territory + " (Прибрежная зона)",
                reward_xp=reward_val,
                organizer="Администрация ООПТ",
                territory=self.new_task_territory
            )
            self.challenges.append(new_c)

default clean_state = CleanProjectState()
