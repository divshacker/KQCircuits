# Copyright (c) 2019-2020 IQM Finland Oy.
#
# All rights reserved. Confidential and proprietary.
#
# Distribution or reproduction of any information contained herein is prohibited without IQM Finland Oy’s prior
# written permission.

from kqcircuits.elements.finger_capacitor_square import FingerCapacitorSquare
from kqcircuits.pya_resolver import pya


class FingerCapacitorSquareMultiface(FingerCapacitorSquare):
    """The PCell declaration for a square finger capacitor with opened ground plane on opposite face.

    Two ports with reference points. The arm leading to the finger has the same width as fingers. The feedline has
    the same length as the width of the ground gap around the coupler. Ground avoidance layer around the capacitor also
    on face 1.
    """

    PARAMETERS_SCHEMA = {
        "margin_other_face": {
            "type": pya.PCellParameterDeclaration.TypeDouble,
            "description": "Margin for the opening on the other face [μm]",
            "default": 20
        },
    }

    def produce_impl(self):

        region_ground = self.get_ground_region()
        region_gap = pya.Region(region_ground.bbox()).size(self.margin_other_face/self.layout.dbu,
                                                           self.margin_other_face/self.layout.dbu, 2)
        region_protection = pya.Region(region_gap.bbox()).size(self.margin/self.layout.dbu,
                                                               self.margin/self.layout.dbu, 2)
        self.cell.shapes(self.get_layer("base metal gap wo grid", 1)).insert(region_gap)
        self.cell.shapes(self.get_layer("ground grid avoidance", 1)).insert(region_protection)

        super().produce_impl()
