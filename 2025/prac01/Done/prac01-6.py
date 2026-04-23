import pygame

pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("본인 학번, 이름")
clock = pygame.time.Clock()

# 캐릭터 설정
character = pygame.Rect(50, 50, 64, 64)
speed = 1
charcter_image = pygame.image.load('C:/Users/sunje/Desktop/Commit/school.png')
charcter_position = [50, 50]

# 적 설정
enemy = pygame.Rect(600, 400, 64, 64)
enemy_color = (255, 0, 0)
enemy_speed = [-1, -1]

# 맵 설정
walls = [pygame.Rect(300, 150, 200, 50), pygame.Rect(100, 300, 50, 200)]

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character.x -= speed
        charcter_position[0] -= speed
    if keys[pygame.K_RIGHT]:
        character.x += speed
        charcter_position[0] += speed
    if keys[pygame.K_UP]:
        character.y -= speed
        charcter_position[1] -= speed
    if keys[pygame.K_DOWN]:
        character.y += speed
        charcter_position[1] += speed

    # 충돌 처리
    for wall in walls:
        if character.colliderect(wall):
            if keys[pygame.K_LEFT]:
                character.x += speed
                charcter_position[0] += speed
            if keys[pygame.K_RIGHT]:
                character.x -= speed
                charcter_position[0] -= speed
            if keys[pygame.K_UP]:
                character.y += speed
                charcter_position[1] += speed
            if keys[pygame.K_DOWN]:
                character.y -= speed
                charcter_position[1] -= speed

    # 적 이동
    enemy.x += enemy_speed[0]
    if enemy.x < 400:
        enemy_speed[0] = 1
    if enemy.x > 600:
        enemy_speed[0] = -1
    enemy.y += enemy_speed[1]
    if enemy.y < 300:
        enemy_speed[1] = 1
    if enemy.y > 500:
        enemy_speed[1] = -1

    # 전투 시스템 구현할 부분 (적과 충돌하면 전투 시작)
    if character.colliderect(enemy):
        enemy_color = (255, 255, 0)
        enemy.x -= enemy_speed[0]
        enemy.y -= enemy_speed[1]

    screen.fill((128, 128, 128)) # 배경색
    
    for wall in walls:
        pygame.draw.rect(screen, (128, 0, 0), wall)

    pygame.draw.rect(screen, enemy_color, enemy)
    #pygame.draw.rect(screen, (0, 128, 255), character) # 캐릭터
    screen.blit(charcter_image, charcter_position)
    pygame.display.update()

    clock.tick(60) # 60 FPS

pygame.quit()
