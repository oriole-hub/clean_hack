## clean_styles.rpy
## Стили, трансформации и графические элементы интерфейса «Чистый берег»

init offset = 1

transform radar_pulse:
    alpha 0.4 zoom 0.8
    linear 1.0 alpha 1.0 zoom 1.2
    linear 1.0 alpha 0.4 zoom 0.8
    repeat

transform marker_pop:
    zoom 0.0 alpha 0.0
    easein 0.25 zoom 1.1 alpha 1.0
    easeout 0.15 zoom 1.0

transform slide_down:
    yoffset -30 alpha 0.0
    easein 0.3 yoffset 0 alpha 1.0

transform glow_subtle:
    alpha 0.85
    linear 1.2 alpha 1.0
    linear 1.2 alpha 0.85
    repeat

style clean_header_text:
    font gui.name_text_font
    size 28
    color "#ffffff"
    bold True

style clean_subheader_text:
    size 18
    color "#94a3b8"

style clean_card_title:
    size 22
    color "#38bdf8"
    bold True

style clean_card_body:
    size 16
    color "#e2e8f0"

style clean_badge_text:
    size 14
    color "#ffffff"
    bold True

style clean_stat_number:
    size 36
    color "#00e6b8"
    bold True

style clean_stat_label:
    size 14
    color "#94a3b8"
