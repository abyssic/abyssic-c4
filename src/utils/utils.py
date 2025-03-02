from rgbprint import gradient_print


class Utils:
    GREEN = ((0, 255, 0), (0, 128, 0))
    RED = ((255, 0, 0), (128, 0, 0))
    RAINBOW = ((0, 255, 255), (128, 0, 255))
    YELLOW = ((255, 165, 0), (255, 69, 0))
    
    @classmethod
    def colorize(cls, text, option='info'):
        match option:
            case 'ok':
                return gradient_print(text, start_color=cls.GREEN[0], end_color=cls.GREEN[1])
            case 'error':
                return gradient_print(text, start_color=cls.RED[0], end_color=cls.RED[1])
            case 'info':
                return gradient_print(text, start_color=cls.YELLOW[0], end_color=cls.YELLOW[1])
            case 'menu':
                return gradient_print(text, start_color=cls.RAINBOW[0], end_color=cls.RAINBOW[1])
