import unittest
import schemdraw
import schemdraw.elements as elm


class UnitTestsECDBrevetUS5149407WaterElectrolyzer(unittest.TestCase):
    # A simplified figure of the patent
    def test_electronic_circuit_diagram_v1(self):
        print("test_electronic_circuit_diagram_v1")

        d = schemdraw.Drawing()

        # Ground
        d.add(G := elm.Ground())
        d += (G_D := elm.Dot())

        # Alterning voltage source
        d.add(V1 := elm.SourceSin().up().label(['-', 'O to 230 V AC \n 60 Hz', '+']))
        d += (E_V1_D := elm.Dot())

        # Lines for linking the neon transformer
        d.add(L_B_NT_A_V1 := elm.Line().at(E_V1_D.end).right())
        d.add(E_L_B_NT_A_V1_D := elm.Dot())

        d.add(L_B_NT_A_G := elm.Line().at(G.end).right())
        d.add(E_L_B_NT_A_G_D := elm.Dot())

        # Transformer
        d.add(neon_transformer := elm.Transformer(t1=5, t2=10).label('Transformer'))
        d.add(elm.Line().at(E_L_B_NT_A_V1_D.end).down().toy(neon_transformer.p1))
        d.add(elm.Line().at(neon_transformer.s1).right())
        d.add(E_L_NT_S1_D := elm.Dot())
        d.add(elm.Line().at(neon_transformer.s2).down())
        d.add(elm.Line().right())
        d.add(E_L_NT_S2_D := elm.Dot())

        # Bridge rectifier
        # Diode 1 of the bridge rectifier
        d += (D1 := elm.Diode().theta(90).label('D1').at(E_L_NT_S1_D.end).down().reverse())
        d.add(E_D1_D := elm.Dot().label('DC +', loc="left"))
        d.add(elm.Line().length(d.unit/4).right())
        d.add(elm.Line().length(d.unit / 1.3).up())
        d.add(elm.Line().length(2 * d.unit).right().label('Full \n wave', halign='left'))
        d.add(E_L_D1_1_D := elm.Dot())
        d.add(elm.Line().at(E_L_NT_S1_D.end).right())
        d.add(E_L_D1_D := elm.Dot())

        # Diode 2 of the bridge rectifier
        d += (D2 := elm.Diode().theta(90).label('D2').endpoints(E_D1_D.end, E_L_NT_S2_D.end).down())
        d += (E_D2_D := elm.Dot())
        d.add(elm.Line().at(E_D2_D.end).right())
        d.add(E_L_D2_D := elm.Dot())

        # Diode 3 of the bridge rectifier
        d += (D3 := elm.Diode().theta(90).label('D3').at(E_L_D1_D.end).down())
        d += (E_D3_D := elm.Dot().label('DC -', loc="left"))
        d += elm.Ground().theta(90)

        # Diode 4 of the bridge rectifier
        d += (D4 := elm.Diode().theta(90).label('D4').endpoints(E_D3_D.end, E_L_D2_D.end).down().reverse())
        d += (E_D4_D := elm.Dot())

        # Resistor
        d.add(R1 := elm.ResistorIEEE().at(E_L_D1_1_D.end).label('R1', loc="top").down())
        d.add(elm.Line().length(d.unit / 4).right())
        d.add(elm.Line().length(d.unit / 4).down())
        d.add(E_R1_D := elm.Dot())

        # Transistor
        d.add(elm.Line().at(E_L_D1_1_D.end).right())
        d.add(T1 := elm.BjtNpn(circle=True).anchor('collector').label('T1', loc='right').up())

        # Optocoupler
        d.add(O1 := elm.compound.Optocoupler().label('O1', loc='right').at(E_R1_D.end).anchor('collector'))
        d.add(elm.Line().length(d.unit / 4).at(O1.emitter))
        d.add(elm.Line().length(d.unit / 2).right())
        d.add(E_O1_E_D := elm.Dot())
        d.add(elm.Line().up().toy(T1.base))
        d.add(VGTPI := elm.SourcePulse().label('Signal \n generator \n HF', loc='top').at(O1.anode).down().reverse())
        d.add(elm.Ground())
        d.add(elm.Ground().at(O1.cathode).down().right())

        # Main transformer
        d.add(elm.Line().at(T1.emitter).right().label("Half \n full \n wave"))
        d.add(E_T1_D := elm.Dot())
        d.add(main_transformer := elm.Transformer(t1=5, t2=10).label('Main \n transformer').at(E_T1_D.end).anchor('p1'))
        d.add(elm.Ground().at(main_transformer.p2))
        d.add(elm.Line().at(main_transformer.s1))
        d.add(E_MT_S1_D := elm.Dot())
        d.add(elm.Line().at(main_transformer.s2))
        d.add(E_MT_S2_D := elm.Dot())

        # Blocking Diode
        d.add(BD := elm.Diode().at(E_MT_S1_D.end).label("Blocking \n diode"))
        d.add(E_BD_D := elm.Dot())

        # Inductor (Resonant charging choke)
        d.add(RCC := elm.Inductor2().at(E_BD_D.end).label("Resonant \n charging \n choke"))
        d.add(E_RCC_D := elm.Dot())

        # Capacitor (Gas resonant cavity)
        d.add(GRC := elm.Capacitor().at(E_RCC_D.end).label("Gas \n resonant \n cavity", loc='bottom').down())
        d.add(E_GRC_D := elm.Dot())
        d.add(elm.Line().length(d.unit / 3).down())

        # Inductor (Variable inductor)
        d.add(VI := elm.Inductor2().label("Variable \n inductor", loc='bottom').left())
        d.add(elm.Line().endpoints(VI.end, E_MT_S2_D.end))

        d.save("ecd_brevet_us_5149407_water_electrolyzer.svg")
        d.save("ecd_brevet_us_5149407_water_electrolyzer.png")
        d.draw()


if __name__ == '__main__':
    unittest.main()
