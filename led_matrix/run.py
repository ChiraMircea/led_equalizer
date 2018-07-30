from apps.pong import Pong
from apps.snake import Snake
# from apps.waves import Waves


AVAILABLE_APPS = [
    Pong, Snake, #Waves
]


if __name__ == '__main__':
    index = 0
    while True:
        app = AVAILABLE_APPS[index]

        print('\n'*5)
        print(app.display_text)

        k = input()

        if k == 'n':
            index += 1
        elif k == 'p':
            index -= 1
        elif k == 'e':
            current_app = app()
            current_app.play()
            while input() != 'ok':
                continue

        index %= len(AVAILABLE_APPS)


