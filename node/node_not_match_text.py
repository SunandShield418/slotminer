from node.node import node
import pdb

class node_not_match_text(node):
    def __init__(self, target_text, logger):
        node.__init__(self, logger=logger)
        self._type = '(NOT)MATCH_TEXT'
        self._attr['target_text'] = target_text

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []

        # 결과물 만드는 경우,
        if text == None:
            return extent, position, True, [self._attr['target_text']]

        if self.num_child():
            if self._logger:
                self._logger.error('(not)match_text_node must be terminal node')
            return extent, position, pass_fail, reserved
        if not self._attr.get('target_text'):
            if self._logger:
                self._logger.error('empty (not)target_text')
            return extent, position, pass_fail, reserved

        target_text = self._attr['target_text']
        pos_begin = position
        i = 0
        while i < len(target_text):
            pos_begin -= 1
            if pos_begin < 0:
                break
            if text[pos_begin] == ' ':
                continue
            i += 1
        if i < len(target_text):
            return extent, position, True, reserved
        pos_end = position
        this_text = text[pos_begin:pos_end].lower().rstrip()

        # overlap check with extent
        if add_extent and extent.is_overlap((pos_begin, pos_end)):
            return extent, position, pass_fail, reserved

        if this_text == target_text:
            reserved += [pos_end-pos_begin]
        else:
            _extent = extent.copy()
            if add_extent:
                _extent.add((pos_begin, pos_end))
            pass_fail = True
            return _extent, position, pass_fail, reserved

        return extent, position, pass_fail, reserved

