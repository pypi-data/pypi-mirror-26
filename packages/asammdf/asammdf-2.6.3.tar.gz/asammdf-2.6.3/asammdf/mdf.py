# -*- coding: utf-8 -*-
"""
common MDF file format module

"""
import csv
import os
from warnings import warn

import numpy as np

from .mdf3 import MDF3
from .mdf4 import MDF4
from .utils import MdfException


MDF3_VERSIONS = ('3.00', '3.10', '3.20', '3.30')
MDF4_VERSIONS = ('4.00', '4.10', '4.11')


__all__ = ['MDF', ]


class MDF(object):
    """Unified access to MDF v3 and v4 files.

    Parameters
    ----------
    name : string
        mdf file name, if provided it must be a real file name
    load_measured_data : bool
        load data option; default *True*

        * if *True* the data group binary data block will be loaded in RAM
        * if *False* the channel data is read from disk on request
    version : string
        mdf file version ('3.00', '3.10', '3.20', '3.30', '4.00', '4.10',
        '4.11'); default '4.10'

    """
    def __init__(self, name=None, load_measured_data=True, version='4.10'):
        if name:
            if os.path.isfile(name):
                with open(name, 'rb') as file_stream:
                    file_stream.read(8)
                    version = file_stream.read(4).decode('ascii')
                if version in MDF3_VERSIONS:
                    self._file = MDF3(name, load_measured_data)
                elif version in MDF4_VERSIONS:
                    self._file = MDF4(name, load_measured_data)
                else:
                    message = ('"{}" is not a supported MDF file; '
                               '"{}" file version was found')
                    raise MdfException(message.format(name, version))
            else:
                raise MdfException('File "{}" does not exist'.format(name))
        else:
            if version in MDF3_VERSIONS:
                self._file = MDF3(version=version,
                                  load_measured_data=load_measured_data)
            elif version in MDF4_VERSIONS:
                self._file = MDF4(version=version,
                                  load_measured_data=load_measured_data)

        # link underlying _file attributes and methods to the new MDF object
        for attr in set(dir(self._file)) - set(dir(self)):
            setattr(self, attr, getattr(self._file, attr))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def convert(self, to, load_measured_data=True):
        """convert MDF to other versions

        Parameters
        ----------
        to : str
            new mdf version from ('3.00', '3.10', '3.20', '3.30', '4.00',
            '4.10', '4.11')
        load_measured_data : bool
            load data option; default *True*

            * if *True* the data group binary data block will be loaded in RAM
            * if *False* the channel data is stored to a temporary file and
            read from disk on request

        Returns
        -------
        out : MDF
            new MDF object

        """
        if to not in MDF3_VERSIONS + MDF4_VERSIONS:
            message = ('Unknown output mdf version "{}".'
                       ' Available versions are {}')
            warn(message.format(to, MDF4_VERSIONS + MDF3_VERSIONS))
            return
        else:
            out = MDF(version=to, load_measured_data=load_measured_data)

            # walk through all groups and get all channels
            for i, gp in enumerate(self.groups):
                sigs = []
                if self.masters_db.get(i, None) is None:
                    excluded_channels = []
                else:
                    excluded_channels = [self.masters_db[i], ]
                channels = gp['channels']

                if self.version in MDF3_VERSIONS:
                    for dep in gp['channel_dependencies']:
                        if dep is None:
                            continue
                        for ch_nr, gp_nr in dep.referenced_channels:
                            if gp_nr == i:
                                excluded_channels.append(ch_nr)
                else:
                    for dependencies in gp['channel_dependencies']:
                        if dependencies is None:
                            continue
                        if all(dep['id'] == b'##CN' for dep in dependencies):
                            for ch in dependencies:
                                excluded_channels.append(channels.index(ch))
                        else:
                            for dep in dependencies:
                                for ch_nr, gp_nr in dep.referenced_channels:
                                    if gp_nr == i:
                                        excluded_channels.append(ch_nr)

                for j, ch in enumerate(gp['channels']):
                    if j in excluded_channels:
                        continue
                    sigs.append(self.get(group=i, index=j))
                if sigs:
                    source_info = 'Converted from {} to {}'
                    out.append(sigs,
                               source_info.format(self.version, to),
                               common_timebase=True)
            return out

    def cut(self, start=None, stop=None, whence=0):
        """convert MDF to other versions

        Parameters
        ----------
        start : float
            start time, default None. If *None* then the start of measurement
            is used
        stop : float
            stop time, default . If *None* then the end of measurement is used
        whence : int
            how to search for the start and stop values

            * 0 : absolute
            * 1 : relative to first timestamp

        Returns
        -------
        out : MDF
            new MDF object

        """
        out = MDF(version=self.version,
                  load_measured_data=self.load_measured_data)

        if whence == 1:
            timestamps = []
            for i, _ in enumerate(self.groups):
                master_index = self.masters_db.get(i, None)
                if master_index is not None:
                    master = self.get(group=i,
                                      index=master_index,
                                      samples_only=True)
                    if len(master):
                        timestamps.append(master[0])
            first_timestamp = np.amin(timestamps)
            if start is not None:
                start += first_timestamp
            if stop is not None:
                stop += first_timestamp

        # walk through all groups and get all channels
        for i, gp in enumerate(self.groups):
            sigs = []
            if self.masters_db.get(i, None) is None:
                excluded_channels = []
            else:
                excluded_channels = [self.masters_db[i], ]
            channels = gp['channels']

            if self.version in MDF3_VERSIONS:
                for dep in gp['channel_dependencies']:
                    if dep is None:
                        continue
                    for ch_nr, gp_nr in dep.referenced_channels:
                        if gp_nr == i:
                            excluded_channels.append(ch_nr)
            else:
                for dependency_list in gp['channel_dependencies']:
                    if dependency_list is None:
                        continue
                    if all(dep['id'] == b'##CN' for dep in dependency_list):
                        for ch in dependency_list:
                            excluded_channels.append(channels.index(ch))
                    else:
                        for dep in dependency_list:
                            for ch_nr, gp_nr in dep.referenced_channels:
                                if gp_nr == i:
                                    excluded_channels.append(ch_nr)

            for j, ch in enumerate(gp['channels']):
                if j in excluded_channels:
                    continue
                sig = self.get(group=i, index=j).cut(start=start, stop=stop)
                sigs.append(sig)

            if sigs:
                if start:
                    start_ = '{}s'.format(start)
                else:
                    start_ = 'start of measurement'
                if stop:
                    stop_ = '{}s'.format(stop)
                else:
                    stop_ = 'end of measurement'
                out.append(sigs,
                           'Cut from {} to {}'.format(start_, stop_),
                           common_timebase=True)
        return out

    def export(self, fmt, filename=None):
        """ export MDF to other formats. The *MDF* file name is used is
        available, else the *filename* aragument must be provided.

        Parameters
        ----------
        fmt : string
            can be one of the following:

                * *csv* : CSV export that uses the ";" delimiter. This option
                will generate a new csv file for each data group
                (<MDFNAME>_DataGroup_XX.csv).
                * *hdf5* : HDF5 file output; each *MDF* data group is mapped to
                a *HDF5* group with the name 'DataGroup_xx'
                (where xx is the index)
                * *excel* : Excel file output (very slow). This option will
                generate a new excel file for each data group
                (<MDFNAME>_DataGroup_XX.xlsx)
                * *mat* : Matlab .mat version 5 export, for Matlab >= 7.6. In
                the mat file the channels will be renamed to
                'DataGroup_xx_<channel name>'. The channel group master will be
                renamed to 'DataGroup_xx_<channel name>_master'
                ( *xx* is the data group index starting from 0).

        filename : string
            export file name

        """

        header_items = (
            'date',
            'time',
            'author',
            'organization',
            'project',
            'subject',
        )

        if filename is None and self.name is None:
            message = ('Must specify filename for export'
                       'if MDF was created without a file name')
            warn(message)
            return

        name = self.name if self.name else filename
        if fmt == 'hdf5':
            try:
                from h5py import File as HDF5
            except ImportError:
                warn('h5py not found; export to HDF5 is unavailable')
                return
            else:
                name = os.path.splitext(name)[0] + '.hdf'
                with HDF5(name, 'w') as f:
                    # header information
                    group = f.create_group(os.path.basename(name))

                    if self.version in MDF3_VERSIONS:
                        for item in header_items:
                            group.attrs[item] = self.header[item]

                    # save each data group in a HDF5 group called
                    # "DataGroup_xx" with the index starting from 1
                    # each HDF5 group will have a string attribute "master"
                    # that will hold the name of the master channel
                    for i, grp in enumerate(self.groups):
                        group_name = r'/' + 'DataGroup_{}'.fmt(i + 1)
                        group = f.create_group(group_name)

                        master_index = self.masters_db[i]

                        for j, ch in enumerate(grp['channels']):
                            name = ch.name
                            sig = self.get(group=i, index=j)
                            if j == master_index:
                                group.attrs['master'] = name
                            dataset = group.create_dataset(name, sig.samples)
                            dataset.attrs['unit'] = sig.unit
                            if sig.comment:
                                dataset.attrs['comment'] = sig.comment
                            else:
                                dataset.attrs['comment'] = ''

        elif fmt == 'excel':
            try:
                import xlsxwriter
            except ImportError:
                warn('xlsxwriter not found; export to Excel unavailable')
                return
            else:
                excel_name = os.path.splitext(name)[0]
                nr = len(self.groups)
                for i, grp in enumerate(self.groups):
                    print('Exporting group {} of {}'.format(i+1, nr))

                    group_name = 'DataGroup_{}'.format(i + 1)
                    wb_name = '{}_{}.xlsx'.format(excel_name, group_name)
                    workbook = xlsxwriter.Workbook(wb_name)
                    bold = workbook.add_format({'bold': True})

                    ws = workbook.add_worksheet("Information")

                    if self.version in MDF3_VERSIONS:
                        for j, item in enumerate(header_items):

                            ws.write(j, 0, item.title(), bold)
                            ws.write(j, 1, self.header[item].decode('latin-1'))

                        ws = workbook.add_worksheet(group_name)

                        # the sheet header has 3 rows
                        # the channel name and unit 'YY [xx]'
                        # the channel comment
                        # the flag for data grup master channel
                        ws.write(0, 0, 'Channel', bold)
                        ws.write(1, 0, 'comment', bold)
                        ws.write(2, 0, 'is master', bold)

                        master_index = self.masters_db[i]

                        for j in range(grp['channel_group']['cycles_nr']):
                            ws.write(j+3, 0, str(j))

                        for j, ch in enumerate(grp['channels']):
                            sig = self.get(group=i, index=j)

                            col = j + 1
                            sig_description = '{} [{}]'.format(sig.name,
                                                               sig.unit)
                            comment = sig.comment if sig.comment else ''
                            ws.write(0, col, sig_description)
                            ws.write(1, col, comment)
                            if j == master_index:
                                ws.write(2, col, 'x')
                            ws.write_column(3, col, sig.samples.astype(str))

                    workbook.close()

        elif fmt == 'csv':
            csv_name = os.path.splitext(name)[0]
            nr = len(self.groups)
            for i, grp in enumerate(self.groups):
                print('Exporting group {} of {}'.format(i+1, nr))
                group_name = 'DataGroup_{}'.format(i + 1)
                group_csv_name = '{}_{}.csv'.format(csv_name, group_name)
                with open(group_csv_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')

                    ch_nr = len(grp['channels'])
                    channels = [self.get(group=i, index=j)
                                for j in range(ch_nr)]

                    master_index = self.masters_db[i]
                    cycles = grp['channel_group']['cycles_nr']

                    names_row = ['Channel', ]
                    names_row += ['{} [{}]'.format(ch.name, ch.unit)
                                  for ch in channels]
                    writer.writerow(names_row)

                    comment_row = ['comment', ]
                    comment_row += [ch.comment for ch in channels]
                    writer.writerow(comment_row)

                    master_row = ['Is master', ]
                    master_row += ['x' if j == master_index else ''
                                   for j in range(ch_nr)]
                    writer.writerow(master_row)

                    vals = [np.array(range(cycles), dtype=np.uint32), ]
                    vals += [ch.samples for ch in channels]

                    writer.writerows(zip(*vals))

        elif fmt == 'mat':
            try:
                from scipy.io import savemat
            except ImportError:
                warn('scipy not found; export to mat is unavailable')
                return

            name = os.path.splitext(name)[0] + '.mat'
            mdict = {}

            master = 'DataGroup_{}_{}_master'
            channel = 'DataGroup_{}_{}'

            for i, grp in enumerate(self.groups):
                for j, ch in enumerate(grp['channels']):
                    if j == master_index:
                        channel_name = master.format(i, ch.name)
                    else:
                        channel_name = channel.format(i, ch.name)
                    mdict[channel_name] = self.get(group=i,
                                                   index=j,
                                                   samples_only=True)

            savemat(name,
                    mdict,
                    long_field_names=True,
                    do_compression=True)

    def filter(self, channels):
        """ return new *MDF* object that contains only the channels listed in
        *channels* argument

        Parameters
        ----------
        channels : list
            list of channel names to be filtered

        Returns
        -------
        mdf : MDF
            new MDF file

        """

        # group channels by group index
        gps = {}
        for ch in channels:
            if ch in self.channels_db:
                for group, index in self.channels_db[ch]:
                    if group not in gps:
                        gps[group] = []
                    gps[group].append(index)
            else:
                message = ('MDF filter error: '
                           'Channel "{}" not found, it will be ignored')
                warn(message.format(ch))
                continue

        mdf = MDF(version=self.version,
                  load_measured_data=self.load_measured_data)

        # append filtered channels to new MDF
        for group in gps:
            sigs = []
            for index in gps[group]:
                sigs.append(self.get(group=group, index=index))
            if sigs:
                if self.name:
                    origin = os.path.basename(self.name)
                else:
                    origin = 'New MDF'
                source = 'Signals filtered from <{}>'.format(origin)
                mdf.append(sigs,
                           source,
                           common_timebase=True)

        return mdf

    @staticmethod
    def merge(files, outversion='4.10', load_measured_data=True):
        """ merge several files and return the merged MDF object. The files
        must have the same internal structure (same number of groups, and same
        channels in each group)

        Parameters
        ----------
        files : list | tuple
            list of MDF file names
        outversion : str
            merged file version
        load_measured_data : bool
            load data option; default *True*

            * if *True* the data group binary data block will be loaded in RAM
            * if *False* the channel data is stored to a temporary file and
            read from disk on request

        Returns
        -------
        merged : MDF
            new MDF object with merged channels

        Raises
        ------
        MdfException : if there are inconsistances between the files
            merged MDF object
        """
        if files:
            files = [MDF(file, load_measured_data) for file in files]

            if not len(set(len(file.groups) for file in files)) == 1:
                message = ("Can't merge files: "
                           "difference in number of data groups")
                raise MdfException(message)

            merged = MDF(version=outversion,
                         load_measured_data=load_measured_data)

            for i, groups in enumerate(zip(*(file.groups for file in files))):
                channels_nr = set(len(group['channels']) for group in groups)
                if not len(channels_nr) == 1:
                    message = ("Can't merge files: "
                               "different channel number for data groups {}")
                    raise MdfException(message.format(i))

                signals = []

                mdf = files[0]
                if mdf.masters_db.get(i, None) is None:
                    excluded_channels = []
                else:
                    excluded_channels = [mdf.masters_db[i], ]

                group = groups[0]
                channels = group['channels']

                if mdf.version in MDF3_VERSIONS:
                    for dep in group['channel_dependencies']:
                        if dep is None:
                            continue
                        for ch_nr, gp_nr in dep.referenced_channels:
                            if gp_nr == i:
                                excluded_channels.append(ch_nr)
                else:
                    for dependencies in group['channel_dependencies']:
                        if dependencies is None:
                            continue
                        if all(dep['id'] == b'##CN' for dep in dependencies):
                            for ch in dependencies:
                                excluded_channels.append(channels.index(ch))
                        else:
                            for dep in dependencies:
                                for ch_nr, gp_nr in dep.referenced_channels:
                                    if gp_nr == i:
                                        excluded_channels.append(ch_nr)

                group_channels = [group['channels'] for group in groups]
                for j, channels in enumerate(zip(*group_channels)):
                    if not len(set(ch.name for ch in channels)) == 1:
                        message = ("Can't merge files: "
                                   "different channel names for data group {}")
                        raise MdfException(message.format(i))

                    if j in excluded_channels:
                        continue

                    sigs = [file.get(group=i, index=j) for file in files]

                    sig = sigs[0]
                    for s in sigs[1:]:
                        sig = sig.extend(s)

                    signals.append(sig)

                if signals:
                    merged.append(signals, common_timebase=True)

            return merged
        else:
            raise MdfException('No files given for merge')

    def iter_to_pandas(self):
        """ generator that yields channel groups as pandas DataFrames"""
        try:
            from pandas import DataFrame
        except ImportError:
            warn('pandas not found; export to pandas DataFrame is unavailable')
            return
        else:
            for i, gp in enumerate(self.groups):
                master_index = self.masters_db[i]
                master_name = gp['channels'][master_index].name
                master = self.get(group=i,
                                  index=master_index,
                                  samples_only=True)
                pandas_dict = {master_name: master}
                for j, _ in (gp['channels']):
                    if j == master_index:
                        continue
                    name = gp['channels'][j].name
                    pandas_dict[name] = self.get(group=i,
                                                 index=j,
                                                 samples_only=True)
                yield DataFrame.from_dict(pandas_dict)


if __name__ == '__main__':
    pass
