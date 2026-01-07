class XVar:
    def __init__(self):
        self.mlx = None
        self.mlx_ptr = None
        self.screen_w = 0
        self.screen_h = 0
        self.win_1 = None
        self.win_2 = None
        self.imgidx = 0
        # image fields
        self.img = None
        self.img_data = None
        self.img_bpp = 0
        self.img_sl = 0
        self.img_format = 0
        self.img_w = 0
        self.img_h = 0


def manage_close(xvar):
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def manage_key_simple(key, xvar):
    if key in (113, 27, 65307):
        xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)
        return 0
    return 0


def manage_expose(xvar):
    if xvar.img:
        xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win_1, xvar.img,
                                         0, 0)
