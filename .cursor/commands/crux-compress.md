---
generated: 2026-07-13 19:14
sourceChecksum: "2919266716"
cruxLevel: 25
beforeTokens: 6395
afterTokens: 1374
reducedBy: 79%
confidence: 94%
---

If this body is CRUX-notated and you cannot decompress it from always-on rules alone, read `CRUX.md` before interpreting the body.

> [!IMPORTANT]
> Generated file - do not edit!

# crux-compress

```crux
⟦CRUX:crux-compress.source.mdx
Κ{mgr=crux-cursor-rule-manager; util=crux-utils skill;
  tpl=.cursor/commands/templates/compress-prompts.md;
  reg=.crux/plugins/registry.json}

Λ.usage{
  /crux-compress ALL→all eligible rules(formatted)
  /crux-compress @path/to/file.md→specific file
  /crux-compress @f1.md @f2.md→multiple files
  /crux-compress @file.md --minified→single-line output
  /crux-compress ALL --force→force recompression(delete existing first)
  /crux-compress @file.md --40→target 40% of original
  /crux-compress @script.sh→code file
  /crux-compress @image.png→image(semantic visual desc)
  /crux-compress https://example.com→URL source
  /crux-compress @file.md --plugin=name→enable plugin
  /crux-compress ALL --no-plugin name→disable default plugin
}

Φ.flags{
  --minified→single-line output; max compression; copy-paste/LLM testing
  --force→delete existing outputs before compress; bypass checksum
  --<n>(1-100)→compression level; overrides frontmatter crux:<n>; default:25(text)|80(image)
  --plugin <name>|--plugin=<name>→enable named plugin; repeatable
  --no-plugin <name>→disable default-enabled plugin
  combinable: ALL --force --minified --40 --plugin quality-gate
}

Φ.level{
  resolution: CLI flag(highest)→frontmatter crux:<n>→default(25|80 images)
  crux:true≡crux:25; outside 1-100→reject+error
  passed to mgr as compressionLevel:<n>; recorded as cruxLevel:<n>
  effect: --10=very aggressive; --25=standard; --40=moderate; --80=light
  images: level=detail retention(100=max,1=minimal)
}

Φ.plugins{
  resolve from reg; hooks:[beforeFetch,beforeCompress,afterCompress,afterValidate]
  default loading(no --plugin flags): collect enabledByDefault:true→remove --no-plugin entries
  explicit mode(--plugin present): ONLY named plugins; defaults ¬implicitly added;
    --no-plugin ignored(warn)
  validation: unknown plugin→fail fast; must declare ≥1 hook
  execution order: default=registry order; explicit=CLI order
  context: sourcePath|sourceUrl,sourceType,outputPath,compressionLevel,format,force,
    beforeTokens,afterTokens,confidence(when avail)
  failures: recorded per plugin; ¬block unless failClosed:true; ¬mutate CRUX.md
}

Λ.force{when --force; BEFORE any compression:
  identify targets by SoT type; delete existing loadable/output; log each deletion
  proceed w/ normal compression(no checksum skip)}

Γ.dispatch{### Source-Type Dispatch; 5 bodies in tpl; load matching section only
  read tpl ## Shared Preamble once per invocation
  image(@*.png|jpg|jpeg|gif|webp|svg)→tpl ## image; default level 80;
    ¬--minified; ¬sourceChecksum tracking
  URL(http://|https://)→tpl ## url; output→.crux/out/; sourceUrl(¬checksum)
  code(@*.sh|bash|ts|tsx|js|jsx|py|rs|go|java|sql|css|scss)→tpl ## code; ¬.crux.mdc
  markdown(@*.md|mdc|source.mdx|SKILL.mdx; ¬image/url/code)→tpl ## markdown
  ALL→tpl ## all; .cursor/rules/**/*.md|mdc w/ crux:true|<n> frontmatter only;
    ¬code/image/URL
}

R.checksum{track source checksum→avoid unnecessary updates
  1.get current checksum via util --cksum
  2.existing CRUX sourceChecksum matches→skip!
  3.no match|no file→proceed
  4.store new sourceChecksum in output frontmatter}

R.parallelism{max 4 parallel mgr instances; >4→sequential batches of 4}

R.eligibility{
  markdown SoT: .md|.mdc|.source.mdx|SKILL.mdx; rules need crux:true|<n>;
    ¬recompress generated loadables; ALL→.cursor/rules/ only; explicit→anywhere
  code: supported ext; explicit @ref only; ¬ALL; ¬crux frontmatter needed; ¬.crux.mdc
  URL: http(s)://; returns fetchable text; explicit only; ¬ALL; output→.crux/out/
  image: supported ext; explicit @ref; ¬ALL; ¬.crux.mdc}

Φ.output.convention{
  rules(.cursor/rules/): SoT=.md → loadable=.crux.mdc(+alwaysApply; ¬.crux.md intermediary)
  commands/agents: SoT=<name>.source.mdx → loadable=<name>.md(CRUX body; keep reg FM)
  skills: SoT=SKILL.mdx → loadable=SKILL.md(CRUX body)
  other markdown/code/image: →.crux.md beside source
  URL→.crux/out/; no implied→.crux/out/
  ⊛¬emit adjacent .crux.md as Cursor-loadable for cmd/agent/skill!
  CRUX header: ⟦CRUX:SoT-filename ... ⟧
}

R.validation{every compression followed by fresh mgr instance validation
  writes CRUX→fresh agent compares→confidence score(0-100%)→update frontmatter
  ≥90% excellent; 80-89% good; 70-79% marginal; <70% revise
  fresh agent ensures: no bias,independent eval,¬relies on CRUX spec knowledge}

M.related{mgr;CRUX.md;.cursor/rules/_CRUX-RULE.mdc;util;tpl}
⟧
```
