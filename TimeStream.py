import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class TimeStream:
    """
    Contains a pair of vectors: data points and the times they were collected

    This class provides convenient access to a data time stream.  It will
    eventually provide support for various time standards (labview, matlab,
    linux, windows?).  Calling the object will return the vector of data
    points.
    """
    
    TIME_TYPES = ['matlab', 'labview', 'unix']
    def __init__(self, values, t, timeType, mask = np.ma.nomask):
        if (not isinstance(values, np.ma.MaskedArray)):
            self.values = np.ma.array(values, mask = mask)
        else:
            self.values = values
        
        timeType = timeType.lower()
        self._CheckTimeType(timeType)
        if (timeType == 'matlab'):
            # significant hackery here: matlab defines
            # datenum('Jan-1-0000 00:00:00') = 1, whereas fromordinal
            # considers 1/1/0001 to be 1.
            t = [dt.datetime.fromordinal(np.floor(t[i])) - \
                     dt.timedelta(days = 366) + \
                     dt.timedelta(t[i] % 1) for i in range(len(t))]
        elif (timeType == 'unix'):
            t = [dt.datetime.fromtimestamp(t[i]) \
                      for i in range(len(t))]
        elif (timeType == 'labview'):
            delta = dt.datetime(1904, 1, 1, 0, 0, 0) - \
                    dt.datetime(1970, 1, 1, 0, 0, 0)
            t += delta.total_seconds()
            t = [dt.datetime.fromtimestamp(t[i]) \
                      for i in range(len(t))]

        self.t = np.ma.array(t, mask = self.values.mask)

    def derivative(self, gaps = True):
        """
        Return the time derivative of the time stream.
        In units of [value units]/second
        """
        self._check_masks()
        if (gaps):
            delta_val = diff(self.values.compressed())
            delta_t = diff(self.t.compressed())
        else:
            delta_val = diff(self.values).compressed()
            delta_t = diff(self.t).compressed()
        for i in range(len(delta_t)):
            delta_t[i] = delta_t[i].total_seconds()
        return (delta_val / delta_t)
    
    def integral(self, gaps = True):
        """
        Return the time integral of the time stream.
        In units of [value units] * second
        """
        self._check_masks()
        if (gaps):


    def get_contiguous(self, minsize = 0, maxgap = 0):
        """
        return a list of arrays, each of which contains contiguous
        samples
        """
        

    def get_time(self):
        '''
        return the time as a vector of datetime objects
        '''
        return self.t

    def get_unixtime(self):
        '''
        return a vector in the unix format (seconds since the eopch)
        '''
        
        epoch = dt.datetime(1970, 1, 1, 0, 0, 0, 0)
        t = np.zeros(np.shape(self.t))
        i = 0
        for tmp in self.t:
            delta = tmp - epoch
            t[i] = delta.total_seconds()
            i += 1
        return t

    def get_matlabtime(self):
        '''
        return a vector in the matlab format (days since 12/31/-0001)
        '''
        
        # more hackery here, see above
        t = np.zeros(np.shape(self.t))
        i = 0
        for tmp in self.t:
            t[i] = tmp.toordinal() + 366 + tmp.hours / 24 + \
                   tmp.minutes / (60 * 24) + tmp.seconds / (60 * 60 * 24) + \
                   tmp.microsecond / (1e6 * 60 * 60 * 24)
        return t

    def get_labviewtime(self):
        '''
        return a vector in the laview format
        (seconds since 1/1/1904 00:00:00)
        '''

        epoch = dt.datetime(1904, 1, 1, 0, 0, 0, 0)
        t = np.zeros(np.shape(self.t))
        i = 0
        for tmp in self.t:
            delta = tmp - epoch
            t[i] = delta.total_seconds()
            i += 1
        return t

    def remove(self, ind):
        '''
        remove data points given by ind

        Parameters
        ----------
        ind : array-like
            an array of indices to remove
        '''
        
        for i in np.atleast_1d(ind):
            self.t[i] = np.ma.mask
            self.values[i] = np.ma.mask
        self.t = self.t[~self.t.mask]
        self.values = self.values[~self.values.mask]

    def plot(self, ax = None, locator_args = None):
        if (ax == None):
            fig = plt.figure()
            ax = sig.add_subplot(111)
        ax.plot(self.t, self.values, '.')

        # set tickmarks for dates
        loc = mdates.AutoDateLocator(**locator_args)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))
        

    def _check_time_type(self, timeType):
        if (timeType not in TIME_TYPES):
            raise ValueError('Time format %s is invalid' %timeType)

    def _check_mask(self):
        raise ValueError('Masks do not match')
        return np.any(self.values.mask ^ self.t.mask)
        
    def __call__(self):
        return self.values

