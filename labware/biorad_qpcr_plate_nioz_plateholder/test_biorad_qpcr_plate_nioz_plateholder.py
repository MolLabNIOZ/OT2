import json
from opentrons import protocol_api, types


TEST_LABWARE_SLOT = '5'

RATE = 0.25  # % of default speeds

PIPETTE_MOUNT = 'right'
PIPETTE_NAME = 'p300_single_gen2'

TIPRACK_SLOT = '11'
TIPRACK_LOADNAME = 'opentrons_96_tiprack_300ul'
LABWARE_DEF_JSON = """{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1"],["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"],["A10","B10","C10","D10","E10","F10","G10","H10"],["A11","B11","C11","D11","E11","F11","G11","H11"],["A12","B12","C12","D12","E12","F12","G12","H12"]],"brand":{"brand":"Eppendorf/Biorad","brandId":[]},"metadata":{"displayName":"biorad_qpcr_plate_nioz_plateholder","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.56,"yDimension":85.48,"zDimension":22.5},"wells":{"A1":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":14,"y":75.24,"z":7.69},"B1":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":14,"y":66.24,"z":7.69},"C1":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":14,"y":57.24,"z":7.69},"D1":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":14,"y":48.24,"z":7.69},"E1":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":14,"y":39.24,"z":7.69},"F1":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":14,"y":30.24,"z":7.69},"G1":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":14,"y":21.24,"z":7.69},"H1":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":14,"y":12.24,"z":7.69},"A2":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":23,"y":75.24,"z":7.69},"B2":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":23,"y":66.24,"z":7.69},"C2":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":23,"y":57.24,"z":7.69},"D2":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":23,"y":48.24,"z":7.69},"E2":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":23,"y":39.24,"z":7.69},"F2":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":23,"y":30.24,"z":7.69},"G2":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":23,"y":21.24,"z":7.69},"H2":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":23,"y":12.24,"z":7.69},"A3":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":32,"y":75.24,"z":7.69},"B3":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":32,"y":66.24,"z":7.69},"C3":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":32,"y":57.24,"z":7.69},"D3":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":32,"y":48.24,"z":7.69},"E3":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":32,"y":39.24,"z":7.69},"F3":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":32,"y":30.24,"z":7.69},"G3":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":32,"y":21.24,"z":7.69},"H3":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":32,"y":12.24,"z":7.69},"A4":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":41,"y":75.24,"z":7.69},"B4":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":41,"y":66.24,"z":7.69},"C4":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":41,"y":57.24,"z":7.69},"D4":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":41,"y":48.24,"z":7.69},"E4":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":41,"y":39.24,"z":7.69},"F4":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":41,"y":30.24,"z":7.69},"G4":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":41,"y":21.24,"z":7.69},"H4":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":41,"y":12.24,"z":7.69},"A5":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":50,"y":75.24,"z":7.69},"B5":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":50,"y":66.24,"z":7.69},"C5":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":50,"y":57.24,"z":7.69},"D5":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":50,"y":48.24,"z":7.69},"E5":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":50,"y":39.24,"z":7.69},"F5":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":50,"y":30.24,"z":7.69},"G5":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":50,"y":21.24,"z":7.69},"H5":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":50,"y":12.24,"z":7.69},"A6":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":59,"y":75.24,"z":7.69},"B6":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":59,"y":66.24,"z":7.69},"C6":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":59,"y":57.24,"z":7.69},"D6":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":59,"y":48.24,"z":7.69},"E6":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":59,"y":39.24,"z":7.69},"F6":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":59,"y":30.24,"z":7.69},"G6":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":59,"y":21.24,"z":7.69},"H6":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":59,"y":12.24,"z":7.69},"A7":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":68,"y":75.24,"z":7.69},"B7":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":68,"y":66.24,"z":7.69},"C7":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":68,"y":57.24,"z":7.69},"D7":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":68,"y":48.24,"z":7.69},"E7":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":68,"y":39.24,"z":7.69},"F7":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":68,"y":30.24,"z":7.69},"G7":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":68,"y":21.24,"z":7.69},"H7":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":68,"y":12.24,"z":7.69},"A8":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":77,"y":75.24,"z":7.69},"B8":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":77,"y":66.24,"z":7.69},"C8":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":77,"y":57.24,"z":7.69},"D8":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":77,"y":48.24,"z":7.69},"E8":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":77,"y":39.24,"z":7.69},"F8":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":77,"y":30.24,"z":7.69},"G8":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":77,"y":21.24,"z":7.69},"H8":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":77,"y":12.24,"z":7.69},"A9":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":86,"y":75.24,"z":7.69},"B9":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":86,"y":66.24,"z":7.69},"C9":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":86,"y":57.24,"z":7.69},"D9":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":86,"y":48.24,"z":7.69},"E9":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":86,"y":39.24,"z":7.69},"F9":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":86,"y":30.24,"z":7.69},"G9":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":86,"y":21.24,"z":7.69},"H9":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":86,"y":12.24,"z":7.69},"A10":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":95,"y":75.24,"z":7.69},"B10":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":95,"y":66.24,"z":7.69},"C10":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":95,"y":57.24,"z":7.69},"D10":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":95,"y":48.24,"z":7.69},"E10":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":95,"y":39.24,"z":7.69},"F10":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":95,"y":30.24,"z":7.69},"G10":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":95,"y":21.24,"z":7.69},"H10":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":95,"y":12.24,"z":7.69},"A11":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":104,"y":75.24,"z":7.69},"B11":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":104,"y":66.24,"z":7.69},"C11":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":104,"y":57.24,"z":7.69},"D11":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":104,"y":48.24,"z":7.69},"E11":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":104,"y":39.24,"z":7.69},"F11":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":104,"y":30.24,"z":7.69},"G11":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":104,"y":21.24,"z":7.69},"H11":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":104,"y":12.24,"z":7.69},"A12":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":113,"y":75.24,"z":7.69},"B12":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":113,"y":66.24,"z":7.69},"C12":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":113,"y":57.24,"z":7.69},"D12":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":113,"y":48.24,"z":7.69},"E12":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":113,"y":39.24,"z":7.69},"F12":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":113,"y":30.24,"z":7.69},"G12":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":113,"y":21.24,"z":7.69},"H12":{"depth":14.81,"totalLiquidVolume":200,"shape":"circular","diameter":5.46,"x":113,"y":12.24,"z":7.69}},"groups":[{"metadata":{"wellBottomShape":"v"},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"biorad_qpcr_plate_nioz_plateholder"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}"""
LABWARE_DEF = json.loads(LABWARE_DEF_JSON)
LABWARE_LABEL = LABWARE_DEF.get('metadata', {}).get(
    'displayName', 'test labware')
LABWARE_DIMENSIONS = LABWARE_DEF.get('wells', {}).get('A1', {}).get('yDimension')

metadata = {'apiLevel': '2.0'}


def run(protocol: protocol_api.ProtocolContext):
    tiprack = protocol.load_labware(TIPRACK_LOADNAME, TIPRACK_SLOT)
    pipette = protocol.load_instrument(
        PIPETTE_NAME, PIPETTE_MOUNT, tip_racks=[tiprack])

    test_labware = protocol.load_labware_from_definition(
        LABWARE_DEF,
        TEST_LABWARE_SLOT,
        LABWARE_LABEL,
    )

    num_cols = len(LABWARE_DEF.get('ordering', [[]]))
    num_rows = len(LABWARE_DEF.get('ordering', [[]])[0])
    total = num_cols * num_rows
    pipette.pick_up_tip()

    def set_speeds(rate):
        protocol.max_speeds.update({
            'X': (600 * rate),
            'Y': (400 * rate),
            'Z': (125 * rate),
            'A': (125 * rate),
        })

        speed_max = max(protocol.max_speeds.values())

        for instr in protocol.loaded_instruments.values():
            instr.default_speed = speed_max

    set_speeds(RATE)

    pipette.home()
    if(PIPETTE_NAME == 'p20_single_gen2' or PIPETTE_NAME == 'p300_single_gen2' or PIPETTE_NAME == 'p1000_single_gen2' or PIPETTE_NAME == 'p50_single' or PIPETTE_NAME == 'p10_single' or PIPETTE_NAME == 'p300_single' or PIPETTE_NAME == 'p1000_single'):
        if(total > 1):
            #testing with single channel
            well = test_labware.well('A1')
            all_4_edges = [
                [well._from_center_cartesian(x=-1, y=0, z=1), 'left'],
                [well._from_center_cartesian(x=1, y=0, z=1), 'right'],
                [well._from_center_cartesian(x=0, y=-1, z=1), 'front'],
                [well._from_center_cartesian(x=0, y=1, z=1), 'back']
            ]

            set_speeds(RATE)
            pipette.move_to(well.top())
            protocol.pause("If the position is accurate click 'resume.'")

            for edge_pos, edge_name in all_4_edges:
                set_speeds(RATE)
                edge_location = types.Location(point=edge_pos, labware=None)
                pipette.move_to(edge_location)
                protocol.pause("If the position is accurate click 'resume.'")
            
            #last well testing
            last_well = (num_cols) * (num_rows)
            well = test_labware.well(last_well-1)
            all_4_edges = [
                [well._from_center_cartesian(x=-1, y=0, z=1), 'left'],
                [well._from_center_cartesian(x=1, y=0, z=1), 'right'],
                [well._from_center_cartesian(x=0, y=-1, z=1), 'front'],
                [well._from_center_cartesian(x=0, y=1, z=1), 'back']
            ]
            for edge_pos, edge_name in all_4_edges:
                set_speeds(RATE)
                edge_location = types.Location(point=edge_pos, labware=None)
                pipette.move_to(edge_location)
                protocol.pause("If the position is accurate click 'resume.'")
            set_speeds(RATE)
            #test bottom of last well
            pipette.move_to(well.bottom())
            protocol.pause("If the position is accurate click 'resume.'")
            pipette.blow_out(well)
        else:
            #testing with single channel + 1 well labware
            well = test_labware.well('A1')
            all_4_edges = [
                [well._from_center_cartesian(x=-1, y=0, z=1), 'left'],
                [well._from_center_cartesian(x=1, y=0, z=1), 'right'],
                [well._from_center_cartesian(x=0, y=-1, z=1), 'front'],
                [well._from_center_cartesian(x=0, y=1, z=1), 'back']
            ]

            set_speeds(RATE)
            pipette.move_to(well.top())
            protocol.pause("If the position is accurate click 'resume.'")

            for edge_pos, edge_name in all_4_edges:
                set_speeds(RATE)
                edge_location = types.Location(point=edge_pos, labware=None)
                pipette.move_to(edge_location)
                protocol.pause("If the position is accurate click 'resume.'")
            
            #test bottom of first well
            well = test_labware.well('A1')
            pipette.move_to(well.bottom())
            protocol.pause("If the position is accurate click 'resume.'")
            pipette.blow_out(well)
    else:
        #testing for multichannel
        if(total == 96 or total == 384): #testing for 96 well plates and 384 first column
            #test first column
            well = test_labware.well('A1')
            all_4_edges = [
                [well._from_center_cartesian(x=-1, y=0, z=1), 'left'],
                [well._from_center_cartesian(x=1, y=0, z=1), 'right'],
                [well._from_center_cartesian(x=0, y=-1, z=1), 'front'],
                [well._from_center_cartesian(x=0, y=1, z=1), 'back']
            ]
            set_speeds(RATE)
            pipette.move_to(well.top())
            protocol.pause("If the position is accurate click 'resume.'")

            for edge_pos, edge_name in all_4_edges:
                set_speeds(RATE)
                edge_location = types.Location(point=edge_pos, labware=None)
                pipette.move_to(edge_location)
                protocol.pause("If the position is accurate click 'resume.'")
            
            #test last column
            if(total == 96):
                last_col = (num_cols * num_rows) - num_rows
                well = test_labware.well(last_col)
                all_4_edges = [
                    [well._from_center_cartesian(x=-1, y=0, z=1), 'left'],
                    [well._from_center_cartesian(x=1, y=0, z=1), 'right'],
                    [well._from_center_cartesian(x=0, y=-1, z=1), 'front'],
                    [well._from_center_cartesian(x=0, y=1, z=1), 'back']
                ]
                for edge_pos, edge_name in all_4_edges:
                    set_speeds(RATE)
                    edge_location = types.Location(point=edge_pos, labware=None)
                    pipette.move_to(edge_location)
                    protocol.pause("If the position is accurate click 'resume.'")
                set_speeds(RATE)
                #test bottom of last column
                pipette.move_to(well.bottom())
                protocol.pause("If the position is accurate click 'resume.'")
                pipette.blow_out(well)
            elif(total == 384):
                #testing for 384 well plates - need to hit well 369, last column
                well369 = (total) - (num_rows) + 1
                well = test_labware.well(well369)
                pipette.move_to(well.top())
                protocol.pause("If the position is accurate click 'resume.'")
                all_4_edges = [
                    [well._from_center_cartesian(x=-1, y=0, z=1), 'left'],
                    [well._from_center_cartesian(x=1, y=0, z=1), 'right'],
                    [well._from_center_cartesian(x=0, y=-1, z=1), 'front'],
                    [well._from_center_cartesian(x=0, y=1, z=1), 'back']
                ]
                for edge_pos, edge_name in all_4_edges:
                    set_speeds(RATE)
                    edge_location = types.Location(point=edge_pos, labware=None)
                    pipette.move_to(edge_location)
                    protocol.pause("If the position is accurate click 'resume.'")
                set_speeds(RATE)
                #test bottom of last column
                pipette.move_to(well.bottom())
                protocol.pause("If the position is accurate click 'resume.'")
                pipette.blow_out(well)
        elif(num_rows == 1 and total > 1 and LABWARE_DIMENSIONS >= 71.2):
            #for 1 row reservoirs - ex: 12 well reservoirs
            well = test_labware.well('A1')
            all_4_edges = [
                [well._from_center_cartesian(x=-1, y=1, z=1), 'left'],
                [well._from_center_cartesian(x=1, y=1, z=1), 'right'],
                [well._from_center_cartesian(x=0, y=0.75, z=1), 'front'],
                [well._from_center_cartesian(x=0, y=1, z=1), 'back']
            ]
            set_speeds(RATE)
            pipette.move_to(well.top())
            protocol.pause("If the position is accurate click 'resume.'")

            for edge_pos, edge_name in all_4_edges:
                set_speeds(RATE)
                edge_location = types.Location(point=edge_pos, labware=None)
                pipette.move_to(edge_location)
                protocol.pause("If the position is accurate click 'resume.'")
            #test last well
            well = test_labware.well(-1)
            all_4_edges = [
                [well._from_center_cartesian(x=-1, y=1, z=1), 'left'],
                [well._from_center_cartesian(x=1, y=1, z=1), 'right'],
                [well._from_center_cartesian(x=0, y=0.75, z=1), 'front'],
                [well._from_center_cartesian(x=0, y=1, z=1), 'back']
            ]
            set_speeds(RATE)

            for edge_pos, edge_name in all_4_edges:
                set_speeds(RATE)
                edge_location = types.Location(point=edge_pos, labware=None)
                pipette.move_to(edge_location)
                protocol.pause("If the position is accurate click 'resume.'")
                #test bottom of first well
            pipette.move_to(well.bottom())
            protocol.pause("If the position is accurate click 'resume.'")
            pipette.blow_out(well)

        
        elif(total == 1 and LABWARE_DIMENSIONS >= 71.2 ):
            #for 1 well reservoirs
            well = test_labware.well('A1')
            all_4_edges = [
                [well._from_center_cartesian(x=-1, y=1, z=1), 'left'],
                [well._from_center_cartesian(x=1, y=1, z=1), 'right'],
                [well._from_center_cartesian(x=0, y=0.75, z=1), 'front'],
                [well._from_center_cartesian(x=0, y=1, z=1), 'back']
            ]
            set_speeds(RATE)
            pipette.move_to(well.top())
            protocol.pause("If the position is accurate click 'resume.'")

            for edge_pos, edge_name in all_4_edges:
                set_speeds(RATE)
                edge_location = types.Location(point=edge_pos, labware=None)
                pipette.move_to(edge_location)
                protocol.pause("If the position is accurate click 'resume.'")
                #test bottom of first well
            pipette.move_to(well.bottom())
            protocol.pause("If the position is accurate click 'resume.'")
            pipette.blow_out(well)
        
        else:
            #for incompatible labwares
            protocol.pause("labware is incompatible to calibrate with a multichannel pipette")




    set_speeds(1.0)
    pipette.return_tip()