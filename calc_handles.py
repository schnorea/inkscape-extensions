import inkex
import math
import os


class BoundingBoxExtension(inkex.EffectExtension):

    @staticmethod
    def get_height(path):
        bbox = path.bounding_box(path.getparent().composed_transform())
        height = bbox.bottom - bbox.top
        return height

    @staticmethod
    def get_width_height(path):
        bbox = path.bounding_box(path.getparent().composed_transform())
        height = bbox.bottom - bbox.top
        width = bbox.right - bbox.left
        return width, height, bbox

    def effect(self):
        # Loop through selected items in the Inkscape document
        # for node in self.selected.values():
        for node in self.svg.selection.filter(inkex.PathElement):
            if node.tag == inkex.addNS('path', 'svg'):
                # Get the PathElement
                pathElement = node

                width, height, bbox = self.get_width_height(pathElement)
                path = pathElement.get_path()

                # scale_factor = 57.15/float(height)
                # path = path.scale(scale_factor, scale_factor, inplace=False)
                # pathElement.set_path(path)
                     
                # Width and height post scaling
                width, height, bbox = self.get_width_height(pathElement)

                # Calculate the delta width to create the perspecitive 
                # required for the 7 degree pint glass
                px_delta = (height * math.tan(math.radians(7)))/ 2.0

                X_new_lower_left = bbox.left - px_delta
                X_new_lower_right = bbox.right + px_delta

                instructions = []
                instructions.append("To apply Pint Glass perspective (7 degrees)")
                instructions.append("to the selected path, adjust the handels in the")
                instructions.append("path effect perspective dialog like this:")
                instructions.append(f"TL  X {bbox.left:.2f}              TR  X {bbox.right:.2f}")
                instructions.append(f"TL  Y {bbox.top:.2f}               TR  Y {bbox.top:.2f}")
                instructions.append("")
                instructions.append(f"LL  X {X_new_lower_left:.2f}              LR  X {X_new_lower_right:.2f}")
                instructions.append(f"LL  Y {bbox.bottom:.2f}            LR  Y {bbox.bottom:.2f}")
                instructions.append("")
                instructions.append("Copy down the LL X and LR X values as they will change others will not")
                instructions.append(f"The internal calc shows this is the height {height} ")
                instructions.append(f"For self.svg.document_unit {self.svg.document_unit}")
                instruction = '\n'.join(instructions)

                expanded_path = os.path.expanduser('~/bound-debug.txt')
                with open(expanded_path , 'w') as ofh:
                    print("*************************************", file=ofh)
                    print("HERE IS THE OUTPUT OF THE EXTENSION  ", file=ofh)
                    print("*************************************", file=ofh)
                    print(f"Unit type {type(self.svg.document_unit)}", file=ofh)
                    ofh.write(instruction)

                
                raise inkex.AbortExtension(
                    _(instruction)
                )




if __name__ == '__main__':
    BoundingBoxExtension().run()
