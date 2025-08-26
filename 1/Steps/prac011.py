import pygame

pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("본인 학번, 이름")

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((128, 128, 128)) # 배경색
    pygame.draw.rect(screen, (0, 128, 255), (50, 50, 50, 50)) # 캐릭터

    pygame.draw.line(screen, (255, 0, 0), (0, 300), (800, 300), 2)
    pygame.draw.line(screen, (0, 255, 0), (400, 0), (400, 800), 2)

    pygame.draw.circle(screen, (255, 255, 0), (400, 300), 50)

    pygame.draw.polygon(screen, (128, 0, 128), ((600, 400), (500, 500), (700, 500)))

    pygame.display.update()

pygame.quit()
