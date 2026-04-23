# Created by 임현우

import pygame, random

pygame.init()                                   # pygame 기능 전부 초기화(화면/입력/사운드 등 준비)

# 게임 초기화 및 기본 설정
screen = pygame.display.set_mode((800, 600))    # 800x600 크기의 게임 창 만들기
pygame.display.set_caption("본인 학번, 이름")
clock = pygame.time.Clock()                     # FPS(초당 프레임) 제어용 시계
font = pygame.font.SysFont(None, 24)            # 기본 글꼴(크기 24)

# 플레이어 관련 변수
player_pos = pygame.Vector2(400, 300)           # 플레이어 위치(화면 중앙에서 시작)
player_color = (255, 255, 255)                  # 플레이어 색
player_speed = 3                                # 플레이어 이동 속도
player_hp = 5                                   # 플레이어 체력

# 적 관련 변수
enemies = []                                    # 적 리스트
enemy_spawn_delay = 1000                        # 적 생성 간격 (마지막 적 생성 후 enemy_spawn_delay 만큼 기다려야 다시 생성)
last_spawn_time = 0                             # 마지막 적 생성 시각

# 총알 관련 변수
bullets = []                                    # 총알 리스트(총알을 발사하는 것 역시 객체이기 때문에)
shoot_delay = 1000                              # 총알 발사 간격 (마지막 발사 시각 이후 shoot_delay만큼 기다려야 다시 발사가 됨)
last_shot_time = 0                              # 마지막 발사 시각

# 경험치 오브 관련 변수
items = []                                      # 아이템 리스트(적을 잡은 후 나오는 경험치 오브젝트들도 여러개 이기 때문)

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

# 입력 처리 함수(플레이어 이동)
def move_player(keys):
    """
    키보드 입력(WASD)에 따라 플레이어 위치를 바꿈.
    좌표는 Vector2라서 .x, .y 로 접근해 더하고 빼면 됨.
    """
    if keys[pygame.K_w]: player_pos.y -= player_speed
    if keys[pygame.K_s]: player_pos.y += player_speed
    if keys[pygame.K_a]: player_pos.x -= player_speed
    if keys[pygame.K_d]: player_pos.x += player_speed

# 적 생성 함수
def spawn_enemy(now):
    """
    일정 간격(enemy_spawn_delay)마다 적 1마리 생성.
    - 적은 랜덤 위치에서 등장함
    """
    global last_spawn_time
    if now - last_spawn_time > enemy_spawn_delay:
        # 초록색 적
        hp, exp, color = 1, 1, (0, 255, 0)

        # 랜덤 위치에서 적이 생성되도록 하는 코드
        pos = pygame.Vector2(random.randint(0, 800), random.choice([-20, 620])) 
        # x 좌표 = random.randint(0, 800): 0~800 사이 랜덤한 위치
        # y 좌표 = random.choice([-20, 620]): -20 이나 620 중 선택
        # -20과 620은 각각 화면의 맨 위와 맨 아래에서 스폰하는 것을 뜻함

        enemies.append({"pos": pos, "hp": hp, "exp": exp, "color": color})  # 위에서 정해진 좌표(pos)를 이용하여 적을 생성함
        last_spawn_time = now                                               # 적이 나온 시간을 기록 후, 다음 적이 생성되기 까지 기다림

# 이동 함수(적)
def move_enemies():
    # (플레이어 위치 - 적 위치) --> 플레이어를 바라보는 방향 벡터
    # normalize() 로 길이를 1로 맞춘 뒤 * 2 해서 속도 적용
    for enemy in enemies:
        enemy["pos"] += (player_pos - enemy["pos"]).normalize() * 2     # * 2 에서 숫자 2 를 바꾸면 적의 속도를 바꿀 수 있음

# 플레이어와 적 사이 거리를 계산해주는 함수
def get_distance(enemy):
    # enemy["pos"] : 적의 위치
    # player_pos.distance_to(적 위치) --> 플레이어와 적 사이 거리(숫자) 반환
    return player_pos.distance_to(enemy["pos"])

# 총알 생성 함수
def shoot_bullet(now):
    global last_shot_time
    if now - last_shot_time > shoot_delay:
        if enemies:
            target = min(enemies, key=get_distance)     # 가장 가까운 적 찾기
            direction = (target["pos"] - player_pos).normalize()
        else:
            direction = pygame.Vector2(1, 0)            # 적이 없는 경우
        bullets.append([player_pos.copy(), direction])
        last_shot_time = now

# 이동 함수(총알)
def move_bullets():
    # bullet[0] = 총알 위치, bullet[1] = 총알 방향
    # 총알 위치를 방향 * 3 만큼 이동 (총알 속도는 3)
    for bullet in bullets:
        bullet[0] += bullet[1] * 3

# 오브젝트 충돌 처리 함수 (총알 <-> 적 | 적 <-> 플레이어)
def check_collisions():
    """
    1) 총알-적: 거리가 15 미만이면 피격 → hp 감소, 0 이하 시 경험치 오브 생성
    2) 적-플레이어: 거리가 20 미만이면 플레이어 피격 → hp 감소, 0 이면 게임오버
    """
    global player_hp

    # 총알-적 충돌 처리
    for bullet in bullets:
        for enemy in enemies:
            if bullet[0].distance_to(enemy["pos"]) < 15:    # 총알-적 충돌 판정
                enemy["hp"] -= 1                            # 적 체력 1만큼 감소
                bullets.remove(bullet)                      # 총알 제거
                if enemy["hp"] <= 0:                        # 적이 죽으면
                    items.append({
                        "pos": enemy["pos"].copy(),         # 경험치 오브 생성 위치 = 적의 위치 값을 복사해 경험치 오브 위치에 넣어줌
                        "value": enemy["exp"]               # 경험치 값
                    })
                    enemies.remove(enemy)                   # 적 제거
                break                                       # 한 총알은 하나의 적만 맞춤

    # 적-플레이어 충돌 처리
    for enemy in enemies:
        if enemy["pos"].distance_to(player_pos) < 20:       # 적-플레이어 충돌
            enemies.remove(enemy)                           # 적 제거 (경험치 오브 생성 X)
            player_hp -= 1                                  # 플레이어 체력 1만큼 감소
            if player_hp <= 0:                              # 체력이 0 이라면
                print("GAME OVER")
                pygame.quit()
                exit()

# 그리기 함수 (배경/플레이어/적/총알/UI)
def draw_scene():
    """
    화면을 모두 그린 뒤 마지막에 flip()으로 실제 모니터에 표시.
    - 플레이어/적/총알을 각각 원(circle)으로 간단히 표현
    - 텍스트는 font.render 로 Surface 만든 뒤 blit 으로 붙임
    """
    screen.fill((0, 0, 0))                                              # 배경 색상
    pygame.draw.circle(screen, player_color, player_pos, 10)            # 플레이어 생성

    for enemy in enemies: 
        pygame.draw.circle(screen, enemy["color"], enemy["pos"], 12)    # 적 객체
    for bullet in bullets: 
        pygame.draw.circle(screen, (255, 255, 0), bullet[0], 5)         # 총알 객체
    for item in items: 
        pygame.draw.circle(screen, (0, 255, 255), item["pos"], 8)       # 경험치 객체

    # UI를 그리는 부분(font.render(표시될 글씨, 안티앨리어싱 여부(True), 색상), (x,y)글씨 위치 좌표)
    screen.blit(font.render("HP " + str(player_hp), True, (255,255,255)), (10, 85))

    pygame.display.flip()                                               # 더블버퍼링 --> 실제 화면으로 전환

# 메인 루프, 모든 함수를 실행 시키는 부분
while True:
    handle_events()                     # 창 닫기 등 OS 이벤트 처리

    keys = pygame.key.get_pressed()     # 키보드 눌림 상태 얻기
    move_player(keys)                   # 입력에 따라 플레이어 이동

    now = pygame.time.get_ticks()       # 현재 시각 (tick)
    spawn_enemy(now)                    # 적 생성
    move_enemies()                      # 적 이동
    shoot_bullet(now)                   # 자동 사격(가까운 적 방향)
    move_bullets()                      # 총알 이동
    check_collisions()                  # 충돌 처리

    draw_scene()                        # 화면 그리기 + flip
    clock.tick(60)                      # 1초에 60프레임으로 고정
