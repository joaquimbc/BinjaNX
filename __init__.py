from binaryninja.binaryview import BinaryView, BinaryViewType
from binaryninja.architecture import Architecture
from binaryninja.platform import Platform

from .plugin import Kip1View, HorizonAarchPlatform

horizonnx = HorizonAarchPlatform(Architecture['aarch64'])
horizonnx.register("switch")

Kip1View.register()