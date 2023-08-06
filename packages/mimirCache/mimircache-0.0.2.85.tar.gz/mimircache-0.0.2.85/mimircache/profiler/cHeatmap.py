# coding=utf-8
"""
This module provides all the heatmap related plotting


TODO: refactoring

Author: Jason Yang <peter.waynechina@gmail.com> 2016/08

"""



import numpy as np
from matplotlib import colors
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

from mimircache.const import CExtensionMode
if CExtensionMode:
    import mimircache.c_heatmap
from mimircache import const
from mimircache.utils.printing import *


class cHeatmap:
    def __init__(self):
        self.other_plot_kwargs = {}

    def get_breakpoints(self, reader, mode, time_interval=-1, num_of_pixels=-1):
        """

        :param num_of_pixels:
        :param reader:
        :param mode:
        :param time_interval:
        :return: a numpy list of break points begin with 0, ends with total_num_requests
        """
        assert time_interval!=-1 or num_of_pixels!=-1, \
            "please provide at least one parameter, time_interval or num_of_pixels"
        return mimircache.c_heatmap.get_breakpoints(reader.cReader, mode,
                                                    time_interval=time_interval,
                                                    num_of_pixels=num_of_pixels)

    def setPlotParams(self, axis, axis_type, **kwargs):
        log_base = 1
        label = ''
        tick = None
        xydict = None

        if 'xydict' in kwargs:
            xydict = kwargs['xydict']

        if 'log_base' in kwargs:
            log_base = kwargs['log_base']

        if 'fixed_range' in kwargs and kwargs['fixed_range']:
            # if 'vmin' in kwargs:
            #     self.other_plot_kwargs['vmin'] = kwargs['vmin']
            # vmin, vmax = kwargs['fixed_range']
            # self.other_plot_kwargs['vmin'] = 0
            # self.other_plot_kwargs['vmax'] = 1
            self.other_plot_kwargs['fixed_range'] = kwargs['fixed_range']

        if 'other_kwargs' in kwargs:
            self.other_plot_kwargs.update(kwargs['other_kwargs'])

        if 'text' in kwargs:
            ax = plt.gca()
            ax.text(kwargs['text'][0], kwargs['text'][1], kwargs['text'][2])  # , fontsize=20)  , color='blue')

        if axis == 'x':
            assert 'xydict' in kwargs, "you didn't provide xydict"
            array = xydict[0]
        elif axis == 'y':
            assert 'xydict' in kwargs, "you didn't provide xydict"
            array = xydict
        elif axis == 'cb':  # color bar
            if axis_type == 'count':
                self.other_plot_kwargs['norm'] = colors.LogNorm()
        else:
            print("unsupported axis: " + str(axis))

        if axis_type == 'virtual time':
            if 'label' in kwargs:
                label = kwargs['label']
            else:
                label = 'virtual time'
            # tick = ticker.FuncFormatter(lambda x, pos: '{:2.0f}'.format(bin_size * x))
            tick = ticker.FuncFormatter(lambda x, pos: '{:2.0f}%'.format(x * 100 / (len(array) - 1)))
        elif axis_type == 'real time':
            if 'label' in kwargs:
                label = kwargs['label']
            else:
                label = 'real time'
            # tick = ticker.FuncFormatter(lambda x, pos: '{:2.0f}'.format(bin_size * x))
            tick = ticker.FuncFormatter(lambda x, pos: '{:2.0f}%'.format(x * 100 / (len(array) - 1)))

        elif axis_type == 'cache_size':
            assert log_base != 1, "please provide log_base"
            label = 'cache size'
            tick = ticker.FuncFormatter(lambda x, pos: '{:2.0f}'.format(log_base ** x))

        elif axis_type == 'reuse_dist' or axis_type == "distance":
            assert log_base != 1, "please provide log_base"
            label = 'reuse distance'
            tick = ticker.FuncFormatter(lambda x, pos: '{:2.0f}'.format(log_base ** x-1))

        if axis == 'x':
            plt.xlabel(label)
            plt.gca().xaxis.set_major_formatter(tick)

        elif axis == 'y':
            plt.ylabel(label)
            plt.gca().yaxis.set_major_formatter(tick)

        elif axis == 'cb':
            pass

        else:
            print("unsupported axis: " + str(axis))

    def heatmap(self, reader, mode, plot_type, algorithm="LRU", time_interval=-1, num_of_pixels=-1,
                cache_params=None, **kwargs):
        """

        :param cache_params:
        :param num_of_pixels:
        :param time_interval:
        :param algorithm:
        :param plot_type:
        :param mode:
        :param reader:
        :param kwargs: include num_of_threads, figname, decay_coefficient (default: 0.2)
        :return:
        """

        DEFAULT_DECAY_COEFFICIENT = 0.2
        figname = None
        self.time_interval = time_interval
        self.num_of_pixels = num_of_pixels
        # assert time_interval != -1 or num_of_pixels != -1, \
        #     "please provide at least one parameter, time_interval or num_of_pixels"
        self.mode = mode
        reader.reset()

        if 'cache_size' in kwargs:
            cache_size = kwargs['cache_size']
        else:
            cache_size = -1            

        if 'num_of_threads' in kwargs:
            num_of_threads = kwargs['num_of_threads']
        else:
            num_of_threads = 4

        if 'figname' in kwargs:
            figname = kwargs['figname']

        if mode == 'r' or mode == 'v':
            if mode == 'r':
                mode_string = "real time"
            else:
                mode_string = "virtual time"

            if plot_type == "hit_ratio_start_time_end_time":
                # assert algorithm!=None, "please specify your cache replacement algorithm in heatmap plotting"
                assert cache_size != -1, "please provide cache_size parameter for plotting hit_ratio_start_time_end_time"
                # this is used to specify the type of hit ratio for each pixel, when it is False, it means
                # the hit ratio is the average hit ratio from beginning of trace,
                # if True, then the hit ratio will be exponentially decayed average hit ratio from beginning plus
                # the hit ratio in current time interval, the coefficient decay_coefficient specify the ratio of
                # average hit ratio in the new calculation
                enable_ihr = False
                decay_coefficient  = DEFAULT_DECAY_COEFFICIENT
                if 'interval_hit_ratio'in kwargs or "enable_ihr" in kwargs:
                    enable_ihr = kwargs.get("interval_hit_ratio", False) or kwargs.get("enable_ihr", False)
                    decay_coefficient  = kwargs.get("decay_coefficient", DEFAULT_DECAY_COEFFICIENT)



                if algorithm.lower() in const.c_available_cache:
                    xydict = mimircache.c_heatmap.heatmap(reader.cReader, mode, plot_type,
                                               cache_size, algorithm,
                                               interval_hit_ratio=enable_ihr,
                                               decay_coefficient=decay_coefficient,
                                               time_interval=time_interval,
                                               num_of_pixels=num_of_pixels,
                                               cache_params=cache_params,
                                               num_of_threads=num_of_threads)
                else:
                    raise RuntimeError("haven't provided support given algorithm in C yet: " + str(algorithm))
                    pass

                text = "      " \
                       "cache size: {},\n      cache type: {},\n      " \
                       "time type:  {},\n      time interval: {},\n      " \
                       "plot type: \n{}".format(cache_size,
                                                algorithm, mode, time_interval, plot_type)

                # np.savetxt("test.out", xydict)
                # coordinate to put the text
                x1, y1 = xydict.shape
                x1 = int(x1 / 2.8)
                y1 /= 8
                if mode == 'r':
                    self.setPlotParams('x', mode_string, xydict=xydict, label='start time (real)',
                                       text=(x1, y1, text))
                    self.setPlotParams('y', mode_string, xydict=xydict, label='end time (real)', fixed_range=(0, 1))
                else:
                    self.setPlotParams('x', mode_string, xydict=xydict, label='start time (virtual)',
                                       text=(x1, y1, text))
                    self.setPlotParams('y', mode_string, xydict=xydict, label='end time (virtual)',
                                       fixed_range=(0, 1))

                if not figname:
                    figname = '_'.join([algorithm, str(cache_size), plot_type]) + '.png'
                self.draw_heatmap(xydict, figname=figname)



            elif plot_type == "hit_ratio_start_time_cache_size":
                pass


            elif plot_type == "avg_rd_start_time_end_time":
                pass


            elif plot_type == "cold_miss_count_start_time_end_time":
                raise RuntimeError("this plot is deprecated")


            elif plot_type == "???":
                pass




            elif plot_type == "rd_distribution":
                if not figname:
                    figname = 'rd_distribution.png'

                xydict, log_base = mimircache.c_heatmap.heatmap_rd_distribution(reader.cReader, mode,
                                                                     time_interval=time_interval,
                                                                     num_of_pixels=num_of_pixels,
                                                                     num_of_threads=num_of_threads)

                if 'filter_rd' in kwargs:
                    # make reuse distance < filter_rd unvisible,
                    # this can be useful when the low-reuse-distance request dominates
                    # thus makes the heatmap hard to read
                    assert kwargs['filter_rd'] > 0, "filter_rd must be positive"
                    index_pos = int(np.log(kwargs['filter_rd'])/np.log(log_base))
                    xydict[:index_pos+1, :] = 0


                self.setPlotParams('x', mode_string, xydict=xydict)
                self.setPlotParams('y', 'reuse_dist', xydict=xydict, log_base=log_base)
                self.setPlotParams('cb', 'count') #, fixed_range=(0.01, 1))
                self.draw_heatmap(xydict, figname=figname, not_mask=True)

            elif plot_type == "rd_distribution_CDF":
                if not figname:
                    figname = 'rd_distribution_CDF.png'

                xydict, log_base = mimircache.c_heatmap.heatmap_rd_distribution(reader.cReader, mode,
                                                                     time_interval=time_interval,
                                                                     num_of_pixels=num_of_pixels,
                                                                     num_of_threads=num_of_threads, CDF=1)
                self.setPlotParams('x', mode_string, xydict=xydict)
                self.setPlotParams('y', 'reuse_dist', xydict=xydict, log_base=log_base)
                self.setPlotParams('cb', 'count') #, fixed_range=(0.01, 1))
                self.draw_heatmap(xydict, figname=figname, not_mask=True)


            elif plot_type == "future_rd_distribution":
                if not figname:
                    figname = 'future_rd_distribution.png'

                xydict, log_base = mimircache.c_heatmap.heatmap_future_rd_distribution(reader.cReader, mode,
                                                                            time_interval=time_interval,
                                                                            num_of_pixels=num_of_pixels,
                                                                            num_of_threads=num_of_threads)
                self.setPlotParams('x', mode_string, xydict=xydict)
                self.setPlotParams('y', 'reuse_dist', xydict=xydict, log_base=log_base)
                self.setPlotParams('cb', 'count') #, fixed_range=(0.01, 1))
                self.draw_heatmap(xydict, figname=figname, not_mask=True)

            elif plot_type == "dist_distribution":
                if not figname:
                    figname = 'dist_distribution.png'

                xydict, log_base = mimircache.c_heatmap.heatmap_dist_distribution(reader.cReader, mode,
                                                                     time_interval=time_interval,
                                                                     num_of_pixels=num_of_pixels,
                                                                     num_of_threads=num_of_threads)

                if 'filter_rd' in kwargs:
                    assert kwargs['filter_rd'] > 0, "filter_rd must be positive"
                    index_pos = int(np.log(kwargs['filter_rd'])/np.log(log_base))
                    xydict[:index_pos+1, :] = 0


                self.setPlotParams('x', mode_string, xydict=xydict)
                self.setPlotParams('y', 'distance', xydict=xydict, log_base=log_base)
                self.setPlotParams('cb', 'count') #, fixed_range=(0.01, 1))
                self.draw_heatmap(xydict, figname=figname, not_mask=True)

            elif plot_type == "reuse_time_distribution":
                if not figname:
                    figname = 'rt_distribution.png'

                xydict, log_base = mimircache.c_heatmap.heatmap_reuse_time_distribution(reader.cReader, mode,
                                                                     time_interval=time_interval,
                                                                     num_of_pixels=num_of_pixels,
                                                                     num_of_threads=num_of_threads)

                if 'filter_rd' in kwargs:
                    assert kwargs['filter_rd'] > 0, "filter_rd must be positive"
                    index_pos = int(np.log(kwargs['filter_rd'])/np.log(log_base))
                    xydict[:index_pos+1, :] = 0


                self.setPlotParams('x', mode_string, xydict=xydict)
                self.setPlotParams('y', 'distance', xydict=xydict, log_base=log_base)
                plt.ylabel("reuse time")
                self.setPlotParams('cb', 'count') #, fixed_range=(0.01, 1))
                self.draw_heatmap(xydict, figname=figname, not_mask=True)



            else:
                raise RuntimeError("Cannot recognize this plot type, "
                    "please check documentation, yoru input is {}".format(plot_type))

        else:
            raise RuntimeError("Cannot recognize this mode, "
                               "it can only be either real time(r) or virtual time(v), "
                               "but your input %s" % mode)

        reader.reset()

    def diffHeatmap(self, reader, mode, plot_type, algorithm1,
                    time_interval=-1, num_of_pixels=-1, algorithm2="Optimal",
                    cache_params1=None, cache_params2=None, **kwargs):
        """

        :param time_interval:
        :param num_of_pixels:
        :param algorithm2:
        :param cache_params1:
        :param cache_params2:
        :param algorithm1:
        :param plot_type:
        :param mode:
        :param reader:
        :param kwargs: include num_of_process, figname
        :return:
        """

        self.time_interval = time_interval
        self.num_of_pixels = num_of_pixels

        self.mode = mode
        reader.reset()

        if 'cache_size' in kwargs:
            cache_size = kwargs['cache_size']
        else:
            cache_size = -1

        figname = '_'.join([algorithm2 + '-' + algorithm1, str(cache_size), plot_type]) + '.png'

        if 'num_of_threads' in kwargs:
            num_of_threads = kwargs['num_of_threads']
        else:
            num_of_threads = 4

        if 'figname' in kwargs:
            figname = kwargs['figname']

        if mode == 'r' or mode == 'v':
            if mode == 'r':
                mode_string = "real time"
            else:
                mode_string = "virtual time"

            if plot_type == "hit_ratio_start_time_end_time":
                assert cache_size != -1, "please provide cache_size for plotting hit_ratio_start_time_end_time"

                xydict = mimircache.c_heatmap.diff_heatmap(reader.cReader, mode,
                                                           plot_type, cache_size,
                                                           algorithm1, algorithm2,
                                                           time_interval=time_interval,
                                                           num_of_pixels=num_of_pixels,
                                                           cache_params1=cache_params1,
                                                           cache_params2=cache_params2,
                                                           num_of_threads=num_of_threads)

                text = "      differential heatmap\n      cache size: {},\n      cache type: ({}-{})/{},\n" \
                       "      time type: {},\n      time interval: {},\n      plot type: \n{}".format(
                    cache_size, algorithm2, algorithm1, algorithm1, mode, time_interval, plot_type)

                x1, y1 = xydict.shape
                x1 = int(x1 / 2.8)
                y1 /= 8
                if mode == 'r':
                    self.setPlotParams('x', mode_string, xydict=xydict, label='start time (real)',
                                       text=(x1, y1, text))
                    self.setPlotParams('y', mode_string, xydict=xydict, label='end time (real)', fixed_range=(-1, 1))
                else:
                    self.setPlotParams('x', mode_string, xydict=xydict, label='start time (virtual)',
                                       text=(x1, y1, text))
                    self.setPlotParams('y', mode_string, xydict=xydict, label='end time (virtual)',
                                       fixed_range=(-1, 1))

                self.draw_heatmap(xydict, figname=figname)



            elif plot_type == "hit_ratio_start_time_cache_size":
                pass


            elif plot_type == "avg_rd_start_time_end_time":
                pass


            elif plot_type == "cold_miss_count_start_time_end_time":
                print("this plot is discontinued")


            elif plot_type == "???":
                pass



            else:
                raise RuntimeError(
                    "Cannot recognize this plot type, please check documentation, yoru input is %s" % mode)

        else:
            raise RuntimeError("Cannot recognize this mode, "
                               "it can only be either real time(r) or virtual time(v), "
                               "but you input %s" % mode)

        reader.reset()

    def draw_heatmap(self, xydict, **kwargs):
        if 'figname' in kwargs:
            filename = kwargs['figname']
        else:
            filename = 'heatmap.png'

        if 'not_mask' in kwargs and kwargs['not_mask']:
            plot_array = xydict
        else:
            plot_array = np.ma.array(xydict, mask=np.tri(len(xydict), dtype=int).T)

        if 'filter_count' in kwargs:
            assert kwargs['filter_count'] > 0, "filter_count must be positive"
            plot_array = np.ma.array(xydict, mask=(xydict<kwargs['filter_count']))

        cmap = plt.cm.jet
        # cmap = plt.get_cmap("Oranges")
        cmap.set_bad('w', 1.)

        plt.title(kwargs.get("title", "Heatmap"))

        try:
            if self.other_plot_kwargs.get('fixed_range', False):
                vmin, vmax = self.other_plot_kwargs['fixed_range']
                del self.other_plot_kwargs['fixed_range']
                img = plt.imshow(plot_array, vmin=vmin, vmax=vmax, interpolation='nearest', origin='lower',
                                 cmap=cmap, aspect='auto', **self.other_plot_kwargs)
            else:
                img = plt.imshow(plot_array, interpolation='nearest', origin='lower', aspect='auto',
                                 cmap=cmap, **self.other_plot_kwargs)

            cb = plt.colorbar(img)
            plt.tight_layout()

            plt.savefig(filename, dpi=600)
            plt.show()
            INFO("plot is saved as {}".format(filename))
            plt.clf()
            self.other_plot_kwargs.clear()
        except Exception as e:
            try:
                import time
                t = int(time.time())
                WARNING("plotting using imshow failed: {}, "
                        "now try to save the plotting data to /tmp/heatmap.{}.pickle".format(e, t))
                import pickle
                with open("/tmp/heatmap.{}.pickle", 'wb') as ofile:
                    pickle.dump(plot_array, ofile)
            except Exception as e:
                WARNING("failed to save plotting data")

            try:
                plt.pcolormesh(plot_array.T, cmap=cmap)
                plt.savefig(filename)
            except Exception as e:
                WARNING("further plotting using pcolormesh failed" + str(e))
