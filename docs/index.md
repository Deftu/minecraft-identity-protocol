# Minecraft Identity Protocol (MIP) — Overview

## The problem this solves

If you've ever built a mod, plugin, or website that needed to answer "is this
really the Minecraft player they claim to be?", you've probably run into the
fact that there's no single standard way to do it. Depending on your setup you
end up either:

- Verifying a player from inside the game, using Mojang's servers, or
- Sending a player through a Microsoft login page from a browser,

and these two paths look nothing alike, use different APIs, and are easy to
get subtly wrong (session fixation, replay attacks, leaking tokens into logs,
etc.) — mistakes that are hard to spot in review and only show up as security
incidents later.

MIP standardizes both paths behind one shared design, so a backend
implementing it once supports both a "verify from inside the game" flow and a
"log in with Minecraft" browser flow, and always ends up with the player's
identity in the same shape, handled the same way, no matter which path they
came in through.

Think of it as something like "Sign in with Google," but for Minecraft
accounts, with an extra in-game option a browser-based standard wouldn't
have.

## Who's involved

- **Player** — the person.
- **Client** — whatever is acting for the player: a mod/launcher, or a
  browser.
- **Backend** (the "Relying Party" in the spec) — the server that wants to
  know who the player is. This is *not* a Minecraft server the player is
  connected to — it's an ordinary web backend, reached over HTTPS, that a mod
  or website talks to.
- **Mojang / Microsoft** — the actual source of truth. MIP doesn't replace
  Mojang's or Microsoft's login systems; it just wraps the "ask them, get an
  answer" step in a consistent, safer envelope.

## Two ways to log in

### In-game verification (for mods)

Used when a mod is already running inside an active game session and just
needs to prove that to its own backend — no browser involved.

1. The mod asks the backend for a one-time challenge.
2. The mod makes Minecraft's normal "join a server" call, using that
   challenge value — this is the same mechanism vanilla Minecraft always uses
   when connecting to any server, just aimed at the backend instead.
3. The mod tells the backend "I did that," and the backend checks with
   Mojang whether it actually happened.
4. If it checks out, the backend hands the mod a session to use from then on.

This never touches a browser and never requires the mod to actually join a
multiplayer server.

### Browser login (for websites)

Used for a website, dashboard, or store that wants a "log in with Minecraft"
button, with no mod involved.

1. The site sends the player's browser to Microsoft's login page.
2. The player logs in there (not on the site itself).
3. Microsoft sends the browser back with proof of login.
4. The backend exchanges that proof, behind the scenes, through Microsoft's
   and Xbox's systems, ending with a verified Minecraft profile.
5. The backend hands the browser a session, usually as a cookie.

There's also a shortcut for tools that already have a Microsoft login token
from doing something else first (like a launcher) — they can skip the
browser redirect and hand that token straight to the backend instead.

## What comes out of either flow

Regardless of which path was used, the backend ends up with the same basic
set of facts about the player:

- Their stable account ID (this doesn't change even if they rename)
- Their current username
- Their skin/cape, if available
- Which method was used to verify them

That last point matters for one specific design decision: **neither method is
treated as "more trusted" than the other.** A player verified through the
in-game flow and a player verified through the browser flow are equally
legitimate — the backend just needs to know which one happened, for its own
logging/debugging.

## Sessions, not raw identity

The backend never just hands the player's raw verified profile back and says
"use this to prove who you are from now on." Instead, it issues a proper
**session** — a short-lived token/cookie meant specifically for that purpose,
the same way most login systems work. This keeps the actual verification
result (which involved talking to Mojang/Microsoft) separate from ongoing
"is this still the same logged-in session" checks, which is faster and safer.

Sessions expire fairly quickly by design. To avoid making players log in
again every hour, MIP optionally supports **refresh tokens** — a longer-lived
value that can be traded in for a new session without repeating the whole
verification dance. If a refresh token is ever used twice (a sign it may have
been stolen), the backend treats that as a red flag and revokes everything
tied to it.

## Linking accounts (optional)

Some backends already have their own account system (email/password, etc.)
and want to let a player *attach* a Minecraft account to an existing account,
rather than create a brand-new session for it — useful for supporting
multiple Minecraft accounts per user, for example. MIP supports this as an
optional add-on: the same verification flows run, but the end result is "link
this Minecraft account to my existing account" instead of "log me in as a
new session."

## Security, in plain terms

A few of the more important protections baked into the design:

- **One-time-use everything.** Challenges, login codes, and tokens can each
  only be used once. Capturing a copy of a request in transit shouldn't let
  anyone replay it later.
- **Nothing sensitive in URLs.** Secrets travel in request bodies, not query
  strings — URLs have a habit of ending up in logs, browser history, and
  proxy records.
- **A subtle relay attack, and how it's handled.** There's a known trick
  where an attacker requests a challenge for themselves, then tricks a victim
  into unknowingly "using" that challenge just by having the victim connect
  to the attacker's own Minecraft server — a completely ordinary action from
  the victim's point of view. MIP addresses this by having the backend check
  that the network address doing the verifying matches the one that actually
  did the in-game join, the same protection real Minecraft servers already
  use against proxy-relay tricks.
- **Consistent error responses.** When something goes wrong, the backend
  gives the same answer whether a challenge didn't exist, expired, or was
  already used — so an attacker probing the system can't learn anything
  useful from the difference.
- **No favoritism between login methods.** As noted above, in-game and
  browser verification are equally valid; nothing downstream should
  special-case one as weaker.

## What's optional vs. required

A backend can support just one of the two login flows, or both. Refresh
tokens, account linking, and a couple of convenience endpoints (like fetching
a player's profile info separately) are all optional add-ons on top of the
core protocol — a backend can pick and choose based on what it actually
needs, as long as whatever it does implement follows the spec exactly rather
than a partial or modified version of it.
