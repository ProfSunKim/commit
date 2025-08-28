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
font = pygame.font.Font(None, 28)                                   # 글꼴 설정 (None = 기본 글꼴, 28 = 글자 크기)

colors = {                                                          # 자주 쓰는 색상 미리 정의
    "WHITE": (255,255,255), "RED": (200,0,0), "BLUE": (50,100,200),
    "GREEN": (0,200,0), "YELLOW": (200,200,0)
}

# --------------------------
# 화면에 글자 그리는 함수
# --------------------------
def draw_text(screen, font, text, pos, color, center=False):
    # 글자를 화면에 렌더링
    image = font.render(text, True, color)
    # 글자 위치 지정
    rectangle = image.get_rect(center=pos) if center else image.get_rect(topleft=pos)
    # 화면에 붙이기
    screen.blit(image, rectangle)

# --------------------------
# 체력바 그리는 함수
# --------------------------
def draw_hp(screen, x, y, width, height, hp, maxhp, colors):
    # 체력바 배경 (흰색 테두리)
    pygame.draw.rect(screen, colors["WHITE"], (x-2, y-2, width+4, height+4))
    # 체력바 기본 빨간색
    pygame.draw.rect(screen, colors["RED"], (x, y, width, height))
    # 체력바 현재 체력만큼 녹색으로 표시
    pygame.draw.rect(screen, colors["GREEN"], (x, y, int(width*max(0,hp/maxhp)), height))

# --------------------------
# 캐릭터/몬스터 클래스
# --------------------------
class Creature:
    def __init__(self, name, hp):
        self.name = name        # 이름
        self.max = hp           # 최대 체력
        self.hp = hp            # 현재 체력


# --------------------------
# 게임 실행
# --------------------------
# 플레이어 캐릭터 생성
player = Creature("Hero", 50)

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

    # 플레이어 그리기
    pygame.draw.rect(screen, colors["BLUE"], (100,300,80,80))
    draw_text(screen, font, player.name, (140,390), colors["WHITE"], True)
    draw_hp(screen, 80, 280, 120, 12, player.hp, player.max, colors)

    pygame.display.flip()                   # 화면 업데이트
    clock.tick(60)                          # 초당 60프레임

pygame.quit()                               # 게임 종료
