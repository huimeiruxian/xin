import pygame
import os
import time
from Peashooter import Peashooter
from sunflower import Sunflower
from WallNut import WallNut
from Sun import Sun
from zombie import Zombie
from Bullet import Bullet
from FlagZombie import FlagZombie

pygame.init()
backgd_size=(1200,600)

screen=pygame.display.set_mode(backgd_size)
pygame.display.set_caption('Plant vs Zoomie')

#初始化音乐模块
pygame.mixer.init()
#加载音乐
pygame.mixer.music.load("material/music/02 - Crazy Dave (Intro Theme).mp3")

bg_img_path='material/images/background1.jpg'
original_bg = pygame.image.load(bg_img_path).convert_alpha()
ba_img_obj = pygame.transform.smoothscale(original_bg, backgd_size)

# ==================== 【主菜单素材】 ====================
menu_bg_orig = pygame.image.load('material/images/Surface.jpg').convert_alpha()
menu_bg = pygame.transform.smoothscale(menu_bg_orig, backgd_size)

def load_and_scale(path, scale_factor=1.3):
    img = pygame.image.load(path).convert_alpha()
    new_size = (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))
    return pygame.transform.smoothscale(img, new_size)

btn_adv_img = load_and_scale('material/images/1.png')
btn_sur_img = load_and_scale('material/images/3.png')
btn_puz_img = load_and_scale('material/images/4.png')
btn_min_img = load_and_scale('material/images/5.png')

POS_ADV = (610, 50)
POS_MIN = (615, 165)
POS_PUZ = (620, 270)
POS_SUR = (625, 365)

btn_adv_rect = btn_adv_img.get_rect(topleft=POS_ADV)

# ==================== 【失败界面素材】 ====================
gameover_img = pygame.image.load('material/images/GameOver.png').convert_alpha()
gameover_rect = gameover_img.get_rect(center=(600, 250))


sunFlowerImg=pygame.image.load('material/images/SunFlower_00.png').convert_alpha()
wallNutImg=pygame.image.load('material/images/WallNut_00.png').convert_alpha()
peashooterImg=pygame.image.load('material/images/Peashooter_00.png').convert_alpha()

sunbackImg=pygame.image.load('material/images/SeedBank.png').convert_alpha()
flower_seed=pygame.image.load("material/images/TwinSunflower.gif")
wallNut_seed=pygame.image.load("material/images/WallNut.gif")
peashooter_seed=pygame.image.load("material/images/Peashooter.gif")

text='1000'
sun_font=pygame.font.Font(None, 25)
sun_num_surface=sun_font.render(text, True, (0,0,0))

bulletGroup=pygame.sprite.Group()
zombieGroup=pygame.sprite.Group()
wallNutGroup=pygame.sprite.Group()
PeashooterGroup=pygame.sprite.Group()
sunFlowerGroup=pygame.sprite.Group()

sunList = pygame.sprite.Group()

clock = pygame.time.Clock()

GEN_SUN_EVENT = pygame.USEREVENT+1
pygame.time.set_timer(GEN_SUN_EVENT, 1000)

GEN_BULLET_EVENT = pygame.USEREVENT+2
pygame.time.set_timer(GEN_BULLET_EVENT, 1000)

GEN_ZOMBIE_EVENT=pygame.USEREVENT+3
pygame.time.set_timer(GEN_ZOMBIE_EVENT, 5000)

GEN_FlagZOMBIE_EVENT=pygame.USEREVENT+4
pygame.time.set_timer(GEN_FlagZOMBIE_EVENT, 8000)

choose=0

STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2
STATE_WIN = 3

game_state = STATE_MENU  
TOTAL_ZOMBIES = 3       
spawned_zombies_cnt = 0  


def main():
    global text, choose
    global sun_num_surface
    global game_state, spawned_zombies_cnt  

    running = True
    index = 0

    while running:
        clock.tick(20)
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        # ==================== 1. 事件处理部分 ====================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if btn_adv_rect.collidepoint(pos):
                        game_state = STATE_PLAYING  

            elif game_state == STATE_PLAYING:
                if event.type == GEN_FlagZOMBIE_EVENT:
                    if spawned_zombies_cnt < TOTAL_ZOMBIES:  
                        zombie = FlagZombie()
                        zombieGroup.add(zombie)
                        spawned_zombies_cnt += 1

                if event.type == GEN_ZOMBIE_EVENT:
                    if spawned_zombies_cnt < TOTAL_ZOMBIES:  
                        zombie = Zombie()
                        zombieGroup.add(zombie)
                        spawned_zombies_cnt += 1

                if event.type == GEN_SUN_EVENT:
                    for sprite in sunFlowerGroup:
                        now = time.time()
                        if now - sprite.lasttime >= 5:
                            sun = Sun(sprite.rect)
                            sunList.add(sun)
                            sprite.lasttime = now

                if event.type == GEN_BULLET_EVENT:
                    for sprite in PeashooterGroup:
                        bullet = Bullet(sprite.rect, backgd_size)
                        bulletGroup.add(bullet)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    press_key = pygame.mouse.get_pressed()
                    if press_key[0] == 1:
                        pos = pygame.mouse.get_pos()
                        x, y = pos
                        if 330 <= x <= 380 and 10 <= y <= 80 and int(text) >= 50:  
                            choose = 1
                        elif 380 < x <= 430 and 10 <= y <= 80 and int(text) >= 50:  
                            choose = 2
                        elif 430 < x <= 480 and 10 <= y <= 80 and int(text) >= 100:
                            choose = 3
                        elif 250 < x < 1200 and 70 < y < 600:
                            
                            # ==============================================================
                            # ====== 【微调：完美居中！整体基准点向左、向上偏移】 ======
                            row = (y - 75) // 100
                            if row < 0: row = 0
                            if row > 4: row = 4
                            snap_y = 85 + row * 100  # Y基准从100提到了85

                            col = (x - 230) // 100
                            if col < 0: col = 0
                            if col > 8: col = 8
                            snap_x = 230 + col * 100 # X基准从250移到了230
                            # ==============================================================

                            is_occupied = False
                            for plant in list(sunFlowerGroup) + list(wallNutGroup) + list(PeashooterGroup):
                                if plant.rect.left == snap_x and plant.rect.top == snap_y:
                                    is_occupied = True
                                    break
                            
                            if not is_occupied:
                                if choose == 1:
                                    current_time = time.time()
                                    sunflower = Sunflower(current_time)
                                    sunflower.rect.top = snap_y
                                    sunflower.rect.left = snap_x   
                                    sunFlowerGroup.add(sunflower)
                                    choose = 0

                                    text = str(int(text) - 50)
                                    myfont = pygame.font.Font(None, 25)
                                    sun_num_surface = myfont.render(text, True, (0,0,0))
                                    
                                elif choose == 2:
                                    wallNut = WallNut()
                                    wallNut.rect.top = snap_y
                                    wallNut.rect.left = snap_x      
                                    wallNutGroup.add(wallNut)
                                    choose = 0

                                    text = str(int(text) - 50)
                                    myfont = pygame.font.Font(None, 25)
                                    sun_num_surface = myfont.render(text, True, (0,0,0))
                                    
                                elif choose == 3:
                                    peashooter = Peashooter()
                                    peashooter.rect.top = snap_y
                                    peashooter.rect.left = snap_x   
                                    PeashooterGroup.add(peashooter)
                                    choose = 0

                                    text = str(int(text) - 100)
                                    myfont = pygame.font.Font(None, 25)
                                    sun_num_surface = myfont.render(text, True, (0,0,0))

                    for sun in sunList:
                        if sun.rect.collidepoint(pos):
                            sunList.remove(sun)
                            text = str(int(text) + 50)
                            sun_num_surface = sun_font.render(text, True, (0,0,0))

            elif game_state in (STATE_GAMEOVER, STATE_WIN):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    zombieGroup.empty()
                    bulletGroup.empty()
                    sunFlowerGroup.empty()
                    PeashooterGroup.empty()
                    wallNutGroup.empty()
                    sunList.empty()
                    text = '1000'
                    sun_num_surface = sun_font.render(text, True, (0,0,0))
                    spawned_zombies_cnt = 0
                    game_state = STATE_MENU


        # ==================== 2. 画面渲染与逻辑更新部分 ====================
        if game_state == STATE_MENU:
            screen.blit(menu_bg, (0, 0))
            screen.blit(btn_adv_img, POS_ADV)
            screen.blit(btn_min_img, POS_MIN)
            screen.blit(btn_puz_img, POS_PUZ)
            screen.blit(btn_sur_img, POS_SUR)

        elif game_state == STATE_PLAYING:
            screen.blit(ba_img_obj, (0,0))
            screen.blit(sunbackImg, (250, 0))
            screen.blit(sun_num_surface, (270, 62))

            screen.blit(flower_seed, (330, 10))
            screen.blit(wallNut_seed, (380, 10))
            screen.blit(peashooter_seed, (430, 10))

            bulletGroup.update(index)
            bulletGroup.draw(screen)
            zombieGroup.update(index)
            zombieGroup.draw(screen)
            wallNutGroup.update(index)
            wallNutGroup.draw(screen)
            PeashooterGroup.update(index)
            PeashooterGroup.draw(screen)
            sunFlowerGroup.update(index)
            sunFlowerGroup.draw(screen)
            sunList.update(index)
            sunList.draw(screen)

            (x,y) = pygame.mouse.get_pos()
            if choose == 1:
                screen.blit(sunFlowerImg,(x,y))
            elif choose == 2:
                screen.blit(wallNutImg, (x, y))
            elif choose == 3:
                screen.blit(peashooterImg, (x, y))

            # ================= 【同步更新：将判定锁的基准修改为 85，缩减受击体积】 =================
            for bullet in bulletGroup:
                for zombie in zombieGroup:
                    bullet_row = (bullet.rect.top - 85) // 100
                    zombie_row = (zombie.rect.top - 30) // 100
                    if bullet_row == zombie_row and bullet.rect.colliderect(zombie.rect.inflate(-100, 0)):
                        zombie.energy -= 1
                        bulletGroup.remove(bullet)
                        break  

            for zombie in zombieGroup:
                zombie.isMeetWallNut = False

            for wallNut in wallNutGroup:
                wallNut.zombies.clear()
            for peaShooter in PeashooterGroup:
                peaShooter.zombies.clear()
            for sunFlower in sunFlowerGroup:
                sunFlower.zombies.clear()

            # 将植物裁掉 60（单边30），僵尸裁掉 100（单边50），逼迫它们必须物理贴脸！
            for wallNut in wallNutGroup:
                for zombie in zombieGroup:
                    plant_row = (wallNut.rect.top - 85) // 100
                    zombie_row = (zombie.rect.top - 30) // 100
                    if plant_row == zombie_row and wallNut.rect.inflate(-60, 0).colliderect(zombie.rect.inflate(-100, 0)):
                        zombie.isMeetWallNut = True        
                        wallNut.zombies.add(zombie)        

            for peaShooter in PeashooterGroup:
                for zombie in zombieGroup:
                    plant_row = (peaShooter.rect.top - 85) // 100
                    zombie_row = (zombie.rect.top - 30) // 100
                    if plant_row == zombie_row and peaShooter.rect.inflate(-60, 0).colliderect(zombie.rect.inflate(-100, 0)):
                        zombie.isMeetWallNut = True
                        peaShooter.zombies.add(zombie)

            for sunFlower in sunFlowerGroup:
                for zombie in zombieGroup:
                    plant_row = (sunFlower.rect.top - 85) // 100
                    zombie_row = (zombie.rect.top - 30) // 100
                    if plant_row == zombie_row and sunFlower.rect.inflate(-60, 0).colliderect(zombie.rect.inflate(-100, 0)):
                        zombie.isMeetWallNut = True
                        sunFlower.zombies.add(zombie)
            # =========================================================================
            
            for zombie in zombieGroup:
                if zombie.rect.left < 80 and zombie.isAlive:
                    game_state = STATE_GAMEOVER

            if spawned_zombies_cnt >= TOTAL_ZOMBIES and len(zombieGroup) == 0:
                game_state = STATE_WIN

            index += 1

        elif game_state == STATE_GAMEOVER:
            screen.blit(ba_img_obj, (0, 0))  
            screen.blit(gameover_img, gameover_rect)  
            tip_surf = pygame.font.Font(None, 40).render("Click screen to return to menu", True, (255, 255, 255))
            screen.blit(tip_surf, (400, 500))

        elif game_state == STATE_WIN:
            screen.blit(ba_img_obj, (0, 0))  
            win_surf = pygame.font.Font(None, 80).render("LEVEL CLEAR!", True, (0, 255, 0))
            tip_surf = pygame.font.Font(None, 40).render("Click screen to return to menu", True, (255, 255, 255))
            screen.blit(win_surf, (400, 220))
            screen.blit(tip_surf, (380, 320))

        pygame.display.update()

if __name__=='__main__':
    main()