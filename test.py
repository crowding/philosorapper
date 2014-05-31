import ipa

#Test the Kirshenbaum-IPA parser

class TestKirshenbaum:
    def test_simple(self):
        tag = list(ipa.to_segments("t&g"))
        assert tag[0] == {'line-start', 'word-start',
                          'voiceless', 'alveolar', 'stop'}
        assert tag[1] == {'unrounded', 'front', 'low', 'vowel'}
        assert tag[2] == {'voiced', 'velar', 'stop', 'word-end', 'line-end'}

    def test_diacritic(self):
        tag = list(ipa.to_segments("t&:g"))
        assert tag[1] == {'unrounded', 'front', 'low', 'vowel', 'long'}
        assert tag[1].ipa == "&:"

    def test_punctuation(self):
        phrase = list(ipa.to_segments("aI hir D@ 'sEkrI,t&ri"))
        assert "word-end" in phrase[1]
        assert "word-start" in phrase[2]
        assert "primary-stress" in phrase[7]
        assert "secondary-stress" in phrase[12]

    def test_delimited_diacritic(self):
        tag = list(ipa.to_segments("t<h>&<:>g<o>"))
        assert tag[0].issuperset(
            {'voiceless', 'aspirated', 'alveolar', 'stop'})
        assert tag[1].issuperset(
            {'unrounded', 'front', 'long', 'low', 'vowel'})
        assert tag[2].issuperset(
            {'unexploded', 'voiced', 'velar', 'stop'})

    def test_explicit_diacritic(self):
        tag = list(ipa.to_segments("t<asp>&<lng>g<unx,asp>"))
        assert tag[0].issuperset(
            {'voiceless', 'aspirated', 'alveolar', 'stop'})
        assert tag[1].issuperset(
            {'unrounded', 'front', 'long', 'low', 'vowel'})
        assert tag[2].issuperset(
            {'unexploded', 'voiced', 'velar', 'aspirated', 'stop'})

    def test_explicit_segment(self):
        tag = list(ipa.to_segments("{vls,alv,stp}{low,fnt,unr,vwl}{vcd,vel,stp}"))
        assert tag[2].issuperset(
            {'voiced', 'velar', 'stop'})
        assert tag[2].ipa == "{vcd,vel,stp}"
