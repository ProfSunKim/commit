# Created by 윤종현

import pygame

# --------------------------
# 게임 초기화
# --------------------------
pygame.init()                                                       # pygame 라이브러리 초기화

screen_width, screen_height = 800, 600                              # 화면 크기 설정
screen = pygame.display.set_mode((screen_width, screen_height))     # 화면 생성
pygame.display.set_caption("본인 학번, 이름")
clock = pygame.time.Clock()                                         # 게임 속도 조절용 시계

# --------------------------
# 게임 루프
# --------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # 종료 버튼 누르면 게임 종료
            running = False
    
    # ----------------------
    # 화면 그리기
    # ----------------------
    screen.fill((40,60,90))                 # 배경색

    pygame.display.flip()                   # 화면 업데이트
    clock.tick(60)                          # 초당 60프레임

pygame.quit()                               # 게임 종료
