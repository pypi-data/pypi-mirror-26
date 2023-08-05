import copy

import h5py
import numpy as np
from skimage.restoration import unwrap_phase

from . import holo
from .image_data import Amplitude, Phase
from .meta import MetaDict
from ._version import version as __version__

VALID_INPUT_DATA = ["field", "phase", "hologram",
                    "phase,amplitude", "phase,intensity"]


class QPImage(object):
    _instances = 0

    def __init__(self, data=None, bg_data=None, which_data="phase",
                 meta_data={}, h5file=None, h5mode="a"
                 ):
        """Quantitative phase image manipulation

        This class implements various tasks for quantitative phase
        imaging, including phase unwrapping, background correction,
        numerical focusing, and data export.

        Parameters
        ----------
        data: 2d ndarray (float or complex) or list
            The experimental data (see `which_data`)
        bg_data: 2d ndarray (float or complex), list, or `None`
            The background data (must be same type as `data`)
        which_data: str
            String or comma-separated list of strings indicating
            the order and type of input data. Valid values are
            "field", "phase", "phase,amplitude", or "phase,intensity",
            where the latter two require an indexable object with
            the phase data as first element.
        meta_data: dict
            Meta data associated with the input data.
            see :py:class:`qpimage.VALID_META_KEYS`
        h5file: str, h5py.Group, h5py.File, or None
            A path to an hdf5 data file where all data is cached. If
            set to `None` (default), all data will be handled in
            memory using the "core" driver of the :mod:`h5py`'s
            :class:`h5py:File` class. If the file does not exist,
            it is created. If the file already exists, it is opened
            with the file mode defined by `hdf5_mode`. If this is
            an instance of h5py.Group or h5py.File, then this will
            be used to internally store all data.
        h5mode: str
            Valid file modes are (only applies if `h5file` is a path)
              - "r": Readonly, file must exist
              - "r+": Read/write, file must exist
              - "w": Create file, truncate if exists
              - "w-" or "x": Create file, fail if exists
              - "a": Read/write if exists, create otherwise (default)
        """
        if isinstance(h5file, h5py.Group):
            self.h5 = h5file
            self._do_h5_cleanup = False
        else:
            if h5file is None:
                h5kwargs = {"name": "qpimage{}.h5".format(QPImage._instances),
                            "driver": "core",
                            "backing_store": False,
                            "mode": "a"}
            else:
                h5kwargs = {"name": h5file,
                            "mode": h5mode}
            self.h5 = h5py.File(**h5kwargs)
            self._do_h5_cleanup = True
        QPImage._instances += 1
        # set meta data
        meta = MetaDict(meta_data)
        for key in meta:
            self.h5.attrs[key] = meta[key]
        if "qpimage version" not in self.h5.attrs:
            self.h5.attrs["qpimage version"] = __version__
        # set data
        for group in ["amplitude", "phase"]:
            if group not in self.h5:
                self.h5.create_group(group)
        self._amp = Amplitude(self.h5["amplitude"])
        self._pha = Phase(self.h5["phase"])
        if data is not None:
            # compute phase and amplitude from input data
            amp, pha = self._get_amp_pha(data=data,
                                         which_data=which_data)
            self._amp["raw"] = amp
            self._pha["raw"] = pha
            # set background data
            self.set_bg_data(bg_data=bg_data,
                             which_data=which_data)

    def __enter__(self):
        return self

    def __eq__(self, other):
        if (np.allclose(self.amp, other.amp) and
            np.allclose(self.pha, other.pha) and
                self.meta == other.meta):
            return True
        else:
            return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._do_h5_cleanup:
            self.h5.flush()
            self.h5.close()

    def __repr__(self):
        rep = "QPImage, {x}x{y}px".format(x=self._amp.raw.shape[0],
                                          y=self._amp.raw.shape[1],
                                          )
        if "wavelength" in self.h5.attrs:
            wl = self.h5.attrs["wavelength"]
            if wl < 2000e-9 and wl > 10e-9:
                # convenience for light microscopy
                rep += ", λ={:.1f}nm".format(wl * 1e9)
            else:
                rep += ", λ={:.2e}m".format(wl)

        return rep

    def _get_amp_pha(self, data, which_data):
        """Convert input data to phase and amplitude

        Parameters
        ----------
        data: 2d ndarray (float or complex) or list
            The experimental data (see `which_data`)
        which_data: str
            String or comma-separated list of strings indicating
            the order and type of input data. Valid values are
            "field", "phase", "hologram", "phase,amplitude", or
            "phase,intensity", where the latter two require an
            indexable object with the phase data as first element.

        Returns
        -------
        amp, pha: tuple of (:py:class:`Amplitdue`, :py:class:`Phase`)
        """
        if which_data not in VALID_INPUT_DATA:
            msg = "`which_data` must be one of {}!".format(VALID_INPUT_DATA)
            raise ValueError(msg)

        if which_data == "field":
            amp = np.abs(data)
            pha = unwrap_phase(np.angle(data))
        elif which_data == "phase":
            pha = unwrap_phase(data)
            amp = np.ones_like(data)
        elif which_data == "phase,amplitude":
            amp = data[1]
            pha = unwrap_phase(data[0])
        elif which_data == "phase,intensity":
            amp = np.sqrt(data[1])
            pha = unwrap_phase(data[0])
        elif which_data == "hologram":
            amp, pha = self._get_amp_pha(holo.get_field(data),
                                         which_data="field")
        return amp, pha

    @property
    def bg_amp(self):
        """background amplitude image"""
        return self._amp.bg

    @property
    def bg_pha(self):
        """background phase image"""
        return self._pha.bg

    @property
    def amp(self):
        """background-corrected amplitude image"""
        return self._amp.image

    @property
    def field(self):
        """background-corrected complex field"""
        return self.amp * np.exp(1j * self.pha)

    @property
    def meta(self):
        """meta data"""
        return MetaDict(self.h5.attrs)

    @property
    def pha(self):
        """background-corrected phase image"""
        return self._pha.image

    @property
    def shape(self):
        """the shape of the image"""
        return self._pha.h5["raw"].shape

    def clear_bg(self, which_data=["amplitude", "phase"], keys="fit"):
        """Clear background correction

        Parameters
        ----------
        which_data: str or list of str
            From which type of data to remove the background
            information. The list contains either "amplitude",
            "phase", or both.
        keys: str or list of str
            Which type of background data to remove. One of:
              - "fit": the background data computed with
                :py:func:`qpimage.QPImage.compute_bg`
              - "data": the experimentally obtained background image

        """
        # convert to list
        if isinstance(which_data, str):
            which_data = [which_data]
        if isinstance(keys, str):
            keys = [keys]
        # Get image data for clearing
        imdats = []
        if "amplitude" in which_data:
            imdats.append(self._amp)
        if "phase" in which_data:
            imdats.append(self._pha)
        if not imdats:
            msg = "`which_data` must contain 'phase' or 'amplitude'!"
            raise ValueError(msg)
        # Perform clearing of backgrounds
        for imdat in imdats:
            for key in keys:
                imdat.set_bg(None, key)

    def compute_bg(self, which_data="phase",
                   fit_offset="average", fit_profile="ramp",
                   border_m=0, border_perc=0, border_px=0,
                   from_binary=None, ret_binary=False):
        """Compute background correction

        Parameters
        ----------
        which_data: str or list of str
            From which type of data to remove the background
            information. The list contains either "amplitude",
            "phase", or both.
        fit_profile: str
            The type of background profile to fit:
              - "ramp": 2D linear ramp with offset (default)
              - "offset": offset only
        fit_offset: str
            The method for computing the profile offset
              - "fit": offset as fitting parameter
              - "gauss": center of a gaussian fit
              - "mean": simple average
              - "mode": mode (see `qpimage.bg_estimate.mode`)
        border_m: float
            Assume that a frame of `border_m` meters around the
            image is background. The value is converted to
            pixels and rounded.
        border_perc: float
            Assume that a frame of `border_perc` percent around
            the image is background. The value is converted to
            pixels and rounded. If the aspect ratio of the image
            is not one, then the average of the data's shape is
            used to compute the percentage in pixels.
        border_px: float
            Assume that a frame of `border_px` pixels around
            the image is background.
        from_binary: boolean np.ndarray or None
            Use a boolean array to define the background area.
            The binary image must have the same shape as the
            input data.
        ret_binary: bool
            Return the binary image used to compute the background.

        Notes
        -----
        The `border_*` values are translated to pixel values and
        the largest pixel border is used to generate a binary
        image for background computation.

        If any of the `border_*` arguments are non-zero and
        `from_binary` is given, the intersection of the two
        resulting binary images is used.

        See Also
        --------
        qpimage.bg_estimate.estimate
        """
        # convert to list
        if isinstance(which_data, str):
            which_data = [which_data]
        # check validity
        if not ("amplitude" in which_data or
                "phase" in which_data):
            msg = "`which_data` must contain 'phase' or 'amplitude'!"
            raise ValueError(msg)
        # get border in px
        border_list = []
        if border_m:
            if border_m < 0:
                raise ValueError("`border_m` must be greater than zero!")
            border_list.append(border_m / self.meta["pixel size"])
        if border_perc:
            if border_perc < 0 or border_perc > 50:
                raise ValueError("`border_perc` must be in interval [0, 50]!")
            size = np.average(self.shape)
            border_list.append(size * border_perc / 100)
        if border_px:
            border_list.append(border_px)
        # get maximum border size
        if border_list:
            border_px = np.int(np.round(np.max(border_list)))
        elif from_binary is None:
            raise ValueError("Neither `from_binary` nor `border_*` given!")
        elif np.all(from_binary == 0):
            raise ValueError("`from_binary` must not be all-zero!")
        # Get affected image data
        imdat_list = []
        if "amplitude" in which_data:
            imdat_list.append(self._amp)
        if "phase" in which_data:
            imdat_list.append(self._pha)
        # Perform correction
        for imdat in imdat_list:
            binary = imdat.estimate_bg(fit_offset=fit_offset,
                                       fit_profile=fit_profile,
                                       border_px=border_px,
                                       from_binary=from_binary,
                                       ret_binary=ret_binary)
        return binary

    def copy(self, h5file=None):
        """Create a copy of the current instance

        This is done by recursively copying the underlying hdf5 data.

        Parameters
        ----------
        h5file: str, h5py.File, h5py.Group, or None
            see `QPImage.__init__`
        """
        h5 = copyh5(self.h5, h5file)
        return QPImage(h5file=h5)

    def refocus(self, distance, method="helmholtz"):
        """Numerically refocus the current field

        Parameters
        ----------
        distance: float
            Focusing distance [m]
        method: str
            Refocusing method, one of ["helmholtz","fresnel"]

        See Also
        --------
        :mod:`nrefocus` library used for numerical focusing
        """
        # TODO:
        # - Perform refocusing and create new image data instances
        # - Remember old image data instances
        # - Maybe return a new instance of QPImage
        # - Allow autofocusing?
        raise NotImplementedError("refocusing not implemented")

    def set_bg_data(self, bg_data, which_data=None):
        """Set background amplitude and phase data

        Parameters
        ----------
        bg_data: 2d ndarray (float or complex), list, QPImage, or `None`
            The background data (must be same type as `data`).
            If set to `None`, the background data is reset.
        which_data: str
            String or comma-separated list of strings indicating
            the order and type of input data. Valid values are
            "field", "phase", "phase,amplitude", or "phase,intensity",
            where the latter two require an indexable object with
            the phase data as first element.
        """
        if isinstance(bg_data, QPImage):
            if which_data is not None:
                msg = "`which_data` must not be set if `bg_data` is QPImage!"
                raise ValueError(msg)
            pha, amp = bg_data.pha, bg_data.amp
        elif bg_data is None:
            # Reset phase and amplitude
            amp, pha = None, None
        else:
            # Compute phase and amplitude from data and which_data
            amp, pha = self._get_amp_pha(bg_data, which_data)
        # Set background data
        self._amp.set_bg(amp, key="data")
        self._pha.set_bg(pha, key="data")


def copyh5(inh5, outh5):
    """Recursively copy all hdf5 data from one group to another

    Parameters
    ----------
    inh5: str, h5py.File, or h5py.Group
        The input hdf5 data. This can be either a file name or
        an hdf5 object.
    outh5: str, h5py.File, h5py.Group, or None
        The output hdf5 data. This can be either a file name or
        an hdf5 object. If set to `None`, a new hdf5 object is
        created in memory.

    Notes
    -----
    All data in outh5 are overridden by the inh5 data.
    """
    if not isinstance(inh5, h5py.Group):
        inh5 = h5py.File(inh5, mode="r")
    if outh5 is None:
        # create file in memory
        h5kwargs = {"name": "qpimage{}.h5".format(QPImage._instances),
                    "driver": "core",
                    "backing_store": False,
                    "mode": "a"}
        outh5 = h5py.File(**h5kwargs)
        return_h5obj = True
        QPImage._instances += 1
    elif not isinstance(outh5, h5py.Group):
        # create new file
        outh5 = h5py.File(outh5, mode="w")
        return_h5obj = False
    else:
        return_h5obj = True
    # begin iteration
    for key in inh5:
        if key in outh5:
            del outh5[key]
        if isinstance(inh5[key], h5py.Group):
            outh5.create_group(key)
            copyh5(inh5[key], outh5[key])
        else:
            outh5[key] = copy.copy(inh5[key].value)
            outh5[key].attrs.update(inh5[key].attrs)
    outh5.attrs.update(inh5.attrs)
    if return_h5obj:
        # in-memory or previously created instance of h5py.File
        return outh5
    else:
        # properly close the file and return its name
        fn = outh5.filename
        outh5.flush()
        outh5.close()
        return fn
