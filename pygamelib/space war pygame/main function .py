def main():
    red = pygame.Rect(700,300,space_w,space_h)
    yellow = pygame.Rect(100,300,space_w,space_h)

    RED_bullets =[]
    YELLOW_BULLETS = []

    red_health = 20
    yellow_health = 20

    Clock = pygame.time.Clock()
    
    run = True
    while run:
        Clock.tick(fps)
        

        for event in pygame.event.get():
            if event .type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(YELLOW_BULLETS) < max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width , yellow.y + yellow.height//2 - 2 , 10 ,5)
                    YELLOW_BULLETS.append(bullet)
                    bullet_firesound.play()


                if event.key == pygame.K_RCTRL and len(RED_bullets) < max_bullets :  
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2 , 10 ,5) 
                    RED_bullets.append(bullet)
                    bullet_firesound.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                bullet_hitsound.play()

            if event.type == YELLOW_HIT: 
                yellow_health -= 1  
                bullet_hitsound.play()

        winner_text =" "    
        if red_health <=0:
            winner_text = " YELLOW WINS      KNOCK OUT !!"

        if yellow_health <=0 :  
            winner_text = " RED WINS          KNOCK OUT !!"
        if winner_text != " "  :
            winner( winner_text)   
            break
         
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)

        handle_bullets( YELLOW_BULLETS,RED_bullets,yellow,red)

        draw_window( red , yellow , RED_bullets ,YELLOW_BULLETS , red_health , yellow_health)



    main()

if __name__ == "__main__" :
    main()
