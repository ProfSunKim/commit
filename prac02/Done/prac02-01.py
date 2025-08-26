# Created by 임현우

import pygame

pygame.init()                                   # pygame 기능 전부 초기화(화면/입력/사운드 등 준비)

# 게임 초기화 및 기본 설정
screen = pygame.display.set_mode((800, 600))    # 800x600 크기의 게임 창 만들기
pygame.display.set_caption("본인 학번, 이름")
clock = pygame.time.Clock()                     # FPS(초당 프레임) 제어용 시계

# 플레이어 관련 변수
player_pos = pygame.Vector2(400, 300)           # 플레이어 위치(화면 중앙에서 시작)
player_color = (255, 255, 255)                  # 플레이어 색

# 이벤트 처리 함수 (창 닫기 등)
def handle_events():
    """
    창 닫기(X 버튼) 등 OS 이벤트를 처리.
    QUIT 이벤트가 오면 pygame을 정리하고 프로그램 종료.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# 그리기 함수 (배경/플레이어)
def draw_scene():
    """
    화면을 모두 그린 뒤 마지막에 flip()으로 실제 모니터에 표시.
    - 플레이어를 각각 원(circle)으로 간단히 표현
    """
    screen.fill((0, 0, 0))                                      # 배경 색상
    pygame.draw.circle(screen, player_color, player_pos, 10)    # 플레이어 생성
    pygame.display.flip()                                       # 더블버퍼링 --> 실제 화면으로 전환

# 메인 루프, 모든 함수를 실행 시키는 부분
while True:
    handle_events()     # 창 닫기 등 OS 이벤트 처리
    draw_scene()        # 화면 그리기 + flip
    clock.tick(60)      # 1초에 60프레임으로 고정
