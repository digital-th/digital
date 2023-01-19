import pygame
from pygame.locals import *
import sys
import pandas as pd

N = 8  # 問題数
WIDTH = 700  # 幅
HEIGHT = 500  # 高さ

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)  # 画面サイズ指定
scene = 0  # 0:初期場面 1:1場面 2: 2場面

# 背景画像の取得
bg = pygame.image.load("images/bg.jpg").convert_alpha()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))  # 600 * 400に画像を縮小
rect_bg = bg.get_rect()

# プレイヤー画像の取得
player = pygame.image.load("images/player.png").convert_alpha()
player = pygame.transform.scale(player, (80, 80))  # 600 * 400に画像を縮小
rect_player = player.get_rect()

# 看板を格納する配列
signs = []
rect_signs = []

# 問題文を格納する配列
probs = []
rect_probs = []

once = [True, True, True]

def main():
    global screen, once
    pygame.init()  # pygame初期化
    pygame.key.set_repeat(500, 30)  # 操作キーを押しっぱなしで移動できるための準備(delay, interval)
    loadProblems()  # 問題を読み込む
    loadSignBoards()  # 看板を読み込む
    rect_player.center = (WIDTH-50, HEIGHT-50)  # プレイヤー画像の初期位置

    visibles = [False]*10
    clears = [False]*10
    font = pygame.font.Font(None, 35) 
    df = pd.read_csv('images/problems/answer.csv', sep=",", names=["id", "answer"], header=0)

    while (1):
        pygame.display.update()  # 画面更新
        pygame.time.wait(30)  # 更新時間間隔

        screen.blit(bg, rect_bg)  # 背景画像の描画

        if scene == 0:
            displayStage(1, 0, scene, clears)
        elif scene == 1:
            displayStage(2, 0, scene, clears)
        elif scene == 2:
            displayStage(3, 1, scene, clears)
        elif scene == 3:
            displayClear()

        screen.blit(player, rect_player)  # プレイヤー画像の描画

        for i in range(N):
            # 看板とプレイヤーが接触した場合
            if visibles[i] and rect_player.colliderect(rect_signs[i]) and not clears[i]:
                screen.blit(probs[i], rect_probs[i])
                displayBox(font, df, i)
                clears[i] = True
            else:
                visibles[i] = False

        # 終了用のイベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたとき
                pygame.quit()  # pygameの終了
                sys.exit()
            if event.type == KEYDOWN:  # キーを押したとき
                pygame.key.get_repeat()  # 操作キーを長押しで移動可能にする
                if event.key == K_LEFT:
                    rect_player.move_ip(-15, 0)
                if event.key == K_RIGHT:
                    rect_player.move_ip(15, 0)
                if event.key == K_UP:
                    for i in range(N):
                        if rect_player.colliderect(rect_signs[i]):
                            if scene == 0 and i < 3:
                                visibles[i] = True
                            elif scene == 1 and i < 6:
                                visibles[i] = True
                            elif scene == 2 and i < 9:
                                visibles[i] = True

# 看板を読み込む
def loadSignBoards():
    global signs, rect_signs

    for i in range(N):
        signs.append(pygame.image.load('images/sign.png'))
        signs[i] = pygame.transform.scale(signs[i], (60, 70))
        rect_signs.append(signs[i].get_rect())


# 問題文を読み込む
def loadProblems():
    global probs, rect_probs

    prob_path = 'images/problems/'
    for i in range(N):
        probs.append(pygame.image.load(
            prob_path + 'prob{}.png'.format(i)))  # 問題文の取得
        probs[i] = pygame.transform.scale(
            probs[i], (WIDTH*4/5, HEIGHT*4/5))  # size変更
        rect_probs.append(probs[i].get_rect())
        rect_probs[i].center = (WIDTH/2, HEIGHT*2/5)  # 問題文の位置を指定する

def displayStage(forward, backward, idx, clears):  
    global scene, once  # 無限ループ防止対策
    ds = 3
    # player位置リセット
    if once[idx]:
        if rect_player.left < -40:
            rect_player.center = (WIDTH-50, HEIGHT-50)
        if rect_player.right > WIDTH + 40:
            rect_player.center = (50, HEIGHT-50)
        once[idx] = False

    n = 3    
    if scene == 2:
        n = 2     
    for i in range(n):
        rect_signs[i+ds*idx].center = (WIDTH*(5-2*i)/6, HEIGHT-45)  # 看板画像の位置指定
        screen.blit(signs[i+ds*idx], rect_signs[i+ds*idx])  # 看板画像の描画

    # 画面端にきたら場面を変える
    if rect_player.left < -40 or rect_player.right > WIDTH + 40:
        if rect_player.left < -40 and all(clears[idx*3:(idx+1)*3]):
            scene = forward
        if scene == 2 and all(clears[6:8]):
            scene = forward
        if rect_player.right > WIDTH + 40:
            scene = backward
        once[idx] = True

def displayBox(font, df, idx):
    answer = ""
    limit = 10

    while True:
        update(font, answer)                 
        # イベント処理
        for event in pygame.event.get():  #イベントを取得
            if event.type == QUIT:  # 閉じるボタンが押されたとき
                pygame.quit()  # pygameの終了
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_BACKSPACE: #修正で戻る
                    if len(answer) >= 1:
                        answer = answer[:-1] 
                elif event.key == K_RETURN: #エンターキー
                    if isCorrect(answer, df, idx):
                        return 
                    else:
                        answer = ""
                        break    

                if len(answer) < limit: 
                    if event.key == K_PERIOD: #ピリオドが入力された 
                        answer+="."
                    if event.key == K_SLASH:
                        answer+="/"    
                    else: 
                        for i in range(10): #0-9キーが入力された
                            if event.key==48+i: 
                                answer+=str(i)
                                break    

def update(font, txt):
    pygame.draw.rect(screen, (255, 255, 255), Rect(rect_player.center[0]-50, 380, 150, 30)) #ボックス内を塗潰す
    answer_g = font.render(txt, True, (55, 55, 55)) #描画する文字列を画像にする
    screen.blit(answer_g, [rect_player.center[0]-50+5, 380+5])  #画像を表示        
    pygame.display.update() 

def isCorrect(input, df, i):
    answer = df["answer"][i]
    if input == answer: 
        return True
    else:
        return False    

def displayClear():
    font = pygame.font.Font(None, 300) 
    pygame.draw.rect(screen, (255, 255, 255), Rect(25, 25, WIDTH-50, HEIGHT-50)) #ボックス内を塗潰す
    clear_g = font.render("Clear!", True, (55, 55, 55)) #描画する文字列を画像にする
    screen.blit(clear_g, [25+5, HEIGHT/2-100])  #画像を表示        
    pygame.display.update() 

if __name__ == '__main__':
    main()

