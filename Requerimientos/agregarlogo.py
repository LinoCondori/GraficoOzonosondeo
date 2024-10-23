from PIL import Image
def get_concat_h_multi_resize(im_list, resample=Image.BICUBIC):
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample)
                      for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst

def get_concat_v_multi_resize(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst

def get_concat_tile_resize(im_list_2d, resample=Image.BICUBIC):
    im_list_v = [get_concat_h_multi_resize(im_list_h, resample=resample) for im_list_h in im_list_2d]
    return get_concat_v_multi_resize(im_list_v, resample=resample)


def crear(fig_temp, axes_Temp, filename):

    extent = axes_Temp.get_window_extent().transformed(fig_temp.dpi_scale_trans.inverted())

    fig_temp.savefig(filename, dpi=300, bbox_inches=extent.expanded(1.1, 1.2))

    im1 = Image.open(filename)
    im2 = Image.open('SMN_Logo.jpg')
    im3 = Image.open('TDF_Logo.jpg')
    get_concat_tile_resize([[im1],
                            [im2, im2, im2, im2, im2, im3]]).save(filename)

def crearGeneral(fig, axes, filename='General'):
    extent = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

    fig.savefig(filename, dpi=500, bbox_inches=extent.expanded(0.9, 0.95))

    im1 = Image.open(filename)
    im2 = Image.open('Requerimientos/VAG_Logo.jpg')
    im3 = Image.open('Requerimientos/SMN_Logo.jpg')
    im4 = Image.open('Requerimientos/TDF_Logo.jpg')
    get_concat_tile_resize([[im1],
                            [ im2, im3, im4]]).save(filename)

