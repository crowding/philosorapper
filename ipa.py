### Routines for unpacking ASCII-formatted IPA into a more expansive
### format.

### This parses the format described here:
### http://www.hpl.hp.com/personal/Evan_Kirshenbaum/IPA/faq.html

import re

# These are the features a segment can have, and their abbreviations.
features = {}
features["nas"] = nas = "nasal"
features["orl"] = orl = "oral"
features["apr"] = apr = "approximant"
features["vwl"] = vwl = "vowel"
features["lat"] = lat = "lateral"
features["ctl"] = ctl = "central"
features["trl"] = trl = "trill"
features["flp"] = flp = "flap"
features["clk"] = clk = "click"
features["ejc"] = ejc = "ejective"
features["imp"] = imp = "implosive"
features["hgh"] = hgh = "high"
features["smh"] = smh = "semi-high"
features["umd"] = umd = "upper-mid"
features["mid"] = mid = "mid"
features["lmd"] = lmd = "lower-mid"
features["low"] = low = "low"
features["vcd"] = vcd = "voiced"
features["vls"] = vls = "voiceless"
features["blb"] = blb = "bilabial"
features["lbd"] = lbd = "labio-dental"
features["dnt"] = dnt = "dental"
features["alv"] = alv = "alveolar"
features["rfx"] = rfx = "retroflex"
features["pla"] = pla = "palato-alveolar"
features["pal"] = pal = "palatal"
features["vel"] = vel = "velar"
features["lbv"] = lbv = "labio-velar"
features["uvl"] = uvl = "uvular"
features["phr"] = phr = "pharyngeal"
features["glt"] = glt = "glottal"
features["stp"] = stp = "stop"
features["frc"] = frc = "fricative"
features["fnt"] = fnt = "front"
features["cnt"] = cnt = "center"
features["bck"] = bck = "back"
features["unr"] = unr = "unrounded"
features["rnd"] = rnd = "rounded"
features["asp"] = asp = "aspirated"
features["unx"] = unx = "unexploded"
features["syl"] = syl = "syllabic"
features["mrm"] = mrm = "murmured"
features["lng"] = lng = "long"
features["vzd"] = vzd = "velarized"
features["lzd"] = lzd = "labialized"
features["pzd"] = pzd = "palatalized"
features["rzd"] = rzd = "rhoticized"
features["nzd"] = nzd = "nasalized"
features["fzd"] = fzd = "pharyngealized"

features["word"] = word = "word-start"
features["line"] = line = "line-start"
features["wend"] = wend = "word-end"
features["lend"] = lend = "line-end"
features["s1"] = s1 = "primary-stress"
features["s2"] = s2 = "secondary-stress"
features["t1"] = t1 = "tone-1"
features["t2"] = t2 = "tone-2"
features["t3"] = t3 = "tone-3"
features["t4"] = t4 = "tone-4"


### Kirshenbaum IPA has both leftward and rightward binding modifiers, so you
### need a flip flop.
class NewSegment(Exception):
    # this exception is raised when the existing segment needs to be cleared
    # and a new one readied; new_segment is the new segment
    def __init__(self, new_segment):
        Exception.__init__(self)
        self.new_segment = new_segment
    pass

class SkipRecordingIpa(Exception):
    pass

class Segment(set):
    def __init__(self, init, ipa = '', seg = False):
        set.__init__(self, init)
        #The "seg" flag is false if we have not seen the
        #segment yet (and are accepting punctuation) and is true
        #of we have seen the segment (and are accepting
        #diacritics)
        self.seg = seg
        self.ipa = ipa

    def punctuate(self, feat,  remove=None):
        if self.seg:
            raise NewSegment(Segment(feat))
        else:
            self.update(feat)

    def segment(self, feat, remove=None):
        print("Segment {}".format(feat))
        if self.seg:
            raise NewSegment(Segment(feat, seg=True))
        else:
            self.update(feat)
            self.seg = True

    def diacriticize(self, feat, remove=None):
        if self.seg:
            self.update(feat)
        else:
            raise ValueError("Not expecting a diacritic before a segment")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{0}({{{1}}}, ipa={2!r})'.format(
            "Segment",
            ", ".join("{!r}".format(i) for i in self),
            self.ipa)

def to_segments(ipa):
    """Convert a Kirshembaum IPA string to a sequence of segments (phonemes).
    Each segment is a set of flags. For instance the "a" in "tag"
    may be represented a_chs set(["low", "front", "long", "unrounded", "vowel"]).
    The full set of features is given by the dictionary ipa.features.
    Argument is a string, or a generator that produces one char at a time.
    Result is a generator of segments.
    """

    seg = Segment({line, word})
    chars = iter(ipa)
    for i in chars:
        try:
            try:
                lut[i](seg, chars)
            except NewSegment as new: #need to output the current segment
                print("Emitted {}".format(seg))
                yield seg
                seg = new.new_segment
            seg.ipa = seg.ipa + i
        except SkipRecordingIpa:
            pass
    if seg.seg:
        seg.diacriticize({wend, lend})
        yield seg

### Many single characters refer to the most common segments.

def segment(feats):
    def apply(segment, _chars):
        segment.segment(feats)
    return apply

lut = {}
lut['&'] = segment({low,fnt,unr,vwl})
lut['*'] = segment({vcd,alv,flp})
lut['?'] = segment({glt,stp})
lut['@'] = segment({mid,cnt,unr,vwl})
lut['A'] = segment({low,bck,unr,vwl})
lut['B'] = segment({vcd,blb,frc})
lut['C'] = segment({vls,pal,frc})
lut['D'] = segment({vcd,dnt,frc})
lut['E'] = segment({lmd,fnt,unr,vwl})
lut['G'] = segment({vcd,uvl,stp})
lut['H'] = segment({vls,phr,frc})
lut['I'] = segment({smh,fnt,unr,vwl})
lut['J'] = segment({vcd,pal,stp})
lut['L'] = segment({vcd,vel,lat})
lut['M'] = segment({lbd,nas})
lut['N'] = segment({vel,nas})
lut['O'] = segment({lmd,bck,rnd,vwl})
lut['P'] = segment({vls,blb,frc})
lut['Q'] = segment({vcd,vel,frc})
lut['R'] = segment({mid,cnt,rzd,vwl})
lut['S'] = segment({vls,pla,frc})
lut['T'] = segment({vls,dnt,frc})
lut['U'] = segment({smh,bck,rnd,vwl})
lut['V'] = segment({lmd,bck,unr,vwl})
lut['W'] = segment({lmd,fnt,rnd,vwl})
lut['X'] = segment({vls,uvl,frc})
lut['Y'] = segment({umd,fnt,rnd,vwl})
lut['Z'] = segment({vcd,pla,frc})
lut['a'] = segment({low,cnt,unr,vwl})
lut['b'] = segment({vcd,blb,stp})
lut['c'] = segment({vls,pal,stp})
lut['d'] = segment({vcd,alv,stp})
lut['e'] = segment({umd,fnt,rnd,vwl})
lut['f'] = segment({vls,lbd,frc})
lut['g'] = segment({vcd,vel,stp})
lut['h'] = segment({glt,apr})
lut['i'] = segment({hgh,fnt,unr,vwl})
lut['j'] = segment({pal,apr}) # /{vcd,pal,frc}
lut['k'] = segment({vls,vel,stp})
lut['l'] = segment({vcd,alv,lat})
lut['m'] = segment({blb,nas})
lut['n'] = segment({alv,nas})
lut['o'] = segment({umd,bck,rnd,vwl})
lut['p'] = segment({vls,blb,stp})
lut['q'] = segment({vls,uvl,stp})
lut['r'] = segment({alv,apr})
lut['s'] = segment({vls,alv,frc})
lut['t'] = segment({vls,alv,stp})
lut['u'] = segment({hgh,bck,rnd,vwl})
lut['v'] = segment({vcd,lbd,frc})
lut['w'] = segment({lbv,apr}) # /{vcd,lbv,frc}
lut['x'] = segment({vls,vel,frc})
lut['y'] = segment({hgh,fnt,rnd,vwl})
lut['z'] = segment({vcd,alv,frc})

### Diacritics modify the preceding segment by adding or removing features.

def diacritic(when_consonant, when_vowel=None,
              remove_when_consonant=[], remove_when_vowel=[]):

    if when_vowel is None:
        when_vowel = when_consonant

    def apply(seg, _chars):
        if vwl in seg:
            seg.diacriticize(when_vowel, remove_when_vowel)
        else:
            seg.diacriticize(when_consonant, remove_when_consonant)

    return apply

## A special lookuptable applies to diacritics delimited with <>.
## It has all the feature abbreviations plus k:v.
diacritic_lut = {k:diacritic({v}) for (k,v) in features.items()}

diacritic_lut['!'] = lut['!'] = diacritic({clk})
diacritic_lut[':'] = lut[':'] = diacritic({lng})
diacritic_lut[';'] = lut[';'] = diacritic({pzd})
diacritic_lut['['] = lut['['] = diacritic({dnt})
diacritic_lut['^'] = lut['^'] = diacritic({pal})

# Some diacritics mean different things following vowels and consonants
diacritic_lut['"'] = lut['"'] = diacritic({cnt}, {uvl})
diacritic_lut['-'] = lut['-'] = diacritic({unr}, {syl}, {rnd}, {})
diacritic_lut['.'] = lut['.'] = diacritic({rnd}, {rfx}, {unr}, {})
diacritic_lut['~'] = lut['~'] = diacritic({nzd}, {vzd})

## backtick means different things to voiced and unvoiced segments
def backtick(seg, _chars):
    if vcd in seg:
        seg.diacriticize({imp})
    else:
        seg.diacriticize({ejc})

lut['`'] = backtick

### Punctuations modify the _following_ segments, as opposed to diacritics which
### modify preceding.

def punctuation(feats):
    def apply(seg, _chars):
        seg.punctuate(feats)
    return apply

lut['#'] = punctuation({}) # syllable boundary...
lut['\''] = punctuation({s1})
lut[','] = punctuation({s2})
lut['/'] = punctuation({})
lut['1'] = punctuation({t1})
lut['2'] = punctuation({t2})
lut['3'] = punctuation({t3})
lut['4'] = punctuation({t4})


#I'm making space and newline act as both diacritic and punctuation
#(since word/line endings are probably important enough to recoird directly)

def space(seg, _chars):
    if seg.seg:
        seg.diacriticize({wend})
        raise NewSegment(Segment({word}))
    else:
        seg.punctuate({word})

def newline(seg, _chars):
    if seg.seg:
        seg.diacriticize({wend, lend})
        raise NewSegment(Segment({word, line}))
    else:
        seg.punctuate({word, line})

lut[' '] = space
lut['\n'] = newline

### These are special explicit diacritics (overriding earlier)

diacritic_lut['?'] = diacritic({mrm})
diacritic_lut['H'] = diacritic({fzd})
diacritic_lut['h'] = diacritic({asp})
diacritic_lut['j'] = diacritic({pzd})
diacritic_lut['o'] = diacritic({unx})
diacritic_lut['r'] = diacritic({rzd})
diacritic_lut['w'] = diacritic({lzd})

def until(gen, delimiter):
    """Yield from generator items up to delimiter (which is swallowed)."""
    for x in gen:
        if x == delimiter:
            return
        else:
            yield x

def explicit_diacritic(segment, characters):
    contents = ''.join(until(characters, '>'))
    things = re.split(",", contents)
    [diacritic_lut[thing](segment, characters) for thing in things]
    raise SkipRecordingIpa

lut['<'] = explicit_diacritic

### Explicit segments have a set of feature abbreviations delimited by {}.

def explicit_segment(segment, characters):
    contents = ''.join(until(characters,'}'))
    things = re.split(",", contents)
    feats = [features[thing] for thing in things]
    segment.segment(feats)
    segment.ipa = segment.ipa + "{" + contents + "}"
    raise SkipRecordingIpa

lut['{'] = explicit_segment
