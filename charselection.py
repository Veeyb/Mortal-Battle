import pygame

class CharacterSelection:
    def __init__(self, screen, characters_dict):
        self.screen = screen
        self.characters_dict = characters_dict
        self.characters = list(characters_dict.keys())
        self.width, self.height = self.screen.get_size()
        self.font = pygame.font.Font("assets/fonts/turok.ttf", 40)
        self.small_font = pygame.font.Font("assets/fonts/turok.ttf", 25)

        self.current_index = 0
        self.player_turn = 1
        self.selected = {1: None, 2: None}

    def draw(self):
        self.screen.fill((0, 0, 0))

        title_text = self.font.render(f"Player {self.player_turn} Select Character", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        back_text = self.small_font.render("Back (Esc)", True, (255, 255, 255))
        self.screen.blit(back_text, (20, 20))

        instr_text = self.small_font.render("Use UP/DOWN to scroll, ENTER to select", True, (200, 200, 200))
        self.screen.blit(instr_text, (self.width // 2 - instr_text.get_width() // 2, self.height - 60))

        # Skip karakter yang sudah dipilih lawan saat menampilkan preview
        other_player = 2 if self.player_turn == 1 else 1
        temp_index = self.current_index
        while self.characters[temp_index] == self.selected.get(other_player):
            temp_index = (temp_index + 1) % len(self.characters)
            if temp_index == self.current_index:
                break  # Semua karakter sudah dipilih lawan
        self.current_index = temp_index

        char_key = self.characters[self.current_index]
        character_obj = self.characters_dict[char_key]

        idle_frames = character_obj.animation_list.get("IDLE", [])
        if idle_frames:
            frame = idle_frames[0]
            frame_rect = frame.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(frame, frame_rect)

        name_surf = self.font.render(char_key, True, (255, 255, 255))
        self.screen.blit(name_surf, (self.width // 2 - name_surf.get_width() // 2, self.height // 2 + 100))

        # Tampilkan tanda karakter yang sudah dipilih masing-masing player
        for p in [1, 2]:
            if self.selected[p] == char_key:
                mark_text = self.small_font.render(f"P{p} Selected", True, (255, 255, 0))
                self.screen.blit(mark_text, (self.width // 2 - mark_text.get_width() // 2, self.height // 2 + 70))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.current_index = (self.current_index + 1) % len(self.characters)
                other_player = 2 if self.player_turn == 1 else 1
                while self.characters[self.current_index] == self.selected.get(other_player):
                    self.current_index = (self.current_index + 1) % len(self.characters)
            elif event.key == pygame.K_UP:
                self.current_index = (self.current_index - 1) % len(self.characters)
                other_player = 2 if self.player_turn == 1 else 1
                while self.characters[self.current_index] == self.selected.get(other_player):
                    self.current_index = (self.current_index - 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                chosen = self.characters[self.current_index]
                other_player = 2 if self.player_turn == 1 else 1
                if chosen == self.selected.get(other_player):
                    # Karakter sudah dipilih lawan, tolak pemilihan
                    # Bisa tambahkan feedback suara atau teks jika ingin
                    return None
                self.selected[self.player_turn] = chosen
                self.player_turn = 2 if self.player_turn == 1 else 1
                if self.selected[1] and self.selected[2]:
                    return "start"
            elif event.key == pygame.K_ESCAPE:
                return "back"
        return None

def run_character_selection(screen, characters_dict):
    selection = CharacterSelection(screen, characters_dict)
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            res = selection.handle_event(event)
            if res == "start":
                return (1, selection.selected[1], selection.selected[2])
            elif res == "back":
                return "back"
        selection.draw()
        pygame.display.update()
