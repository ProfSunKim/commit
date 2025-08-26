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
    pygame.display.update()

pygame.quit()
