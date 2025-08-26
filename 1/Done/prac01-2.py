import pygame

pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("본인 학번, 이름")
clock = pygame.time.Clock()

# 캐릭터 설정
character = pygame.Rect(50, 50, 50, 50)
speed = 1

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character.x -= speed
    if keys[pygame.K_RIGHT]:
        character.x += speed
    if keys[pygame.K_UP]:
        character.y -= speed
    if keys[pygame.K_DOWN]:
        character.y += speed
    
    screen.fill((128, 128, 128)) # 배경색
    pygame.draw.rect(screen, (0, 128, 255), character) # 캐릭터
    pygame.display.update()

    clock.tick(60) # 60 FPS

pygame.quit()
