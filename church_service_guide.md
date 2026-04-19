# Church Service Order Guide

This document describes the standard order of worship and how to organize each element of a Sunday service.

---

## camera scene
- include a source for each of the main cameras to allow for quick switching during the service (e.g., `CameraMain`, `CameraPulpit`, `CameraChoir`).
- ensure each camera source is properly configured with the correct video input and settings in OBS.
- include this scene in all other scenes, so that audio is consistent throughout the service regardless of which visual scene is active.

## audio scene
- include sources for the main audio inputs: `PulpitMic`, `ChoirMics`, `HouseMic`, and any additional instruments or ambient mics.
- set up audio levels and routing in OBS to ensure a balanced mix for both in-house sound and live stream output.
- include this scene in all other scenes, so that audio is consistent throughout the service regardless of which visual scene is active.
- consider adding audio filters (e.g., noise gate, compressor) to the mic sources to improve sound quality.

## Emergency Slides
- create a scene called `EmergencySlides` that can be quickly switched to in case of technical difficulties.
- one slide for 'be right back'
- one slide for service interrupted
- one slide for technical difficulties
- ensure these slides are visually distinct and clearly communicate the situation to viewers.

## Order of Worship
### PreService
- OBS scene: `preservice` — countdown title visible, info bar scrolling
- title centered at top, and announcements scrolling at bottom,
- Slides: display a welcome graphic
### 1. Prelude
**Purpose**: Prepare the congregation for worship through instrumental or choral music as people gather and are seated.

**Typical duration**: 5–10 minutes before the service begins.

**Production notes**:
- Organ, piano, or ensemble plays softly
- House lights at full; no announcements during prelude
- OBS scene: `prelude` — countdown title visible, info bar scrolling

---

### 2. Welcome
**Purpose**: Greet the congregation, acknowledge visitors, and briefly introduce the day's service theme.

**Typical duration**: 2–3 minutes.

**Production notes**:
- Pastor or worship leader speaks from the pulpit or center stage
- Slides: display "Welcome" graphic with date and service name
- OBS scene: `MainWorship` — speaker area active, title bar showing service name

---

### 3. Opening Hymn (Hymn 1)
**Purpose**: Gather the congregation in unified praise through corporate singing.

**Typical duration**: 3–5 minutes (2–4 verses).

**Production notes**:
- Display hymn number and title on screen
- Slides: lyric slides per verse; ensure font is large enough for readability
- OBS scene: `MainWorship` — announcement slides replaced with lyric slides
- Notify sound team to raise congregation mic mix

---

### 4. Ritual / Liturgical Opening (Ritual 1)
**Purpose**: A spoken or responsive liturgical element — such as the Invocation, Confession and Absolution, or Apostles' Creed — that grounds the service in the tradition of the church.

**Typical duration**: 3–5 minutes.

**Common forms**:
- Invocation: "In the name of the Father, Son, and Holy Spirit…"
- Confession & Absolution: Spoken responsively from bulletin or screen
- Creed: Congregation recites together

**Production notes**:
- Display liturgy text on screen so visitors can follow along
- OBS scene: `ScriptureScene` — verse text area used for liturgy text
- Keep text large and high-contrast for readability

---

### 5. Prayer of the Day
**Purpose**: A short, focused prayer that summarizes the theme of the day's scripture readings.

**Typical duration**: 1–2 minutes.

**Production notes**:
- Pastor leads; congregation responds "Amen"
- Slides: display a simple background or prayer text if desired
- OBS scene: maintain `ScriptureScene` or return to `MainWorship`

---

### 6. Offertory (Offertory 1)
**Purpose**: Receive the congregation's financial gifts and, in some traditions, prepare the communion elements.

**Typical duration**: 3–5 minutes during the collection; hymn or anthem sung simultaneously.

**Production notes**:
- Display giving information (online giving URL, text-to-give number)
- Slides: `slide_giving.jpg` or offertory hymn lyrics
- OBS scene: `MainWorship` — announcement slides panel updated with giving slide
- Info bar can scroll giving instructions

---

### 7. First Reading
**Purpose**: Read aloud a passage from the Old Testament or Epistles as appointed for the day.

**Typical duration**: 2–3 minutes.

**Production notes**:
- Lector reads from lectern
- Display passage reference (e.g., "Isaiah 40:28–31") before and after reading
- OBS scene: `ScriptureScene` — `VerseRef` source shows book/chapter/verse
- End with "The Word of the Lord" / "Thanks be to God"

---

### 8. Second Reading
**Purpose**: A second scripture reading, typically from the New Testament Epistles.

**Typical duration**: 2–3 minutes.

**Production notes**:
- Same production setup as First Reading
- Update `VerseRef` source text to new passage reference
- OBS scene: `ScriptureScene`

---

### 9. Gospel Reading
**Purpose**: Read the Gospel passage for the day; treated with particular reverence as the words of Christ.

**Typical duration**: 2–4 minutes.

**Production notes**:
- Pastor or deacon reads; congregation traditionally stands
- Display "Holy Gospel according to [Book] chapter [X]"
- OBS scene: `ScriptureScene` — highlight Gospel book reference
- Ends with "The Gospel of the Lord" / "Praise to you, O Christ"

---

### 10. Gospel Acclamation
**Purpose**: A sung response to the Gospel — typically "Alleluia" — that frames the reading with praise.

**Typical duration**: 1–2 minutes.

**Production notes**:
- Sung before **and** after the Gospel reading (or after, depending on tradition)
- Display acclamation text and musical notation cue if needed
- OBS scene: `MainWorship` with lyric slide for the acclamation text

---

### 11. Communion
**Purpose**: The central sacramental act — distribution of bread and wine (or juice) as the body and blood of Christ.

**Typical duration**: 10–20 minutes depending on congregation size and distribution method.

**Sub-elements**:
1. Sermon / Homily (10–15 min) — Pastor preaches on the day's texts
2. Creed (if not done earlier)
3. Prayers of the Church (2–3 min)
4. Words of Institution / Consecration
5. Distribution of elements
6. Communion hymn(s) played/sung during distribution

**Production notes**:
- Sermon: speaker camera active; display scripture references as quoted
- During distribution: display communion hymn lyrics or a reverent background slide
- OBS scene: `MainWorship` — speaker area for sermon; `ScriptureScene` for scripture references
- Lower house lights slightly during distribution if desired

---

### 12. Announcements
**Purpose**: Communicate upcoming events, ministry opportunities, and community news.

**Typical duration**: 2–4 minutes.

**Production notes**:
- Display announcement slides in rotation during spoken announcements
- OBS scene: `MainWorship` — `AnnouncementSlides` slideshow cycling through event graphics
- Info bar can scroll key dates/events simultaneously
- Keep each announcement brief: who, what, when, where

---

### 13. Postlude
**Purpose**: Send the congregation out with music that celebrates the conclusion of worship.

**Typical duration**: 3–5 minutes as people depart.

**Production notes**:
- Organ, piano, or ensemble plays upbeat closing piece
- OBS scene: `PreService` — return to service end graphic or next week preview slide
- Stream can fade or cut after 1–2 minutes of postlude
- House lights return to full

### post service
- OBS scene: `PostService` — display "Thank you for joining us" slide with next service information
- Countdown timer can be used for post-service announcements

---

## OBS Scene Summary

### Scene List — `sundayService1.csv`

| Scene                | Description                                      |
|----------------------|--------------------------------------------------|
| `CameraScene`        | Camera input hub — CameraMain, CameraPulpit, CameraChoir |
| `AudioScene`         | Audio input hub — visual placeholder only        |
| `EmergencySlides`    | Instant fallback — BRB, ServiceInterrupted, TechnicalDifficulties |
| `PreService`         | Pre-service gathering — countdown, announcement slides, info bar |
| `Prelude`            | Prelude music — title, date, info bar            |
| `MainWorship`        | Main service — speaker area, announcement slides, news ticker |
| `ScriptureScene`     | Readings / liturgy — verse text, reference, scripture slides |
| `PostService`        | Post-service — thank-you title, next service info |

### Always-Active Background Scenes
These scenes are nested inside every visual scene to ensure consistent audio and camera switching.

| Scene            | Purpose                                    | Key Sources                                   |
|------------------|--------------------------------------------|-----------------------------------------------|
| `CameraScene`    | Video input hub — switch cameras here      | CameraMain, CameraPulpit, CameraChoir          |
| `AudioScene`     | Audio input hub — all mic and instrument routing | PulpitMic, ChoirMics, HouseMic, Instruments |

### Emergency / Fallback Scene

| Scene              | Purpose                                   | Key Sources                                               |
|--------------------|-------------------------------------------|-----------------------------------------------------------|
| `EmergencySlides`  | Instant fallback for technical problems   | BRBSlide, ServiceInterruptedSlide, TechnicalDifficultiesSlide |

### Service Scenes

| Service Element        | Recommended OBS Scene | Key Sources Active                          |
|------------------------|-----------------------|---------------------------------------------|
| Pre-service gathering  | `PreService`          | CountdownTitle, PreServiceAnnouncements, InfoBar |
| Prelude                | `Prelude`             | PreludeTitle, PreludeInfoBar                |
| Welcome                | `MainWorship`         | ServiceTitle, SpeakerArea                   |
| Hymn 1                 | `MainWorship`         | Lyric slides in AnnouncementSlides          |
| Ritual 1               | `ScriptureScene`      | VerseText (liturgy text)                    |
| Prayer of the Day      | `ScriptureScene`      | ScriptureBG, VerseRef                       |
| Offertory 1            | `MainWorship`         | AnnouncementSlides (giving), NewsTicker     |
| 1st Reading            | `ScriptureScene`      | VerseText, VerseRef                         |
| 2nd Reading            | `ScriptureScene`      | VerseText, VerseRef                         |
| Gospel Reading         | `ScriptureScene`      | VerseText, VerseRef                         |
| Gospel Acclamation     | `MainWorship`         | Lyric slide                                 |
| Sermon                 | `MainWorship`         | SpeakerArea, ServiceTitle                   |
| Communion              | `MainWorship`         | SpeakerArea / lyric slides                  |
| Announcements          | `MainWorship`         | AnnouncementSlides, NewsTicker              |
| Postlude               | `Prelude`             | PreludeInfoBar                              |
| Post-service           | `PostService`         | PostServiceTitle, NextServiceInfo, PostInfoBar |

---

## Production Checklist

- [ ] All scripture references loaded into `ScriptureScene` sources before service
- [ ] Announcement slides updated in `AnnouncementSlides` slideshow
- [ ] Service title updated in `ServiceTitle` text source
- [ ] Speaker name updated in `SpeakerName` text source
- [ ] Giving information current in info bar scroll text
- [ ] Hymn/lyric slides prepared and queued
- [ ] Audio levels checked for pulpit mic, choir, and instruments
- [ ] Countdown timer set and started before prelude ends
- [ ] Stream confirmed live before prelude begins

