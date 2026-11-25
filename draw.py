from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# A restrained broadsheet palette: warm newsprint, near-black ink, and signal red.
W = H = 1024
PAPER = (244, 240, 229)
INK = (24, 27, 28)
RED = (190, 47, 39)
MUTED = (104, 104, 96)
RULE = (192, 185, 169)
WHITE = (250, 248, 241)

im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)
font_dir = '/usr/share/fonts/truetype/dejavu'
def font(name, size):
    return ImageFont.truetype(f'{font_dir}/{name}.ttf', size)

SERIF = 'DejaVuSerif-Bold'
SANS = 'DejaVuSans'
SANS_B = 'DejaVuSans-Bold'

def txt(x, y, s, size, fill=INK, face=SANS_B, anchor=None):
    d.text((x, y), s, font=font(face, size), fill=fill, anchor=anchor)

def line(points, fill=INK, width=2):
    d.line(points, fill=fill, width=width)

def panel(box, number, category, headline, detail, headline_size=19):
    x0,y0,x1,y1=box
    d.rectangle(box, fill=WHITE, outline=INK, width=2)
    d.rectangle((x0,y0,x1,y0+7), fill=RED)
    txt(x0+14,y0+14, f'{number:02d}  /  {category}', 11, RED, SANS_B)
    available=x1-x0-28
    hs=headline_size
    while hs>10 and font(SANS_B,hs).getlength(headline)>available: hs-=1
    txt(x0+14,y0+34, headline, hs, INK, SANS_B)
    # Keep every caption within its panel while preserving the smallest readable size.
    ds=12
    while ds>9 and font(SANS,ds).getlength(detail)>available: ds-=1
    txt(x0+14,y1-26,detail,ds,MUTED,SANS)

# Masthead and date: oversized, high-contrast and unmistakable.
d.rectangle((0,0,W,11), fill=RED)
txt(34,22,'THE WORLD',48,INK,SERIF)
txt(36,78,'GLOBAL NEWS  /  THE MONDAY EDITION',12,MUTED,SANS_B)
d.rectangle((32,108,992,177), fill=INK)
txt(48,119,'MONDAY',15,(238,232,217),SANS_B)
txt(159,112,'24 NOVEMBER 2026',42,WHITE,SANS_B)
txt(967,133,'01',18,RED,SANS_B,anchor='ra')
line([(32,190),(992,190)],INK,3)

# Panel geometry: two lead stories, a full-width Ukraine report, and two closing briefs.
# 1 Iran / US diplomacy and blockade
b1=(32,204,620,447)
panel(b1,1,'IRAN / UNITED STATES','VANCE & RUBIO MEET QATAR PM','WHITE HOUSE TALKS AS IRAN VOWS TO FIGHT NAVAL BLOCKADE',18)
# diplomatic table / White House columns
# muted globe/map disk
d.ellipse((475,258,590,373), fill=(232,228,216), outline=RULE, width=2)
# simplified Gulf/West Asia map silhouette
poly=[(503,278),(525,267),(542,273),(548,287),(562,293),(554,305),(564,319),(548,328),(541,345),(526,337),(517,321),(501,315),(495,299)]
d.polygon(poly,fill=(201,194,177))
# Qatar marker and route
for cx,cy in [(536,317),(521,302)]: d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=RED)
d.arc((510,281,557,331),200,335,fill=RED,width=3)
# three flags + conference table
# US flag
fx,fy=65,281
d.rectangle((fx,fy,fx+82,fy+46),fill=WHITE,outline=RULE,width=1)
for k in range(6): d.rectangle((fx,fy+k*7,fx+82,fy+k*7+3),fill=RED)
d.rectangle((fx,fy,fx+34,fy+24),fill=(43,67,105))
for sx,sy in [(6,5),(15,5),(24,5),(10,13),(20,13),(6,20),(15,20),(24,20)]: d.ellipse((fx+sx,fy+sy,fx+sx+2,fy+sy+2),fill=WHITE)
# Qatar flag
qx=166
d.rectangle((qx,fy,qx+82,fy+46),fill=(121,35,58),outline=RULE,width=1)
d.rectangle((qx,fy,qx+27,fy+46),fill=WHITE)
for yy in range(fy+2,fy+46,8): d.polygon([(qx+27,yy),(qx+36,yy+4),(qx+27,yy+8)],fill=WHITE)
# Iran flag
ix=267
d.rectangle((ix,fy,ix+82,fy+46),fill=WHITE,outline=RULE,width=1)
d.rectangle((ix,fy,ix+82,fy+15),fill=(38,112,76)); d.rectangle((ix,fy+31,ix+82,fy+46),fill=(192,53,53))
d.rectangle((ix+36,fy+18,ix+45,fy+28),fill=RED)
# table and figures
d.rectangle((64,348,379,355),fill=INK)
for cx in [105,185,266,340]:
    d.ellipse((cx-8,326,cx+8,342),fill=(188,177,154)); d.rectangle((cx-11,341,cx+11,348),fill=(74,82,86))

# 2 Gaza
b2=(636,204,992,447)
panel(b2,2,'GAZA','STRIKES KILL HAMAS SECURITY CHIEF','NAEEM ABU NAHEL AND SIX OTHERS KILLED IN ISRAELI AIRSTRIKES',17)
# skyline in a dusk-toned inset
sx0,sy0,sx1,sy1=660,271,968,385
d.rectangle((sx0,sy0,sx1,sy1),fill=(226,222,210))
d.rectangle((sx0,sy1-24,sx1,sy1),fill=(90,87,80))
# buildings
for x,y,w,h in [(671,320,43,41),(716,301,37,60),(756,328,48,33),(809,291,51,70),(865,316,40,45),(911,302,45,59)]:
    d.rectangle((x,y,x+w,y+h),fill=(151,145,132))
    for wx in range(x+7,x+w-4,13):
        for wy in range(y+9,y+h-9,14): d.rectangle((wx,wy,wx+4,wy+5),fill=(226,218,195))
# impact plume, red alert mark
for cx,cy,r in [(827,286,17),(815,285,12),(838,280,13),(825,270,10)]: d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(178,169,151))
d.polygon([(821,276),(827,252),(832,276),(843,267),(836,282),(847,287),(831,286),(824,300),(824,285),(810,290)],fill=RED)

# 3 Ukraine, most detailed panel
b3=(32,463,992,742)
panel(b3,3,'UKRAINE','ZAPORIZHZHIA HIT — WARSHIP SUNK OFF LIBYA','RUSSIAN NIGHT STRIKE: 2 DEAD, 40 WOUNDED — INCLUDING 4 CHILDREN  /  GERMANY GETS DELTA ACCESS',18)
# left: city blocks and strike path
ux0,uy0=55,535
d.rectangle((ux0,uy0,ux0+325,uy0+157),fill=(229,226,216))
# skyline
for x,y,w,h in [(69,590,46,72),(120,566,54,96),(179,605,51,57),(238,550,61,112),(304,584,58,78)]:
    d.rectangle((x,y,x+w,y+h),fill=(119,126,127))
    for wx in range(x+8,x+w-5,14):
        for wy in range(y+10,y+h-7,17): d.rectangle((wx,wy,wx+5,wy+7),fill=(214,207,188))
# red blast and trajectory
d.ellipse((272,568,298,594),fill=RED)
line([(90,549),(174,530),(264,558)],RED,3)
d.polygon([(260,552),(274,558),(262,566)],fill=RED)
txt(69,673,'ZAPORIZHZHIA',11,INK,SANS_B)
# center: waves and warship off Libya
wx0=402
d.rectangle((wx0,535,679,692),fill=(231,228,218))
# horizon, waves
line([(wx0+8,603),(671,603)],(130,145,148),2)
for yy in [620,636,652,668]:
    for xx in range(wx0+8,670,46):
        line([(xx,yy),(xx+24,yy-3),(xx+40,yy)],(99,127,137),2)
# ship silhouette
ship=[(436,596),(637,596),(619,616),(469,616)]
d.polygon(ship,fill=INK)
d.rectangle((486,576,570,596),fill=INK); d.rectangle((516,562,552,576),fill=INK)
d.rectangle((531,550,535,562),fill=INK); line([(533,551),(548,557)],RED,2)
d.ellipse((591,584,600,593),fill=RED)
txt(424,673,'BLACK SEA  →  LIBYA',11,INK,SANS_B)
# right: Delta system access card
rx0=704
d.rectangle((rx0,535,968,692),fill=(232,228,216),outline=RULE,width=1)
txt(rx0+15,548,'DELTA',23,INK,SANS_B)
txt(rx0+15,577,'BATTLEFIELD SYSTEM',10,RED,SANS_B)
# network nodes over map-ish grid
for xx in range(rx0+19,rx0+248,38): line([(xx,606),(xx,665)],(199,194,181),1)
for yy in [607,625,643,661]: line([(rx0+14,yy),(rx0+250,yy)],(199,194,181),1)
for cx,cy in [(rx0+45,625),(rx0+86,644),(rx0+130,612),(rx0+172,636),(rx0+220,610)]:
    d.ellipse((cx-5,cy-5,cx+5,cy+5),fill=RED)
line([(rx0+45,625),(rx0+86,644),(rx0+130,612),(rx0+172,636),(rx0+220,610)],INK,2)
txt(rx0+15,671,'GERMANY FIRST TO GAIN ACCESS',10,INK,SANS_B)

# 4 NATO / space
b4=(32,758,503,992)
panel(b4,4,'NATO / SPACE','NATO BRACES FOR SPACE THREATS','RUTTE VOWS DEFENCE AS REPORTS FLAG RUSSIAN NUCLEAR-ARMED SATELLITE',16)
# star field, satellite, earth arc
# sparse stars
for x,y,r in [(79,830,2),(120,862,2),(212,823,2),(287,851,2),(441,821,2),(390,873,2),(146,824,1),(349,829,1)]: d.ellipse((x-r,y-r,x+r,y+r),fill=RED)
d.arc((58,847,465,1055),195,342,fill=(102,125,136),width=4)
# satellite central
cx,cy=275,855
d.rectangle((cx-18,cy-15,cx+18,cy+15),fill=INK)
d.rectangle((cx-9,cy-9,cx+9,cy+9),fill=(196,177,116))
d.polygon([(cx-18,cy-8),(cx-64,cy-22),(cx-59,cy+16),(cx-18,cy+8)],fill=(93,124,143),outline=INK)
d.polygon([(cx+18,cy-8),(cx+64,cy-22),(cx+59,cy+16),(cx+18,cy+8)],fill=(93,124,143),outline=INK)
for x in range(cx-56,cx-21,11): line([(x,cy-17),(x+3,cy+12)],(191,205,208),1)
for x in range(cx+25,cx+60,11): line([(x,cy-17),(x-3,cy+12)],(191,205,208),1)
line([(cx,cy-15),(cx+9,cy-35)],INK,3); d.ellipse((cx+6,cy-39,cx+12,cy-33),fill=RED)
txt(62,930,'DEFEND THE ORBIT',11,RED,SANS_B)

# 5 Tech / Nvidia
b5=(519,758,992,992)
panel(b5,5,'TECH / NVIDIA','HUANG RETURNS AS NVIDIA CEO','JENSEN HUANG REINSTATED LESS THAN TWO WEEKS AFTER RESIGNING',16)
# chip, pins, green accent absent by design: maintain single red accent
cx,cy=752,865
d.rectangle((cx-56,cy-45,cx+56,cy+45),fill=(224,221,210),outline=INK,width=3)
d.rectangle((cx-36,cy-27,cx+36,cy+27),fill=INK)
txt(cx,cy-16,'N',34,WHITE,SANS_B,anchor='mm')
# chip pin grid
for y in range(cy-34,cy+39,14):
    line([(cx-69,y),(cx-56,y)],INK,3); line([(cx+56,y),(cx+69,y)],INK,3)
for x in range(cx-41,cx+42,14):
    line([(x,cy-58),(x,cy-45)],INK,3); line([(x,cy+45),(x,cy+58)],INK,3)
# return arrow around chip
d.arc((cx+70,cy-45,cx+139,cy+34),205,60,fill=RED,width=5)
d.polygon([(cx+126,cy-30),(cx+142,cy-26),(cx+130,cy-16)],fill=RED)
txt(841,844,'JENSEN',14,INK,SANS_B)
txt(841,864,'HUANG',14,INK,SANS_B)
txt(841,887,'BACK AT THE HELM',10,RED,SANS_B)

# footer folio
line([(32,1003),(992,1003)],INK,2)
txt(32,1007,'THE WORLD  •  FIVE STORIES, ONE DAY',9,MUTED,SANS_B)
txt(992,1007,'24 NOV 2026',9,MUTED,SANS_B,anchor='ra')

im.save(Path(__file__).with_name('entry.png'), format='PNG', optimize=True)
