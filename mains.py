message_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
message_surface = message_surface.convert_alpha()
ui_manager2 = pygame_gui.UIManager(WINDOW_SIZE, r'./ui_themes/json/message.json')


class Initial:
    def __init__(self, manager, surface):
        self.manager = manager
        self.surface = surface

        self.son_window = pygame_gui.elements.ui_window.UIWindow(
            rect=pygame.Rect(((WINDOW_SIZE[0] - 500) / 2, (WINDOW_SIZE[1] - 300) / 2, 400, 200)),
            window_display_title="提示",
            manager=self.manager,
            object_id='window')

        self.text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(100, 20, 200, 50),
            text="有效数字位数不对！",
            manager=self.manager,
            container=self.son_window,
            object_id='message')

        self.OK_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 80, 100, 30)),
            text="确认",
            manager=self.manager,
            container=self.son_window,
            object_id='button')

while is_running:  # 主程序
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == initial.OK_button:
                    initial.son_window.hide()
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if len(event.text) != 5:
                    initial = Initial(manager=ui_manager2, surface=message_surface)


        ui_manager2.process_events(event)

    message_surface.fill((0, 0, 0, 0))
    ui_manager2.update(time_delta)
    ui_manager2.draw_ui(message_surface)
    window_surface.blit(message_surface, (0, 0))

    pygame.display.update()
