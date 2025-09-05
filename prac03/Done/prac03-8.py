# Created by 윤종현

import pygame, random

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
# 공격 스킬 클래스
# --------------------------
class Skill:
    def __init__(self, name, power, hit):
        self.name = name    # 기술 이름
        self.power = power  # 공격력 배율
        self.hit = hit      # 명중률 (%)

# --------------------------
# 캐릭터/몬스터 클래스
# --------------------------
class Creature:
    def __init__(self, name, hp, attack, skills):
        self.name = name        # 이름
        self.max = hp           # 최대 체력
        self.hp = hp            # 현재 체력
        self.attack = attack    # 공격력
        self.skills = skills    # 가지고 있는 기술 리스트

     # 데미지를 입음
    def take(self, damage):
        self.hp = max(0, self.hp - damage)  # 체력은 0 미만으로 내려가지 않음

    # 살아있는지 확인
    def alive(self):
        return self.hp > 0

# --------------------------
# 공격 처리 함수
# --------------------------
def attack(attacker, target, skill):
    # 명중 체크
    if random.randint(1, 100) > skill.hit:
        return f"{attacker.name} missed!"
    # 데미지 계산 (랜덤으로 80~120% 변동)
    damage = int(attacker.attack * skill.power * random.uniform(0.8, 1.2))
    # 대상 체력 감소
    target.take(damage)
    return f"{attacker.name} used {skill.name}! ({damage})"

# --------------------------
# 게임 실행
# --------------------------
# 플레이어 캐릭터 생성
player = Creature("Hero", 50, 5, [Skill("Slash", 4, 85), Skill("Fire", 6, 75)])

# 적 캐릭터 생성
enemies = [
    Creature("SlimeA", 30, 3, [Skill("Bite", 3, 80)]),
    Creature("SlimeB", 25, 3, [Skill("Bite", 3, 85)]),
    Creature("SlimeC", 20, 2, [Skill("Bite", 2, 90)])
]

# --------------------------
# 게임 루프
# --------------------------
options = ["Fight","Run"]                           # 메뉴 버튼 글자
choice, level = -1, 0                               # 선택한 메뉴 (choice=0 첫번째 메뉴, choice=2 두번째 메뉴, ...), 메뉴 레벨
message = "Enemies have appeared!"
btn_width, btn_height, btn_gap = 60, 30, 40         # 메뉴 버튼 크기, 간격 (변경 가능)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               # 종료 버튼 누르면 게임 종료
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:    # 마우스 버튼이 눌렸을 때
            mouse_pos = pygame.mouse.get_pos()      # 마우스의 포지션을 받아서 mouse_pos에 저장
            # ----------------------
            # 메인 메뉴 선택 (Fight / Run)
            # ----------------------
            if level == 0:
                for i, option in enumerate(options):
                    button = pygame.Rect(screen_width//2-btn_width//2, 400+i*btn_gap-btn_height//2, btn_width, btn_height)
                    if mouse_pos[0] > button.x and mouse_pos[0] < button.x+button.width:
                        if mouse_pos[1] > button.y and mouse_pos[1] < button.y+button.height:
                            choice = i
                if choice == 0:                     # Fight 메뉴 선택
                    level, choice = 1, -1
                elif choice == 1:                   # Run 메뉴 선택
                    message = "You can't run away!"
                
            # ----------------------
            # 스킬 선택
            # ----------------------
            elif level == 1:
                for i, skill in enumerate(player.skills):
                    button = pygame.Rect(screen_width//2-btn_width//2, 400+i*btn_gap-btn_height//2, btn_width, btn_height)
                    if mouse_pos[0] > button.x and mouse_pos[0] < button.x+button.width:
                        if mouse_pos[1] > button.y and mouse_pos[1] < button.y+button.height:
                            choice = i
                back_button = pygame.Rect(screen_width//2-btn_width//2, 400+(i+1)*btn_gap-btn_height//2, btn_width, btn_height)
                if mouse_pos[0] > back_button.x and mouse_pos[0] < back_button.x+back_button.width:
                    if mouse_pos[1] > back_button.y and mouse_pos[1] < back_button.y+back_button.height:
                        choice = i+1
                
                if choice >= 0:                     # Skill 선택 후 Attack 버튼 선택 가능
                    attack_button = pygame.Rect(screen_width//2 + btn_width//2, 400+(i+1)*btn_gap-btn_height//2, btn_width, btn_height)
                    if mouse_pos[0] > attack_button.x and mouse_pos[0] < attack_button.x+attack_button.width:
                        if mouse_pos[1] > attack_button.y and mouse_pos[1] < attack_button.y+attack_button.height:
                            message = "You choose " + player.skills[choice].name + "\n Click one Slime!"
                            level = 2
                
                if choice == i+1:                   # Back 버튼 선택
                    level, choice = 0, -1
                #elif choice >= 0:                   # Skill 선택
                #    message = "You choose " + player.skills[choice].name
                #elif choice == -1:
                #    message = "Please select one"

            # ----------------------
            # 공격 대상 선택
            # ----------------------
            elif level == 2:
                gap, left = 150, (screen_width - (len(enemies)-1) * 150) // 2
                for i, enemy in enumerate(enemies):
                    x, y = left + i*gap, 120
                    if mouse_pos[0] > x and mouse_pos[0] < x+80 and mouse_pos[1] > y and mouse_pos[1] < y+80:
                        target = enemies[i]
                        log = [attack(player, target, player.skills[choice])]               # 플레이어가 적을 공격
                        for enemy in enemies:
                            log.append(attack(enemy, player, random.choice(enemy.skills)))  # 적이 플레이어를 공격
                        message = "\n".join(log)
                        level, choice = 0, -1

    # ----------------------
    # 화면 그리기
    # ----------------------
    screen.fill((40,60,90))                 # 배경색

    # 적 그리기
    gap, left = 150, (screen_width - (len(enemies)-1) * 150) // 2
    for i, enemy in enumerate(enemies):
        x, y = left + i*gap, 120
        pygame.draw.rect(screen, colors["RED"] if enemy.alive() else colors["WHITE"], (x, y, 80, 80))
        draw_text(screen,font, enemy.name, (x+40, y+90), colors["WHITE"], True)
        draw_hp(screen , x, y-20, 80, 10, enemy.hp, enemy.max, colors)

    # 플레이어 그리기
    pygame.draw.rect(screen, colors["BLUE"] if player.alive() else (100,100,100), (100,300,80,80))
    draw_text(screen, font, player.name, (140,390), colors["WHITE"], True)
    draw_hp(screen, 80, 280, 120, 12, player.hp, player.max, colors)

    # 메시지 출력
    for i, line in enumerate(message.split("\n")):
        draw_text(screen, font, line, (screen_width//2, 500+i*25), colors["YELLOW"], True)

    # 메뉴 옵션 표시
    if level == 0:
        for i, option in enumerate(options):
            draw_text(screen, font, option, (screen_width//2, 400+i*btn_gap), (0,200,200) if i==choice else colors["WHITE"], True)
    elif level == 1:
        for i, skill in enumerate(player.skills):
            draw_text(screen, font, skill.name, (screen_width//2, 400+i*btn_gap), (0,200,200) if i==choice else colors["WHITE"], True)
        draw_text(screen, font, "Back", (screen_width//2, 400+(i+1)*btn_gap), colors["WHITE"], True)
        if choice >= 0:
            draw_text(screen, font, "Attack", (screen_width//2 + btn_width, 400+(i+1)*btn_gap), (200, 0, 200), True)

    pygame.display.flip()                   # 화면 업데이트
    clock.tick(60)                          # 초당 60프레임

pygame.quit()                               # 게임 종료
