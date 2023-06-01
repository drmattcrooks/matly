class SpineClass:
    def __init__(self, label, visible, color):
        self.spine_type = label
        self.edgecolor = color
        self.visible = visible

    def get_visible(self):
        return self.visible

    def set_visible(self, is_visible):
        self.visible = is_visible

    def get_color(self):
        return self.get_edgecolor()

    def set_color(self, color):
        self.set_edgecolor(color)

    def get_edgecolor(self):
        return self.edgecolor

    def set_edgecolor(self, color):
        self.edgecolor = color
