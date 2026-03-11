---
generated: 2026-03-09 10:15
beforeSize: 4271011
afterSize: 15938
reducedBy: 99.6%
---

# Goldfish School in Dual-Light Water Environment

```crux
⟦CRUX:image-original.png
Ρ{digital art;goldfish school;water environment;dual lighting zones;
  photorealistic rendering w/ painterly softness;contemplative aquatic scene}

Κ{
  GF=goldfish;cal=calico;orn=orange;gld=gold;wht=white;blk=black;
  caud=caudal(tail);pect=pectoral;dors=dorsal;
  caust=caustic light pattern;trans=translucent;
  @=position(%from-edges);θ=orientation angle;
  sat=saturation;lum=luminance;sz=size relative scale
}

Π.color-palette{
  water.dark=[#2D3436,#3D4449,#4A5157]→charcoal-slate gradient w/subtle green
  water.bright=[#5B9BD5,#6BA8E0,#7CB5EB]→azure-cerulean gradient
  caustics=[#FFFFFF,#E8F4FC,#D4ECFA]→pure white→pale ice blue
  fish.orn=[#FF6B35,#FF8C42,#FFA64D,#FFD166]→vivid orange→amber→gold gradient
  fish.wht=[#F5F5F5,#E8E8E8,#FAFAFA]→cream-white w/ subtle warmth
  fish.blk=[#1A1A1A,#2C2C2C]→true black markings
  fish.pale=[#D4D4D4,#C0C0C0,#B8B8B8]→silvery-gray for ghostly fish
  highlights=[#FFFFFF,#FFFDE7]→specular white+warm gleam
  shadow.edge=[#1A2327,#232D33]→dark finger shadows at zone transition
}

Π.layout{
  canvas:aspect≈16:9;landscape orientation
  zone.division:horizontal≈45% mark from top
  upper.zone:dark water @0-45% vertical
  lower.zone:bright water @45-100% vertical
  transition.edge:irregular scalloped curve;
    left.entry@(0%,52%);
    curve.up@(15%,43%);
    curve.down@(35%,48%);
    central.dip@(50%,50%);
    curve.up@(70%,42%);
    right.exit@(100%,48%)
  shadow.fingers:extend down from dark zone;
    finger1@(8%,55%)→(10%,62%);
    finger2@(12%,54%)→(14%,60%);
    finger3@(18%,53%)→(20%,58%);
    finger4@(25%,52%)→(27%,56%)
  fish.distribution:organic cluster;center-weighted;
    diagonal flow ↗ upper-right;
    some crossing zone boundary
}

E.caustics{
  pattern:network of irregular curved cells
  geometry:Voronoi-like tessellation w/ rounded edges
  line.width:2-4px equivalent;variable thickness
  line.color:#FFFFFF→#E8F4FC gradient along curves
  cell.shapes:roughly circular→elliptical;5-15% canvas width each
  density.gradient:
    lower-right@(70-100%,70-100%):highest density;tight cells
    center@(40-70%,60-80%):medium density
    lower-left@(0-40%,70-100%):medium-sparse
    near.transition@(0-100%,45-60%):sparse;interrupted by fish+shadows
  brightness:intensity peaks at curve intersections
  implied.surface:suggests sun-dappled shallow water from above
}

E.fish01{
  id:top-left orange goldfish
  @(8%,18%);θ=15°clockwise from horizontal(facing right-down)
  sz:medium-large≈8%canvas width
  body.color:vivid orange #FF6B35→amber #FFA64D ventral gradient
  body.shape:elongated fusiform;slight arch in spine
  scale.detail:subtle iridescent sheen;individual scales implied not distinct
  caud.fin:flowing fan shape;deeply forked;
    membrane.trans:50-60%;veining faint
    color:orange→pale gold→translucent edge
    spread≈70°arc
  dors.fin:low profile;orange matching body
  pect.fins:small;swept back;partially obscured
  eye:dark dot w/ gold iris ring;small specular highlight
  highlight.spec:white gleam on dorsal ridge;@20% from head
  lighting:even from dark zone;no caustic interference
}

E.fish02{
  id:upper-center orange-gold goldfish
  @(28%,14%);θ=20°clockwise(facing right-down)
  sz:medium≈7%canvas width
  body.color:#FF8C42 orange-gold;warmer gold on belly
  body.shape:compact rounded;healthy plump proportions
  caud.fin:fan spread;semi-transparent;amber gradient
    membrane.trans:55%;delicate veining visible
    spread≈65°arc
  dors.fin:erect;moderate height;orange
  pect.fins:visible both sides;fan-like;active posture
  eye:visible;dark center w/ gold surround
  highlight.spec:subtle dorsal gleam
  depth.cue:slightly more saturated than fish01→closer to viewer
}

E.fish03{
  id:calico koi (white+orange+black)
  @(38%,22%);θ=170°(facing left-down)
  sz:medium≈7%canvas width
  body.color:base white #F5F5F5;
    orange patch #FF7A45 on head extending to mid-body;
    black speckles #1A1A1A scattered across flanks
  pattern:classic Sanke-type calico;orange concentrated dorsal;black irregular spots
  body.shape:slightly more elongated than pure goldfish
  caud.fin:split/butterfly style;dramatic spread;
    membrane.trans:65-70%;highly translucent
    color:white base w/ faint orange wash
    veining:visible darker lines
    spread≈80°arc
  dors.fin:white;translucent;moderate
  pect.fins:extended wide;white+translucent
  eye:dark;visible through head-turn
  contrast:stands out against dark water+orange neighbors
  highlight.spec:white gleam on orange patch
}

E.fish04{
  id:upper-right orange goldfish
  @(62%,15%);θ=30°clockwise(facing right-down toward lower zone)
  sz:medium≈6.5%canvas width
  body.color:vivid orange #FF6B35;gold #FFD166 on ventral
  body.shape:streamlined;active swimming posture
  caud.fin:swept back;moderate spread;
    membrane.trans:50%;
    color:orange→golden tips
    spread≈55°arc
  dors.fin:folded back;streamlined
  pect.fins:swept posterior;swimming motion
  eye:small dark dot visible
  highlight.spec:bright dorsal gleam;sun-catching
  depth.cue:slightly smaller→further back in school
}

E.fish05{
  id:mid-upper orange goldfish
  @(48%,20%);θ=350°(facing slightly up-right)
  sz:medium≈6%canvas width
  body.color:#FF7A45 red-orange;richer saturation
  body.shape:compact;rounded belly
  caud.fin:semi-spread;flowing;
    membrane.trans:55%;
    spread≈60°arc
  dors.fin:visible;upright
  pect.fins:mid-position
  highlight.spec:subtle gleam
  partial.obscure:slightly overlapped by fish03
}

E.fish06{
  id:mid-center orange goldfish (transitional)
  @(42%,38%);θ=200°(facing left-down)
  sz:medium-large≈7%canvas width
  body.color:rich orange #FF6B35;golden belly
  body.shape:healthy proportions;slight turn
  caud.fin:elegant fan;good spread;
    membrane.trans:50%;
    veining:subtle dark lines
    spread≈70°arc
  dors.fin:prominent;erect
  pect.fins:spread wide;visible both sides
  zone.crossing:body in dark zone;tail approaching transition edge
  highlight.spec:dorsal ridge gleam
  depth.cue:foreground fish→larger+more saturated
}

E.fish07{
  id:right-side ghostly/pale fish
  @(88%,25%);θ=195°(facing left-down)
  sz:medium≈6%canvas width
  body.color:silvery-white #D4D4D4;ghostly pale;
    faint warm cream undertone #F5F0E6
  body.shape:elongated;elegant
  caud.fin:exceptionally long flowing;dramatic;
    membrane.trans:75-80%;highly translucent;ethereal
    color:near-white;pale silver
    veining:fine dark threads visible
    length≈150% of body length;
    spread≈90°arc
  dors.fin:tall;flowing;white-silver
  pect.fins:extended;translucent flowing
  eye:dark;provides contrast
  special:most ethereal fish in composition;ghost-like quality
  highlight.spec:subtle silver gleam on flank
  depth.cue:pale coloring→further back OR stylistic variety
}

E.fish08{
  id:lower-left orange goldfish
  @(18%,72%);θ=15°(facing right)
  sz:medium≈6%canvas width
  body.color:warm orange #FF8C42;gold highlights
  body.shape:compact rounded
  caud.fin:moderate spread;
    membrane.trans:55%;
    spread≈60°arc
  dors.fin:visible;moderate
  pect.fins:fan position
  zone:fully in bright caustic water
  caustic.effect:light network visible through body edges;
    body interrupts pattern creating shadow
  highlight.spec:caustic-enhanced dorsal gleam;brighter than dark-zone fish
}

E.fish09{
  id:lower-left small reddish goldfish
  @(12%,78%);θ=25°(facing right-down)
  sz:small≈4.5%canvas width
  body.color:deep red-orange #E55934;richest red in composition
  body.shape:compact;juvenile proportions
  caud.fin:short;developing;
    membrane.trans:50%;
    spread≈50°arc
  dors.fin:small;proportional
  pect.fins:small;active
  zone:bright caustic water
  caustic.effect:strong caustic patterns surrounding
  highlight.spec:bright caustic-reflected gleam
  depth.cue:small size→young fish OR distant
}

E.fish10{
  id:large central orange goldfish (hero fish)
  @(38%,68%);θ=345°(facing slightly up-right)
  sz:large≈9%canvas width→largest fish in composition
  body.color:gradient #FF6B35 dorsal→#FFD166 gold belly→
    pale cream #FFF5E1 ventral
  body.shape:robust;mature;commanding presence
  scale.detail:individual scales catching light;iridescent shimmer
  caud.fin:magnificent spread;dominant feature;
    membrane.trans:45-55%;more opaque than others
    color:rich orange→gold→translucent cream edge
    veining:visible radiating pattern
    spread≈85°arc
  dors.fin:tall;prominent;fully erect
  pect.fins:large;spread wide;alpha posture
  eye:clearly visible;dark center;gold iris;bright specular
  highlight.spec:
    primary:large white gleam on dorsal ridge @30% from head
    secondary:smaller gleams on gill plate+flank
  caustic.effect:
    caustic lines visible on lower body creating light striations
    body casts subtle shadow interrupting nearby caustic pattern
  depth.cue:size+saturation+detail→primary foreground fish
  compositional.role:visual anchor;draws eye first
}

E.fish11{
  id:mid-center orange goldfish
  @(52%,58%);θ=340°(facing up-right toward dark zone)
  sz:medium≈6.5%canvas width
  body.color:#FF7A45 orange;gold belly
  body.shape:streamlined;upward-swimming posture
  caud.fin:swept down;moderate;
    membrane.trans:55%;
    spread≈55°arc
  dors.fin:folded;swimming mode
  pect.fins:swept back
  zone.crossing:approaching transition edge from below
  caustic.effect:partial caustic overlay on body
  highlight.spec:bright dorsal gleam
}

E.fish12{
  id:right-center orange-gold goldfish
  @(65%,60%);θ=10°(facing right)
  sz:medium-large≈7.5%canvas width
  body.color:golden-orange #FFA64D;more gold than orange
  body.shape:healthy;rounded
  caud.fin:beautiful spread;
    membrane.trans:55%;
    color:gold→pale amber
    spread≈70°arc
  dors.fin:erect;golden
  pect.fins:spread;visible
  caustic.effect:strong caustic lines crossing body;
    creates striped light effect
  highlight.spec:multiple caustic-enhanced gleams
  depth.cue:mid-ground positioning
}

E.fish13{
  id:lower-right calico/spotted goldfish
  @(78%,72%);θ=185°(facing left)
  sz:medium≈6%canvas width
  body.color:cream-white #F5F0E6 base;
    orange #FF8C42 patches on head+dorsal;
    black #2C2C2C irregular spots on flanks
  pattern:calico;less dramatic than fish03
  body.shape:compact
  caud.fin:moderate spread;
    membrane.trans:65%;translucent white+orange wash
    spread≈60°arc
  dors.fin:white+orange
  pect.fins:visible;white
  caustic.effect:heavy caustic pattern overlay;
    light lines create complex shadow-light interaction on white body
  highlight.spec:caustic-induced multiple gleams
}

E.fish14{
  id:far-right pale/white goldfish
  @(90%,68%);θ=200°(facing left-down)
  sz:small-medium≈5%canvas width
  body.color:pale cream #F5F0E6;ghostly;
    faint orange wash on head
  body.shape:slender
  caud.fin:flowing;translucent;
    membrane.trans:70%;
    spread≈65°arc
  dors.fin:pale;translucent
  zone:bright caustic water;edge of frame
  caustic.effect:strong;patterns visible through translucent fins
  depth.cue:smaller+paler→background fish
}

Π.lighting{
  source.implied:overhead sun;slightly behind-right
  upper.zone:
    ambient:low;dark water absorbs light
    fish.lighting:even soft illumination
    no.caustics:shadowed from surface refraction
  lower.zone:
    ambient:bright;direct light penetration
    caustic.source:sun through moving water surface
    intensity:brightest at lower-right→dimmer toward transition
  transition.edge:
    hard.light.boundary:dramatic contrast jump
    shadow.fingers:dark zone extends into bright as gradient fingers
    fish.crossing:illumination changes sharply on bodies
  fish.reflection:
    specular.highlights:small white gleams on dorsal ridges
    scale.iridescence:subtle rainbow shimmer on well-lit fish
    fin.transillumination:light passes through membranes;
      creates glow effect on thin fin edges
}

Π.water-physics{
  dark.zone:
    interpretation:deep water OR shadow from above
    color.origin:absorption of light;depth>3m equivalent
    particulate:subtle gray-green texture;organic matter implied
  bright.zone:
    interpretation:shallow sun-penetrated water
    color.origin:sky reflection+light scattering;<1m depth equivalent
    clarity:high;individual fish details visible
  caustic.physics:
    formation:surface wave lensing concentrates light
    cell.pattern:typical of calm-to-mild surface ripples
    brightness.variation:constructive interference at lines
  transition.mechanism:
    possibility1:shadow edge from structure above
    possibility2:underwater terrain creating light/dark boundary
    possibility3:artistic dramatic effect
}

Π.composition{
  balance:asymmetric organic
  visual.weight:concentrated lower-center (hero fish)
  flow:
    eye.entry:large fish@lower-center→
    upward.sweep:following fish school diagonal→
    upper.exploration:scattered fish in dark zone→
    right.exit:pale ghost fish draws eye to edge
  rule.of.thirds:
    hero fish anchors lower-left intersection
    calico fish (fish03) near upper-right intersection
  depth.layers:
    foreground:fish10(hero)+fish06
    mid-ground:fish08,11,12+most others
    background:fish07(ghost)+fish04+smaller fish
  negative.space:
    upper-left dark zone:restful
    lower-right caustic zone:active texture
  tension:diagonal line of fish creates dynamic energy
  harmony:color repetition(orange school)+zone contrast
}

Π.rendering-style{
  medium:digital painting;photorealistic base w/ artistic softening
  technique:likely photo reference→painterly processing
  brush.quality:smooth gradients;soft edges on fins
  detail.level:
    fish.bodies:high detail;individual anatomy correct
    fins:medium-high;membrane trans+veining rendered
    caustics:geometric precision;clean curves
    water:flat color zones;minimal texture
  color.handling:
    saturation:vivid orange fish contrast w/ neutral water
    temperature:warm fish vs cool water environment
  edges:
    fish.bodies:soft but defined
    fins:very soft;feathered into water
    caustic.lines:sharp;crisp white
  overall.impression:serene;contemplative;elegant naturalism
}

Ω.metaphor{
  primary:
    contrast(dark↔light)→transition;emergence;threshold
    fish school→collective movement;shared direction;community
    crossing boundary→transformation;entering new environment
  secondary:
    orange warmth in cool water→life persisting;vitality
    ghost fish(white)→difference;individuality in group
    caustic patterns→complexity beneath surface;hidden beauty
  mood:
    tranquil;meditative;peaceful observation
    slight tension at zone boundary→anticipation
    overall warmth despite cool tones
  atmosphere:
    summer afternoon;dappled sunlight;garden pond
    quiet contemplation;nature observation
    Japanese aesthetic influence(koi pond tradition)
  symbolic:
    fish as fortune/abundance(cultural)
    light vs shadow→knowledge vs mystery
    surface patterns→order within chaos
    collective individuality→unity w/ diversity
}

Ω.reconstruction-hints{
  critical.elements:[
    dual-zone water(dark upper/bright lower);
    caustic network pattern in lower zone;
    ~14 goldfish in organic school formation;
    color scheme:orange fish + blue/gray water;
    transition edge w/ shadow fingers;
    hero fish lower-center;
    ghost fish far right;
    calico fish provide variety
  ]
  style.guidance:
    photorealistic digital art;
    soft painterly finish;
    vivid but harmonious colors;
    emphasis on light/shadow contrast
  avoid:
    cartoonish rendering;
    uniform fish placement;
    missing caustic patterns;
    flat lighting
}
⟧
```
