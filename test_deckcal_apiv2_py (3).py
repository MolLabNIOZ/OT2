import logging

from opentrons import types
from opentrons.hardware_control import robot_calibration as robot_cal

metadata={"apiLevel": "2.6"}

log = logging.getLogger('opentrons.current_protocol')

tipracks = {
    'p1000': 'opentrons_96_tiprack_1000ul',
    'p300': 'opentrons_96_tiprack_300ul',
    'p50': 'opentrons_96_tiprack_300ul',
    'p20': 'opentrons_96_tiprack_20ul',
    'p10': 'opentrons_96_tiprack_10ul'
}


def pipette_offset(instr):
    if instr.channels != 1:
        return types.Point(0, 63, 0)
    else:
        return types.Point(0, 0, 0)

def get_instruments(ctx):
    ctx._hw_manager.hardware.cache_instruments()
    attached = ctx._hw_manager.hardware.get_attached_instruments()
    instr = ctx._hw_manager.hardware._attached_instruments
    if attached[types.Mount.LEFT]:
        left_tr_kind = tipracks[attached[types.Mount.LEFT]['name'].split('_')[0]]
        left_tr = ctx.load_labware(left_tr_kind, '5')
        left = ctx.load_instrument(
            attached[types.Mount.LEFT]['name'], 'left', tip_racks=[left_tr])
    else:
        left = None
        left_tr = None
        left_tr_kind = None

    if attached[types.Mount.RIGHT]:
        right_tr_kind = tipracks[attached[types.Mount.RIGHT]['name'].split('_')[0]]
        if left_tr_kind == right_tr_kind:
            right_tr = left_tr
        else:
            right_tr = ctx.load_labware(right_tr_kind, '8')
        right = ctx.load_instrument(
            attached[types.Mount.RIGHT]['name'], 'right', tip_racks=[right_tr])
    else:
        right = None
        right_tr = None
    log.info(
        f"Using left instr={left} with tr {left_tr}, right instr={right} with tr {right_tr}")

    return left, right

def run(ctx):
    ctx.set_rail_lights(True)
    left, right = get_instruments(ctx)
    deck = ctx.deck

    if right:
        right.pick_up_tip()
    if left:
        left.pick_up_tip()
    ctx.pause('Remove tipracks')

    pointnames = ['1BLC', '3BRC', '7TLC']

    for name in pointnames:
        pt = deck.get_calibration_position(name).position
        if right:
            point = types.Point(*pt) + pipette_offset(right)
            log.info(f'right move to point {point}')
            right.move_to(types.Location(point, None), minimum_z_height=50)
            ctx.pause(f'Right on cross {name}')

        if left:
            point = types.Point(*pt) + pipette_offset(left)
            log.info(f'left move to point {point}')
            left.move_to(
                types.Location(point, None), minimum_z_height=50)
            ctx.pause(f'Left on cross {name}')

    if right:
        right.return_tip()
    if left:
        left.return_tip()
    ctx.set_rail_lights(False)
