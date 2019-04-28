import textwrap 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from operator import truediv, mul
from lucs_tools.formatting import ascii_canvas

class joyful:

    ORIGINAL_DIMS = (204., 167.)
    DESIGN_DIMS = (625, 593, 140, 100)

    @staticmethod
    def _scale_facs(
        size,
    ):
        return list(map(truediv, size, joyful.DESIGN_DIMS[0:2]))

    @staticmethod
    def _get_boundaries(
        size,
    ):
        scale = min(joyful._scale_facs(size))
        return [
                [- joyful.DESIGN_DIMS[3]*scale, - joyful.DESIGN_DIMS[2]*scale],
                [joyful.DESIGN_DIMS[3]*scale + size[0], joyful.DESIGN_DIMS[2]*scale + size[1]]
        ]

    @staticmethod
    def _rand(
        min,
        max
    ):
        return np.random.random()*(max - min) + min

    @staticmethod
    def _rand_int(
        min,
        max
    ):
        return int(np.floor(np.random.random()*(max - min + 1)) + min)
    
    @staticmethod
    def _rand_normal(
        mu,
        sigma,
        n=6
    ):
        sum = 0
        for i in range(n):
            sum += joyful._rand(-1., 1.)
        return mu + sigma*sum / n

    @staticmethod
    def _normal_pdf(
        x,
        mu,
        sigma
    ):
        num = np.e**(-((x-mu)**2.)/(2.*(sigma**2.)))
        denom = np.sqrt(2.*np.pi*(sigma**2.))
        return num/denom

    @staticmethod
    def _textwrap_converge(
        text_str,
        n_lines
    ):
        text_lines = len(text_str)
        while len(textwrap.wrap(text_str, text_lines)) < n_lines:
            text_lines -= 1
        return textwrap.wrap(text_str, text_lines)

    @staticmethod    
    def _points(
        lines=60,
        points=80,
        size=(625, 593)
    ):
        # set up all this trash... 
        width = joyful.DESIGN_DIMS[0]
        height = joyful.DESIGN_DIMS[1]
        xmin = joyful.DESIGN_DIMS[2]
        xmax = width - xmin
        ymin = joyful.DESIGN_DIMS[3]
        ymax = height - ymin
        mx = 0.5*(xmin + xmax)
        dx = (xmax - xmin) / points
        dy = (ymax - ymin) / lines
        x = xmin
        y = ymin
        xplt = np.empty(points)
        yplt = np.empty((lines, points))
        for i in range(lines):
            nmodes = joyful._rand_int(1, 4)
            mus = np.empty(nmodes)
            sigmas = np.empty(nmodes)
            for j in range(nmodes):
                mus[j] = joyful._rand(mx - 50., mx + 50.)
                sigmas[j] = joyful._rand_normal(24, 30)
            w = y
            for k in range(points):
                x = x + dx
                noise = 0
                for l in range(nmodes):
                    noise += joyful._normal_pdf(x, mus[l], sigmas[l])
                yy = 0.3*w + 0.7*(y - 600 * noise + noise * np.random.random() * 200 + np.random.random())
                yplt[i,k] = yy
                xplt[k] = x
                w = yy
            x = xmin
            y = y + dy
        (max_x, max_y), (min_x, min_y) = [map(f, [xplt, yplt]) for f in [np.max, np.min]]
        return (xplt - min_x)*size[0]/(max_x - min_x), (max_y - yplt)*size[1]/(max_y - min_y)
        # return size[0]*xplt/np.max(xplt), (1 - ((yplt - joyful.DESIGN_DIMS[4])/np.max(yplt)))*size[1]

    @staticmethod
    def lines(
        width,
        height,
        linewidth=1.,
        size=(400, 600),
        dpi=96,
        inverted=False,
        title=None,
        mode='normal',
    ):

        modes = ['normal', 'bright', 'transparent']

        if mode not in modes:
            raise TypeError("Mode '{}' not in known modes {}".format(mode, modes))

        main, sub = 'black', 'white'

        if inverted:
            main, sub = sub, main

        x, ys = joyful._points(height, width, size)
        psize = np.squeeze(np.diff(joyful._get_boundaries(size), axis=0))
        fig = plt.figure(figsize=(psize[0]/dpi, psize[1]/dpi), dpi=dpi)
        ax = plt.gca()
        xr, yr = [np.asarray(joyful._get_boundaries(size))[:,i] for i in range(2)]
        plt.fill_between(xr,[yr[0], yr[0]], [yr[1], yr[1]], color=main)
        max_y = np.zeros(x.shape)
        if mode=='bright':
            for y in np.flip(ys, axis=0):
                max_y = np.max([y, max_y], axis=0)
                plt.plot(x, max_y, c=sub, linewidth=linewidth)
        elif mode=='transparent':
            for y in ys:
                plt.plot(x, y, c=sub, linewidth=linewidth)
        else:
            for y in ys:
                plt.fill_between(x, y, np.zeros(y.shape), facecolor=main, edgecolor=main, alpha=1., linewidth=linewidth)
                plt.fill_between(x, y, y, color=sub, linewidth=linewidth)
            


        # for vertex in joyful._get_boundaries(size):
        #     print(vertex)
        #     plt.plot(*vertex, 'ro') 
        
        ax = plt.gca()
        ax.set_aspect('equal')
        
        if title is not None:
            plt.title(title)
        
        # ax.set_facecolor('black')
        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])
        for spot in ['top', 'right', 'bottom', 'left']:
            ax.spines[spot].set_visible(False)
        plt.tight_layout()

        plt.show()
        
    @staticmethod
    def ascii(
        text,
        width,
        height,
        wskip=0,
        hskip=1,
        remove_whitespace=False,
    ):

        text += ' '
        if remove_whitespace:
            text = text.replace(' ', '')

        while len([text[i:i+width] for i in range(0, len(text), width)]) <= height:
            text += text

        text = np.flip([text[i:i+width] for i in range(0, len(text), width)][0:height], axis=0)

        x, ys = joyful._points(height, width, ((wskip + 1)*(width - 1), (hskip + 1)*(height - 1)))
        
        # renormalize to edges for ascii 
        ys = ( ys / np.max(np.mean([ys[:,-1], ys[:,0]], axis=0) ) )*((hskip + 1)*(height - 1))

        assert(len(x) == width)
        
        canvas = ascii_canvas(list(map(int, (np.ceil(np.max(x) + 1), np.ceil(np.max(ys) + 1)))))

        ys = np.flip(ys, axis=0)

        max_y = -np.ones(x.shape)

        for i in range(height):
            for j in range(len(text[i])):
                yplt = int(np.round(ys[i, j]))
                xplt = int(np.round(x[j]))
                if yplt > max_y[j]:
                    canvas[xplt, yplt] = text[i][j]
                    max_y[j] = yplt

        canvas = np.flip(canvas, axis=1)
        
        return canvas.raw()
        

        # max_y = np.zeros(x.shape)   

        # for i in range(lines):
        #     for j in range(len(text[i])):
        #         if ys[i,j] > max_y[j] + factor:
        #             plt.text(x[j], ys[i,j], text[i][j], fontsize=fontsize, weight=weight, color='white', verticalalignment='top', horizontalalignment='left')
        #     max_y = np.max([ys[i], max_y], axis=0)
        #     if write_lines:
        #         plt.plot(x, max_y, c='white', linewidth=0.5)

        # for vertex in joyful._get_boundaries(size):
        #     print(vertex)
        #     plt.plot(*vertex, 'ro') 

        # # plt.plot(x, np.min(ys, axis=0), 'black')
        # # plt.plot(x[0], ys[0,-1])
        # # plt.plot(x, np.max(ys, axis=0), 'black')
        # ax = plt.gca()
        # ax.set_aspect('equal')
        # # ax.set_facecolor('black')
        # ax.axes.get_xaxis().set_ticks([])
        # ax.axes.get_yaxis().set_ticks([])
        # for spot in ['top', 'right', 'bottom', 'left']:
        #     ax.spines[spot].set_visible(False)
        # plt.tight_layout()
        # plt.show()
    
    @staticmethod
    def text(
        text,
        size=(400,800),
        fontsize=6.,
        spacing=2.,
        weight='light',
        replace=False,
        write_lines=False,
        factor=1.,
        dpi=96.,
        inverted=False,
    ):
        main, sub = 'black', 'white'
        if inverted:
            main, sub = sub, main

        fontwidth=.7*fontsize
        fontheight=fontsize
        spcwidth=0.1*spacing
        spcheight=2.*spacing
        points=int(size[0]/(fontwidth + spcwidth))
        lines=int(size[1]/(fontheight + spcheight))

        text += ' '
        if replace:
            text = text.replace(' ', '')

        while len([text[i:i+points] for i in range(0, len(text), points)]) <= lines:
            text += text

        text = np.flip([text[i:i+points] for i in range(0, len(text), points)][0:lines], axis=0)

        size = (size[0] + points*spcwidth, size[1] + lines*spcheight)

        x, ys = joyful._points(lines, points, size)
        ys = np.flip(ys, axis=0)

        max_y = np.zeros(x.shape)   

        psize = np.squeeze(np.diff(joyful._get_boundaries(size), axis=0))
        plt.figure(figsize=(psize[0]/dpi, psize[1]/dpi), dpi=dpi)
        ax = plt.gca()
        ax.add_patch(patches.Rectangle(joyful._get_boundaries(size)[0], *psize, color=main))

        for i in range(lines):
            for j in range(len(text[i])):
                if ys[i,j] > max_y[j] + factor:
                    plt.text(x[j], ys[i,j], text[i][j], fontsize=fontsize, weight=weight, color='white', verticalalignment='top', horizontalalignment='left')
            max_y = np.max([ys[i], max_y], axis=0)
            if write_lines:
                plt.plot(x, max_y, c='white', linewidth=0.5)

        for vertex in joyful._get_boundaries(size):
            print(vertex)
            plt.plot(*vertex, 'ro') 

        # plt.plot(x, np.min(ys, axis=0), 'black')
        # plt.plot(x[0], ys[0,-1])
        # plt.plot(x, np.max(ys, axis=0), 'black')
        ax = plt.gca()
        ax.set_aspect('equal')
        # ax.set_facecolor('black')
        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])
        for spot in ['top', 'right', 'bottom', 'left']:
            ax.spines[spot].set_visible(False)
        plt.tight_layout()
        plt.show()
    
    def __trashcanman(
        self
    ):
        pass
        # @staticmethod
        # def joy_text(
        #     text,
        #     points,
        #     fontsize=6,
        #     weight='light',
        #     size=(625, 593),
        #     subaspect=1.4,
        #     factor=1.,
        #     replace=False,
        #     write_lines=False,
        # ):
        #     # formatted = _textwrap_converge(data, lines)
        #     if replace:
        #         text = text.replace(' ', '')
        #     formatted = textwrap.wrap(text, points)
        #     lines = len(formatted)
        #     points = max(map(len, formatted))
        #     x, ys = joyful._points(lines, points, size)
        #     formatted = np.flip(formatted, axis=0)
        #     ys = np.flip(ys, axis=0)
        #     max_y = np.zeros(x.shape)   

        #     for i in range(lines):
        #         for j in range(len(formatted[i])):
        #             if ys[i,j] > max_y[j] + factor:
        #                 plt.text(x[j], ys[i,j], formatted[i][j], fontsize=fontsize, weight=weight, color='white', verticalalignment='top', horizontalalignment='left')
        #         max_y = np.max([ys[i], max_y], axis=0)
        #         if write_lines:
        #             plt.plot(x, max_y, c='white', linewidth=0.5)

        #     plt.plot(x, np.min(ys, axis=0), 'black')
        #     #plt.plot(x[0], ys[0,-1])
        #     plt.plot(x, np.max(ys, axis=0), 'black')
        #     ax = plt.gca()
        #     ax.set_aspect(subaspect*float(lines)/float(points))
        #     ax.set_facecolor('black')
        #     ax.axes.get_xaxis().set_ticks([])
        #     ax.axes.get_yaxis().set_ticks([])
        #     plt.show()
        