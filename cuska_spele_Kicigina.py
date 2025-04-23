import pygame
import random
import sqlite3

pygame.init()

conn = sqlite3.connect('snake_game.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER NOT NULL
    )
''')
conn.commit()

balts = (255, 255, 255)
dzeltens = (255, 255, 102)
melns = (0, 0, 0)
sarkans = (213, 50, 80)
zals = (136, 242, 131)
zils = (70, 153, 213)
roza = (255, 46, 247)

ekrana_platums = 600
ekrana_augstums = 400
ekrans = pygame.display.set_mode((ekrana_platums, ekrana_augstums))
pygame.display.set_caption('Čūskas Spēle')

pulkstenis = pygame.time.Clock()
cuskas_bloks = 10
cuskas_atrums = 15

font_style = pygame.font.SysFont("PalatinoLinotypeBlack", 25)
rezultats_font = pygame.font.SysFont("ArialBlack", 35)

def speletaja_rezultats(rezultats):
    vertiba = rezultats_font.render("Punkti: " + str(rezultats), True, melns)
    ekrans.blit(vertiba, [0, 0])

def speletaja_cuska(cuskas_bloks, cuska_list):
    for x in cuska_list:
        pygame.draw.rect(ekrans, zals, [x[0], x[1], cuskas_bloks, cuskas_bloks])

def message(msg, krasa, y_offset=ekrana_augstums / 3):
    mesg = font_style.render(msg, True, krasa)
    ekrans.blit(mesg, [ekrana_platums / 6, y_offset])

def saglabat_rezultatu(rezultats):
    c.execute('SELECT score FROM scores ORDER BY score DESC LIMIT 5')
    labakie_rezultati = [row[0] for row in c.fetchall()]
    if rezultats not in labakie_rezultati:
        c.execute('INSERT INTO scores (score) VALUES (?)', (rezultats,))
        conn.commit()

def iegut_labakos_rezultatus():
    c.execute('SELECT DISTINCT score FROM scores ORDER BY score DESC LIMIT 5')
    return [rinda[0] for rinda in c.fetchall()]

def paradit_labakos_rezultatus(): 
    radit_rezultatu = True
    while radit_rezultatu:
        ekrans.fill(zils)
        nosaukums = rezultats_font.render("TOP 5", True, sarkans)
        ekrans.blit(nosaukums, [ekrana_platums / 2 - nosaukums.get_width() / 2, 40])

        labakie_rezultati = iegut_labakos_rezultatus()
        y_offset = 100
        for idx, rezultats in enumerate(labakie_rezultati):
            rezultats_teksts = font_style.render(f"{idx+1}. {rezultats}", True, melns)
            ekrans.blit(rezultats_teksts, [ekrana_platums / 2 - 50, y_offset])
            y_offset += 30

        message("Q - Beigt | C - Turpināt | M - Izvēlne", sarkans, y_offset + 30)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    paradit_labakos_rezultatus = False
                    speleLoop()
                elif event.key == pygame.K_m:
                    paradit_labakos_rezultatus = False
                    galvena_izvelne()

def galvena_izvelne():
    izvelne_bg = pygame.image.load("menu_fons.jpg")
    izvelne_bg = pygame.transform.scale(izvelne_bg, (ekrana_platums, ekrana_augstums))
    izvelne = True
    while izvelne:
        ekrans.blit(izvelne_bg, (0,0))
        nosaukums = rezultats_font.render("Spēle 'Čuska'", True, roza)
        opcija1 = font_style.render("1. Sākt spēli", True, roza, 2)
        opcija2 = font_style.render("2. Labākie rezultāti", True, roza, 2)
        opcija3 = font_style.render("3. Beigt", True, roza, 2)

        ekrans.blit(nosaukums, [ekrana_platums / 2 - nosaukums.get_width() / 2, 80])
        ekrans.blit(opcija1, [ekrana_platums / 2 - 80, 150])
        ekrans.blit(opcija2, [ekrana_platums / 2 - 80, 200])
        ekrans.blit(opcija3, [ekrana_platums / 2 - 80, 250])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    izvelne = False
                    speleLoop()
                elif event.key == pygame.K_2:
                    paradit_labakos_rezultatus()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    quit()

def speleLoop():
    spele_beidzas = False
    spele_izsledzas = False

    x1 = ekrana_platums / 2
    y1 = ekrana_augstums / 2
    x1_maina = 0
    y1_maina = 0

    cuska_List = []
    cuskas_garums = 1

    ediensx = round(random.randrange(0, ekrana_platums - cuskas_bloks) / 10.0) * 10.0
    ediensy = round(random.randrange(0, ekrana_augstums - cuskas_bloks) / 10.0) * 10.0

    while not spele_beidzas:

        while spele_izsledzas:
            ekrans.fill(zils)
            message("You Lost! Q - Quit | C - Replay | M - Menu", sarkans)
            speletaja_rezultats(cuskas_garums - 1)
            pygame.display.update()

            saglabat_rezultatu(cuskas_garums - 1)
            paradit_labakos_rezultatus()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spele_beidzas = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_maina = - cuskas_bloks
                    y1_maina = 0
                elif event.key == pygame.K_RIGHT:
                    x1_maina = cuskas_bloks
                    y1_maina = 0
                elif event.key == pygame.K_UP:
                    y1_maina = - cuskas_bloks
                    x1_maina = 0
                elif event.key == pygame.K_DOWN:
                    y1_maina = cuskas_bloks
                    x1_maina = 0

        if x1 >= ekrana_platums or x1 < 0 or y1 >= ekrana_augstums or y1 < 0:
            spele_izsledzas = True

        x1 += x1_maina
        y1 += y1_maina
        ekrans.fill(zils)
        pygame.draw.rect(ekrans, dzeltens, [ediensx, ediensy, cuskas_bloks, cuskas_bloks])

        cuska_galva = [x1, y1]
        cuska_List.append(cuska_galva)
        if len(cuska_List) > cuskas_garums:
            del cuska_List[0]

        for x in cuska_List[:-1]:
            if x == cuska_galva:
                spele_izsledzas = True

        speletaja_cuska(cuskas_bloks, cuska_List)
        speletaja_rezultats(cuskas_garums - 1)
        pygame.display.update()

        if x1 == ediensx and x1 != ekrana_platums and y1 == ediensy:
            ediensx = round(random.randrange(0, ekrana_platums - cuskas_bloks) / 10.0) * 10.0
            ediensy = round(random.randrange(0, ekrana_augstums - cuskas_bloks) / 10.0) * 10.0
            cuskas_garums += 1

        pulkstenis.tick(cuskas_atrums)

    pygame.quit()
    quit()

galvena_izvelne()
conn.close()
