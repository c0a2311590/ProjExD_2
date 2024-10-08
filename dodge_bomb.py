import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0,-5),
         pg.K_DOWN: (0,5),
         pg.K_LEFT: (-5,0),
         pg.K_RIGHT: (5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとん,または,爆弾のRect
    戻り値:真理値タプル(横判定結果,縦判定結果)
    画面内ならTure,画面外ならFalse
    """
    side ,vertical = True,True
    if obj_rct.left < 0 or WIDTH< obj_rct.right:
        side = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        vertical = False
    return side,vertical


def game_over(screen:pg.Surface) -> None: 
    """
    引数:画面のスクリーン
    戻り値:なし
    画面を暗くしてゲームオーバーを表示
    """
    t_img = pg.Surface((WIDTH,HEIGHT))#サーフェイスを用意する
    pg.draw.rect(t_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))#黒い四角を用意
    t_img.set_alpha(128)#半透明にする
    screen.blit(t_img,(0,0))
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",True,(255,255,255))
    screen.blit(txt,(WIDTH/2-125,HEIGHT/2))#GameOverを表示
    bg_img = pg.image.load("fig/8.png")
    for i in range(2):
        screen.blit(bg_img,(WIDTH/2 - 250 + 500*i,HEIGHT/2))#こうかとんを表示
    pg.display.update()#画面をアップデート
    time.sleep(5)


def time_bom(tmr: int,vx: int,vy:int) -> tuple[int,int,pg.Surface]:
    """
    引数:タイマー、vx、vy
    戻り値：　vx,vy,bb_img
    速度と大きさの制御
    """
    for r in range(1, 11):
        if tmr//500 + 1< r:
            break
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0,0,0))#爆弾の四隅を透過させる
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    if tmr%500 ==0:
        i =vx//5
        avx = vx*(i+1)
        avy = vy*(i+1)
        if avx > 50:#制限速度を付ける
            avx = 50
            avy = 50
    else:
        avx = vx
        avy = vy
    return avx,avy,bb_img


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img =pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)#円の追加
    bb_rct = bb_img.get_rect()#爆弾rectの抽出
    bb_img.set_colorkey((0,0,0))#爆弾の四隅を透過させる
    bb_rct.center = random.randint(0, WIDTH), random.randint(0,HEIGHT)
    vx, vy = +5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):#こうかとんと爆弾が重なっていたら
            game_over(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        vx,vy,bb_img= time_bom(tmr,vx,vy)
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]#横方向
                sum_mv[1] += tpl[1]#縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        
        bb_rct.move_ip((vx,vy))
        side ,vertical = check_bound(bb_rct)
        if not side:
            vx *= -1
        if not vertical:
            vy *= -1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
