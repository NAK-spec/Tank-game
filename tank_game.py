import pygame, sys, random

pygame.init()

# Screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mountain Tank Battle")
clock = pygame.time.Clock()

# Load images
tank1_img = pygame.image.load("tankBlue.png")
tank2_img = pygame.image.load("tankGreen.png")# new update
tank3_img = pygame.image.load("tankRed.png")
bullet_img = pygame.image.load("bulletBlue.png")
bullet_img = pygame.image.load("bulletRed.png")
bullet_img = pygame.image.load("bulletGreen.png")



# Resize images
tank1_img = pygame.transform.scale(tank1_img, (60, 60))
tank2_img = pygame.transform.scale(tank2_img, (60, 60))
tank3_img = pygame.transform.scale(tank3_img, (60, 60))
bullet_img = pygame.transform.scale(bullet_img,(15,15))
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

# Tank rectangles
tank1 = pygame.Rect(100, 300, 60, 60)
tank2 = pygame.Rect(400, 300, 60, 60)
tank3 = pygame.Rect(700, 300, 60, 60)

speed = 5
bullet_speed = 10
bullets = []
explosions = []

cliff_y = 550  # tank falls beyond this = lose

# Players list
players = [
    {"rect": tank1, "img": tank1_img, "color": "Red"},
    {"rect": tank2, "img": tank2_img, "color": "Green"},
    {"rect": tank3, "img": tank3_img, "color": "Blue"},
]

# Controls
controls = [
    {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_SPACE},
    {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_RETURN},
    {"up": pygame.K_i, "down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l, "shoot": pygame.K_u},
]

# Explosion function
def create_explosion(x, y):
    # Explosion is a list of expanding circles
    explosion = {"x": x, "y": y, "radius": 10, "max_radius": 50, "color": random.choice([(255,0,0),(255,165,0),(255,255,0)])}
    explosions.append(explosion)

running = True
winner = None

while running:
    clock.tick(60)
    screen.blit(background, (0,0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            for i, player in enumerate(players):
                if keys[controls[i]["shoot"]]:
                    bullets.append({"x": player["rect"].x+player["rect"].width//2,
                                    "y": player["rect"].y,
                                    "owner": player})

    # Move tanks
    for i, player in enumerate(players):
        rect = player["rect"]
        ctrl = controls[i]
        if keys[ctrl["left"]] and rect.x - speed > 0: rect.x -= speed
        if keys[ctrl["right"]] and rect.x + rect.width + speed < WIDTH: rect.x += speed
        if keys[ctrl["up"]] and rect.y - speed > 0: rect.y -= speed
        if keys[ctrl["down"]] and rect.y + rect.height + speed < HEIGHT: rect.y += speed

    # Move bullets and check collisions
    for bullet in bullets[:]:
        bullet["y"] -= bullet_speed
        if bullet["y"] < 0:
            bullets.remove(bullet)# small update
        else:
            for player in players:
                if player != bullet["owner"] and player["rect"].collidepoint(bullet["x"], bullet["y"]):
                    player["rect"].y += 20  # knockback
                    create_explosion(player["rect"].x, player["rect"].y)
                    if bullet in bullets:
                        bullets.remove(bullet)

    # Draw tanks
    for player in players:
        screen.blit(player["img"], (player["rect"].x, player["rect"].y))

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet_img, (bullet["x"], bullet["y"]))

    # Draw explosions
    for explosion in explosions[:]:
        pygame.draw.circle(screen, explosion["color"], (explosion["x"], explosion["y"]), explosion["radius"])
        explosion["radius"] += 3  # expand
        if explosion["radius"] > explosion["max_radius"]:
            explosions.remove(explosion)

    # Check if anyone fell off cliff
    for player in players:
        if player["rect"].y > cliff_y:
            winner = [p for p in players if p != player][0]
            running = False

    pygame.display.update() # small update

# Display winner
screen.fill((0,0,0))
font = pygame.font.SysFont(None, 60)
text = font.render(f"{winner['color']} Tank Wins!", True, (255,255,255))
screen.blit(text, (WIDTH//3, HEIGHT//2))
pygame.display.update()
pygame.time.delay(5000)

pygame.quit()
sys.exit()
