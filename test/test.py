import lucs_tools
import numpy as np
import matplotlib.pyplot as plt

# call lucs_tools.formatting.joyful.joy_text to plot the string
# lucs_tools.formatting.joyful.text(
#     input_string,
#     90,
#     fontsize=5.5,
#     weight='light',
#     factor=3.,
#     write_lines=True,
# )

# standard joy division cover recreation, with multiple modes:
# ax1 = lucs_tools.formatting.joyful.lines(90, 60, size=(400,600), title='standard', mode='normal')
# ax2 = lucs_tools.formatting.joyful.lines(90, 60, size=(400,600), title='standard', mode='normal')
# # bright mode
# lucs_tools.formatting.joyful.lines(90, 60, size=(400,600), title='bright-peaks', mode='bright')

# # transparent landscape mode
# lucs_tools.formatting.joyful.lines(90, 60, size=(400,600), title='transparent_mode', mode='transparent')

# # ... inverted switch
# lucs_tools.formatting.joyful.lines(30, 50, size=(400,500), title='inverted :-0', inverted=True)

# # a bizzare combo
lucs_tools.formatting.joyful.lines(90, 1000, size=(400,600), title='weird', linewidth=0.1, inverted=True, mode='bright')


# lucs_tools.formatting.joyful.joy_text_new(text, size=(500,600), spacing=4., fontsize=9., write_lines=False, weight='normal')


# ascii formatting; returns a loooong string you can view, from an original seed string (cuts/loops if needed)
# text = """it was a good run. A new coach to soccer that coaching rec ed would realize if you're down 3-0 in the first 25 mins of the game, you need to change your strategy. Scolari and the rest of the coaching staff including perreira will never be apart of the brasilian futbol federation again. There were so many players to choose. He chose jo and fred one of the two most lazy ass strikers to be his "offense". Then I realize that  pato is 24 why not play him. How about fabiano or even coutinho or damiao. It's crazy, he made a team centered around neymar. Kaka ronaldinho or robinho should of made the team. Congrats on germany, if argentina goes to the final they better not fuck up man. Because that will be a nightmare if the argentines win in brasil. GO NEUR AND SHURLLE"""
# print(lucs_tools.formatting.joyful.ascii(text, 300, 60, 0, 2))
