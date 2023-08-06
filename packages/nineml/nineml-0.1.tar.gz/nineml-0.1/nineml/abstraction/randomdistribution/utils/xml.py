"""
docstring needed

:copyright: Copyright 2010-2013 by the Python lib9ML team, see AUTHORS.
:license: BSD-3, see LICENSE for details.
"""
from nineml.annotations import annotate_xml
from nineml.utils import expect_single
from nineml.xmlns import E
from ..base import RandomDistribution, RandomDistributionBlock
from nineml.annotations import read_annotations
from ...componentclass.utils.xml import (
    ComponentClassXMLLoader, ComponentClassXMLWriter)
from nineml.exceptions import handle_xml_exceptions


class RandomDistributionXMLLoader(ComponentClassXMLLoader):

    """This class is used by XMLReader interny.

    This class loads a NineML XML tree, and stores
    the components in ``components``. It o records which file each XML node
    was loaded in from, and stores this in ``component_srcs``.

    """

    @read_annotations
    @handle_xml_exceptions
    def load_componentclass(self, element):
        subblocks = ('Parameter', 'RandomDistribution')
        children = self._load_blocks(element, blocks=subblocks)
        randomdistributionblock = expect_single(children["RandomDistribution"])
        return RandomDistribution(
            name=element.attrib['name'],
            parameters=children["Parameter"],
            randomdistributionblock=randomdistributionblock,
            url=self.document.url)

    @read_annotations
    @handle_xml_exceptions
    def load_randomdistributionblock(self, element):
        subblocks = ()
        children = self._load_blocks(element, blocks=subblocks)  # @UnusedVariable @IgnorePep8
        return RandomDistributionBlock(
            standard_library=element.attrib['standard_library'])

    tag_to_loader = {
        "ComponentClass": load_componentclass,
        "RandomDistribution": load_randomdistributionblock
    }


class RandomDistributionXMLWriter(ComponentClassXMLWriter):

    @annotate_xml
    def visit_componentclass(self, componentclass):
        elements = ([p.accept_visitor(self)
                     for p in componentclass.parameters] +
                    [componentclass._main_block.accept_visitor(self)])
        return E('ComponentClass', *elements, name=componentclass.name)

    @annotate_xml
    def visit_randomdistributionblock(self, randomdistributionblock):
        return E('RandomDistribution',
                 standard_library=randomdistributionblock.standard_library)
