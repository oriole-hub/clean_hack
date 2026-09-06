## script.rpy
## Основная точка входа проекта «Чистый берег»
## Полный обход стандартных меню Ren'Py: мгновенный вход в интерфейс

label main_menu:
    # Показываем интерактивное главное меню «Чистый берег»
    call screen main_menu
    return

label start:
    # Инициализация состояния
    $ clean_state.gis_mgr.start_game()
    
    # 1. Показ вводного интерактивного пролога (ввод в курс дела)
    show screen clean_prologue_screen

label clean_main_loop:
    # Энергоэффективный цикл ожидания событий Ren'Py без спин-лупов и нагрузки на CPU
    $ renpy.pause(3600, hard=True)
    jump clean_main_loop

label clean_quit:
    $ renpy.quit()
