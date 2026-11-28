// GitHub social preview card, 1280x640 at 72 ppi (1 pt = 1 px).
// Every value arrives through sys.inputs from the social-preview CLI, which
// validates and derives the colors; this file only lays them out.

#let input(key) = sys.inputs.at(key, default: "")
#let color(key) = rgb(sys.inputs.at(key))

#let W = 1280pt
#let H = 640pt
// Safe area: X and LinkedIn crop the edges and feeds show the card at 400-600 px wide.
#let LEFT = 88pt
#let RIGHT = 80pt
#let TOP = 72pt
#let BOTTOM = 64pt
#let LOGO = 320pt
#let LOGO-GAP = 40pt
#let BAR = 6pt
#let GRID = 40pt

#let bg = color("bg")
#let fg = color("fg")
#let muted = color("muted")
#let accent = color("accent")
#let accent2 = color("accent2")
#let highlight = color("highlight")
#let pop = color("pop")
#let pane = color("pane")
#let pane-fg = color("pane-fg")
#let sans = input("font")
#let mono = input("mono")
#let logo = input("logo")

#set page(width: W, height: H, margin: 0pt, fill: bg)
#set text(font: sans, fill: fg)

#let has-logo = logo != ""
#let column = W - LEFT - RIGHT - if has-logo { LOGO + LOGO-GAP } else { 0pt }

// Largest size from max down to min (2 pt steps) whose content fits `lines` lines of `width`.
#let fit(make, max, min, width, lines: 1) = context {
	let limit = measure(block(width: width, make(max, [X] + range(lines - 1).map(_ => linebreak() + [X]).sum(default: [])))).height
	let size = max
	while size > min {
		let scale = size / max
		if measure(block(width: width, make(size, none))).height <= limit * scale + 1pt { break }
		size -= 2pt
	}
	make(size, none)
}

// Faint grid: texture that reads as "built", drawn at 6% so text always wins.
#let grid-tile = tiling(size: (GRID, GRID))[
	#place(line(start: (0pt, 0pt), end: (GRID, 0pt), stroke: 1pt + accent.transparentize(94%)))
	#place(line(start: (0pt, 0pt), end: (0pt, GRID), stroke: 1pt + accent.transparentize(94%)))
]
#place(rect(width: W, height: H, fill: grid-tile))
#place(top, rect(width: W, height: BAR, fill: gradient.linear(accent, accent2)))
#place(bottom, rect(width: W, height: BAR, fill: gradient.linear(accent, accent2)))

#if has-logo {
	place(top + left, dx: W - RIGHT - LOGO, dy: (H - LOGO) / 2, box(width: LOGO, height: LOGO, align(
		center + horizon,
		image(logo, width: 100%, height: 100%, fit: "contain", scaling: input("logo-scaling")),
	)))
}

#let wordmark(size, sample) = text(
	font: if input("wordmark") == "mono" { mono } else { sans },
	size: size,
	weight: 700,
	tracking: if input("wordmark") == "mono" { 0.12em } else { -0.02em },
	fill: accent,
	if sample == none { input("name") } else { sample },
)

#let title(size, sample) = {
	set par(leading: 0.3em)
	text(size: size, weight: 800, tracking: -0.04em, fill: fg, if sample == none { input("tagline") } else { sample })
}

#let subline(size, sample) = text(size: size, weight: 600, fill: highlight, if sample == none {
	input("subline")
} else { sample })

// Each piece is its own block: inline boxes would otherwise share a paragraph and swallow the gaps.
#place(top + left, dx: LEFT, dy: TOP, block(width: column, height: H - TOP - BOTTOM, {
	set block(spacing: 0pt)
	block(fit(wordmark, 68pt, 40pt, column))
	if input("badge") != "" {
		v(30pt)
		block(box(fill: accent.transparentize(88%), stroke: 2pt + accent, inset: (x: 17pt, y: 11pt), text(
			font: mono,
			size: 17pt,
			weight: 700,
			tracking: 0.09em,
			fill: highlight,
			upper(input("badge")),
		)))
	}
	v(1fr)
	block(fit(title, 64pt, 40pt, column, lines: 2))
	if input("subline") != "" {
		v(32pt)
		block(fit(subline, 32pt, 22pt, column))
	}
	v(1fr)
	if input("install") != "" {
		block(box(fill: pane, stroke: 2pt + fg.transparentize(85%), inset: (x: 24pt, y: 17pt), text(
			font: mono,
			size: 22pt,
			weight: 700,
			fill: pane-fg,
		)[#text(fill: pop)[\$] #input("install")]))
		v(30pt)
	}
	if input("url") != "" {
		block(text(font: mono, size: 21pt, weight: 700, fill: muted, input("url")))
	}
}))
