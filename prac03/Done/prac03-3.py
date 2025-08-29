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

# 적 캐릭터 생성
enemies = [
    Creature("SlimeA", 30),
    Creature("SlimeB", 25),
    Creature("SlimeC", 20)
]

# --------------------------
# 게임 루프
# --------------------------
options = ["Fight","Run"]
choice = -1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               # 종료 버튼 누르면 게임 종료
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:    # 마우스 버튼이 눌렸을 때
            choice = -1
            mouse_pos = pygame.mouse.get_pos()      # 마우스의 포지션을 받아서 mouse_pos에 저장
            button_width, button_height = 60, 30    # 메뉴 버튼 크기 (변경 가능)
            for i, option in enumerate(options):
                button = pygame.Rect(screen_width//2-button_width//2, 400+i*40-button_height//2, button_width, button_height)
                if mouse_pos[0] > button.x and mouse_pos[0] < button.x+button.width:
                    if mouse_pos[1] > button.y and mouse_pos[1] < button.y+button.height:
                        choice = i

    # ----------------------
    # 화면 그리기
    # ----------------------
    screen.fill((40,60,90))                 # 배경색

    # 적 그리기
    gap, left = 150, (screen_width - (len(enemies)-1) * 150) // 2
    for i, enemy in enumerate(enemies):
        x, y = left + i*gap, 120
        pygame.draw.rect(screen, colors["RED"], (x, y, 80, 80))
        draw_text(screen,font, enemy.name, (x+40, y+90), colors["WHITE"], True)
        draw_hp(screen , x, y-20, 80, 10, enemy.hp, enemy.max, colors)

    # 플레이어 그리기
    pygame.draw.rect(screen, colors["BLUE"], (100,300,80,80))
    draw_text(screen, font, player.name, (140,390), colors["WHITE"], True)
    draw_hp(screen, 80, 280, 120, 12, player.hp, player.max, colors)

    # 메뉴 옵션 표시
    for i, option in enumerate(options):
        draw_text(screen, font, option, (screen_width//2, 400+i*40), (0,200,200) if i==choice else colors["WHITE"], True)

    pygame.display.flip()                   # 화면 업데이트
    clock.tick(60)                          # 초당 60프레임

pygame.quit()                               # 게임 종료
