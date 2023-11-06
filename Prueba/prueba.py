import pygame, sys, random

pygame.init()
pygame.display.set_caption("Wordle")
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30

GRIS = (100, 100, 100)
GRIS_OSCURO= (20, 20, 20)
BLANCO = (255, 255, 255)
ROJO = (255, 108, 108)
ERROR = (255, 0, 0)
MEDIO = (255, 193, 53)
ACIERTO = (0, 185, 6)
LETRAS= 5
TEXT_TIMER = 2
INTENTOS = 6



CASILLA_ANCHO = 50
CASILLA_ALTO = 50
# Pixels between each Rect
DX = 10
DY = 10
X_PADDING = 5
Y_PADDING = 5
# Leftmost topmost coordinate where the first rect will be drawn, should be symmetrical. Accounts for number of rects, pixels between rects and rect sizes.
BASE_OFFSET_X = (WIDTH / 2) - ((LETRAS / 2) * DX) - ((LETRAS / 2) * CASILLA_ANCHO) + (((LETRAS + 1) % 2) * (DX / 2))
BASE_OFFSET_Y = (HEIGHT / 2) - ((INTENTOS / 2) * DY) - ((INTENTOS / 2) * CASILLA_ALTO) + (
            ((INTENTOS + 1) % 2) * (DY / 2))

def main():

    ACIERTOS = 0
    FALLOS = 0
    PARTIDAS = 0
    global palabras
    palabras = [word.replace("\n", "") for word in list(open("wordlist.txt"))]
    clock = pygame.time.Clock()
    letter_font = pygame.font.Font(None, 65)
    text = pygame.font.Font(None, 40)
    def juego(letras):
        letras=int(letras)
        global LETRAS
        LETRAS = letras
        LONGITUD_PALABRA = LETRAS
        used_words = []
        curr_word = ""
        word_count = 0
        curr_letter = 0
        rects = []
        flag_win = False
        flag_lose = False
        flag_invalid_word = False
        flag_not_enough_letters = False
        timer_flag_1 = 0
        timer_flag_2 = 0
        print(letras)
        posibles=[palabra for palabra in palabras if len(palabra) == letras]
        print(posibles)
        palabra = random.choice(posibles)
        print(palabra)
        assert (len(palabra) == LONGITUD_PALABRA)
        assert (palabra.islower())
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Option to restart game
                if flag_win or flag_lose:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            main()
                else:
                    # Upon keypress
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            # Prevents IndexErrors
                            if curr_word:
                                curr_word = curr_word[:-1]
                                curr_letter -= 1
                        elif event.key == pygame.K_RETURN:
                            if len(curr_word) == letras:
                                if curr_word.lower() in palabras:
                                    word_count += 1
                                    used_words.append(curr_word)
                                    curr_word = ""
                                    curr_letter = 0
                                else:
                                    flag_invalid_word = True
                                    timer_flag_1 = 0
                            else:
                                flag_not_enough_letters = True
                                timer_flag_2 = 0
                        else:
                            if len(curr_word) < LONGITUD_PALABRA:
                                if event.unicode.isalpha():
                                    curr_word += event.unicode.upper()
                                    curr_letter += 1
            SCREEN.fill(GRIS_OSCURO)
            # Draw title and underline
            draw_title(letter_font)
            # Draws base 5x6 grid for letters
            for y in range(INTENTOS):
                row_rects = []
                for x in range(LETRAS):
                    x_pos = BASE_OFFSET_X + (x * DX) + (x * CASILLA_ANCHO)
                    y_pos = BASE_OFFSET_Y + (y * DY) + (y * CASILLA_ALTO)
                    curr_rect = pygame.Rect((x_pos, y_pos), (CASILLA_ANCHO, CASILLA_ALTO))
                    pygame.draw.rect(SCREEN, GRIS, curr_rect, 2)
                    row_rects.append((x_pos, y_pos))
                rects.append(row_rects)
            if flag_invalid_word:
                timer_flag_2 = 0
                flag_not_enough_letters = False
                text_surface = text.render("Palabra inválida", True, ROJO)
                # Should be about center aligned. Use of magic numbers, but not serious.
                x_pos = BASE_OFFSET_X + (CASILLA_ANCHO * (LETRAS / 5))
                y_pos = BASE_OFFSET_Y - (DY * 4)
                SCREEN.blit(text_surface, (x_pos, y_pos))
                timer_flag_1 += 1
            if flag_not_enough_letters:
                timer_flag_1 = 0
                flag_invalid_word = False
                text_surface = text.render("Completa la palabra", True, ROJO)
                x_pos = BASE_OFFSET_X + (CASILLA_ANCHO * (LETRAS / 10))
                y_pos = BASE_OFFSET_Y - (DY * 4)
                SCREEN.blit(text_surface, (x_pos, y_pos))
                timer_flag_2 += 1
            if timer_flag_1 == TEXT_TIMER * FPS:
                flag_invalid_word = False
                timer_flag_1 = 0
            if timer_flag_2 == TEXT_TIMER * FPS:
                flag_not_enough_letters = False
                timer_flag_2 = 0

            if flag_win:

                text_surface = text.render("Ganaste! Presiona R para volver a jugar", True, ACIERTO)
                x_pos = BASE_OFFSET_X - (CASILLA_ANCHO * (LETRAS / 5))
                y_pos = BASE_OFFSET_Y + (DY * 7) + (CASILLA_ALTO * INTENTOS)
                SCREEN.blit(text_surface, (x_pos, y_pos))


            if flag_lose:
                text_surface = text.render(f"Perdiste!{palabra} Presiona R para volver a jugar", True, ROJO)
                x_pos = BASE_OFFSET_X - (CASILLA_ANCHO * (LETRAS / 2))
                y_pos = BASE_OFFSET_Y + (DY * 7) + (CASILLA_ALTO * INTENTOS)
                SCREEN.blit(text_surface, (x_pos, y_pos))
            if curr_word:
                for letter_index in range(len(curr_word)):
                    word_surface = letter_font.render(curr_word[letter_index], True, BLANCO)
                    # [0] represents X coord, [1] Y.
                    SCREEN.blit(word_surface, (
                    rects[word_count][letter_index][0] + X_PADDING, rects[word_count][letter_index][1] + Y_PADDING))

            # Renders letters and rects of words already inputted by player.
            if used_words:
                for word_index in range(len(used_words)):
                    remaining_letters = list(palabra)
                    num_correct = 0

                    # Used to make sure that letters that appear more than once don't get counted if that letter appears in palabra only once.
                    # EG: palabra = "proxy", word = "droop", and 'o' appears more than once. The second 'o' in droop does not get counted.
                    same_indeces = [i for i, x in enumerate(zip(palabra, used_words[word_index].lower())) if
                                    all(y == x[0] for y in x)]
                    # Same indeces - if guessword is "beast" and usedword[word_index] is "toast", same indeces contains the indeces where same letters in the same positions collide, in this case, "a","s","t" - which have indeces of [2,3,4] respectively.
                    if same_indeces:
                        for index in range(len(same_indeces)):
                            num_correct += 1
                            remaining_letters[same_indeces[index]] = ""
                            curr_rect = pygame.Rect(
                                (rects[word_index][same_indeces[index]][0], rects[word_index][same_indeces[index]][1]),
                                (CASILLA_ANCHO, CASILLA_ALTO))
                            pygame.draw.rect(SCREEN, ACIERTO, curr_rect)
                            past_letter_surface = letter_font.render(used_words[word_index][same_indeces[index]].upper(),
                                                                     True, BLANCO)
                            SCREEN.blit(past_letter_surface, (rects[word_index][same_indeces[index]][0] + X_PADDING,
                                                              rects[word_index][same_indeces[index]][1] + Y_PADDING))

                    for letter_index in range(LONGITUD_PALABRA):
                        if letter_index not in same_indeces:
                            curr_rect = pygame.Rect(
                                (rects[word_index][letter_index][0], rects[word_index][letter_index][1]),
                                (CASILLA_ANCHO, CASILLA_ALTO))
                            cur_past_letter = used_words[word_index][letter_index].lower()
                            past_letter_surface = letter_font.render(cur_past_letter.upper(), True, BLANCO)
                            # Incorrect Letters
                            if cur_past_letter not in remaining_letters:
                                pygame.draw.rect(SCREEN, ERROR, curr_rect)
                            # Letter exists in word, but wrong position.
                            else:
                                pygame.draw.rect(SCREEN, MEDIO, curr_rect)
                                remaining_letters[remaining_letters.index(cur_past_letter)] = ""
                            SCREEN.blit(past_letter_surface, (
                            rects[word_index][letter_index][0] + X_PADDING, rects[word_index][letter_index][1] + Y_PADDING))
     # Win/lose condition
                    if num_correct == letras:
                        flag_win = True
                    elif len(used_words) == INTENTOS:
                        flag_lose = True

            pygame.display.update()
            clock.tick(FPS)

    # Opciones del menú
    options = ['4 letras', '5 letras', '6 letras', '7 letras', '8 letras']
    selected_option = -1
    # Configuración de la pantalla
    pygame.display.set_caption("Menú Principal")

    # Colores
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)

    # Fuentes
    font = pygame.font.Font(None, 36)
    # Función para dibujar el menú
    def draw_menu(partidas=0,aciertos=0,fallos=0):
        SCREEN.fill(white)
        text = font.render('Selecciona el número de letras:', True, black)
        text_rect = text.get_rect(center=(400, 50))
        SCREEN.blit(text, text_rect)

        y = 120
        for i, option in enumerate(options):
            button_rect = pygame.Rect(300, y, 200, 50)
            pygame.draw.rect(SCREEN, black, button_rect, 2)

            option_text = font.render(option, True, black)
            option_rect = option_text.get_rect(center=button_rect.center)
            SCREEN.blit(option_text, option_rect)

            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(SCREEN, red, button_rect, 2)
                if pygame.mouse.get_pressed()[0]:
                    selected_option = i
                    return selected_option

            y += 60

        pygame.display.flip()

    # Función para el menú principal
    def menu_principal():
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            selected_option=draw_menu()

            if selected_option != None:
                print(f'Se ha seleccionado la opción: {options[selected_option]}')
                juego(options[selected_option][0])
                running = False

    menu_principal()

def draw_title(font):
        pygame.draw.line(SCREEN, BLANCO, (BASE_OFFSET_X - CASILLA_ANCHO, BASE_OFFSET_Y - CASILLA_ALTO), (
            BASE_OFFSET_X + (CASILLA_ANCHO * (LETRAS + 1)) + (DX * (LETRAS - 1)), BASE_OFFSET_Y - CASILLA_ALTO),
                         width=1)
        title_surface = font.render("WORDLE", True, BLANCO)
        SCREEN.blit(title_surface, (BASE_OFFSET_X + CASILLA_ANCHO, BASE_OFFSET_Y - (CASILLA_ALTO * 2)))

if __name__ == "__main__":
        main()