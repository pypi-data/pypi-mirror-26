#!/usr/bin/env python
"""
Scan Data File Viewer
"""
import os
import sys
import time
import numpy as np
np.seterr(all='ignore')

from functools import partial

import wx
import wx.lib.agw.flatnotebook as flat_nb
import wx.lib.scrolledpanel as scrolled
import wx.lib.mixins.inspection

from wx.richtext import RichTextCtrl

is_wxPhoenix = 'phoenix' in wx.PlatformInfo

from wxutils import (SimpleText, pack, Button, HLine, FileSave,
                     Choice,  Check, MenuItem, GUIColors, GridPanel,
                     CEN, RCEN, LCEN, FRAMESTYLE, Font)


from larch import Interpreter, Group
from larch.utils import index_of
from larch.utils.strutils import file2groupname

from larch.larchlib import read_workdir, save_workdir, read_config, save_config

from larch.wxlib import (LarchPanel, LarchFrame, ColumnDataFileFrame, ReportFrame,
                         BitmapButton, FileCheckList, FloatCtrl, SetTip)


from larch.fitting import fit_report

from larch_plugins.std import group2dict

from larch_plugins.wx.plotter import _newplot, _plot
from larch_plugins.wx.icons import get_icon
from larch_plugins.wx.athena_importer import AthenaImporter

from larch_plugins.wx.xyfit_fitpanel import XYFitPanel

from larch_plugins.io import (read_ascii, read_xdi, read_gsexdi,
                              gsescan_group,
                              fix_varname, is_athena_project)

from larch_plugins.xafs import pre_edge

LCEN = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
CEN |=  wx.ALL
FILE_WILDCARDS = "Data Files(*.0*,*.dat,*.xdi,*.prj)|*.0*;*.dat;*.xdi;*.prj|All files (*.*)|*.*"
FNB_STYLE = flat_nb.FNB_NO_X_BUTTON|flat_nb.FNB_NODRAG|flat_nb.FNB_NO_NAV_BUTTONS


PLOTOPTS_1 = dict(style='solid', linewidth=3, marker='None', markersize=4)
PLOTOPTS_2 = dict(style='short dashed', linewidth=2, zorder=-5,
                  marker='None', markersize=4)
PLOTOPTS_D = dict(style='solid', linewidth=2, zorder=-5,
                  side='right',  marker='None', markersize=4)

ICON_FILE = 'larch.ico'

SMOOTH_OPS = ('None', 'Boxcar', 'Savitzky-Golay', 'Convolution')
CONV_OPS  = ('Lorenztian', 'Gaussian')


def assign_gsescan_groups(group):
    labels = group.array_labels
    labels = []
    for i, name in enumerate(group.pos_desc):
        name = fix_varname(name.lower())
        labels.append(name)
        setattr(group, name, group.pos[i, :])

    for i, name in enumerate(group.sums_names):
        name = fix_varname(name.lower())
        labels.append(name)
        setattr(group, name, group.sums_corr[i, :])

    for i, name in enumerate(group.det_desc):
        name = fix_varname(name.lower())
        labels.append(name)
        setattr(group, name, group.det_corr[i, :])

    group.array_labels = labels


XASOPChoices=('Raw Data', 'Normalized', 'Derivative',
              'Normalized + Derivative',
              'Pre-edge subtracted',
              'Raw Data + Pre-edge/Post-edge')


class ProcessPanel(wx.Panel):
    def __init__(self, parent, controller=None, reporter=None, **kws):
        wx.Panel.__init__(self, parent, -1, **kws)

        self.controller = controller
        self.reporter = reporter
        self.needs_update = False
        self.proc_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onProcessTimer, self.proc_timer)
        self.proc_timer.Start(100)
        self.build_display()

    def edit_config(self, event=None):
        pass

    def fill(self, dgroup):
        opts = self.controller.get_proc_opts(dgroup)

        self.xshift.SetValue(opts['xshift'])
        self.yshift.SetValue(opts['yshift'])
        self.xscale.SetValue(opts['xscale'])
        self.yscale.SetValue(opts['yscale'])

        self.smooth_op.SetStringSelection(opts['smooth_op'])
        self.smooth_conv.SetStringSelection(opts['smooth_conv'])
        self.smooth_c0.SetValue(opts['smooth_c0'])
        self.smooth_c1.SetValue(opts['smooth_c1'])
        self.smooth_sig.SetValue(opts['smooth_sig'])

        if dgroup.datatype == 'xas':
            self.xas_op.SetStringSelection(opts['xas_op'])
            self.xas_e0.SetValue(opts['e0'])
            self.xas_step.SetValue(opts['edge_step'])
            self.xas_pre1.SetValue(opts['pre1'])
            self.xas_pre2.SetValue(opts['pre2'])
            self.xas_nor1.SetValue(opts['norm1'])
            self.xas_nor2.SetValue(opts['norm2'])
            self.xas_vict.SetSelection(opts['nvict'])
            self.xas_nnor.SetSelection(opts['nnorm'])
            self.xas_showe0.SetValue(opts['show_e0'])
            self.xas_autoe0.SetValue(opts['auto_e0'])
            self.xas_autostep.SetValue(opts['auto_step'])

    def build_display(self):
        self.SetFont(Font(10))
        titleopts = dict(font=Font(11), colour='#AA0000')

        gopts = dict(ncols=4, nrows=4, pad=2, itemstyle=LCEN)
        xas = self.xaspanel = GridPanel(self, **gopts)
        gen = self.genpanel = GridPanel(self, **gopts)
        self.btns = {}
        #gen
        opts  = dict(action=self.UpdatePlot, size=(65, -1), gformat=True)

        self.xshift = FloatCtrl(gen, value=0.0, **opts)
        self.xscale = FloatCtrl(gen, value=1.0, **opts)

        self.yshift = FloatCtrl(gen, value=0.0, **opts)
        self.yscale = FloatCtrl(gen, value=1.0, **opts)

        self.btns['xshift'] = BitmapButton(gen, get_icon('plus'),
                                           action=partial(self.on_selpoint, opt='xshift'),
                                           tooltip='use last point selected from plot')
        self.btns['yshift'] = BitmapButton(gen, get_icon('plus'),
                                           action=partial(self.on_selpoint, opt='yshift'),
                                           tooltip='use last point selected from plot')

        opts  = dict(action=self.onSmoothChoice, size=(30, -1))
        sm_row1 = wx.Panel(gen)
        sm_row2 = wx.Panel(gen)
        sm_siz1= wx.BoxSizer(wx.HORIZONTAL)
        sm_siz2= wx.BoxSizer(wx.HORIZONTAL)

        self.smooth_c0 = FloatCtrl(sm_row1, value=2, precision=0, minval=1, **opts)
        self.smooth_c1 = FloatCtrl(sm_row1, value=1, precision=0, minval=1, **opts)
        self.smooth_msg = SimpleText(sm_row1, label='         ', size=(205, -1))
        opts['size'] =  (65, -1)
        self.smooth_sig = FloatCtrl(sm_row2, value=1, gformat=True, **opts)

        opts['size'] =  (120, -1)
        self.smooth_op = Choice(sm_row1, choices=SMOOTH_OPS, **opts)
        self.smooth_op.SetSelection(0)

        self.smooth_conv = Choice(sm_row2, choices=CONV_OPS, **opts)

        self.smooth_c0.Disable()
        self.smooth_c1.Disable()
        self.smooth_sig.Disable()
        self.smooth_conv.SetSelection(0)
        self.smooth_conv.Disable()

        sm_siz1.Add(self.smooth_op,  0, LCEN, 1)
        sm_siz1.Add(SimpleText(sm_row1, ' n= '), 0, LCEN, 1)
        sm_siz1.Add(self.smooth_c0,  0, LCEN, 1)
        sm_siz1.Add(SimpleText(sm_row1, ' order= '), 0, LCEN, 1)
        sm_siz1.Add(self.smooth_c1,  0, LCEN, 1)
        sm_siz1.Add(self.smooth_msg, 0, LCEN, 1)

        sm_siz2.Add(SimpleText(sm_row2, ' form= '), 0, LCEN, 1)
        sm_siz2.Add(self.smooth_conv,  0, LCEN, 1)
        sm_siz2.Add(SimpleText(sm_row2, ' sigma= '), 0, LCEN, 1)
        sm_siz2.Add(self.smooth_sig,  0, LCEN, 1)
        pack(sm_row1, sm_siz1)
        pack(sm_row2, sm_siz2)

        gen.Add(SimpleText(gen, ' General Data Processing', **titleopts), dcol=8)
        gen.Add(SimpleText(gen, ' X shift:'),  newrow=True)
        gen.Add(self.btns['xshift'])
        gen.Add(self.xshift, dcol=2)
        gen.Add(SimpleText(gen, ' X scale:'))
        gen.Add(self.xscale, dcol=2)

        gen.Add(SimpleText(gen, ' Y shift:'),  newrow=True)
        gen.Add(self.btns['yshift'])
        gen.Add(self.yshift, dcol=2)
        gen.Add(SimpleText(gen, ' Y scale:'))
        gen.Add(self.yscale, dcol=2)

        gen.Add(SimpleText(gen, ' Smoothing:'), newrow=True)
        gen.Add(sm_row1, dcol=8)
        gen.Add(sm_row2, icol=1, dcol=7, newrow=True)

        gen.pack()

        #xas
        opts = {'action': self.UpdatePlot}
        e0opts_panel = wx.Panel(xas)
        self.xas_autoe0   = Check(e0opts_panel, default=True, label='auto?', **opts)
        self.xas_showe0   = Check(e0opts_panel, default=True, label='show?', **opts)
        sx = wx.BoxSizer(wx.HORIZONTAL)
        sx.Add(self.xas_autoe0, 0, LCEN, 4)
        sx.Add(self.xas_showe0, 0, LCEN, 4)
        pack(e0opts_panel, sx)

        self.xas_autostep = Check(xas, default=True, label='auto?', **opts)
        opts['size'] = (250, -1)
        self.xas_op  = Choice(xas, choices=XASOPChoices,  **opts)

        self.xas_op.SetStringSelection('Normalized')

        for name in ('e0', 'pre1', 'pre2', 'nor1', 'nor2'):
            bb = BitmapButton(xas, get_icon('plus'),
                              action=partial(self.on_selpoint, opt=name),
                              tooltip='use last point selected from plot')
            self.btns[name] = bb

        opts = {'size': (65, -1), 'gformat': True}

        self.xas_e0   = FloatCtrl(xas, value=0, action=self.onSet_XASE0, **opts)
        self.xas_step = FloatCtrl(xas, value=0, action=self.onSet_XASStep, **opts)

        opts['precision'] = 1
        opts['action'] =  self.UpdatePlot
        self.xas_pre1 = FloatCtrl(xas, value=-200, **opts)
        self.xas_pre2 = FloatCtrl(xas, value= -30, **opts)
        self.xas_nor1 = FloatCtrl(xas, value=  50, **opts)
        self.xas_nor2 = FloatCtrl(xas, value= -50, **opts)

        opts = {'size': (50, -1),
                'choices': ('0', '1', '2', '3'),
                'action': self.UpdatePlot}
        self.xas_vict = Choice(xas, **opts)
        self.xas_nnor = Choice(xas, **opts)
        self.xas_vict.SetSelection(1)
        self.xas_nnor.SetSelection(1)

        def CopyBtn(name):
            return Button(xas, 'Copy', size=(50, 30),
                          action=partial(self.onCopyParam, name))


        xas.Add(SimpleText(xas, ' XAS Data Processing', **titleopts), dcol=6)
        xas.Add(SimpleText(xas, ' Copy to Selected Groups?'), style=RCEN, dcol=3)
        xas.Add(SimpleText(xas, 'Arrays to Plot: '),  newrow=True)
        xas.Add(self.xas_op,  dcol=6)
        xas.Add((10, 10))
        xas.Add(CopyBtn('xas_op'), style=RCEN)

        xas.Add(SimpleText(xas, 'E0 : '), newrow=True)
        xas.Add(self.btns['e0'])
        xas.Add(self.xas_e0)
        xas.Add(e0opts_panel, dcol=4)
        xas.Add((10, 1))
        xas.Add(CopyBtn('xas_e0'), style=RCEN)

        xas.Add(SimpleText(xas, 'Edge Step: '), newrow=True)
        xas.Add((10, 1))
        xas.Add(self.xas_step)
        xas.Add(self.xas_autostep, dcol=3)
        xas.Add((10, 1))
        xas.Add((10, 1))
        xas.Add(CopyBtn('xas_step'), style=RCEN)

        xas.Add(SimpleText(xas, 'Pre-edge range: '), newrow=True)
        xas.Add(self.btns['pre1'])
        xas.Add(self.xas_pre1)
        xas.Add(SimpleText(xas, ':'))
        xas.Add(self.btns['pre2'])
        xas.Add(self.xas_pre2)
        xas.Add(SimpleText(xas, 'Victoreen:'))
        xas.Add(self.xas_vict)
        xas.Add(CopyBtn('xas_pre'), style=RCEN)

        xas.Add(SimpleText(xas, 'Normalization range: '), newrow=True)
        xas.Add(self.btns['nor1'])
        xas.Add(self.xas_nor1)
        xas.Add(SimpleText(xas, ':'))
        xas.Add(self.btns['nor2'])
        xas.Add(self.xas_nor2)
        xas.Add(SimpleText(xas, 'PolyOrder:'))
        xas.Add(self.xas_nnor)
        xas.Add(CopyBtn('xas_norm'), style=RCEN)

        xas.pack()

        saveconf = Button(self, 'Save as Default Settings',
                          size=(175, 30),
                          action=self.onSaveConfigBtn)

        hxline = HLine(self, size=(550, 2))

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.AddMany([((10, 10), 0, LCEN, 10), (gen,      0, LCEN, 10),
                       ((10, 10), 0, LCEN, 10), (hxline,   0, LCEN, 10),
                       ((10, 10), 0, LCEN, 10), (xas,      0, LCEN, 10),
                       ((10, 10), 0, LCEN, 10), (saveconf, 0, LCEN, 10),
                       ])

        xas.Disable()

        pack(self, sizer)

    def onSaveConfigBtn(self, evt=None):
        conf = self.controller.larch.symtable._sys.xyfit

        data_proc = {}
        data_proc.update(getattr(conf, 'data_proc', {}))

        data_proc['xshift'] = self.xshift.GetValue()
        data_proc['yshift'] = self.yshift.GetValue()
        data_proc['xscale'] = self.xscale.GetValue()
        data_proc['yscale'] = self.yscale.GetValue()
        data_proc['smooth_op'] = str(self.smooth_op.GetStringSelection())
        data_proc['smooth_c0'] = int(self.smooth_c0.GetValue())
        data_proc['smooth_c1'] = int(self.smooth_c1.GetValue())
        data_proc['smooth_sig'] = float(self.smooth_sig.GetValue())
        data_proc['smooth_conv'] = str(self.smooth_conv.GetStringSelection())

        conf.data_proc = data_proc

        if self.xaspanel.Enabled:
            xas_proc = {}
            xas_proc.update(getattr(conf, 'xas_proc', {}))

            xas_proc['auto_e0'] = True
            xas_proc['auto_step'] = True

            xas_proc['pre1']  = self.xas_pre1.GetValue()
            xas_proc['pre2']  = self.xas_pre2.GetValue()
            xas_proc['norm1'] = self.xas_nor1.GetValue()
            xas_proc['norm2'] = self.xas_nor2.GetValue()
            xas_proc['nvict'] = self.xas_vict.GetSelection()
            xas_proc['nnorm'] = self.xas_nnor.GetSelection()

            xas_proc['show_e0'] = self.xas_showe0.IsChecked()
            xas_proc['nnorm'] = int(self.xas_nnor.GetSelection())
            xas_proc['nvict'] = int(self.xas_vict.GetSelection())
            xas_proc['xas_op'] = str(self.xas_op.GetStringSelection())
            conf.xas_proc = xas_proc

    def onCopyParam(self, name=None, event=None):
        proc_opts = self.controller.group.proc_opts
        opts = {}
        name = str(name)
        if name == 'xas_op':
            opts['xas_op'] = proc_opts['xas_op']
        elif name == 'xas_e0':
            opts['e0'] = proc_opts['e0']
            opts['show_e0'] = proc_opts['show_e0']
            opts['auto_e0'] = False
        elif name == 'xas_step':
            opts['edge_step'] = proc_opts['edge_step']
            opts['auto_step'] = False
        elif name == 'xas_pre':
            opts['nvict'] = proc_opts['nvict']
            opts['pre1'] = proc_opts['pre1']
            opts['pre2'] = proc_opts['pre2']
        elif name == 'xas_norm':
            opts['nnorm'] = proc_opts['nnorm']
            opts['norm1'] = proc_opts['norm1']
            opts['norm2'] = proc_opts['norm2']

        for checked in self.controller.filelist.GetCheckedStrings():
            groupname = self.controller.file_groups[str(checked)]
            grp = self.controller.get_group(groupname)
            if grp != self.controller.group:
                grp.proc_opts.update(opts)
                self.fill(grp)
                self.process(grp.groupname)

    def onSmoothChoice(self, evt=None, value=1):
        try:
            choice = self.smooth_op.GetStringSelection().lower()
            conv  = self.smooth_conv.GetStringSelection()
            self.smooth_c0.Disable()
            self.smooth_c1.Disable()
            self.smooth_conv.Disable()
            self.smooth_sig.Disable()
            self.smooth_msg.SetLabel('')
            self.smooth_c0.SetMin(1)
            self.smooth_c0.odd_only = False
            if choice.startswith('box'):
                self.smooth_c0.Enable()
            elif choice.startswith('savi'):
                self.smooth_c0.Enable()
                self.smooth_c1.Enable()
                self.smooth_c0.Enable()
                self.smooth_c0.odd_only = True

                c0 = int(self.smooth_c0.GetValue())
                c1 = int(self.smooth_c1.GetValue())
                x0 = max(c1+1, c0)
                if x0 % 2 == 0:
                    x0 += 1
                self.smooth_c0.SetMin(c1+1)
                if c0 != x0:
                    self.smooth_c0.SetValue(x0)
                self.smooth_msg.SetLabel('n must odd and  > order+1')

            elif choice.startswith('conv'):
                self.smooth_conv.Enable()
                self.smooth_sig.Enable()
            self.needs_update = True
        except AttributeError:
            pass

    def onSet_XASE0(self, evt=None, **kws):
        self.xas_autoe0.SetValue(0)
        self.needs_update = True

    def onSet_XASStep(self, evt=None, **kws):
        self.xas_autostep.SetValue(0)
        self.needs_update = True

    def onProcessTimer(self, evt=None):
        if self.needs_update and self.controller.groupname is not None:
            self.process(self.controller.groupname)
            self.controller.plot_group(groupname=self.controller.groupname, new=True)
            self.needs_update = False

    def UpdatePlot(self, evt=None, **kws):
        self.needs_update = True

    def on_selpoint(self, evt=None, opt='e0'):
        xval, yval = self.controller.get_cursor()
        if xval is None:
            return

        e0 = self.xas_e0.GetValue()
        if opt == 'e0':
            self.xas_e0.SetValue(xval)
            self.xas_autoe0.SetValue(0)
        elif opt == 'pre1':
            self.xas_pre1.SetValue(xval-e0)
        elif opt == 'pre2':
            self.xas_pre2.SetValue(xval-e0)
        elif opt == 'nor1':
            self.xas_nor1.SetValue(xval-e0)
        elif opt == 'nor2':
            self.xas_nor2.SetValue(xval-e0)
        elif opt == 'xshift':
            self.xshift.SetValue(xval)
        elif opt == 'yshift':
            self.yshift.SetValue(yval)

    def process(self, gname,  **kws):
        """ handle process (pre-edge/normalize) XAS data from XAS form, overwriting
        larch group 'x' and 'y' attributes to be plotted
        """
        dgroup = self.controller.get_group(gname)
        proc_opts = {}

        proc_opts['xshift'] = self.xshift.GetValue()
        proc_opts['yshift'] = self.yshift.GetValue()
        proc_opts['xscale'] = self.xscale.GetValue()
        proc_opts['yscale'] = self.yscale.GetValue()
        proc_opts['smooth_op'] = self.smooth_op.GetStringSelection()
        proc_opts['smooth_c0'] = int(self.smooth_c0.GetValue())
        proc_opts['smooth_c1'] = int(self.smooth_c1.GetValue())
        proc_opts['smooth_sig'] = float(self.smooth_sig.GetValue())
        proc_opts['smooth_conv'] = self.smooth_conv.GetStringSelection()

        self.xaspanel.Enable(dgroup.datatype.startswith('xas'))
        if dgroup.datatype.startswith('xas'):
            proc_opts['datatype'] = 'xas'
            proc_opts['e0'] = self.xas_e0.GetValue()
            proc_opts['edge_step'] = self.xas_step.GetValue()
            proc_opts['pre1']  = self.xas_pre1.GetValue()
            proc_opts['pre2']  = self.xas_pre2.GetValue()
            proc_opts['norm1'] = self.xas_nor1.GetValue()
            proc_opts['norm2'] = self.xas_nor2.GetValue()
            proc_opts['nvict'] = self.xas_vict.GetSelection()
            proc_opts['nnorm'] = self.xas_nnor.GetSelection()

            proc_opts['auto_e0'] = self.xas_autoe0.IsChecked()
            proc_opts['show_e0'] = self.xas_showe0.IsChecked()
            proc_opts['auto_step'] = self.xas_autostep.IsChecked()
            proc_opts['nnorm'] = int(self.xas_nnor.GetSelection())
            proc_opts['nvict'] = int(self.xas_vict.GetSelection())
            proc_opts['xas_op'] = self.xas_op.GetStringSelection()

        self.controller.process(dgroup, proc_opts=proc_opts)

        if dgroup.datatype.startswith('xas'):

            if self.xas_autoe0.IsChecked():
                self.xas_e0.SetValue(dgroup.proc_opts['e0'], act=False)
            if self.xas_autostep.IsChecked():
                self.xas_step.SetValue(dgroup.proc_opts['edge_step'], act=False)

            self.xas_pre1.SetValue(dgroup.proc_opts['pre1'])
            self.xas_pre2.SetValue(dgroup.proc_opts['pre2'])
            self.xas_nor1.SetValue(dgroup.proc_opts['norm1'])
            self.xas_nor2.SetValue(dgroup.proc_opts['norm2'])

            dgroup.orig_ylabel = dgroup.plot_ylabel
            dgroup.plot_ylabel = '$\mu$'
            dgroup.plot_y2label = None
            dgroup.plot_xlabel = '$E \,\mathrm{(eV)}$'
            dgroup.plot_yarrays = [(dgroup.mu, PLOTOPTS_1, dgroup.plot_ylabel)]
            y4e0 = dgroup.mu

            out = self.xas_op.GetStringSelection().lower() # raw, pre, norm, flat
            if out.startswith('raw data + pre'):
                dgroup.plot_yarrays = [(dgroup.mu,        PLOTOPTS_1, '$\mu$'),
                                       (dgroup.pre_edge,  PLOTOPTS_2, 'pre edge'),
                                       (dgroup.post_edge, PLOTOPTS_2, 'post edge')]
            elif out.startswith('pre'):
                dgroup.pre_edge_sub = dgroup.norm * dgroup.edge_step
                dgroup.plot_yarrays = [(dgroup.pre_edge_sub, PLOTOPTS_1,
                                        'pre-edge subtracted $\mu$')]
                y4e0 = dgroup.pre_edge_sub
                dgroup.plot_ylabel = 'pre-edge subtracted $\mu$'
            elif 'norm' in out and 'deriv' in out:
                dgroup.plot_yarrays = [(dgroup.norm, PLOTOPTS_1, 'normalized $\mu$'),
                                       (dgroup.dmude, PLOTOPTS_D, '$d\mu/dE$')]
                y4e0 = dgroup.norm
                dgroup.plot_ylabel = 'normalized $\mu$'
                dgroup.plot_y2label = '$d\mu/dE$'
                dgroup.y = dgroup.norm

            elif out.startswith('norm'):
                dgroup.plot_yarrays = [(dgroup.norm, PLOTOPTS_1, 'normalized $\mu$')]
                y4e0 = dgroup.norm
                dgroup.plot_ylabel = 'normalized $\mu$'
                dgroup.y = dgroup.norm

            elif out.startswith('deriv'):
                dgroup.plot_yarrays = [(dgroup.dmude, PLOTOPTS_1, '$d\mu/dE$')]
                y4e0 = dgroup.dmude
                dgroup.plot_ylabel = '$d\mu/dE$'
                dgroup.y = dgroup.dmude

            dgroup.plot_ymarkers = []
            if self.xas_showe0.IsChecked():
                ie0 = index_of(dgroup.xdat, dgroup.e0)
                dgroup.plot_ymarkers = [(dgroup.e0, y4e0[ie0], {'label': '_nolegend_'})]

class XYFitController():
    """
    class hollding the Larch session and doing the
    processing work for Larch XYFit
    """
    config_file = 'xyfit.conf'
    def __init__(self, wxparent=None, _larch=None):
        self.wxparent = wxparent
        self.larch = _larch
        if self.larch is None:
            self.larch = Interpreter()

        self.filelist = None
        self.file_groups = {}
        self.proc_opts = {}
        self.fit_opts = {}
        self.group = None

        self.groupname = None
        self.report_frame = None
        self.symtable = self.larch.symtable
        self.symtable.set_symbol('_sys.wx.wxapp', wx.GetApp())
        self.symtable.set_symbol('_sys.wx.parent', self)

    def init_larch(self):
        fico = self.get_iconfile()

        _larch = self.larch
        _larch.eval("import xafs_plots")
        _larch.symtable._sys.xyfit = Group()
        config = read_config(self.config_file)
        if (config is None or 'workdir' not in config or
            'data_proc' not in config or 'xas_proc' not in config):
            config = self.make_default_config()

        for key, value in config.items():
            setattr(_larch.symtable._sys.xyfit, key, value)
        os.chdir(config['workdir'])

    def make_default_config(self):
        """ default config, probably called on first run of program"""
        config = {'chdir_on_fileopen': True,
                  'workdir': os.getcwd()}
        config['data_proc'] = dict(xshift=0, xscale=1, yshift=0,
                                   yscale=1, smooth_op='None',
                                   smooth_conv='Lorentzian',
                                   smooth_c0=2, smooth_c1=1,
                                   smooth_sig=1)
        config['xas_proc'] = dict(e0=0, pre1=-200, pre2=-10,
                                  edge_step=0, nnorm=2, norm1=25,
                                  norm2=-10, nvict=1, auto_step=True,
                                  auto_e0=True, show_e0=True,
                                  xas_op='Normalized')
        return config

    def get_config(self, key, default=None):
        "get configuration setting"
        confgroup = self.larch.symtable._sys.xyfit
        return getattr(confgroup, key, default)


    def save_config(self):
        """save configuration"""
        conf = group2dict(self.larch.symtable._sys.xyfit)
        conf.pop('__name__')
        save_config(self.config_file, conf)

    def set_workdir(self):
        self.larch.symtable._sys.xyfit.workdir = os.getcwd()

    def show_report(self, text, evt=None):
        shown = False
        try:
            self.report_frame.Raise()
            shown = True
        except:
            del self.report_frame
        if not shown:
            self.report_frame = ReportFrame(self.wxparent)

        self.report_frame.SetFont(Font(8))
        self.report_frame.set_text(text)
        self.report_frame.SetFont(Font(8))
        self.report_frame.Raise()

    def get_iconfile(self):
        larchdir = self.symtable._sys.config.larchdir
        return os.path.join(larchdir, 'icons', ICON_FILE)

    def get_display(self, stacked=False):
        win = 1
        wintitle='Larch XYFit Array Plot Window'
        if stacked:
            win = 2
            wintitle='Larch XYFit Fit Plot Window'
        opts = dict(wintitle=wintitle, stacked=stacked, win=win)
        out = self.symtable._plotter.get_display(**opts)
        return out

    def get_group(self, groupname):
        if groupname is None:
            groupname = self.groupname
        grp = getattr(self.symtable, groupname, None)
        if not hasattr(grp, 'proc_opts'):
            grp.proc_opts = {}
        return grp

    def get_proc_opts(self, dgroup):
        opts = {}
        opts.update(self.get_config('data_proc', default={}))
        if dgroup.datatype == 'xas':
            opts.update(self.get_config('xas_proc', {}))

        if hasattr(dgroup, 'proc_opts'):
            opts.update(dgroup.proc_opts)
        return opts

    def process(self, dgroup, proc_opts=None):
        if not hasattr(dgroup, 'proc_opts'):
            dgroup.proc_opts = {}

        if 'xscale' not in dgroup.proc_opts:
            dgroup.proc_opts.update(self.get_proc_opts(dgroup))

        if proc_opts is not None:
            dgroup.proc_opts.update(proc_opts)

        opts = {'group': dgroup.groupname}
        opts.update(dgroup.proc_opts)

        # scaling
        cmds = []
        cmds.append("{group:s}.x = {xscale:f}*({group:s}.xdat + {xshift:f})")
        cmds.append("{group:s}.y = {yscale:f}*({group:s}.ydat + {yshift:f})")

        # smoothing
        smop = opts['smooth_op'].lower()
        smcmd = None
        if smop.startswith('box'):
            opts['smooth_c0'] = int(opts['smooth_c0'])
            smcmd = "boxcar({group:s}.y, {smooth_c0:d})"
        elif smop.startswith('savit'):
            opts['smooth_c0'] = int(opts['smooth_c0'])
            opts['smooth_c1'] = int(opts['smooth_c1'])
            smcmd = "savitzky_golay({group:s}.y, {smooth_c0:d}, {smooth_c1:d})"
        elif smop.startswith('conv'):
            cform = str(opts['smooth_conv'].lower())
            smcmd = "smooth({group:s}.x, {group:s}.y, sigma={smooth_sig:f}, form='{smooth_conv:s}')"

        if smcmd is not None:
            cmds.append("{group:s}.y = " + smcmd)

        for cmd in cmds:
            self.larch.eval(cmd.format(**opts))


        # xas
        if dgroup.datatype.startswith('xas'):

            dgroup.energy = dgroup.x*1.0
            dgroup.mu = dgroup.y*1.0

            copts = [dgroup.groupname]
            if not opts['auto_e0']:
                _e0 = opts['e0']
                if _e0 < max(dgroup.energy) and _e0 > min(dgroup.energy):
                    copts.append("e0=%.4f" % float(_e0))

            if not opts['auto_step']:
                copts.append("step=%.4f" % opts['edge_step'])

            for attr in ('pre1', 'pre2', 'nvict', 'nnorm', 'norm1', 'norm2'):
                copts.append("%s=%.4f" % (attr, opts[attr]))

            self.larch.eval("pre_edge(%s)" % (','.join(copts)))

            opts['e0'] = dgroup.e0
            opts['edge_step'] = dgroup.edge_step
            for attr in  ('pre1', 'pre2', 'norm1', 'norm2'):
                opts[attr] = getattr(dgroup.pre_edge_details, attr)
            dgroup.proc_opts.update(opts)


    def get_cursor(self):
        try:
            xval = self.symtable._plotter.plot1_x
            yval = self.symtable._plotter.plot1_y
        except:
            xval, yval = None, None
        return xval, yval

    def plot_group(self, groupname=None, title=None, new=True, **kws):
        ppanel = self.get_display(stacked=False).panel
        newplot = ppanel.plot
        oplot   = ppanel.oplot
        plotcmd = oplot
        if new:
            plotcmd = newplot

        dgroup = self.get_group(groupname)
        if not hasattr(dgroup, 'xdat'):
            print("Cannot plot group ", groupname)

        if dgroup.datatype == 'xas':
            if ((getattr(dgroup, 'plot_yarrays', None) is None or
                 getattr(dgroup, 'energy', None) is None or
                 getattr(dgroup, 'mu', None) is None)):
                # print("-> Mode.process")
                self.process(dgroup)

        if not hasattr(dgroup, 'x'):
            dgroup.x = dgroup.xdat[:]
        if not hasattr(dgroup, 'y'):
            dgroup.y = dgroup.ydat[:]

        if hasattr(dgroup, 'plot_yarrays'):
            plot_yarrays = dgroup.plot_yarrays
        else:
            plot_yarrays = [(dgroup.y, {}, None)]

        popts = kws
        path, fname = os.path.split(dgroup.filename)
        if not 'label' in popts:
            popts['label'] = dgroup.plot_ylabel

        popts['xlabel'] = dgroup.plot_xlabel
        popts['ylabel'] = dgroup.plot_ylabel
        if getattr(dgroup, 'plot_y2label', None) is not None:
            popts['y2label'] = dgroup.plot_y2label

        plot_ymarkers = None
        if new:
            if title is None:
                title = fname
            plot_ymarkers = getattr(dgroup, 'plot_ymarkers', None)

        popts['title'] = title
        for yarr in plot_yarrays:
            popts.update(yarr[1])
            if popts['label'] is None and yarr[2] is not None:
                popts['label'] = yarr[2]
            plotcmd(dgroup.x, yarr[0], **popts)
            plotcmd = oplot

        if plot_ymarkers is not None:
            axes = ppanel.axes
            for x, y, opts in plot_ymarkers:
                popts = {'marker': 'o', 'markersize': 4,
                         'markerfacecolor': 'red', 'label': '',
                         'markeredgecolor': 'black'}
                popts.update(opts)
                axes.plot([x], [y], **popts)

        ppanel.canvas.draw()


class XYFitFrame(wx.Frame):
    _about = """Larch XYFit: XY Data Viewing & Curve Fitting

    Matt Newville <newville @ cars.uchicago.edu>
    """
    def __init__(self, parent=None, size=(875, 550), _larch=None, **kws):
        wx.Frame.__init__(self, parent, -1, size=size, style=FRAMESTYLE)

        self.last_array_sel = {}
        self.paths2read = []

        title = "Larch XYFit: XY Data Viewing & Curve Fitting"

        self.larch_buffer = parent
        if not isinstance(parent, LarchFrame):
            self.larch_buffer = LarchFrame(_larch=_larch)


        self.larch_buffer.Show()
        self.larch_buffer.Raise()
        self.larch=self.larch_buffer.larchshell
        self.controller = XYFitController(wxparent=self, _larch=self.larch)

        self.subframes = {}
        self.plotframe = None
        self.SetTitle(title)
        self.SetSize(size)
        self.SetFont(Font(10))

        self.larch_buffer.Hide()

        self.createMainPanel()
        self.createMenus()
        self.statusbar = self.CreateStatusBar(2, 0)
        self.statusbar.SetStatusWidths([-3, -1])
        statusbar_fields = ["Initializing....", " "]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)

    def createMainPanel(self):
        splitter  = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(250)

        leftpanel = wx.Panel(splitter)
        ltop = wx.Panel(leftpanel)

        def Btn(msg, x, act):
            b = Button(ltop, msg, size=(x, 30),  action=act)
            b.SetFont(Font(10))
            return b

        plot_one = Btn('Plot One',      120, self.onPlotOne)
        plot_sel = Btn('Plot Selected', 120, self.onPlotSel)
        sel_none = Btn('Select None',   120, self.onSelNone)
        sel_all  = Btn('Select All',    120, self.onSelAll)

        self.controller.filelist = FileCheckList(leftpanel, main=self,
                                                 select_action=self.ShowFile,
                                                 remove_action=self.RemoveFile)
        self.controller.filelist.SetBackgroundColour(wx.Colour(255, 255, 255))

        tsizer = wx.GridBagSizer(1, 1)
        tsizer.Add(plot_one, (0, 0), (1, 1), LCEN, 2)
        tsizer.Add(plot_sel, (0, 1), (1, 1), LCEN, 2)
        tsizer.Add(sel_all,  (1, 0), (1, 1), LCEN, 2)
        tsizer.Add(sel_none, (1, 1), (1, 1), LCEN, 2)

        pack(ltop, tsizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(ltop, 0, LCEN|wx.GROW, 1)
        sizer.Add(self.controller.filelist, 1, LCEN|wx.GROW|wx.ALL, 1)

        pack(leftpanel, sizer)

        # right hand side
        panel = wx.Panel(splitter)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.title = SimpleText(panel, 'initializing...', size=(300, -1))
        self.title.SetFont(Font(10))

        ir = 0
        sizer.Add(self.title, 0, LCEN|wx.GROW|wx.ALL, 1)

        self.nb = flat_nb.FlatNotebook(panel, -1, agwStyle=FNB_STYLE)

        self.nb.SetTabAreaColour(wx.Colour(250,250,250))
        self.nb.SetActiveTabColour(wx.Colour(254,254,195))

        self.nb.SetNonActiveTabTextColour(wx.Colour(10,10,128))
        self.nb.SetActiveTabTextColour(wx.Colour(128,0,0))

        panel_opts = dict(parent=self.nb, controller=self.controller)

        self.proc_panel = ProcessPanel(**panel_opts)
        self.fit_panel =  XYFitPanel(**panel_opts)

        self.nb.AddPage(self.proc_panel,  ' Data Processing ',   True)
        self.nb.AddPage(self.fit_panel,   ' Curve Fitting ',  True)

        sizer.Add(self.nb, 1, LCEN|wx.EXPAND, 2)
        self.nb.SetSelection(0)

        pack(panel, sizer)

        splitter.SplitVertically(leftpanel, panel, 1)
        wx.CallAfter(self.init_larch)

    def onSelAll(self, event=None):
        self.controller.filelist.SetCheckedStrings(self.controller.file_groups.keys())

    def onSelNone(self, event=None):
        self.controller.filelist.SetCheckedStrings([])

    def init_larch(self):
        self.SetStatusText('initializing Larch')
        self.title.SetLabel('')

        self.fit_panel.larch = self.controller.larch

        self.controller.init_larch()

        plotframe = self.controller.get_display(stacked=False)
        xpos, ypos = self.GetPosition()
        xsiz, ysiz = self.GetSize()
        plotframe.SetPosition((xpos+xsiz, ypos))

        self.SetStatusText('ready')
        self.Raise()


    def write_message(self, s, panel=0):
        """write a message to the Status Bar"""
        self.SetStatusText(s, panel)

    def onPlotOne(self, evt=None, groupname=None):
        if groupname is None:
            groupname = self.controller.groupname

        dgroup = self.controller.get_group(groupname)
        if dgroup is not None:
            self.controller.plot_group(groupname=groupname, new=True)

    def onPlotSel(self, evt=None):
        newplot = True
        group_ids = self.controller.filelist.GetCheckedStrings()
        for checked in group_ids:
            groupname = self.controller.file_groups[str(checked)]
            dgroup = self.controller.get_group(groupname)
            if dgroup is not None:
                self.controller.plot_group(groupname=groupname, title='',
                                           new=newplot, label=dgroup.filename)
                newplot=False

    def plot_group(self, groupname=None, title=None, new=True, **kws):
        self.controller.plot_group(groupname=groupname, title=title, new=new, **kws)
        self.Raise()

    def RemoveFile(self, fname=None, **kws):
        if fname is not None:
            s = str(fname)
            if s in self.controller.file_groups:
                group = self.controller.file_groups.pop(s)

    def ShowFile(self, evt=None, groupname=None, **kws):
        filename = None
        if evt is not None:
            filename = str(evt.GetString())
        if groupname is None and filename is not None:
            groupname = self.controller.file_groups[filename]

        if not hasattr(self.larch.symtable, groupname):
            return

        dgroup = self.controller.get_group(groupname)
        self.controller.group = dgroup
        self.controller.groupname = groupname
        self.nb.SetSelection(0)
        self.proc_panel.fill(dgroup)
        if filename is None:
            filename = dgroup.filename
        self.title.SetLabel(filename)

    def createMenus(self):
        # ppnl = self.plotpanel
        self.menubar = wx.MenuBar()
        #
        fmenu = wx.Menu()
        MenuItem(self, fmenu, "&Open Data File\tCtrl+O",
                 "Open Data File",  self.onReadDialog)

        fmenu.AppendSeparator()
        MenuItem(self, fmenu, 'Show Larch Buffer\tCtrl+L',
                 'Show Larch Programming Buffer',
                 self.onShowLarchBuffer)

        MenuItem(self, fmenu, "debug wx\tCtrl+I", "", self.showInspectionTool)
        MenuItem(self, fmenu, "&Quit\tCtrl+Q", "Quit program", self.onCloseNicely)

        self.menubar.Append(fmenu, "&File")

        omenu = wx.Menu()
        self.menubar.Append(omenu, "Options")
        MenuItem(self, omenu, "Configure Data Processing",
                  "Configure Data Processing", self.onConfigDataProcessing)

        MenuItem(self, omenu, "Configure Data Fitting",
                  "Configure Data Fitting", self.onConfigDataFitting)

        self.SetMenuBar(self.menubar)
        self.Bind(wx.EVT_CLOSE,  self.onExit)

    def onShowLarchBuffer(self, evt=None):
        if self.larch_buffer is None:
            self.larch_buffer = LarchFrame(_larch=self.larch)
        self.larch_buffer.Show()
        self.larch_buffer.Raise()


    def onConfigDataProcessing(self, event=None):
        pass

    def onConfigDataFitting(self, event=None):
        pass

    def showInspectionTool(self, event=None):
        app = wx.GetApp()
        app.ShowInspectionTool()

    def onAbout(self,evt):
        dlg = wx.MessageDialog(self, self._about,
                               "About Larch XYFit",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def onExit(self, evt):
        for nam in dir(self.larch.symtable._plotter):
            obj = getattr(self.larch.symtable._plotter, nam)
            time.sleep(0.05)
            try:
                obj.Destroy()
            except:
                pass

        for nam in dir(self.larch.symtable._sys.wx):
            obj = getattr(self.larch.symtable._sys.wx, nam)
            time.sleep(0.05)
            del obj

        if self.larch_buffer is not None:
            try:
                self.larch_buffer.Destroy()
            except:
                pass
        self.Destroy()

    def onCloseNicely(self, evt):
        dlg = wx.MessageDialog(None, 'Really Quit?', 'Question',
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if wx.ID_YES != dlg.ShowModal():
            return

        self.controller.save_config()
        self.proc_panel.proc_timer.Stop()
        time.sleep(0.05)
        self.onExit(evt)

    def show_subframe(self, name, frameclass, **opts):
        shown = False
        if name in self.subframes:
            try:
                self.subframes[name].Raise()
                shown = True
            except:
                del self.subframes[name]
        if not shown:
            self.subframes[name] = frameclass(self, **opts)

    def onSelectColumns(self, evt=None):
        dgroup = self.controller.get_group(self.controller.groupname)
        self.show_subframe('readfile', ColumnDataFileFrame,
                           group=dgroup.raw,
                           last_array_sel=self.last_array_sel,
                           _larch=self.larch,
                           read_ok_cb=partial(self.onRead_OK,
                                              overwrite=True))

    def onReadDialog(self, evt=None):
        dlg = wx.FileDialog(self, message="Read Data File",
                            defaultDir=os.getcwd(),
                            wildcard=FILE_WILDCARDS,
                            style=wx.FD_OPEN|wx.FD_MULTIPLE)
        self.paths2read = []
        if dlg.ShowModal() == wx.ID_OK:
            self.paths2read = dlg.GetPaths()
        dlg.Destroy()

        if len(self.paths2read) < 1:
            return

        path = self.paths2read.pop(0)
        path = path.replace('\\', '/')
        do_read = True
        if path in self.controller.file_groups:
            do_read = (wx.ID_YES == popup(self,
                                          "Re-read file '%s'?" % path,
                                          'Re-read file?'))
        if do_read:
            self.onRead(path)

    def onRead(self, path):
        filedir, filename = os.path.split(path)
        if self.controller.get_config('chdir_on_fileopen'):
            os.chdir(filedir)
            self.controller.set_workdir()


        # check for athena projects
        if is_athena_project(path):
            kwargs = dict(filename=path,
                          _larch = self.controller.larch,
                          read_ok_cb=self.onReadAthenaProject_OK)
            self.show_subframe('athena_import', AthenaImporter, **kwargs)
        else:

            kwargs = dict(filename=path,
                          _larch=self.larch_buffer.larchshell,
                          last_array_sel = self.last_array_sel,
                          read_ok_cb=self.onRead_OK)

            self.show_subframe('readfile', ColumnDataFileFrame, **kwargs)

    def onReadAthenaProject_OK(self, path, namelist):
        """read groups from a list of groups from an athena project file"""
        self.larch.eval("_prj = read_athena('{path:s}', do_fft=False, do_bkg=False)".format(path=path))

        s = """{group:s} = _prj.{group:s}
        {group:s}.datatype = 'xas'
        {group:s}.x = {group:s}.xdat = {group:s}.energy
        {group:s}.y = {group:s}.ydat = {group:s}.mu
        {group:s}.yerr = 1.0
        {group:s}.plot_ylabel = 'mu'
        {group:s}.plot_xlabel = 'energy'
        """
        for gname in namelist:
            self.larch.eval(s.format(group=gname))
            self.install_group(gname, gname)
        self.larch.eval("del _prj")


    def onRead_OK(self, script, path, groupname=None, array_sel=None,
                  overwrite=False):
        """ called when column data has been selected and is ready to be used
        overwrite: whether to overwrite the current datagroup, as when
        editing a datagroup
        """
        abort_read = False
        filedir, filename = os.path.split(path)
        if not overwrite and hasattr(self.larch.symtable, groupname):
            newname = file2groupname(filename, symtable=self.larch.symtable)
            msg = """Warning: groupname '%s' already used.
            Will use groupname '%s' instead """  % (groupname, newname)
            dlg = wx.MessageDialog(self, msg, 'Warning',
                                   wx.OK | wx.CANCEL )

            abort_read = (wx.ID_OK != dlg.ShowModal())
            dlg.Destroy()
            groupname = newname

        if abort_read:
            return
        self.larch.eval(script.format(group=groupname, path=path))
        if array_sel is not None:
            self.last_array_sel = array_sel

        self.install_group(groupname, filename)

        if len(self.paths2read) > 0 :
            path = self.paths2read.pop(0)
            path = path.replace('\\', '/')
            filedir, filename = os.path.split(path)
            gname = file2groupname(filename, symtable=self.larch.symtable)
            self.onRead_OK(script, path, groupname=gname)


    def install_group(self, groupname, filename):
        """add groupname / filename to list of available data groups"""

        thisgroup = getattr(self.larch.symtable, groupname)
        thisgroup.groupname = groupname
        thisgroup.filename = filename

        datatype = getattr(thisgroup, 'datatype', 'raw')
        # file /group may already exist in list
        if filename in self.controller.file_groups and not overwrite:
            for i in range(1, 101):
                ftest = "%s (%i)"  % (filename, i)
                if ftest not in self.controller.file_groups:
                    filename = ftest
                    break

        if filename not in self.controller.file_groups:
            self.controller.filelist.Append(filename)
            self.controller.file_groups[filename] = groupname
        self.nb.SetSelection(0)
        self.ShowFile(groupname=groupname)


class XYFitViewer(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def __init__(self, **kws):
        wx.App.__init__(self, **kws)

    def run(self):
        self.MainLoop()

    def createApp(self):
        frame = XYFitFrame()
        frame.Show()
        self.SetTopWindow(frame)

    def OnInit(self):
        self.Init()
        self.createApp()
        return True

def initializeLarchPlugin(_larch=None):
    """add XYFitFrame to _sys.gui_apps """
    if _larch is not None:
        _sys = _larch.symtable._sys
        if not hasattr(_sys, 'gui_apps'):
            _sys.gui_apps = {}
        _sys.gui_apps['xyfit'] = ('XY Data Viewing & Fitting', XYFitFrame)

def registerLarchPlugin():
    return ('_sys.wx', {})

if __name__ == "__main__":
    XYFitViewer().run()
